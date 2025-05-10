from nanoid import generate

# no vowels to prevent accidental profanity
ALPHABET = "123456789BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz"

USER_ID_PREFIX = "u"
USER_ID_LENGTH = 8

def generate_user_id():
    return USER_ID_PREFIX + generate(ALPHABET, USER_ID_LENGTH - len(USER_ID_PREFIX))

CLUB_ID_PREFIX = "c"
CLUB_ID_LENGTH = 8

def generate_club_id():
    return CLUB_ID_PREFIX + generate(ALPHABET, CLUB_ID_LENGTH - len(CLUB_ID_PREFIX))

RDLEVEL_PREFILL_ID_PREFIX = "p"
RDLEVEL_PREFILL_ID_LENGTH = 8

def generate_rdlevel_prefill_id():
    return RDLEVEL_PREFILL_ID_PREFIX + generate(ALPHABET, RDLEVEL_PREFILL_ID_LENGTH - len(RDLEVEL_PREFILL_ID_PREFIX))

RDLEVEL_ID_PREFIX = "r"
RDLEVEL_ID_LENGTH = 8

def generate_rdlevel_id():
    return RDLEVEL_ID_PREFIX + generate(ALPHABET, RDLEVEL_ID_LENGTH - len(RDLEVEL_ID_PREFIX))
