"""리더 명령 세션 : 응답 대기 시간(FWT) 계산과 재시도."""
import logging

from .hal import Transport

log = logging.getLogger(__name__)

FC_HZ = 13_560_000  # 반송파 주파수 fc


class ReaderTimeout(Exception):
    pass


def fwt_ms(fwi: int) -> int:
    """ISO/IEC 14443-4 : FWT = (256 * 16 / fc) * 2**FWI  → 밀리초."""
    return (256 * 16 * (2 ** fwi)) // (FC_HZ // 1000)


class ReaderSession:
    def __init__(self, transport: Transport, fwi: int = 4, max_attempts: int = 3):
        self.transport = transport
        self.fwi = fwi
        self.max_attempts = max_attempts

    def command(self, frame: bytes) -> bytes:
        timeout = fwt_ms(self.fwi)
        for attempt in range(1, self.max_attempts + 1):
            resp = self.transport.transceive(frame, timeout_ms=timeout)
            if resp is not None:
                return resp
            log.warning("no response after FWT, retry=%d", attempt)
        raise ReaderTimeout("no response after FWT")

    def close(self) -> None:
        self.transport.close()
