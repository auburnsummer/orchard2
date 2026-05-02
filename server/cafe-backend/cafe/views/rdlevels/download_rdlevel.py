from urllib.parse import quote

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404

from cafe.models.rdlevels.rdlevel import RDLevel

# Including the rdzip extension.
MAXIMUM_FILENAME_LENGTH = 80

def get_filename_for_rdlevel(rdlevel: RDLevel) -> str:
    num_authors = len(rdlevel.authors)
    while num_authors > 0:
        et_al_part = "" if len(rdlevel.authors) == num_authors else "et al."
        proposed_filename = f"{rdlevel.song} - {', '.join(rdlevel.authors[:num_authors])} {et_al_part} {rdlevel.id}.rdzip"

        if len(proposed_filename) <= MAXIMUM_FILENAME_LENGTH:
            return proposed_filename
        num_authors -= 1
    # ok I guess even the first author was too long
    # just return song title and id
    proposed_filename = f"{rdlevel.song} {rdlevel.id}.rdzip"
    if len(proposed_filename) <= MAXIMUM_FILENAME_LENGTH:
        return proposed_filename
    # what?? just the id then.
    return f"{rdlevel.id}.rdzip"

def download_rdlevel(request: HttpRequest, level_id: str):
    rdlevel = get_object_or_404(RDLevel, id=level_id)

    filename = get_filename_for_rdlevel(rdlevel)
    url = f"{rdlevel.rdzip_url}?filename={quote(filename)}"
    return HttpResponseRedirect(url)
