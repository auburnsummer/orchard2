# parse a unity-style <color> string
# returns a tuple of the string _without_ the colors, then what bits are colored by 0-indexed ranges.
import re


class InvalidColorException(Exception):
    pass


# (<color=([a-zA-Z0-9#]+)>)|(<\/color>)
TAG_FINDER = re.compile(r"(<color=([a-zA-Z0-9#]+)>)|(</color>)")


def parse_color_tagged_string(s: str):
    matches = list(TAG_FINDER.finditer(s.strip()))

    color_stack = ["default"]

    # where we are in the original string
    curr_pos = 0

    # where we are in the string when it has been stripped of color tags.
    literals = []
    tokens = []

    for match in matches:
        # from curr_pos to the starting position of this match is a literal.
        literal = s[curr_pos : match.start()]
        literals.append(literal)
        # ...which is whatever color is previous (at the top of the stack.)
        tokens.append({"len": len(literal), "color": color_stack[-1]})

        opening, color, closing = match.groups()
        if opening:
            # it's an opening tag, so add a new color to the stack.
            if not color:
                raise InvalidColorException(
                    "Opening color tag found without a given color."
                )
            color_stack.append(color)
        if closing:
            color_stack.pop()

        curr_pos = match.end()

    # we might have leftover text.
    leftover = s[curr_pos:]
    if leftover:
        # it's whatever color is left.
        literals.append(leftover)
        tokens.append({"len": len(leftover), "color": color_stack.pop()})

    tokens = [t for t in tokens if t["len"] > 0]

    return "".join(literals), tokens
