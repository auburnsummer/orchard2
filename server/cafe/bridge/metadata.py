from typing import NotRequired, TypedDict, Literal


# OpenGraph metadata — see https://ogp.me/
class OpenGraphMetadata(TypedDict, total=False):
    title: str
    description: str
    image: str
    url: str
    type: str
    site_name: str


class Metadata(TypedDict):
    title: str
    og: NotRequired[OpenGraphMetadata]
