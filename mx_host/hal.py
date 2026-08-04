"""리더 IC와 통신하는 하드웨어 추상 계층."""
from typing import Protocol


class Transport(Protocol):
    def transceive(self, frame: bytes, timeout_ms: float) -> bytes | None:
        """프레임을 보내고 응답을 기다린다. timeout_ms 안에 응답이 없으면 None."""

    def tag_count(self) -> int:
        """리더 앞에 있는 태그 수."""

    def read_uids(self, start: int, n: int) -> list[str]:
        """충돌 방지 라운드에서 start 번째부터 n개 태그 UID를 읽는다."""

    def close(self) -> None:
        ...


class SerialTransport:
    """실제 시험 장비(시리얼) 연결. 이 교육 환경에는 장비가 없다."""

    FIFO_SIZE = 128

    def __init__(self, port: str = "COM3", baud: int = 115200):
        self.port = port
        self.baud = baud
        raise RuntimeError(f"시험 장비가 연결되어 있지 않습니다 ({port}). 교육 환경에서는 모의 장치를 쓰세요.")

    def transceive(self, frame: bytes, timeout_ms: float) -> bytes | None:  # pragma: no cover
        raise NotImplementedError

    def tag_count(self) -> int:  # pragma: no cover
        raise NotImplementedError

    def read_uids(self, start: int, n: int) -> list[str]:  # pragma: no cover
        raise NotImplementedError

    def close(self) -> None:  # pragma: no cover
        pass
