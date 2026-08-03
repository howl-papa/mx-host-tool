import pytest

from mx_host.frame import FrameError, build_frame, parse_frame


def test_roundtrip():
    f = build_frame(0x0C, b"\x30\x04")
    assert parse_frame(f) == (0x0C, b"\x30\x04")


def test_empty_data():
    assert parse_frame(build_frame(0x02)) == (0x02, b"")


def test_bad_crc():
    f = bytearray(build_frame(0x0C, b"\x01"))
    f[-1] ^= 0xFF
    with pytest.raises(FrameError):
        parse_frame(bytes(f))
