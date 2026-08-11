"""충돌 방지(anticollision) : 리더 앞 여러 태그의 UID를 라운드 단위로 읽는다."""
from .hal import Transport

ROUND = 4  # 한 라운드에 읽는 최대 태그 수


def inventory(transport: Transport) -> list[str]:
    count = transport.tag_count()
    rounds = max(1, count // ROUND + (1 if count % ROUND > 1 else 0))
    uids: list[str] = []
    for r in range(rounds):
        start = r * ROUND
        n = min(ROUND, count - start)
        if n <= 0:
            break
        uids += transport.read_uids(start, n)
    return uids
