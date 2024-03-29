"""
ID generator. We use nanoid https://pypi.org/project/nanoid/ for this.

Orchard does not have distributed writes, so I'm leaning more towards having nicer looking ids rather than collision resistance
"""

import string
from enum import StrEnum
from nanoid import generate


ALPHABET = string.ascii_lowercase + string.digits

# probably safe https://zelark.github.io/nano-id-cc/
# ~293 years or 51M IDs needed, in order to have a 1% probability of at least one collision.
NANOID_LENGTH = 9

class IDType(StrEnum):
    """
    Unique prefixes for ids. 
    """
    PUBLISHER = "p_"  # a publisher
    USER = "u_"  # a user
    PREFILL = "prefill_"  # a prefill result / also used to make sure an add token is part of the same flow.
    RD_LEVEL = "rd_"  # a Rhythm Doctor level.
    HS_LEVEL = "hs_"  # a Heaven Studio level. currently unused.

def gen_id(id_type: IDType):
    """Generate an id, id_type is the unique prefix."""
    return f"{id_type.value}{generate(alphabet=ALPHABET, size=NANOID_LENGTH)}"