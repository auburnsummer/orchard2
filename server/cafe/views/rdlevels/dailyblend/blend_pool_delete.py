from django.shortcuts import redirect
from rules.contrib.views import permission_required
from cafe.tasks.report_blend_change import blend_pool_deleted, report_blend_change
from cafe.views.types import HttpRequest
from cafe.models.rdlevels.blend_pool import BlendPool, DEFAULT_BLEND_POOL_ID
from django.shortcuts import get_object_or_404

from django.contrib import messages

@permission_required('cafe.blend_rdlevel')
def blend_pool_delete(request: HttpRequest, pool_id: str):
    if request.method == "POST":
        pool = get_object_or_404(BlendPool, id=pool_id)
        pool_name = pool.name
        if pool.id == DEFAULT_BLEND_POOL_ID:
            messages.error(request, "Cannot delete the default blend pool.")
            return redirect("cafe:blend_pool", pool_id=pool_id)
        pool.delete()
        messages.success(request, f"Deleted blend pool {pool_name}")
        report_blend_change(blend_pool_deleted(pool_name, request.user))
    # redirect back to the pool list page after deleting.
    return redirect("cafe:blend_pools")