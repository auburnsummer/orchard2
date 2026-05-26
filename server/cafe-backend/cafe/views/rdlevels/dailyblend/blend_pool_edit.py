from django.shortcuts import redirect
from rules.contrib.views import permission_required
from django.forms.models import ModelForm
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.blend_pool import BlendPool

from django.shortcuts import get_object_or_404

class BlendPoolEditForm(ModelForm):
    class Meta:
        model = BlendPool
        fields = ['name']

@permission_required('cafe.blend_rdlevel')
def blend_pool_edit(request: HttpRequest, pool_id: str):
    if request.method == "POST":
        pool = get_object_or_404(BlendPool, id=pool_id)
        form = BlendPoolEditForm(request.POST, instance=pool)
        if form.is_valid():
            form.save()
    # redirect back to the pool page after editing.
    return redirect("cafe:blend_pool", pool_id=pool_id)