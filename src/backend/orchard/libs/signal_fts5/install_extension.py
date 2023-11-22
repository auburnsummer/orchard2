"""
Installs the extension
"""
import pathlib
import apsw

def file_exists():
    path = pathlib.Path(__file__).resolve().parent
    results = list(path.glob("./Signal-FTS5-Extension/target/release/libsignal_tokenizer.*"))
    return bool(results)

class SignalFTS5ExtensionNotBuilt(Exception):
    pass

def install_extension(conn: apsw.Connection):
    if not file_exists():
        raise SignalFTS5ExtensionNotBuilt("The libsignal_tokenizer library is not built. Please follow instructions in src/backend/orchard/libs/signal_fts5/README.md")

