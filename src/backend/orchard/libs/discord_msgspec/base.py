import msgspec

class BaseDiscordStruct(
    msgspec.Struct,
    frozen=True
):
    "Base class for discord_msgspec. Frozen is set: https://jcristharif.com/msgspec/structs.html#frozen-instances"