
def is_hold(evt):
    return "hold" in evt and evt["hold"] > 0


def is_classic(evt):
    return evt["type"] == "AddClassicBeat" and not is_hold(evt)


def is_freetime(evt):
    return evt["type"] == "AddFreeTimeBeat"


def is_oneshot(evt):
    return evt["type"] == "AddOneshotBeat" and (
        "pulseType" not in evt or evt["pulseType"] == "Wave"
    )


def is_squareshot(evt):
    return evt["type"] == "AddOneshotBeat" and (
        "pulseType" not in evt or evt["pulseType"] == "Square"
    )


def is_skipshot(evt):
    return evt["type"] == "AddOneshotBeat" and (
        "skipshot" in evt and evt["skipshot"]  # it exists and is True
    )


def is_freezeshot(evt):
    return evt["type"] == "AddOneshotBeat" and "delay" in evt and evt["delay"] > 0


def is_window_dance(evt):
    return evt["type"] == "NewWindowDance"


def event_type_facet(obj, **kwargs):
    events = obj["events"]

    return (
        any(func(evt) for evt in events)
        for func in [
            is_classic,
            is_oneshot,
            is_squareshot,
            is_freezeshot,
            is_freetime,
            is_hold,
            is_skipshot,
            is_window_dance,
        ]
    )
