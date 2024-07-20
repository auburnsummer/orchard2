import sys
import pprint

from .vitals import vitals

def main():
    try:
        file_name = sys.argv[1]
        with open(file_name, "rb") as f:
            vit = vitals(f)
            with open("./image.png", "wb") as f:
                f.write(vit.image)

            with open("./thumb.webp", "wb") as f:
                f.write(vit.thumb);

            vit.image = ""
            vit.thumb = ""
            vit.icon = ""

            pprint.pprint(vit)
    except IndexError:
        print("Did you pass a file name in?")
