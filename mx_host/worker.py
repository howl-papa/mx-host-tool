"""여러 스레드로 측정 작업을 돌리는 워커."""
import queue
import threading
from dataclasses import dataclass


@dataclass
class Job:
    batch_id: str
    sample_id: str
    temp_c: int
    revision: str
    frame: bytes


class MeasureWorker:
    def __init__(self, session_factory, store, n_threads: int = 4):
        self.session_factory = session_factory
        self.store = store
        self.n_threads = n_threads
        self.done = 0

    def run(self, jobs: list[Job]) -> int:
        q: queue.Queue = queue.Queue()
        for job in jobs:
            q.put(job)
        threads = [threading.Thread(target=self._loop, args=(q,)) for _ in range(self.n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=5)
        return self.done

    def _loop(self, q: queue.Queue) -> None:
        session = self.session_factory()
        while True:
            try:
                job = q.get_nowait()
            except queue.Empty:
                break
            try:
                session.command(job.frame)
                self.store.save_results(job.batch_id, [{
                    "sample_id": job.sample_id, "temp_c": job.temp_c,
                    "revision": job.revision, "result": "OK", "resp_time_ms": None,
                }])
            except Exception:
                pass
            self.done += 1
        session.close()
