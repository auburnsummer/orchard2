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



def is_burnshot(evt):
    return evt["type"] == "AddOneshotBeat" and (
        "freezeBurnMode" in evt and evt["freezeBurnMode"] == "Burnshot"
    )


def is_window_dance(evt):
    return evt["type"] == "NewWindowDance"



def is_syncopation(evt):
    return evt["type"] == "SetRowXs" and "syncoBeat" in evt and evt["syncoBeat"] > -1



def is_holdshot(evt):
    return evt["type"] == "AddOneshotBeat" and "hold" in evt and evt["hold"]



def is_triangleshot(evt):
    return evt["type"] == "AddOneshotBeat" and (
        "pulseType" in evt and evt["pulseType"] == "Triangle"
    )


def is_subdiv(evt):
    return evt["type"] == "AddOneshotBeat" and (
        "subdivisions" in evt and evt["subdivisions"] > 0
    )


def is_rdcode(evt):
    return evt["type"] == "CallCustomMethod" and evt.get("methodName", "") != ""

def event_type_facet(obj, **kwargs):
    events = obj["events"]

    return (
        any(func(evt) for evt in events)
        for func in [
            is_classic,
            is_oneshot,
            is_squareshot,
            is_freezeshot,
            is_burnshot,
            is_holdshot,
            is_triangleshot,
            is_skipshot,
            is_subdiv,
            is_syncopation,
            is_freetime,
            is_hold,
            is_window_dance,
            is_rdcode,
        ]
    )