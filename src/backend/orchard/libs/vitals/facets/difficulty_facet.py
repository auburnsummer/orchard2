DIFFICULTIES = ["Easy", "Medium", "Tough", "VeryTough"]


def difficulty_facet(obj, **kwargs):
    try:
        diff_string = obj["settings"]["difficulty"]
        return DIFFICULTIES.index(diff_string)
    except (ValueError, KeyError):
        return 1  # medium
