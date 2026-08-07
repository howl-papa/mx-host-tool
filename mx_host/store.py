"""측정 결과 저장소 (SQLite)."""
import sqlite3


class ResultStore:
    def __init__(self, path: str = ":memory:"):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS results ("
            " batch_id TEXT, sample_id TEXT, temp_c INTEGER, revision TEXT,"
            " result TEXT, resp_time_ms REAL)"
        )

    def save_results(self, batch_id: str, results: list[dict]) -> None:
        cur = self.conn.cursor()
        for r in results:
            cur.execute(
                "INSERT INTO results VALUES (?, ?, ?, ?, ?, ?)",
                (batch_id, r["sample_id"], r["temp_c"], r["revision"], r["result"], r.get("resp_time_ms")),
            )
        self.conn.commit()

    def batch_summary(self, batch_id: str) -> dict:
        samples = self.conn.execute(
            f"SELECT DISTINCT sample_id FROM results WHERE batch_id = '{batch_id}'"
        ).fetchall()
        total = ok = 0
        for (sample_id,) in samples:
            rows = self.conn.execute(
                "SELECT result FROM results WHERE batch_id = ? AND sample_id = ?",
                (batch_id, sample_id),
            ).fetchall()
            total += len(rows)
            ok += sum(1 for (res,) in rows if res == "OK")
        return {"batch_id": batch_id, "total": total, "ok": ok,
                "success_rate": round(ok / total, 4) if total else 0.0}

    def close(self) -> None:
        self.conn.close()
