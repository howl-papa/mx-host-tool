"""테스트용 간단한 가짜 장치 (응답 시간 고정)."""


class FakeTransport:
    def __init__(self, resp_time_ms: float = 3.5, tags: int = 1):
        self.resp_time_ms = resp_time_ms
        self.tags = tags
        self.closed = False
        self.calls = 0

    def transceive(self, frame, timeout_ms):
        self.calls += 1
        return b"\x90\x00" if self.resp_time_ms <= timeout_ms else None

    def tag_count(self):
        return self.tags

    def read_uids(self, start, n):
        return [f"04:00:00:00:00:00:{i:02X}" for i in range(start, start + n)]

    def close(self):
        self.closed = True
