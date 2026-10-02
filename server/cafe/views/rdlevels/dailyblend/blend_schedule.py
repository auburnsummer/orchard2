from django import forms
from django.http import JsonResponse
from cafe.models.rdlevels.rdlevel import RDLevel
from cafe.tasks.report_blend_change import report_blend_change, blend_schedule_changed
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required
from datetime import datetime

from cafe.bridge.response import Response
from cafe.models.rdlevels.daily_blend import DailyBlend

from django.contrib import messages

class BlendScheduleForm(forms.Form):
    featured_date = forms.DateField()
    level_or_pool_id = forms.CharField(required=False)

@permission_required('cafe.blend_rdlevel')
def blend_schedule(request: HttpRequest) -> JsonResponse:
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    if request.method == 'POST':
        form = BlendScheduleForm(request.POST)
        if form.is_valid():
            featured_date = form.cleaned_data['featured_date']
            level_or_pool_id = form.cleaned_data['level_or_pool_id']

            prev = DailyBlend.objects.filter(featured_date=featured_date).first()

            if level_or_pool_id == "":
                DailyBlend.objects.filter(featured_date=featured_date).delete()
                messages.success(request, f"Cleared blend schedule for {featured_date}.")
                report_blend_change(blend_schedule_changed(featured_date, prev, None, request.user))
            elif level_or_pool_id.startswith("r"):
                # it's a level.
                level = RDLevel.objects.filter(id=level_or_pool_id).first()
                if not level:
                    messages.error(request, f"Level with ID {level_or_pool_id} does not exist.")
                else:
                    blend, _ = DailyBlend.objects.update_or_create(
                        featured_date=featured_date,
                        defaults={'level': level, 'pool': None}
                    )
                    messages.success(request, f"Set blend schedule for {featured_date} to level '{level.song}'.")
                    report_blend_change(blend_schedule_changed(featured_date, prev, blend, request.user))
            elif level_or_pool_id.startswith("b"):
                # it's a pool.
                from cafe.models.rdlevels.blend_pool import BlendPool
                pool = BlendPool.objects.filter(id=level_or_pool_id).first()
                if not pool:
                    messages.error(request, f"Pool with ID {level_or_pool_id} does not exist.")
                else:
                    blend, _ = DailyBlend.objects.update_or_create(
                        featured_date=featured_date,
                        defaults={'pool': pool, 'level': None}
                    )
                    messages.success(request, f"Set blend schedule for {featured_date} to pool '{pool.name}'.")
                    report_blend_change(blend_schedule_changed(featured_date, prev, blend, request.user))
            else:
                messages.error(request, "Invalid ID")
        else:
            messages.error(request, "Invalid form submission.")
    
    # Filter DailyBlend objects by year and month
    blends = DailyBlend.objects.filter(
        featured_date__year=year,
        featured_date__month=month
    )
    
    props = {
        "blends": [blend.to_dict() for blend in blends],
        "year": year,
        "month": month,
    }

    return Response(request, request.resolver_match.view_name, props)