"""
A row_factory implementation, based on https://rogerbinns.github.io/apsw/ext.html#apsw.ext.DataClassRowFactory

Give it a msgspec struct to 
"""
from __future__ import annotations

import msgspec
import typing
import apsw
from orchard.libs.melite.base import JSON, MeliteStruct

def get_melite_struct(type_: typing.Any) -> typing.Optional[typing.Type[MeliteStruct]]:
    """
    if `type_` is a MeliteStruct or Optional[MeliteStruct], extract the type.
    Otherwise, returns None.
    """
    try:
        if issubclass(type_, MeliteStruct):
            return type_
    except TypeError:
        pass

    if typing.get_origin(type_) == typing.Union:
        for t in typing.get_args(type_):
            if issubclass(t, MeliteStruct):
                return t

    return None

def get_json_struct(type_: typing.Any) -> typing.Optional[typing.Any]:
    """
    if `type_` is of the form Annotated[type2, JSON], returns type2.
    Otherwise, returns None.
    """
    if typing.get_origin(type_) == typing.Annotated:
        type_to_convert_into, annot = typing.get_args(type_)
        if annot == JSON:
            return type_to_convert_into

    return None



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
                sub_struct = get_melite_struct(field.type)
                # it may also be in a form Annotated[type, JSON]
                type_to_convert_into = get_json_struct(field.type)
                if type_to_convert_into:
                    value = msgspec.json.decode(value, type=type_to_convert_into, strict=False)
            if sub_struct is not None:
                cursor = conn.cursor()
                cursor.row_trace = make_row_trace(sub_struct, conn)
                q = f"""
                    --sql
                    SELECT * FROM "{sub_struct.table_name}"
                    WHERE
                        "{sub_struct.table_name}"."{sub_struct.primary_key}" = ?
                """
                cursor.execute(q, [value])
                value = next(cursor)
            
            final[field.encode_name] = value


        return msgspec.convert(final, type=spec, strict=False)

    return inner