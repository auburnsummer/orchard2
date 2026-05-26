from django.forms import ModelForm
from rules.contrib.views import permission_required
from cafe.models.rdlevels.blend_pool import BlendPool
from cafe.views.types import HttpRequest

from cafe.bridge.response import Response

class BlendPoolForm(ModelForm):
    class Meta:
        model = BlendPool
        fields = ["name"]

@permission_required('cafe.blend_rdlevel')
def blend_pools(request: HttpRequest):
    if request.method == 'POST':
        form = BlendPoolForm(request.POST)
        if form.is_valid():
            form.save()

    blend_pools = BlendPool.objects.all()
    props = {
        "pools": [b.to_dict() for b in blend_pools]
    }

    return Response(request, request.resolver_match.view_name, props)