from orchard.projects.v1.core.parse import parse_body_as
from orchard.projects.v1.models.users import inject_user
from pydantic import BaseModel

import httpx

from orchard.libs.vitals import analyze
from starlette.requests import Request
from starlette.responses import JSONResponse

from tempfile import TemporaryFile

class PrefillHandlerArgs(BaseModel):
    source_url: str

from io import BytesIO

@parse_body_as(PrefillHandlerArgs)
@inject_user  # this is an authenticated endpoint, even though we don't actually use the user here.
async def prefill_handler(request: Request):
    data: PrefillHandlerArgs = request.state.body

    # rdzips can be big! let
    with TemporaryFile(mode="w+b") as f:
        async with httpx.AsyncClient() as client:
            resp = await client.get(data.source_url)
            async for chunk in resp.aiter_bytes():
                f.write(chunk)
        f.seek(0)
        level = analyze(f)

    return JSONResponse(level.model_dump(mode="json"))