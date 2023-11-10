from apsw import Connection
from orchard.libs.melite.base import MeliteStruct
from typing import List, Tuple

import msgspec
from orchard.libs.melite.factory import get_json_struct, get_melite_struct
from orchard.libs.melite.utils import wrap_quotes

def insert(conn: Connection, obj: MeliteStruct, recurse=True):
    """
    Insert a struct into the database. 

    recurse: also inserts other structs into the database that are being referenced
    """
    to_insert: List[Tuple[str, str]] = []
    for field in msgspec.structs.fields(obj):
        value = getattr(obj, field.encode_name)
        if value is not None:
            sub_struct = get_melite_struct(field.type)
            if sub_struct:
                if recurse:
                    insert(conn, value)
                value = getattr(value, sub_struct.primary_key)

            if get_json_struct(field.type) is not None:
                value = msgspec.json.encode(value).decode(encoding='utf-8')

        to_insert.append((field.encode_name, value))

    
    q = f"""--sql
    INSERT INTO "{obj.table_name}" ({",".join(wrap_quotes(t[0]) for t in to_insert)})
    VALUES
        ({",".join("?" for _ in to_insert)})
    """
    conn.execute(q, [t[1] for t in to_insert])
