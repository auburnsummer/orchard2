from nanoid import generate

# no vowels to prevent accidental profanity
ALPHABET = "123456789BCDFGHJKLMNPQRSTVWXYZbcdfghjklmnpqrstvwxyz"

USER_ID_PREFIX = "u"
USER_ID_LENGTH = 9

def generate_user_id():
    return USER_ID_PREFIX + generate(ALPHABET, USER_ID_LENGTH)