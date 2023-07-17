
from typing import Dict, Set, Any


def without_keys(dict: Dict[str, Any], keys: Set[str]):
    "Return a version of the dictionary without the keys in the supplied set."
    return {
        k:v
        for k,v in dict.items() if k not in keys
    }