from math import ceil
from zipfile import ZipFile
from PIL import Image

from io import BytesIO

THUMBNAIL_WIDTH = 300
THUMBNAIL_HEIGHT = 168


def thumbnail_facet(obj, zip, **kwargs):
    """return two file objects, one for the thumbnail and the original."""
    image_name = obj["settings"]["previewImage"]

    orig_file_p = BytesIO()
    thumb_file_p = BytesIO()
    with zip.open(image_name, "r") as image_buffer:
        image = Image.open(image_buffer)
        orig = image.copy()
        image.thumbnail((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.Resampling.LANCZOS)

        orig.save(orig_file_p, format="png")
        image.save(thumb_file_p, format="png")
        orig.close()
        image.close()

    orig_file_p.seek(0)
    thumb_file_p.seek(0)
    return orig_file_p.read(), thumb_file_p.read()
