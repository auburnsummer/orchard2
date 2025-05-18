from huey.contrib.djhuey import on_commit_task

from cafe.management.commands.setupmeili import RDLEVEL_INDEX_NAME
from cafe.models import RDLevel
from orchard.settings import MEILI_API_URL, MEILI_API_KEY
import meilisearch


client = meilisearch.Client(MEILI_API_URL, MEILI_API_KEY)

@on_commit_task()
def sync_level_to_meili(level_id: str):
    level = RDLevel.objects.get(id=level_id)

    index = client.get_index(RDLEVEL_INDEX_NAME)
    index.add_documents([level.to_dict()])
