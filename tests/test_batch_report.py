from mx_host.batch_report import summarize, to_html

ROWS = [
    {"lot": "L1", "temp_c": "125", "revision": "B", "result": "OK"},
    {"lot": "L1", "temp_c": "125", "revision": "B", "result": "NO_RESPONSE"},
    {"lot": "L1", "temp_c": "25", "revision": "B", "result": "OK"},
]


def test_summarize():
    s = summarize(ROWS)
    hot = [r for r in s["rows"] if r["temp_c"] == 125][0]
    assert hot["n"] == 2 and hot["no_response_rate"] == 0.5
    assert s["total"] == 3


def test_html():
    h = to_html(summarize(ROWS))
    assert "<table" in h and "http" not in h
