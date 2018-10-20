# pylint: disable=no-self-use, redefined-outer-name
from datetime import datetime
import pytest

import schema.base as sut


@pytest.fixture
def dt():
    return sut.Datetime(description="<description>")


class TestDateTime:
    def test_parses_according_to_fmt_string(self, dt):
        parse = dt.parser(fmt="%Y-%m-%dT%H:%M:%S")
        expected = datetime(2018, 10, 10, 20, 20, 20)
        actual = parse("2018-10-10T20:20:20")
        assert actual == expected
