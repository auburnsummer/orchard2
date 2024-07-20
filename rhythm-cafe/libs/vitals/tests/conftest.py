import pytest
from pathlib import Path


def rdzip_paths():
    path = Path(__file__).parent  # / "./fixtures/*.rdzip"
    glob = list(path.glob("./fixtures/*.rdzip"))
    return glob


@pytest.fixture
def rdzip_path_map():
    return rdzip_path_map2()


def rdzip_path_map2():
    glob = rdzip_paths()
    return {p.name: p.as_posix() for p in glob}


def pytest_generate_tests(metafunc):
    if "rdzip" in metafunc.fixturenames:
        # get all my rdzips
        rdzip_map = rdzip_path_map2()
        metafunc.parametrize("rdzip", list(rdzip_map.keys()))
