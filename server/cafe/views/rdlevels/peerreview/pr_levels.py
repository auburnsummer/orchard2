from cafe.models.rdlevels.rdlevel import RDLevel


def get_pr_pending_levels():
    # we want the oldest level first
    return RDLevel.objects.filter(approval=0, is_private=False).order_by('last_updated')