from django.http import JsonResponse
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.rdlevel import RDLevel


def peer_review_pending_levels(request: HttpRequest) -> JsonResponse:
    """
    View to display levels pending peer review.
    """
    pr_levels = RDLevel.objects.filter(approval=0)
    payload = [level.to_dict() for level in pr_levels]
    return JsonResponse({"levels": payload})