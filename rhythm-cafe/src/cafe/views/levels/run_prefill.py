import asyncio
from email.mime import image
from io import BufferedRandom, BytesIO
from tempfile import TemporaryFile
from typing import NamedTuple
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
import msgspec
from vitals.msgspec_schema import VitalsLevel

from .check import check_if_ok_to_continue

from huey.contrib.djhuey import db_task
from cafe.views.discord_bot.handlers.add import addlevel_signer
from vitals import vitals
from bunny_storage import BunnyStorage

from cafe.models import Club, RDLevelPrefillResult

import httpx

from orchard.settings import BUNNY_STORAGE_API_KEY, BUNNY_STORAGE_BASE_ENDPOINT, BUNNY_STORAGE_CDN_URL, BUNNY_STORAGE_ZONE_NAME
from django.forms.models import model_to_dict

from loguru import logger

from rules.contrib.views import permission_required

from asgiref.sync import async_to_sync

class UploadFilesURLs(NamedTuple):
    rdzip_url: str
    image_url: str
    icon_url: str | None
    thumb_url: str
    rdzip_url_public: str
    image_url_public: str
    icon_url_public: str | None
    thumb_url_public: str

@async_to_sync
async def upload_files(level: VitalsLevel, f: BufferedRandom):
    async with httpx.AsyncClient() as client:
        bun = BunnyStorage(
            api_key=BUNNY_STORAGE_API_KEY,
            base_endpoint=BUNNY_STORAGE_BASE_ENDPOINT,
            storage_zone_name=BUNNY_STORAGE_ZONE_NAME,
            public_cdn_base=BUNNY_STORAGE_CDN_URL,
            client=client
        )
        async with asyncio.TaskGroup() as tg:
            rdzip_task = tg.create_task(bun.upload_file_by_hash(f, "rdzips", ".rdzip"))
            image_task = tg.create_task(bun.upload_file_by_hash(BytesIO(level.image), "images", ".png"))
            icon_task = tg.create_task(bun.upload_file_by_hash(BytesIO(level.icon), "icons", ".png")) if level.icon else None
            thumb_task = tg.create_task(bun.upload_file_by_hash(BytesIO(level.thumb), "thumbs", ".webp"))

        rdzip_url = rdzip_task.result()
        image_url = image_task.result()
        icon_url = icon_task.result() if icon_task else None
        thumb_url = thumb_task.result()
        rdzip_url_public = bun.get_public_url(rdzip_url)
        image_url_public = bun.get_public_url(image_url)
        icon_url_public = bun.get_public_url(icon_url) if icon_url else None
        thumb_url_public = bun.get_public_url(thumb_url)

    # public urls return as well
    return UploadFilesURLs(
        rdzip_url,
        image_url,
        icon_url,
        thumb_url,
        rdzip_url_public,
        image_url_public,
        icon_url_public,
        thumb_url_public
    )


@db_task()
def _run_prefill(level_url: str, prefill_result: RDLevelPrefillResult):    
    try:
        with TemporaryFile(mode="w+b") as f:
            with httpx.Client() as client:
                # bun = BunnyStorage(
                #     api_key=BUNNY_STORAGE_API_KEY,
                #     base_endpoint=BUNNY_STORAGE_BASE_ENDPOINT,
                #     storage_zone_name=BUNNY_STORAGE_ZONE_NAME,
                #     public_cdn_base=BUNNY_STORAGE_CDN_URL,
                #     client=client
                # )
                resp = client.get(level_url)
                resp.raise_for_status()
                for chunk in resp.iter_bytes():
                    f.write(chunk)
            f.seek(0)
            level = vitals(f)

            urls = upload_files(level, f)

            payload = msgspec.structs.asdict(level)
            payload['rdzip_url'] = urls.rdzip_url_public
            payload['image_url'] = urls.image_url_public
            payload['icon_url'] = urls.icon_url_public
            payload['thumb_url'] = urls.thumb_url_public
            del payload['image']
            del payload['thumb']
            del payload['icon']

            prefill_result.data = msgspec.json.encode(payload)
            prefill_result.ready = True
            prefill_result.save()
    except Exception as e:
        # print traceback
        import traceback
        traceback.print_exc()
        logger.error(e)
        prefill_result.errors = str(e)
        prefill_result.save()


@permission_required('prefill.ok', fn=lambda _, code: code)
def run_prefill(request, code):
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