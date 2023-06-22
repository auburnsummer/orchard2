import pytest
from orchard.libs.vitals import analyze
from syrupy.filters import props

# for vitals, we just test with snapshots.
# all levels used for snapshots are in the "fixtures" directory.

# snapshots don't necessarily show correctness of the data, just that it hasn't changed.
# so I have to remember to check the data added to the snapshot when I add new things to vitals.

EXCLUDE_FROM_SNAPSHOT = ["image", "thumb", "icon"]


def test_snapshot(rdzip, snapshot, rdzip_path_map):
    with open(rdzip_path_map[rdzip], "rb") as f:
        actual = analyze(f).model_dump(exclude=EXCLUDE_FROM_SNAPSHOT)
        assert actual == snapshot
