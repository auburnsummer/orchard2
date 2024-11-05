"""
ID generator. We use nanoid https://pypi.org/project/nanoid/ for this.

Orchard does not have distributed writes, so I'm leaning more towards having nicer looking ids rather than collision resistance
"""

import functools
from enum import StrEnum
from nanoid import generate

from .bad_words import BAD_WORDS

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

# probably safe https://zelark.github.io/nano-id-cc/
NANOID_LENGTH = 12

class IDType(StrEnum):
    """
    Unique prefixes for ids. 
    """
    PUBLISHER = "p-"  # A publisher. Unused but required for backwards compatability with migrations.
    CLUB = "c-"  # a club
    USER = "u-"  # a user
    PREFILL = "prefill-"  # a prefill result / also used to make sure an add token is part of the same flow.
    RD_LEVEL = "rd-"  # a Rhythm Doctor level.
    HS_LEVEL = "hs-"  # a Heaven Studio level. currently unused.

def is_ok(s: str):
    """Returns true if the string is ok to use as an id."""
    test_string = s.replace("_", "").replace('-', "").lower()
    for word in BAD_WORDS:
        if word in test_string:
            return False
    return True


def _gen_id(id_type: IDType):
    """Generate an id, id_type is the unique prefix."""
    id_part = generate(alphabet=ALPHABET, size=NANOID_LENGTH)
    with_dashes = '-'.join(id_part[i:i+4] for i in range(0, len(id_part), 4))
    return f"{id_type.value}{with_dashes}"

def gen_id(id_type: IDType):
    while True:
        id = _gen_id(id_type)
        if is_ok(id):
            return id

def default_id(id_type: IDType):
    """Returns a default function for a django model."""
    return functools.partial(gen_id, id_type)