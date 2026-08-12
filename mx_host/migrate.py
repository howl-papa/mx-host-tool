"""옛 스캔 이력 CSV → SQLite 이관."""
import csv
import sqlite3


def migrate(csv_path: str, db_path: str) -> int:
    conn = sqlite3.connect(db_path)
    conn.execute("CREATE TABLE IF NOT EXISTS scans (uid TEXT, product TEXT, shipped_at TEXT,"
                 " scan_ts TEXT, location TEXT, result TEXT)")
    n = 0
    with open(csv_path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            conn.execute("INSERT INTO scans VALUES (?, ?, ?, ?, ?, ?)",
                         (r["uid"], r["product"], r["shipped_at"], r.get("scan_ts_kst") or r.get("scan_ts"),
                          r["location"], r["result"]))
            n += 1
    conn.commit()
    conn.close()
    return n
