import sys
import pprint
from .vitals import main

import msgspec


try:
    file_name = sys.argv[1]
    with open(file_name, "rb") as f:
        vit = main(f)
        with open("./image.webp", "wb") as f:
            f.write(vit.image)

        with open("./thumb.webp", "wb") as f:
            f.write(vit.thumb);

        vit.image = ""
        vit.thumb = ""
        vit.icon = ""

        pprint.pprint(vit)
except IndexError:
    print("Did you pass a file name in?")
