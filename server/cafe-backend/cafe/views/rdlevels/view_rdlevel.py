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
    title = f"{rdlevel.song} \u2014 {rdlevel.artist}"
    og_description = rdlevel.description or f"By {', '.join(rdlevel.authors)}"
    metadata = Metadata(
        title=title,
        og={
            "title": title,
            "description": og_description,
            "image": request.build_absolute_uri(rdlevel.thumb_url),
            "url": request.build_absolute_uri(reverse("cafe:level_download", args=[rdlevel.id])),
            "type": "website",
        },
    )
    return Response(request, request.resolver_match.view_name, props, metadata=metadata)