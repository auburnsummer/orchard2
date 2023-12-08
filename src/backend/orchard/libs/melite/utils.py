import contextlib
from apsw import Connection
from nanoid import non_secure_generate

def wrap_quotes(s: str):
    "Return the string with quotes around it"
    return "\"" + s + "\""

def single_quotes(s: str):
    return "'" + s + "'"

@contextlib.contextmanager
def temporary_table(conn: Connection):
    temp_table_id = non_secure_generate()
    try:
        conn.execute(f"ATTACH ':memory:' AS \"{temp_table_id}\";")
        yield temp_table_id
    finally:
        conn.interrupt()
        conn.execute(f"DETACH \"{temp_table_id}\";")