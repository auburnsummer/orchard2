from django.shortcuts import redirect
from rules.contrib.views import permission_required
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.blend_pool import BlendPool, DEFAULT_BLEND_POOL_ID
from django.shortcuts import get_object_or_404

from django.contrib import messages

@permission_required('cafe.blend_rdlevel')
def blend_pool_delete(request: HttpRequest, pool_id: str):
    if request.method == "POST":
        pool = get_object_or_404(BlendPool, id=pool_id)
        if pool.id == DEFAULT_BLEND_POOL_ID:
            messages.error(request, "Cannot delete the default blend pool.")
            return redirect("cafe:blend_pool", pool_id=pool_id)
        messages.success(request, f"Deleted blend pool {pool.name}")
        pool.delete()
    # redirect back to the pool list page after deleting.
    return redirect("cafe:blend_pools")