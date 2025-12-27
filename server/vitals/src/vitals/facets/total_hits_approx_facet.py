
CLOSE_ENOUGH = 0.001

def total_hits_approx_facet(obj, **kwargs):
    """
    We are NOT going to attempt to be perfectly accurate here, there are
    lots of edge cases.
    this is a best-effort approximate total hit count mostly for the purposes
    of detecting "joke" levels that have ~0 hits. 
    """
    total = 0
    crotchets_per_bar = {}
    
    start_abs_curr_oneshot = -1.0
    end_abs_curr_oneshot = -1.0
    
    events = obj["events"]

    # first determine crotchets per bar across the whole level
    for evt in events:
        if evt["type"] == "SetCrotchetsPerBar":
            crotchets_per_bar[evt["bar"]] = evt["crotchetsPerBar"]

    def bar_and_beat_to_absolute_beat(bar, beat):
        abs_beat = 0.0
        for b in range(bar):
            abs_beat += crotchets_per_bar.get(b, 8.0)
        abs_beat += beat
        return abs_beat
    
    def add_beat_to_bar_and_beat(bar, beat, delta):
        beat = beat + delta
        while beat >= crotchets_per_bar.get(bar, 8.0):
            beat -= crotchets_per_bar.get(bar, 8.0)
            bar += 1
        return bar, beat

    for evt in events:
        # classic and freetimes are always worth one hit
        if evt["type"] == "AddClassicBeat":
            total += 1
        if evt["type"] == "AddFreeTimeBeat":
            total += 1
        # the more complicated oneshot beats...
        # assume that all oneshots that are in between the start and the end
        # of this oneshot are part of it.
        # this is an approximation.
        if evt["type"] == "AddOneshotBeat":
            loops = evt.get("loops", 1)
            start_abs_this_event = bar_and_beat_to_absolute_beat(evt["bar"], evt["beat"])
            duration = evt["tick"]
            end_bar, end_beat = add_beat_to_bar_and_beat(evt["bar"], evt["beat"], duration * loops)
            end_abs_this_event = bar_and_beat_to_absolute_beat(end_bar, end_beat)

            if start_abs_this_event >= (start_abs_curr_oneshot-CLOSE_ENOUGH) and start_abs_this_event <= (end_abs_curr_oneshot+CLOSE_ENOUGH):
                # this oneshot is within the current oneshot, so ignore it
                continue

            # update the current oneshot range
            start_abs_curr_oneshot = start_abs_this_event
            end_abs_curr_oneshot = end_abs_this_event
            # credit the beats
            subdivs = evt.get("subdivisions", 1)
            total_to_credit = loops * subdivs
            total += total_to_credit


    return total