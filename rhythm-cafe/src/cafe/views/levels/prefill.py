from email.mime import image
from io import BytesIO
from tempfile import TemporaryFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed, JsonResponse
import msgspec

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

@db_task()
def _run_prefill(level_url: str, prefill_result: RDLevelPrefillResult):    
    try:
        with httpx.Client() as client:
            with TemporaryFile(mode="w+b") as f:
                bun = BunnyStorage(
                    api_key=BUNNY_STORAGE_API_KEY,
                    base_endpoint=BUNNY_STORAGE_BASE_ENDPOINT,
                    storage_zone_name=BUNNY_STORAGE_ZONE_NAME,
                    public_cdn_base=BUNNY_STORAGE_CDN_URL,
                    client=client
                )
                resp = client.get(level_url)
                resp.raise_for_status()
                for chunk in resp.iter_bytes():
                    f.write(chunk)
                f.seek(0)
                level = vitals(f)

                rdzip_url = bun.upload_file_by_hash(f, "rdzips", ".rdzip")
                image_url = bun.upload_file_by_hash(BytesIO(level.image), "images", ".png")
                icon_url = bun.upload_file_by_hash(BytesIO(level.icon), "icons", ".png") if level.icon else None
                thumb_url = bun.upload_file_by_hash(BytesIO(level.thumb), "thumbs", ".webp")

                payload = msgspec.structs.asdict(level)
                payload['rdzip_url'] = bun.get_public_url(rdzip_url)
                payload['image_url'] = bun.get_public_url(image_url)
                payload['icon_url'] = bun.get_public_url(icon_url)
                payload['thumb_url'] = bun.get_public_url(thumb_url)
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


@login_required
def prefill(request, code):
    if request.method != "POST":
        return HttpResponseNotAllowed()

    check_if_ok_to_continue(code, request.user)

    result = addlevel_signer.unsign_object(code)
    level_url = result['level_url']
    club_id = result['club_id']
    prefill_result = RDLevelPrefillResult(
        user=request.user,
        club=Club.objects.get(id=club_id)
    )
    _run_prefill(level_url, prefill_result)
    return JsonResponse(model_to_dict(prefill_result))