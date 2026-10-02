
def has_cpu_rows_facet(obj, **kwargs):
    # did any rows start as CPU?
    rows = obj["rows"]
    for row in rows:
        if row.get("player", "") == "CPU":
            return True
        
    # rows could have been changed to CPU later
    events = obj["events"]
    for evt in events:
        if evt["type"] == "ChangePlayersRows":
            players = evt.get("players", [])
            for p in players:
                if p == "CPU":
                    return True
                
    return False