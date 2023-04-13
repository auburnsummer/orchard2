import pprint
import sys
import zipfile
from typing import BinaryIO

import toml

from rdlevel_parse import parse
from vitals.facets.artist_list_facet import artist_list_facet
from vitals.facets.rdlevel_sha1_facet import rdlevel_sha1_facet
from vitals.facets.sha1_facet import sha1_facet
from vitals.facets.author_facet import author_facet
from vitals.facets.event_type_facet import event_type_facet
from vitals.facets.bpm_facet import bpm_facet
from vitals.facets.difficulty_facet import difficulty_facet
from vitals.facets.icon_facet import icon_facet
from vitals.facets.key_facet import make_key_facet, make_color_enabled_key_facet
from vitals.facets.player_facet import player_facet
from vitals.facets.tags_facet import tags_facet
from vitals.facets.thumbnail_facet import thumbnail_facet
from vitals.facets.updated_facet import updated_facet

from .pydantic_model import VitalsLevel


class VitalsException(Exception):
    pass


def main(f: BinaryIO):
    facets = {
        ("artist",): make_color_enabled_key_facet(["settings", "artist"]),
        "artist_tokens": artist_list_facet,
        ("song", "song_ct"): make_color_enabled_key_facet(["settings", "song"]),
        "seizure_warning": make_key_facet(["settings", "seizureWarning"], True),
        ("description", "description_ct"): make_color_enabled_key_facet(
            ["settings", "description"]
        ),
        "hue": make_key_facet(["settings", "songNameHue"], 0.0),
        ("authors", "authors_raw"): author_facet,
        ("max_bpm", "min_bpm"): bpm_facet,
        "difficulty": difficulty_facet,
        ("single_player", "two_player"): player_facet,
        "last_updated": updated_facet,
        "tags": tags_facet,
        ("image", "thumb"): thumbnail_facet,
        "icon": icon_facet,
        (
            "has_classics",
            "has_oneshots",
            "has_squareshots",
            "has_freezeshots",
            "has_freetimes",
            "has_holds",
            "has_skipshots",
            "has_window_dance",
        ): event_type_facet,
        "sha1": sha1_facet,
        "rdlevel_sha1": rdlevel_sha1_facet,
    }

    try:
        with zipfile.ZipFile(f) as z:
            with z.open("main.rdlevel", "r") as rdlevel:
                text = rdlevel.read().decode("utf-8-sig")
                parsed = parse(text)

                # get the TOML comment if there is one.
                # there can be only one
                comments = [evt for evt in parsed["events"] if evt["type"] == "Comment"]
                toml_comment = None
                for comment in comments:
                    try:
                        content = comment["text"]
                        if "#orchard" not in content:
                            continue
                        toml_comment = toml.loads(content)
                        break  # only consider the first valid comment we find.
                    except:
                        # it's fine if there isn't a comment.
                        continue

                final = {}
                for key, func in facets.items():
                    try:
                        result = func(
                            **{"obj": parsed, "zip": z, "file": f, "toml": toml_comment}
                        )
                        if isinstance(key, tuple):
                            # multiple keys with (expected) multiple values that map to the keys.
                            for k, v in zip(key, result):
                                final[k] = v
                        else:
                            final[key] = result
                    except Exception as e:
                        raise VitalsException(
                            f"vitals: An unhandled error occured in a facet: {e}"
                        )

                # return final
                return VitalsLevel(**final)

    except zipfile.BadZipFile:
        raise VitalsException(
            "vitals: this is not a zip file, or we couldn't decode it for some reason."
        )
    except KeyError:
        raise VitalsException("vitals: there is no main.rdlevel in the zip.")
