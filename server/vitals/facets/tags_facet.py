
def tags_facet(obj, **kwargs):
    tags_raw = obj["settings"]["tags"]
    return [s.strip() for s in tags_raw.split(",") if s.strip()]
