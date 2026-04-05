from django.core.signing import TimestampSigner

# Signs time-limited "add level" delegation tokens shared between
# the Discord bot add handler and the prefill flow.
addlevel_signer = TimestampSigner(salt="addlevel")
