import pytest
from orchard.libs.vitals import analyze

from orchard.libs.hash import sha1

from io import BytesIO

# for vitals, we just test with snapshots.
# all levels used for snapshots are in the "fixtures" directory.

# snapshots don't necessarily show correctness of the data, just that it hasn't changed.
# so I have to remember to check the data added to the snapshot when I add new things to vitals.

# if a change is on purpose, update the snapshots by passing the --snapshot-update flag to pytest.

REPLACE_WITH_HASH = {"image", "thumb", "icon"}


def test_snapshot(rdzip, snapshot, rdzip_path_map):
    with open(rdzip_path_map[rdzip], "rb") as f:
        result = analyze(f)
        # so the snapshots aren't too large, we're replacing the fields mentioned in
        # REPLACE_WITH_HASH with just the sha1 hash
        for prop in REPLACE_WITH_HASH:
            hash = sha1(BytesIO(getattr(result, prop)))
            setattr(result, prop, hash)

        assert result == snapshot
