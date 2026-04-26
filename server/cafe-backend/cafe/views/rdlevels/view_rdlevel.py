from django.http.response import JsonResponse
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
    view_name = request.resolver_match.view_name if request.resolver_match else None
    return Response(request, view_name, props, metadata=metadata)

def view_rdlevel_api(request: HttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    return JsonResponse(rdlevel.to_dict())

def todays_blend_api(request: HttpRequest):
    from cafe.models.rdlevels.daily_blend import get_todays_blend
    blend = get_todays_blend()
    if blend is None:
        return JsonResponse({"blend": None})
    return JsonResponse({"blend": blend.to_dict()})