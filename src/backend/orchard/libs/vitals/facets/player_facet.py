from orchard.libs.vitals.utils import try_dig


def player_facet(obj, toml, **kwargs):
    s = obj["settings"]["canBePlayedOn"]
    toml_1 = try_dig(["modes", "1p"], toml)
    toml_2 = try_dig(["modes", "2p"], toml)
    single_player = (
        toml_1 if toml_1 is not None else s in ["OnePlayerOnly", "BothModes"]
    )
    two_player = toml_2 if toml_2 is not None else s in ["TwoPlayerOnly", "BothModes"]
    return single_player, two_player
