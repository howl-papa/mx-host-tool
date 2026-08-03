"""ISO/IEC 14443 Type A 방식 CRC (CRC_A)."""


def crc16_a(data: bytes) -> int:
    crc = 0x6363
    for byte in data:
        b = byte ^ (crc & 0xFF)
        b = (b ^ (b << 4)) & 0xFF
        crc = ((crc >> 8) ^ (b << 8) ^ (b << 3) ^ (b >> 4)) & 0xFFFF
    return crc
