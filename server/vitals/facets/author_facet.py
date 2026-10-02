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

    # if every item in author_tokens is blank, just return the original authors as a single token
    # this can happen if the author name consists entirely of separators
    # e.g. "////" who made "none"
    if all(not x for x in author_tokens):
        return [authors]

    return author_tokens
