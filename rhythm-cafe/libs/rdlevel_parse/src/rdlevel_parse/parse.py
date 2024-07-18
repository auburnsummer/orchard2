from .naya import parse_string
from typing import Any

import json

def parse(f: str) -> Any:
    # standard JSON encoder is fast, so we'll try that first.
    try:
        return json.loads(f)
    except json.decoder.JSONDecodeError:
        return parse_string(f)