from huey.contrib.djhuey import task

from cafe.management.commands.setuptypesense import RDLEVEL_ALIAS_NAME, typesense_client, client_healthy
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime

def apply_typesense_specific_adjustments(level_data: dict) -> dict:
    """
    Apply any Typesense-specific adjustments to the level data.
    """
    # last_updated should be a unix timestamp
    dict_data = level_data.copy()
    dict_data["last_updated"] = int(datetime.fromisoformat(level_data["last_updated"]).timestamp())

    return dict_data

@task()
def sync_level_to_typesense(level_id: str):
    from cafe.models import RDLevel
    if not client_healthy(typesense_client):
        print("Typesense is not healthy. Exiting sync.")
        return

    try:
        level = RDLevel.objects.get(id=level_id)
        dict_data = apply_typesense_specific_adjustments(level.to_dict())
        typesense_client.collections[RDLEVEL_ALIAS_NAME].documents.upsert(dict_data)
    except ObjectDoesNotExist:
        try:
            typesense_client.collections[RDLEVEL_ALIAS_NAME].documents[level_id].delete()
        except Exception as e:
            print(f"Error deleting document {level_id} from Typesense: {e}")
    except Exception as e:
        print(f"Error syncing level {level_id} to Typesense: {e}")