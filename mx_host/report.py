"""측정 CSV → 텍스트 리포트."""
import csv
from collections import defaultdict


def load_rows(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def build_text_report(rows: list[dict]) -> str:
    by_key: dict = defaultdict(lambda: [0, 0])
    for r in rows:
        key = (r["revision"], int(r["temp_c"]))
        by_key[key][0] += 1
        if r["result"] != "OK":
            by_key[key][1] += 1
    lines = ["MX-7 측정 리포트", f"전체 {len(rows)}건", "리비전 | 온도(°C) | 건수 | 무응답 | 무응답률(%)"]
    for (rev, temp), (n, bad) in sorted(by_key.items()):
        lines.append(f"{rev} | {temp} | {n} | {bad} | {100 * bad / n:.2f}")
    return "\n".join(lines) + "\n"
