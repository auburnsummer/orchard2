# Removes <color> tags from string
# we might need to remove other unity-type rich text, but in practice,
# people only seem to use <color> for now.
import re

TAG_FINDER = re.compile(r'</?color.*?>')


def parse_color_tagged_string(s: str):
    stripped = re.sub(TAG_FINDER, "", s.strip())

    return stripped
