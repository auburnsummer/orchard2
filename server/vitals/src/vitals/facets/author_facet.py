import re

# Get things like
# donte, ladybug
# donte & ladybug
# donte and ladybug
# donte, noche, and ladybug
# donte, noche, & ladybug
from vitals.color_tagged_string import parse_color_tagged_string

AUTHOR_REGEX = r"\s*?(?:,|&|\/|\\|,? ,?and )\s*?"

def author_facet(obj, **kwargs):
    author_raw = obj["settings"]["author"]
    authors = parse_color_tagged_string(author_raw.strip())

    author_tokens = [s.strip() for s in re.split(AUTHOR_REGEX, authors) if s]

    return author_tokens
