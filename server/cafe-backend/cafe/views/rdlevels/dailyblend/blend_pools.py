from rules.contrib.views import permission_required
from cafe.models.rdlevels.blend_pool import BlendPool
from cafe.views.types import HttpRequest

from cafe.bridge.response import Response

@permission_required('cafe.blend_rdlevel')
def blend_pools(request: HttpRequest):
    blend_pools = BlendPool.objects.all()
    props = {
        "pools": [b.to_dict() for b in blend_pools]
    }

    return Response(request, request.resolver_match.view_name, props)