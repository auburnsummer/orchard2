from typing import Iterable
from huey.contrib.djhuey import task
import sentry_sdk

from cafe.management.commands.setuptypesense import RDLEVEL_ALIAS_NAME, get_typesense_client, client_healthy
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
def mass_sync_levels_to_typesense(level_ids: Iterable[str]):
    typesense_client = get_typesense_client()

    if not client_healthy(typesense_client):
        print("Typesense is not healthy. Exiting mass sync.")
        return
    
    data = []
    ids_to_delete = []
    from cafe.models import RDLevel
    for level_id in level_ids:
        try:
            level = RDLevel.objects.get(id=level_id)
            # Private levels should not be in search
            if level.is_private:
                ids_to_delete.append(level_id)
                continue
            dict_data = apply_typesense_specific_adjustments(level.to_dict())
            data.append(dict_data)
        except ObjectDoesNotExist:
            # If the level does not exist, we skip it in mass sync
            continue
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("typesense_mass_sync", {
                    "level_id": level_id,
                    "task": "mass_sync_levels_to_typesense",
                    "operation": "prepare_level"
                })
                sentry_sdk.capture_exception(e)
            print(f"Error preparing level {level_id} for Typesense: {e}")
    
    if data:
        typesense_client.collections[RDLEVEL_ALIAS_NAME].documents.import_(data, {
            "action": "upsert"
        })
        print(f"Mass synced {len(data)} levels to Typesense.")
    
    # Delete private levels from search index
    for level_id in ids_to_delete:
        try:
            typesense_client.collections[RDLEVEL_ALIAS_NAME].documents[level_id].delete()
        except Exception:
            # Document may not exist in Typesense, that's fine
            pass

    

@task()
def sync_level_to_typesense(level_id: str):
    typesense_client = get_typesense_client()
    from cafe.models import RDLevel
    if not client_healthy(typesense_client):
        print("Typesense is not healthy. Exiting sync.")
        return

    try:
        level = RDLevel.objects.get(id=level_id)
        # Private levels should not be in search - delete if exists
        if level.is_private:
            try:
                typesense_client.collections[RDLEVEL_ALIAS_NAME].documents[level_id].delete()
            except Exception:
                # Document may not exist in Typesense, that's fine
                pass
            return
        dict_data = apply_typesense_specific_adjustments(level.to_dict())
        typesense_client.collections[RDLEVEL_ALIAS_NAME].documents.upsert(dict_data)
    except ObjectDoesNotExist:
        try:
            typesense_client.collections[RDLEVEL_ALIAS_NAME].documents[level_id].delete()
        except Exception as e:
            with sentry_sdk.push_scope() as scope:
                scope.set_context("typesense_delete", {
                    "level_id": level_id,
                    "task": "sync_level_to_typesense",
                    "operation": "delete_document"
                })
                sentry_sdk.capture_exception(e)
            print(f"Error deleting document {level_id} from Typesense: {e}")
    except Exception as e:
        with sentry_sdk.push_scope() as scope:
            scope.set_context("typesense_sync", {
                "level_id": level_id,
                "task": "sync_level_to_typesense",
                "operation": "sync_level"
            })
            sentry_sdk.capture_exception(e)
        print(f"Error syncing level {level_id} to Typesense: {e}")