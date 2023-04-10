def dig(dig_list, obj):
    "get something from a json dictionary, array, etc by a list of properties"
    final = obj
    for prop in dig_list:
        final = final[prop]
    return final


def try_dig(dig_list, obj):
    "similar to dig() but returns None if prop does not exist"
    if obj is None:
        return None
    try:
        return dig(dig_list, obj)
    except KeyError:
        return None
