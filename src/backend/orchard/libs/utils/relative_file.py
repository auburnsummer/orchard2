import inspect
from pathlib import Path

def whereami():
    "Return the directory that the caller of this function is in."
    return Path(inspect.stack()[1].filename).resolve().parent