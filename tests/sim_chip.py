"""모의 MX-7 칩 : hal.Transport 인터페이스를 지키는 가짜 장치."""


class SimChip:
    T_RESP_MS = 3.5          # 25°C 대표값 (데이터시트 Table 7-1)
    ERR03_EXTRA_MS = 0.9     # Rev B, Tj > 110°C 최대 증가 (ERR-03)

    def __init__(self, mode: str = "normal", revision: str = "B", temp_c: int = 25, tags: int = 1):
        self.mode, self.revision, self.temp_c, self.tags = mode, revision, temp_c, tags
        self.regs = {0x0B: 0x04}
        self.calls = 0
        self.closed = False

    def resp_time_ms(self) -> float:
        t = self.T_RESP_MS
        if self.mode == "hot_delay" or (self.revision == "B" and self.temp_c > 110):
            t += self.ERR03_EXTRA_MS
        return t

    def transceive(self, frame, timeout_ms):
        self.calls += 1
        if self.mode == "no_response":
            return None
        return b"\x90\x00" if self.resp_time_ms() <= timeout_ms else None

    def tag_count(self):
        return self.tags

    def read_uids(self, start, n):
        return [f"04:10:00:00:00:00:{i:02X}" for i in range(start, start + n)]

    def close(self):
        self.closed = True
