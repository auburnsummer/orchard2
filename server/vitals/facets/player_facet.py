from vitals.utils import try_dig


def player_facet(obj, **kwargs):
    s = obj["settings"]["canBePlayedOn"]
    single_player = s in ["OnePlayerOnly", "BothModes"]
    two_player = s in ["TwoPlayerOnly", "BothModes"]
    return single_player, two_player
