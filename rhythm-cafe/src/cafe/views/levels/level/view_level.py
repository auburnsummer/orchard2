import rules

from django.shortcuts import render
from cafe.models.rdlevel import RDLevel


def view_level(request, level_id):
    level = RDLevel.objects.get(id=level_id)

    # clubs = [crl.club for crl in ClubRDLevel.objects.filter(rdlevel=level)]

    def has_permission(perm):
        return rules.has_perm(perm, request.user, level)
    
    print(rules.perm_exists('cafe.change_rdlevel'))
    print(has_permission('cafe.change_rdlevel'))

    payload = {
        "has_permission": has_permission,
        "level": level
    }
    return render(request, 'cafe/levels/view_level.jinja', payload)