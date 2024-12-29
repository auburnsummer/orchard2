from math import ceil
from zipfile import ZipFile
from PIL import Image

from io import BytesIO

THUMBNAIL_SIZE = 480


def thumbnail_facet(obj, zip, **kwargs_):
    """return two file objects, one for the thumbnail and the original."""
    image_name = obj["settings"]["previewImage"]

    orig_file_p = BytesIO()
    thumb_file_p = BytesIO()
    with zip.open(image_name, "r") as image_buffer:
        image = Image.open(image_buffer)
        image.load()

        is_animated = getattr(image, "is_animated", False)
        
        # make a copy that we then thumbnail
        thumbnail_image = image.copy()
        thumbnail_image.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE), Image.Resampling.LANCZOS, reducing_gap=None)

        try:
            image.save(
                orig_file_p,
                format="png",
                save_all=True,
                optimize=True,
            )
        # whatever Samario is doing with his thumbnails, PIL's save_all doesn't work with it
        except ValueError:
            image.save(
                orig_file_p,
                format="png" 
            )
        
        thumbnail_image.save(
            thumb_file_p,
            format="webp",
            quality=82,
            method=6
        )
        image.close()
        thumbnail_image.close()

    orig_file_p.seek(0)
    thumb_file_p.seek(0)
    return orig_file_p.read(), thumb_file_p.read(), is_animated
