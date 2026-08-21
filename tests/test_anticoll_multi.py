import pytest

from mx_host.anticoll import inventory
from tests.fakes import FakeTransport


@pytest.mark.parametrize("n", [1, 2, 4, 5, 8, 9, 13])
def test_reads_all_tags(n):
    assert len(inventory(FakeTransport(tags=n))) == n
