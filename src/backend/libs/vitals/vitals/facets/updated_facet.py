from zipfile import ZipFile
from datetime import datetime


def updated_facet(zip, **kwargs):
    info = zip.getinfo("main.rdlevel")
    return datetime(*info.date_time)
