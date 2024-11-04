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
    PUBLISHER = "p_"  # A publisher. Unused but required for backwards compatability with migrations.
    CLUB = "c_"  # a club
    USER = "u_"  # a user
    PREFILL = "prefill_"  # a prefill result / also used to make sure an add token is part of the same flow.
    RD_LEVEL = "rd_"  # a Rhythm Doctor level.
    HS_LEVEL = "hs_"  # a Heaven Studio level. currently unused.

def _gen_id(id_type: IDType):
    """Generate an id, id_type is the unique prefix."""
    return f"{id_type.value}{generate(alphabet=ALPHABET, size=NANOID_LENGTH)}"

def gen_id(id_type: IDType):
    while True:
        id = _gen_id(id_type)
        for word in BAD_WORDS:
            if word in id:
                continue
        else:
            return id

def default_id(id_type: IDType):
    """Returns a default function for a django model."""
    return functools.partial(gen_id, id_type)