from mx_host.report import build_text_report, load_rows


def test_report_header_and_rows():
    text = build_text_report(load_rows("data/sample_batch.csv"))
    lines = text.splitlines()
    assert lines[0] == "MX-7 측정 리포트"
    assert lines[1].startswith("전체 ")
    assert any(line.startswith("B | 125 |") for line in lines)
