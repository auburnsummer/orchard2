import asyncio
from io import BufferedRandom, BytesIO
from tempfile import TemporaryFile
from typing import NamedTuple
from aiohttp import ClientSession
from aiohttp_s3_client import S3Client
from essfree.essfree import Essfree
import msgspec
from vitals import vitals
from huey.contrib.djhuey import db_periodic_task, db_task, on_commit_task
import httpx
from cafe.models.rdlevels.prefill import RDLevelPrefillResult
from asgiref.sync import async_to_sync
from vitals.msgspec_schema import VitalsLevel
import traceback
import sentry_sdk

from orchard.settings import S3_API_URL, S3_ACCESS_KEY_ID, S3_SECRET_ACCESS_KEY, S3_REGION, S3_PUBLIC_CDN_URL

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
def run_prefill(prefill_id: str):
    prefill_result = RDLevelPrefillResult.objects.get(id=prefill_id)
    try:
        with TemporaryFile(mode="w+b") as f:
            with httpx.Client() as client:
                resp = client.get(prefill_result.url)
                resp.raise_for_status()
                for chunk in resp.iter_bytes():
                    f.write(chunk)
            f.seek(0)
            level = vitals(f)

            urls = upload_files(level, f)

            payload = msgspec.structs.asdict(level)
            payload['rdzip_url'] = urls.rdzip_url
            payload['image_url'] = urls.image_url
            payload['icon_url'] = urls.icon_url
            payload['thumb_url'] = urls.thumb_url
            del payload['image']
            del payload['thumb']
            del payload['icon']

            prefill_result.data = payload
            prefill_result.ready = True
            prefill_result.save()

    except Exception as e:
        # Capture exception with isolated context for better debugging
        with sentry_sdk.push_scope() as scope:
            scope.set_context("prefill_task", {
                "prefill_id": prefill_id,
                "url": prefill_result.url,
                "task": "run_prefill"
            })
            sentry_sdk.capture_exception(e)
        prefill_result.errors = traceback.format_exc()
        prefill_result.save()