import datetime
from typing import Optional
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rules.contrib.views import objectgetter, permission_required
from django.views.decorators.csrf import csrf_exempt

from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.models.rdlevels.daily_blend import DailyBlend
import msgspec

from cafe.views.types import AuthenticatedHttpRequest

class SetDailyBlendPayload(msgspec.Struct):
    level_id: str
    featured_date: Optional[str]  # ISO format date string

@csrf_exempt
# @permission_required("cafe.blend_rdlevel", fn=objectgetter(RDLevel, attr_name="level_id"))
def set_daily_blend(request: AuthenticatedHttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = msgspec.json.decode(request.body, type=SetDailyBlendPayload)
    except msgspec.ValidationError as e:
        return JsonResponse({"error": "Invalid payload", "details": str(e)}, status=400)
    
    level = get_object_or_404(RDLevel, id=payload.level_id)

    if not request.user.has_perm("cafe.blend_rdlevel", level):
        return JsonResponse({"error": "Permission denied"}, status=403)

    if payload.featured_date is None:
        targeted_date = datetime.date.today()
    else:
        targeted_date = datetime.date.fromisoformat(payload.featured_date)

    if targeted_date < datetime.date.today():
        return JsonResponse({"error": "Cannot set daily blend for past dates"}, status=400)
    
    daily_blend, _ = DailyBlend.objects.update_or_create(
        featured_date=targeted_date,
        level=level
    )
    
    return JsonResponse({"success": True, "level": level.to_dict(), "featured_date": str(daily_blend.featured_date)})