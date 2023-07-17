import hashlib
from zipfile import ZipFile


def rdlevel_sha1_facet(zip: ZipFile, **kwargs):
    """
    this is the sha1 of the .rdlevel file.
    this is used as the unique identifier for the level.
    """

    sha1 = hashlib.sha1()
    with zip.open("main.rdlevel") as rdlevel:
        text = rdlevel.read()
        sha1.update(text)
    return sha1.hexdigest()
