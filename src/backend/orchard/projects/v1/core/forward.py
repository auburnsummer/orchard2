from httpx import Response as HTTPXResponse
from starlette.responses import Response

DONT_FORWARD_THESE_HEADERS = {
    "content-type",
    "content-length",
    "transfer-encoding",
    "set-cookie",
    "content-encoding"
}

def forward_httpx(resp: HTTPXResponse) -> Response:
    filtered_headers = { k: v for k, v in resp.headers.items() if k.lower() not in DONT_FORWARD_THESE_HEADERS }
    print(filtered_headers)
    return Response(
        resp.content,
        status_code=resp.status_code,
        headers=filtered_headers
    )