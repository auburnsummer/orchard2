from urllib.parse import urlencode

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from cafe.models.rdlevels.rdlevel import RDLevel


def download_rdlevel(request: HttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)
    filename = f"{rdlevel.song} - {', '.join(rdlevel.authors)} {rdlevel.id}.rdzip"
    url = f"{rdlevel.rdzip_url}?{urlencode({'filename': filename})}"
    return HttpResponseRedirect(url)
