"""충돌 방지(anticollision) : 리더 앞 여러 태그의 UID를 라운드 단위로 읽는다."""
from .hal import Transport

ROUND = 4  # 한 라운드에 읽는 최대 태그 수


def inventory(transport: Transport) -> list[str]:
    count = transport.tag_count()
    uids: list[str] = []
    for start in range(0, count - 1, ROUND):
        uids += transport.read_uids(start, min(ROUND, count - start))
    return uids
