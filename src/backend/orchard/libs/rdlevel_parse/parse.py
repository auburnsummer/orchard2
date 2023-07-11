from .naya import parse_string
from typing import Any

def parse(f: str) -> Any:
    return parse_string(f)