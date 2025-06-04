import sys
import pprint
import argparse
import msgspec

from .vitals import vitals

def main():
    parser = argparse.ArgumentParser(description='Process metadata from a Rhythm Doctor .rdzip file.')
    parser.add_argument('file', help='Input file to process')
    parser.add_argument('--write-image', action='store_true', help='Write out image.png')
    parser.add_argument('--write-thumb', action='store_true', help='Write out thumb.webp')
    
    try:
        args = parser.parse_args()
        with open(args.file, "rb") as f:
            vit = vitals(f)
            
            if args.write_image:
                with open("./image.png", "wb") as f:
                    f.write(vit.image)

            if args.write_thumb:
                with open("./thumb.webp", "wb") as f:
                    f.write(vit.thumb)

            vit.image = ""
            vit.thumb = ""
            vit.icon = ""

            pprint.pprint(msgspec.structs.asdict(vit))
    except FileNotFoundError:
        print(f"Error: Could not find or open the specified file.")
        sys.exit(1)