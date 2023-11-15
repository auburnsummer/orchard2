
import datetime
from typing import List, Tuple
from apsw import Connection
import msgspec
from orchard.libs.melite.factory import get_json_struct, get_melite_struct
from orchard.libs.melite.utils import wrap_quotes
from .base import MeliteStruct

def update(conn: Connection, obj: MeliteStruct, recurse=True):
    """
    Update a row in the database.

    recurse: also updates other structs being referenced.
    """
    to_update: List[Tuple[str, str]] = []
    for field in msgspec.structs.fields(obj):
        if field.encode_name == obj.primary_key:
            continue
        value = getattr(obj, field.encode_name)
        if value is not None:
            sub_struct = get_melite_struct(field.type)
            if sub_struct:
                if recurse:
                    update(conn, value)
                value = getattr(value, sub_struct.primary_key)

            if get_json_struct(field.type) is not None:
                value = msgspec.json.encode(value).decode(encoding='utf-8')

            if isinstance(value, datetime.datetime):
                value = value.replace(microsecond=0).astimezone(tz=datetime.timezone.utc).isoformat()


        to_update.append((field.encode_name, value))

    q = f"""--sql
        UPDATE "{obj.table_name}"
        SET ({",".join(wrap_quotes(t[0]) for t in to_update)})
        = ({",".join("?" for _ in to_update)})
        WHERE "{obj.table_name}"."{obj.primary_key}" = ?
    """
    conn.execute(q, [t[1] for t in to_update] + [getattr(obj, obj.primary_key)])
