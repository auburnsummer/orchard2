from re import M
import zipfile
from typing import IO
import msgspec

from rdlevel_parse import parse
from .facets.artist_list_facet import artist_list_facet
from .facets.rdlevel_sha1_facet import rdlevel_sha1_facet
from .facets.sha1_facet import sha1_facet
from .facets.author_facet import author_facet
from .facets.bpm_facet import bpm_facet
from .facets.difficulty_facet import difficulty_facet
from .facets.icon_facet import icon_facet
from .facets.key_facet import make_key_facet, make_color_enabled_key_facet
from .facets.player_facet import player_facet
from .facets.tags_facet import tags_facet
from .facets.thumbnail_facet import thumbnail_facet
from .facets.updated_facet import updated_facet
from .facets.rdmd5_facet import rdmd5_facet
from .facets.total_hits_approx_facet import total_hits_approx_facet
from .facets.beat_types_facet import event_type_facet

from .msgspec_schema import VitalsLevel, VitalsLevelImmutable

import msgspec

PREFILL_VERSION = 1

class VitalsException(Exception):
    pass

def _vitals(facets: dict, f: IO[bytes]) -> dict:
    try:
        with zipfile.ZipFile(f) as z:
            with z.open("main.rdlevel", "r") as rdlevel:
                text = rdlevel.read().decode("utf-8-sig")
                parsed = parse(text)

                final = {}
                for key, func in facets.items():
                    try:
                        result = func(
                            **{"obj": parsed, "zip": z, "file": f}
                        )
                        if isinstance(key, tuple):
                            # multiple keys with (expected) multiple values that map to the keys.
                            for k, v in zip(key, result):
                                final[k] = v
                        else:
                            final[key] = result
                    except Exception as e:
                        raise VitalsException(
                            f"vitals: An unhandled error occured in a facet {func.__name__}: {e}"
                        )
                return final

    except zipfile.BadZipFile:
        raise VitalsException(
            "vitals: this is not a zip file, or we couldn't decode it for some reason."
        )
    except KeyError:
        raise VitalsException("vitals: there is no main.rdlevel in the zip.")

def vitals(f: IO[bytes]) -> VitalsLevel:
    facets = {
        "artist": make_color_enabled_key_facet(["settings", "artist"]),
        "artist_raw": make_key_facet(["settings", "artist"]),
        "artist_tokens": artist_list_facet,
        "song": make_color_enabled_key_facet(["settings", "song"]),
        "song_raw": make_key_facet(["settings", "song"]),
        "seizure_warning": make_key_facet(["settings", "seizureWarning"], True),
        "description": make_color_enabled_key_facet(
            ["settings", "description"]
        ),
        (
            "has_classics",
            "has_oneshots",
            "has_squareshots",
            "has_freezeshots",
            "has_burnshots",
            "has_holdshots",
            "has_triangleshots",
            "has_skipshots",
            "has_subdivs",
            "has_synco",
            "has_freetimes",
            "has_holds",
            "has_window_dance",
            "has_rdcode"
        ): event_type_facet,
        "total_hits_approx": total_hits_approx_facet,
        "hue": make_key_facet(["settings", "songNameHue"], 0.0),
        "authors_raw": make_key_facet(["settings", "author"]),
        "authors": author_facet,
        ("max_bpm", "min_bpm"): bpm_facet,
        "difficulty": difficulty_facet,
        ("single_player", "two_player"): player_facet,
        "last_updated": updated_facet,
        "tags": tags_facet,
        ("image", "thumb", "is_animated"): thumbnail_facet,
        "icon": icon_facet,
        "sha1": sha1_facet,
        "rdlevel_sha1": rdlevel_sha1_facet,
        "rd_md5": rdmd5_facet
    }

    result = _vitals(facets, f)
    return msgspec.convert(result, type=VitalsLevel)

def vitals_quick(f: IO[bytes]) -> VitalsLevelImmutable:
    """
    In an update operation on an rdzip, we trust the existing metadata is correct, and therefore
    we only need to update file-related metadata.

    to be honest, atm this isn't really much faster than vitals, since we still parse the entire file
    """
    facets = {
        ("image", "thumb", "is_animated"): thumbnail_facet,
        "icon": icon_facet,
        "sha1": sha1_facet,
        "rdlevel_sha1": rdlevel_sha1_facet,
        "rd_md5": rdmd5_facet,
        "last_updated": updated_facet,
        "artist_raw": make_key_facet(["settings", "artist"]),
        "song_raw": make_key_facet(["settings", "song"]),
        "authors_raw": make_key_facet(["settings", "author"])
    }

    result = _vitals(facets, f)
    return msgspec.convert(result, type=VitalsLevelImmutable)
