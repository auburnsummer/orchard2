import pytest

from vitals.color_tagged_string import parse_color_tagged_string


@pytest.fixture
def color_tagged1():
    return "hello <color=blue>world</color>"


def test_parse_color_tagged_string_returns_the_original_string_if_no_color_tags():
    s = "This is a normal string without any tags"
    s1, _ = parse_color_tagged_string(s)
    assert s == s1


def test_parse_color_tagged_string_returns_string_without_tags(color_tagged1):
    s1, t1 = parse_color_tagged_string(color_tagged1)
    assert t1 == [{"len": 6, "color": "default"}, {"len": 5, "color": "blue"}]
    assert s1 == "hello world"


def test_parse_color_tagged_string_works_with_trailing_untagged_text():
    s = "There is a <color=blue>word</color> and then back to normal"
    s1, t1 = parse_color_tagged_string(s)
    assert s1 == "There is a word and then back to normal"
    assert t1 == [
        {"len": 11, "color": "default"},
        {"len": 4, "color": "blue"},
        {"len": 24, "color": "default"},
    ]


def test_parse_color_tagged_string_works_with_unclosed_color_tag():
    s = "<color=#ababab>this entire string is this color"
    s1, t1 = parse_color_tagged_string(s)
    assert s1 == "this entire string is this color"
    assert t1 == [{"len": len(s1), "color": "#ababab"}]


def test_parse_nested_strings():
    s = "hello <color=red>this is red then<color=blue> this is blue </color>back to red</color> and finally this is normal"
    s1, t1 = parse_color_tagged_string(s)
    assert (
        s1
        == "hello this is red then this is blue back to red and finally this is normal"
    )
    assert t1 == [
        {"color": "default", "len": 6},
        {"color": "red", "len": 16},
        {"color": "blue", "len": 14},
        {"color": "red", "len": 11},
        {"color": "default", "len": 27},
    ]
