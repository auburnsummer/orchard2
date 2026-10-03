from vitals.utils import try_dig
from math import ceil, floor

def is_bpm_event(evt):
    return evt["type"] in ["PlaySong", "SetBeatsPerMinute"]


def get_bpm_from_event(evt):
    # then, the bpm is either in the ["bpm"] or ["beatsPerMinute"] key
    try:
        return evt["bpm"]
    except KeyError:
        return evt["beatsPerMinute"]


def bpm_facet(obj, **kwargs):
    bpms = [get_bpm_from_event(e) for e in obj["events"] if is_bpm_event(e)]
    # then, the bpm is either in the ["bpm"] or ["beatsPerMinute"] key
    if len(bpms) == 0:
        return 0, 0
    return ceil(max(bpms)), floor(min(bpms))
