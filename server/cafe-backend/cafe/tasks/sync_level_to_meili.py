from huey.contrib.djhuey import task

from cafe.management.commands.setupmeili import RDLEVEL_INDEX_NAME
import meilisearch
from django.core.exceptions import ObjectDoesNotExist
from orchard.settings import MEILI_API_URL, MEILI_API_KEY

client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)

@task()
def sync_level_to_meili(level_id: str):
    from cafe.models import RDLevel
    try:
        level = RDLevel.objects.get(id=level_id)

        index = client.get_index(RDLEVEL_INDEX_NAME)
        index.add_documents([level.to_dict()])
    except ObjectDoesNotExist:
        index = client.get_index(RDLEVEL_INDEX_NAME)
        index.delete_document(level_id)
