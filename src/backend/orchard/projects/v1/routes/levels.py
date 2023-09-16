from typing import IO, List, Tuple, Optional
from orchard.libs.bunny_storage import BunnyStorage
from orchard.libs.hash import sha1
from orchard.libs.vitals.pydantic_model import VitalsLevelBase
from orchard.projects.v1.core.config import config
from orchard.projects.v1.core.forward import forward_httpx
from orchard.projects.v1.core.wrapper import msgspec_return, parse_body_as
from orchard.projects.v1.models.users import inject_user

import httpx

from orchard.libs.vitals import analyze
from starlette.requests import Request
from starlette.responses import Response

from tempfile import TemporaryFile

import msgspec

from io import BytesIO
import asyncio

class PrefillHandlerArgs(msgspec.Struct):
    source_url: str

class VitalsLevelExport(VitalsLevelBase):
    image: str
    thumb: str
    url: str
    icon: Optional[str] = None

@msgspec_return(200)
@parse_body_as(PrefillHandlerArgs)
@inject_user  # this is an authenticated endpoint, even though we don't actually use the user here.
async def prefill_handler(request: Request):
    data: PrefillHandlerArgs = request.state.body

    c = config()
    async with BunnyStorage(
        api_key=c.BUNNY_STORAGE_API_KEY.get_secret_value(),
        base_endpoint=c.BUNNY_STORAGE_HOSTNAME,
        storage_zone_name=c.BUNNY_STORAGE_USERNAME,
        public_cdn_base=c.BUNNY_CDN_URL
    ) as bun:
        with TemporaryFile(mode="w+b") as f:
            async with httpx.AsyncClient() as client:
                resp = await client.get(data.source_url)
                try:
                    resp.raise_for_status()
                except httpx.HTTPStatusError as exc:
                    return forward_httpx(resp)
                async for chunk in resp.aiter_bytes():
                    f.write(chunk)
            f.seek(0)
            level = analyze(f)
            # also we have to upload the rdzip now
            # nb the function here also seeks back to 0 already
            # todo: figure out what sorta errors can happen here?
            rdzip_args = f, "levels", "rdzip"
            image_args = BytesIO(level.image), "images", "png"
            icon_args = (BytesIO(level.icon), "icons", "png") if level.icon else None
            thumb_args = BytesIO(level.thumb), "thumbnails", "png"
            async with asyncio.TaskGroup() as tg:
                tg.create_task(bun.upload_file_by_hash(*rdzip_args))
                tg.create_task(bun.upload_file_by_hash(*image_args))
                tg.create_task(bun.upload_file_by_hash(*thumb_args))
                if icon_args:
                    tg.create_task(bun.upload_file_by_hash(*icon_args))

            payload = {
                **msgspec.structs.asdict(level),
                "thumb": bun.get_public_url(bun.get_url_by_hash(*thumb_args)),
                "image": bun.get_public_url(bun.get_url_by_hash(*image_args)),
                "icon": bun.get_public_url(bun.get_url_by_hash(*icon_args) if icon_args else None),
                "url": bun.get_public_url(bun.get_url_by_hash(*rdzip_args))
            }
            to_send = msgspec.convert(payload, VitalsLevelExport)

    return to_send

