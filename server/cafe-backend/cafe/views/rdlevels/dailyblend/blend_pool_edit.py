from django.shortcuts import redirect
from rules.contrib.views import permission_required
from django.forms.models import ModelForm
from cafe.tasks.report_blend_change import blend_pool_name_changed, blend_pool_weighting_system_changed, report_blend_change
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.blend_pool import BlendPool
from django.contrib import messages
from django.shortcuts import get_object_or_404

class BlendPoolEditForm(ModelForm):
    class Meta:
        model = BlendPool
        fields = ['name', 'weighting_system']

@permission_required('cafe.blend_rdlevel')
def blend_pool_edit(request: HttpRequest, pool_id: str):
    if request.method == "POST":
        pool = get_object_or_404(BlendPool, id=pool_id)
        form = BlendPoolEditForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
            if 'name' in form.changed_data:
                report_blend_change(blend_pool_name_changed(form.initial['name'], form.cleaned_data['name'], request.user))
            if 'weighting_system' in form.changed_data:
                report_blend_change(blend_pool_weighting_system_changed(pool.name, form.initial['weighting_system'], form.cleaned_data['weighting_system'], request.user))
            messages.success(request, "Blend pool updated successfully.")
    # redirect back to the pool page after editing.
    return redirect("cafe:blend_pool", pool_id=pool_id)