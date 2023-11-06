"""
A row_factory implementation, based on https://rogerbinns.github.io/apsw/ext.html#apsw.ext.DataClassRowFactory

Give it a msgspec struct to 
"""
from __future__ import annotations

import msgspec
import typing
import apsw
from orchard.libs.melite.base import MeliteStruct


def make_row_trace(spec: typing.Type[MeliteStruct], conn: apsw.Connection):
    """
    Produces a function that can be attached to a cursor row_trace to make it return MeliteStruct directly.

    Also will resolve foreign keys in the table and attach them
    """
    if not spec.table_name:
        raise ValueError("Provided struct does not have a table")
    def inner(cursor: apsw.Cursor, row: apsw.SQLiteValues) -> MeliteStruct:
        column_names = [d[0] for d in cursor.get_description()]

        converted = dict(zip(column_names, row))
        final = {}
        for field in msgspec.structs.fields(spec):
            value = converted[field.encode_name]
            # if it's None, it's always None in the resulting struct regardless of the type.
            sub_struct: typing.Optional[typing.Type[MeliteStruct]] = None
            if value is not None:
                # otherwise, it might be a struct reference...
                try:
                    if issubclass(field.type, MeliteStruct):
                        sub_struct = field.type
                except TypeError:
                    pass
                # it may also be in the form Optional[cls]
                if typing.get_origin(field.type) == typing.Union:
                    for t in typing.get_args(field.type):
                        if issubclass(t, MeliteStruct):
                            sub_struct = t

            if sub_struct is not None:
                cursor = conn.cursor()
                cursor.row_trace = make_row_trace(sub_struct, conn)
                q = f"""
                    --sql
                    SELECT * FROM "{sub_struct.table_name}"
                    WHERE "{sub_struct.table_name}"."{sub_struct.primary_key}" = ?
                """
                cursor.execute(q, [value])
                result = next(cursor)
                final[field.encode_name] = result
            else:
                final[field.encode_name] = value


        return msgspec.convert(final, type=spec, strict=False)

    return inner