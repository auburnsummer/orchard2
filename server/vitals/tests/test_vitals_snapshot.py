import os
import pytest
import msgspec
from pathlib import Path
from vitals import vitals, vitals_quick
from syrupy.extensions.json import JSONSnapshotExtension

class VitalsSnapshotExtension(JSONSnapshotExtension):
    """Custom extension to save snapshots with meaningful filenames"""
    _file_extension = "json"

    @classmethod
    def get_snapshot_name(cls, *, test_location, index: int) -> str:
        """Generate a snapshot name based on the fixture filename"""
        test_name = str(test_location)
        # The test name will be like "test_vitals_snapshot[filename]"
        # Extract just the filename part
        if '[' in test_name and ']' in test_name:
            return test_name.split('[')[1].split(']')[0]
        return super().get_snapshot_name(test_location=test_location, index=index)

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def get_fixture_files():
    """Get all .rdzip files from the fixtures directory."""
    return sorted([f for f in FIXTURES_DIR.iterdir() if f.suffix == '.rdzip'])

def get_test_id(fixture_path):
    """Generate a test ID from the fixture path."""
    return fixture_path.stem

@pytest.mark.parametrize("fixture_path", get_fixture_files(), ids=get_test_id)
def test_vitals_snapshot(snapshot, fixture_path):
    """Test that vitals output matches the stored snapshot for each fixture."""
    with open(fixture_path, 'rb') as f:
        result = vitals(f)
        # Convert to dict using msgspec's asdict
        result_dict = msgspec.structs.asdict(result)
        # Remove binary data from snapshot for readability
        result_dict['image'] = '<binary>'
        result_dict['thumb'] = '<binary>'
        if result_dict.get('icon'):
            result_dict['icon'] = '<binary>'
        assert result_dict == snapshot(extension_class=VitalsSnapshotExtension) 

@pytest.mark.parametrize("fixture_path", get_fixture_files(), ids=get_test_id)
def test_vitals_quick_snapshot(snapshot, fixture_path):
    """Test that vitals_quick output matches the stored snapshot for each fixture."""
    with open(fixture_path, 'rb') as f:
        result = vitals_quick(f)
        # Convert to dict using msgspec's asdict
        result_dict = msgspec.structs.asdict(result)
        # Remove binary data from snapshot for readability
        result_dict['image'] = '<binary>'
        result_dict['thumb'] = '<binary>'
        if result_dict.get('icon'):
            result_dict['icon'] = '<binary>'
        assert result_dict == snapshot(extension_class=VitalsSnapshotExtension)
