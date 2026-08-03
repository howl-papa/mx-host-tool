"""호스트 ↔ 리더 프레임 : [LEN][CMD][DATA...][CRC_L][CRC_H]
LEN은 CMD부터 CRC_H까지의 바이트 수다 (LEN 자기 자신은 제외).
"""
from .crc import crc16_a


class FrameError(ValueError):
    pass


def build_frame(cmd: int, data: bytes = b"") -> bytes:
    body = bytes([cmd]) + bytes(data)
    crc = crc16_a(body)
    payload = body + bytes([crc & 0xFF, crc >> 8])
    return bytes([len(payload)]) + payload


def parse_frame(buf: bytes) -> tuple[int, bytes]:
    if len(buf) < 4:
        raise FrameError("frame too short")
    length = buf[0]
    if len(buf) != length + 1:
        raise FrameError("length mismatch")
    body = buf[1:-2]
    crc = buf[-2] | (buf[-1] << 8)
    if crc != crc16_a(body):
        raise FrameError("crc error")
    return body[0], bytes(body[1:])
