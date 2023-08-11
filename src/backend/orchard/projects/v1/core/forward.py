from httpx import Response as HTTPXResponse
from starlette.responses import Response

def forward_httpx(resp: HTTPXResponse) -> Response:
    return Response(
        status_code=resp.status_code,
        headers=resp.headers,
        content=resp.text
    )