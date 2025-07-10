from huey.contrib.djhuey import task

from cafe.management.commands.setuptypesense import RDLEVEL_ALIAS_NAME, typesense_client, client_healthy
from django.core.exceptions import ObjectDoesNotExist

import charabia_py

from datetime import datetime

tokenizer = charabia_py.PyTokenizer()
# the first usage is slow since it loads dictionaries, so we do it here
tokenizer.tokenize("こんにちは世界")

def tokenize(s: str) -> str:
    tokens = tokenizer.tokenize(s)
    return " ".join(token.lemma for token in tokens if token.kind == "word")

def apply_typesense_specific_adjustments(level_data: dict) -> dict:
    """
    Apply any Typesense-specific adjustments to the level data.
    """
    # todo, but basically, uhhh
    # last_updated should be a unix timestamp but it's stored
    # as an ISO 8601 string 
    dict_data = level_data.copy()
    dict_data["last_updated"] = int(datetime.fromisoformat(level_data["last_updated"]).timestamp())
    # and we need to manually tokenize several fields using charabia_py
    fields_to_tokenize = [
        "artist_tokens",
        "song",
        "song_alt",
        "description",
        "authors",
        "tags"
    ]
    for field in fields_to_tokenize:
        if field in dict_data and isinstance(dict_data[field], str):
            # Tokenize the string field
            tokenified = tokenize(dict_data[field])
            dict_data[field] = tokenified
        elif field in dict_data and isinstance(dict_data[field], list):
            # Tokenize each string in the list
            tokenified = [tokenize(item) for item in dict_data[field]]
            dict_data[field] = tokenified
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