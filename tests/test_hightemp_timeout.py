"""고객 이슈 재현 : 리비전 B, 125°C에서 응답이 최대 +0.9 ms 늦어짐 (데이터시트 v1.3 ERR-03)."""
from mx_host.session import ReaderSession, fwt_ms
from tests.fakes import FakeTransport


def test_rev_b_125c_delayed_response_is_received():
    # 25°C 최대 3.9 ms + ERR-03 +0.9 ms 중 일부 → 4.4 ms
    s = ReaderSession(FakeTransport(resp_time_ms=4.4))
    assert s.command(b"\x01") == b"\x90\x00"


def test_fwt_not_truncated():
    assert abs(fwt_ms(4) - 4.833) < 0.001
