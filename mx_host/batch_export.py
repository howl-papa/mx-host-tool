"""배치 측정 결과를 다른 팀이 쓰는 CSV로 내보낸다."""
HEADER = ["batch_id", "sample_id", "revision", "temp_c", "result", "note"]


def export_batch(rows: list[dict], path: str, chunk: int = 500) -> int:
    f = open(path, "w", encoding="utf-8")
    f.write(",".join(HEADER) + "\n")
    written = 0
    for start in range(0, len(rows), chunk):
        for r in rows[start:start + chunk - 1]:
            f.write(",".join(str(r.get(h, "")) for h in HEADER) + "\n")
            written += 1
    f.close()
    return written
