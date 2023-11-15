from __future__ import annotations

from typing import ClassVar
import msgspec
import enum

class _JSONMark(enum.Enum):
    JSON = "JSONMARK"

JSON = _JSONMark.JSON
"Mark a field with Annotated[type, JSON] to have it be deserialized and serialized automatically."


class MeliteStruct(msgspec.Struct):
    """
    any sqlite-backed struct should inherit from here.
    """
    table_name: ClassVar[str] = ""
    primary_key: ClassVar[str] = "id"
