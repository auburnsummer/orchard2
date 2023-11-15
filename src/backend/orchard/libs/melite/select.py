from typing import Iterable, Optional, TypeVar, Type, Generic

from orchard.libs.melite.factory import make_row_trace
from .base import MeliteStruct

from apsw import Connection

T_co = TypeVar('T_co', bound=MeliteStruct, covariant=True)

class Select(Generic[T_co]):
    spec: Type[T_co]
    conn: Connection

    def __init__(self, conn: Connection, spec: Type[T_co]):
        self.spec = spec
        self.conn = conn

    def by_id(self, id_: int | str) -> Optional[T_co]:
        "Run a select query for an id and return the first result, or None if it was not found."
        cursor = self.conn.cursor()
        cursor.row_trace = make_row_trace(self.spec, self.conn)
        cursor.execute(f"""--sql
            SELECT * FROM "{self.spec.table_name}"
            WHERE "{self.spec.table_name}"."{self.spec.primary_key}" = ?
        """, [id_])

        return next(cursor, None)

    def all(self) -> Iterable[T_co]:
        "Run a select query and return all rows."
        cursor = self.conn.cursor()
        cursor.row_trace = make_row_trace(self.spec, self.conn)
        cursor.execute(f"""--sql
            SELECT * FROM "{self.spec.table_name}"
        """)

        return cursor