from .naya import parse_string
from typing import TextIO, Any

def parse(f: TextIO) -> Any:
    return parse_string(f)