"""
Installs the extension
"""
import pathlib
import apsw
from orchard.libs.utils.relative_file import whereami

def file_exists():
    path = whereami()
    results = list(path.glob("./Signal-FTS5-Extension/target/release/libsignal_tokenizer.*"))
    return bool(results)

class SignalFTS5ExtensionNotBuilt(Exception):
    pass

def install_extension(conn: apsw.Connection):
    if not file_exists():
        raise SignalFTS5ExtensionNotBuilt("The libsignal_tokenizer library is not built. Please follow instructions in src/backend/orchard/libs/signal_fts5/README.md")

    conn.enable_load_extension(True)

    path_to_load = whereami() / "Signal-FTS5-Extension/target/release/libsignal_tokenizer"
    conn.load_extension(str(path_to_load), "signal_fts5_tokenizer_init")