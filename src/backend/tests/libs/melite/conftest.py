import pytest
import apsw

import apsw.bestpractice


@pytest.fixture
def db():
    apsw.bestpractice.apply(apsw.bestpractice.recommended)
    conn = apsw.Connection(":memory:")
    yield conn