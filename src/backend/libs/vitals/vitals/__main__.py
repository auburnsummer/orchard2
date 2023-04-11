import sys
import pprint
from .vitals import main

try:
    file_name = sys.argv[1]
    with open(file_name, "rb") as f:
        vit = main(f)
        pprint.pprint(vit)
except IndexError:
    print("Did you pass a file name in?")
