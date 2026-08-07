from mx_host.store import ResultStore


def test_summary():
    st = ResultStore()
    st.save_results("L1", [
        {"sample_id": "S1", "temp_c": 25, "revision": "B", "result": "OK"},
        {"sample_id": "S2", "temp_c": 25, "revision": "B", "result": "NO_RESPONSE"},
    ])
    s = st.batch_summary("L1")
    assert s["total"] == 2 and s["ok"] == 1
