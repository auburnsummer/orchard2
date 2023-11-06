from __future__ import annotations

from typing import ClassVar
import msgspec


class MeliteStruct(msgspec.Struct):
    """
    any sqlite-backed struct should inherit from here.
    """
    table_name: ClassVar[str] = ""
    primary_key: ClassVar[str] = "id"
