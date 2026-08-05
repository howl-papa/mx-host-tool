from mx_host.anticoll import inventory
from tests.fakes import FakeTransport


def test_four_tags():
    assert len(inventory(FakeTransport(tags=4))) == 4


def test_eight_tags():
    assert len(inventory(FakeTransport(tags=8))) == 8
