from django.shortcuts import get_object_or_404
from django.urls import reverse
from cafe.bridge.metadata import Metadata
from cafe.bridge.response import Response

from cafe.models import RDLevel
from cafe.views.types import HttpRequest


def view_rdlevel(request: HttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    props = {
        "rdlevel": rdlevel.to_dict(),
        "can_edit": request.user.has_perm("cafe.change_rdlevel", rdlevel),
        "can_delete": request.user.has_perm("cafe.delete_rdlevel", rdlevel),
    }
    alt_title_frag = f"({rdlevel.song_alt})" if rdlevel.song_alt else ""
    title = f"{rdlevel.song} {alt_title_frag} - {rdlevel.artist}"
    og_description = rdlevel.description or ""
    metadata = Metadata(
        title=title,
        og={
            "title": title,
            "description": og_description,
            "image": request.build_absolute_uri(rdlevel.thumb_url),
            "url": request.build_absolute_uri(reverse("cafe:level_view", args=[rdlevel.id])),
            "type": "article",
            "site_name": f"Level by {', '.join(rdlevel.authors)}",
        },
    )
    return Response(request, request.resolver_match.view_name, props, metadata=metadata)