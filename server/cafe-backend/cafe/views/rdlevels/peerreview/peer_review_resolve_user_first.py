from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
import msgspec
from rules.contrib.views import objectgetter, permission_required
from cafe.models import RDLevel
from django.views.decorators.csrf import csrf_exempt

from allauth.socialaccount.models import SocialAccount

@csrf_exempt
@permission_required('cafe.peerreview_rdlevel', fn=objectgetter(RDLevel, attr_name="level_id"), raise_exception=True)
def peer_review_resolve_user_first(request: HttpRequest, level_id: int) -> JsonResponse:
    """
    View to report that a level is the user's first level.
    """
    level = get_object_or_404(RDLevel, id=level_id)
    submitter = level.submitter

    # other levels?
    other_levels = RDLevel.objects.filter(submitter=submitter).exclude(id=level.id)
    is_first_level = not other_levels.exists()

    # also resolve their discord id if possible
    social_account = SocialAccount.objects.filter(user=submitter, provider='discord').first()

    discord_id = social_account.uid if social_account else None

    return JsonResponse({"is_first_level": is_first_level, "discord_id": discord_id})