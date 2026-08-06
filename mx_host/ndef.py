"""NDEF 텍스트 레코드 해석 (짧은 레코드 / 긴 레코드)."""


class NdefError(ValueError):
    pass


def parse_text_records(msg: bytes) -> list[str]:
    texts = []
    i = 0
    while i < len(msg):
        header = msg[i]
        sr = bool(header & 0x10)   # Short Record
        il = bool(header & 0x08)   # ID Length 있음
        type_len = msg[i + 1]
        i += 2
        if sr:
            payload_len = msg[i]
            i += 1
        else:
            payload_len = int.from_bytes(msg[i:i + 4], "big")
            i += 4
        id_len = msg[i] if il else 0
        i += 1 if il else 0
        rtype = msg[i:i + type_len]
        i += type_len + id_len
        payload = msg[i:i + payload_len]
        if len(payload) != payload_len:
            raise NdefError("payload truncated")
        i += payload_len
        if rtype == b"T":
            lang_len = payload[0] & 0x3F
            texts.append(payload[1 + lang_len:].decode("utf-8"))
        if header & 0x40:  # ME (Message End)
            break
    return texts


def build_text_record(text: str, lang: str = "ko", last: bool = True) -> bytes:
    body = bytes([len(lang)]) + lang.encode() + text.encode("utf-8")
    if len(body) < 256:
        header = 0x80 | 0x10 | 0x01 | (0x40 if last else 0)
        return bytes([header, 1, len(body)]) + b"T" + body
    header = 0x80 | 0x01 | (0x40 if last else 0)
    return bytes([header, 1]) + len(body).to_bytes(4, "big") + b"T" + body
