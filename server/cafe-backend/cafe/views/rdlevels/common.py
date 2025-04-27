from vitals.msgspec_schema import VitalsLevelBaseMutable


class AddLevelPayload(VitalsLevelBaseMutable):
    song_alt: str
