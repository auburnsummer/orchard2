from django import forms
from django.http import JsonResponse
from cafe.models.rdlevels.rdlevel import select_rdlevel_by_id_or_url
from cafe.views.types import HttpRequest
from rules.contrib.views import permission_required
from datetime import datetime

from django_bridge.response import Response
from cafe.models.rdlevels.daily_blend import DailyBlend

from django.contrib import messages

class BlendScheduleForm(forms.Form):
    featured_date = forms.DateField()
    level_id = forms.CharField(required=False)

@permission_required('cafe.blend_rdlevel')
def blend_schedule(request: HttpRequest) -> JsonResponse:
    now = datetime.now()
    year = int(request.GET.get('year', now.year))
    month = int(request.GET.get('month', now.month))

    if request.method == 'POST':
        form = BlendScheduleForm(request.POST)
        if form.is_valid():
            featured_date = form.cleaned_data['featured_date']
            level_id = form.cleaned_data['level_id']

            if level_id:
                level = select_rdlevel_by_id_or_url(level_id)
                if not level:
                    messages.error(request, f"Level with ID {level_id} does not exist.")
                    return Response(request, request.resolver_match.view_name, {})
                DailyBlend.objects.update_or_create(
                    featured_date=featured_date,
                    defaults={'level_id': level.id}
                )
                messages.success(request, f"Scheduled blend for {featured_date} with level ID {level_id}.")
            else:
                DailyBlend.objects.filter(featured_date=featured_date).delete()
                messages.success(request, f"Cleared blend schedule for {featured_date}.")
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