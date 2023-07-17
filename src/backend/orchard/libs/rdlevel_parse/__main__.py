import sys
import json
from . import parse


def with_first_file_or_stdin(func):
    def inner():
        if len(sys.argv) == 1:
            # no arg
            func(sys.stdin)
        else:
            with open(sys.argv[1], "r", encoding="utf-8-sig") as f:
                func(f)

    return inner


@with_first_file_or_stdin
def main(file):
    parsed = parse(file.read())
    print(json.dumps(parsed))


main()
