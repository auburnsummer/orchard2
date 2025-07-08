from huey.contrib.djhuey import task

from cafe.management.commands.setuptypesense import RDLEVEL_ALIAS_NAME, typesense_client, client_healthy

import charabia_py

def apply_typesense_specific_adjustments(level_data: dict) -> dict:
    """
    Apply any Typesense-specific adjustments to the level data.
    """
    # todo, but basically, uhhh
    # last_updated should be a unix timestamp
    # and we need to manually tokenize several fields using charabia_py
    return level_data

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
    except Exception as e:
        print(f"Error syncing level to Typesense: {e}")