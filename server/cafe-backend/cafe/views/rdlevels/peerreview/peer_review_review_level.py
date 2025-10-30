
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
import msgspec
from rules.contrib.views import objectgetter, permission_required
from cafe.models import RDLevel
from django.views.decorators.csrf import csrf_exempt

class PeerReviewReviewLevelPayload(msgspec.Struct):
    approval: int

@csrf_exempt
@permission_required('cafe.peerreview_rdlevel', fn=objectgetter(RDLevel, attr_name="level_id"), raise_exception=True)
def peer_review_review_level(request: HttpRequest, level_id: int) -> JsonResponse:
    """
    View to handle peer review of a specific level.
    """
    level = get_object_or_404(RDLevel, id=level_id)
    pr_payload = msgspec.json.decode(request.body, type=PeerReviewReviewLevelPayload)
    print(pr_payload)
    # set level approval and save
    level.approval = pr_payload.approval
    level.save()
    # return success
    return JsonResponse({"level": level.to_dict()})