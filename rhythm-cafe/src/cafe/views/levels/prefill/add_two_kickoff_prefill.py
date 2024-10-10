import asyncio
from io import BufferedRandom, BytesIO
from tempfile import TemporaryFile
from typing import NamedTuple
from aiohttp import ClientSession
from aiohttp_s3_client import S3Client
from django.http import HttpResponseNotAllowed, JsonResponse
import msgspec
from vitals.msgspec_schema import VitalsLevel
from essfree import Essfree

from huey.contrib.djhuey import db_task
from cafe.views.discord_bot.handlers.add import addlevel_signer
from vitals import vitals

from cafe.models import Club, RDLevelPrefillResult

import httpx

from orchard.settings import S3_ACCESS_KEY_ID, S3_API_URL, S3_PUBLIC_CDN_URL, S3_REGION, S3_SECRET_ACCESS_KEY
from django.forms.models import model_to_dict

from loguru import logger

from rules.contrib.views import permission_required

from asgiref.sync import async_to_sync

class UploadFilesURLs(NamedTuple):
    rdzip_url: str
    image_url: str
    icon_url: str | None
    thumb_url: str

@async_to_sync
async def upload_files(level: VitalsLevel, f: BufferedRandom):
    async with ClientSession(raise_for_status=True) as session:
        client = S3Client(
            url=S3_API_URL,
            session=session,
            access_key_id=S3_ACCESS_KEY_ID,
            secret_access_key=S3_SECRET_ACCESS_KEY,
            region=S3_REGION
        )
        esfree = Essfree(client, S3_PUBLIC_CDN_URL)

        async with asyncio.TaskGroup() as tg:
            rdzip_task = tg.create_task(esfree.upload_file(f, "rdzips", ".rdzip"))
            image_task = tg.create_task(esfree.upload_file(BytesIO(level.image), "images", ".png"))
            icon_task = tg.create_task(esfree.upload_file(BytesIO(level.icon), "icons", ".png")) if level.icon else None
            thumb_task = tg.create_task(esfree.upload_file(BytesIO(level.thumb), "thumbs", ".webp"))

        rdzip_url = rdzip_task.result()
        image_url = image_task.result()
        icon_url = icon_task.result() if icon_task else None
        thumb_url = thumb_task.result()
        return UploadFilesURLs(
            rdzip_url,
            image_url,
            icon_url,
            thumb_url
        )

@db_task()
def _run_prefill(level_url: str, prefill_result: RDLevelPrefillResult):    
    try:
        with TemporaryFile(mode="w+b") as f:
            with httpx.Client() as client:
                resp = client.get(level_url)
                resp.raise_for_status()
                for chunk in resp.iter_bytes():
                    f.write(chunk)
            f.seek(0)
            level = vitals(f)

            urls = upload_files(level, f)

            payload = msgspec.structs.asdict(level)
            payload['rdzip_url'] = urls.rdzip_url
            payload['image_url'] = urls.image_url
            # the other three are required but icon is optional
            # we don't want to send None, just leave it out
            if urls.icon_url:
                payload['icon_url'] = urls.icon_url
            payload['thumb_url'] = urls.thumb_url
            del payload['image']
            del payload['thumb']
            del payload['icon']

            prefill_result.data = payload
            prefill_result.ready = True
            prefill_result.save()
    except Exception as e:
        import traceback
        tb = traceback.TracebackException.from_exception(e)
        s = tb.format(chain=True)
        prefill_result.errors = "\n".join(s)
        prefill_result.save()


@permission_required('prefill.ok', fn=lambda _, code: code)
def add_two_kickoff_prefill(request, code):
    "Stage 2: Kick off the prefill process and return a prefill id that can be polled for the result."
    if request.method != "POST":
        return HttpResponseNotAllowed()

    result = addlevel_signer.unsign_object(code)
    level_url = result['level_url']
    club_id = result['club_id']
    prefill_result = RDLevelPrefillResult(
        user=request.user,
        club=Club.objects.get(id=club_id),
        version=1,
        url=level_url
    )
    prefill_result.save()
    _run_prefill(level_url, prefill_result)
    return JsonResponse(model_to_dict(prefill_result))