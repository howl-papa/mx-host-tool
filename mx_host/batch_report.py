"""REQ-012 배치 측정 리포트 : 집계(T1) · HTML(T2)."""
import html
from collections import defaultdict


def summarize(rows: list[dict]) -> dict:
    """배치 · 온도 · 리비전별 성공률과 무응답 비율."""
    groups: dict = defaultdict(lambda: {"n": 0, "ok": 0, "no_response": 0})
    for r in rows:
        key = (r.get("lot", ""), int(r["temp_c"]), r["revision"])
        g = groups[key]
        g["n"] += 1
        if r["result"] == "OK":
            g["ok"] += 1
        elif r["result"] == "NO_RESPONSE":
            g["no_response"] += 1
    out = []
    for (lot, temp, rev), g in sorted(groups.items()):
        out.append({"lot": lot, "temp_c": temp, "revision": rev, "n": g["n"],
                    "success_rate": round(g["ok"] / g["n"], 4),
                    "no_response_rate": round(g["no_response"] / g["n"], 4)})
    return {"rows": out, "total": sum(g["n"] for g in groups.values())}


def to_html(summary: dict, title: str = "MX-7 배치 측정 리포트") -> str:
    head = "<tr><th>배치</th><th>온도(°C)</th><th>리비전</th><th>건수</th><th>성공률</th><th>무응답률</th></tr>"
    body = "".join(
        f"<tr><td>{html.escape(r['lot'])}</td><td>{r['temp_c']}</td><td>{r['revision']}</td>"
        f"<td>{r['n']}</td><td>{r['success_rate']:.2%}</td><td>{r['no_response_rate']:.2%}</td></tr>"
        for r in summary["rows"])
    return (f"<!doctype html><meta charset='utf-8'><title>{html.escape(title)}</title>"
            f"<h1>{html.escape(title)}</h1><p>전체 {summary['total']}건</p>"
            f"<table border='1'>{head}{body}</table>")
