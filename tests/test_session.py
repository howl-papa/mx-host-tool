import pytest

from mx_host.session import ReaderSession, ReaderTimeout
from tests.fakes import FakeTransport


def test_normal_response():
    s = ReaderSession(FakeTransport(resp_time_ms=3.5))
    assert s.command(b"\x01") == b"\x90\x00"


def test_no_device_response_raises():
    t = FakeTransport(resp_time_ms=50)
    with pytest.raises(ReaderTimeout):
        ReaderSession(t).command(b"\x01")
    assert t.calls == 3
