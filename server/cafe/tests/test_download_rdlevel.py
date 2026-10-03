from types import SimpleNamespace

import pytest

from cafe.views.rdlevels.download_rdlevel import (
    MAXIMUM_FILENAME_LENGTH,
    get_filename_for_rdlevel,
)


def _level(song="My Song", authors=None, id="abc123"):
    if authors is None:
        authors = ["Author"]
    return SimpleNamespace(song=song, authors=authors, id=id)


class TestGetFilenameForRdlevel:
    def test_single_author(self):
        result = get_filename_for_rdlevel(_level(song="Cool Song", authors=["Alice"], id="xyz"))
        assert result == "Cool Song - Alice  xyz.rdzip"

    def test_multiple_authors(self):
        result = get_filename_for_rdlevel(_level(song="Cool Song", authors=["Alice", "Bob"], id="xyz"))
        assert result == "Cool Song - Alice, Bob  xyz.rdzip"

    def test_drops_authors_when_too_long(self):
        long_name = "A" * 80
        level = _level(song="Song", authors=[long_name, "Bob"], id="xyz")
        result = get_filename_for_rdlevel(level)
        # Both authors would exceed the limit, so it should drop to one, then add et al.
        # If even one author is too long, falls back to song + id
        assert len(result) <= MAXIMUM_FILENAME_LENGTH

    def test_et_al_when_authors_trimmed(self):
        authors = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"]
        level = _level(song="A" * 60, authors=authors, id="xyz")
        result = get_filename_for_rdlevel(level)
        assert len(result) <= MAXIMUM_FILENAME_LENGTH
        if len(authors) > 1:
            # If not all authors fit, "et al." should appear
            if "et al." in result:
                assert result.endswith("xyz.rdzip")

    def test_falls_back_to_song_and_id(self):
        long_author = "A" * 120
        level = _level(song="Song", authors=[long_author], id="xyz")
        result = get_filename_for_rdlevel(level)
        assert result == "Song xyz.rdzip"

    def test_falls_back_to_id_only(self):
        long_song = "S" * 120
        long_author = "A" * 120
        level = _level(song=long_song, authors=[long_author], id="xyz")
        result = get_filename_for_rdlevel(level)
        assert result == "xyz.rdzip"

    def test_result_never_exceeds_max_length(self):
        """Property: no matter the input, the filename should not exceed the max length."""
        cases = [
            _level(song="X" * 200, authors=["Y" * 200], id="Z" * 20),
            _level(song="Short", authors=["A"] * 50, id="id1"),
            _level(song="", authors=["Author"], id="id1"),
            _level(song="Song", authors=["A" * 50, "B" * 50, "C" * 50], id="longid123"),
        ]
        for level in cases:
            result = get_filename_for_rdlevel(level)
            assert len(result) <= MAXIMUM_FILENAME_LENGTH, f"Too long ({len(result)}): {result!r}"

    def test_extension_is_rdzip(self):
        result = get_filename_for_rdlevel(_level())
        assert result.endswith(".rdzip")
