import pytest
import debugpy

DEBUGPY_PORT = 5678

@pytest.fixture
def debug():
    debugpy.listen(DEBUGPY_PORT)
    debugpy.wait_for_client()  # blocks execution until client is attached
    yield