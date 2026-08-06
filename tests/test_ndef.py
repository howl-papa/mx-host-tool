from mx_host.ndef import build_text_record, parse_text_records


def test_short_record():
    assert parse_text_records(build_text_record("MX-7 Demo")) == ["MX-7 Demo"]


def test_long_record():
    text = "가" * 120  # UTF-8 360바이트 → 긴 레코드
    assert parse_text_records(build_text_record(text)) == [text]
