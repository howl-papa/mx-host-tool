# mx-host-tool

가상 NFC 리더 IC **MX-7**(누리칩스, 가상 회사)의 시험용 호스트 툴입니다.
**교육용 저장소** — 제품 · 회사 · 수치는 모두 가상이며 실제 표준 · 사양과 다를 수 있습니다.
`.env`, `tools/` 안의 장비 · DB 스크립트는 실습용 가짜 파일입니다(실제 장비 · DB · 키 없음).

## 하는 일

- 리더 IC와 명령을 주고받고(세션 · 재시도), 태그를 읽고(충돌 방지 · NDEF)
- 측정 결과를 저장하고(SQLite), 텍스트 리포트를 만듭니다.

## 설치

```
python -m pip install pytest
```

Python 3.11 이상. 그 밖의 외부 라이브러리는 쓰지 않습니다.

## 실행 방법

```
python -m mx_host report data/sample_batch.csv --save report.txt
```

## 테스트

```
python -m pytest
```

## 폴더 구조

| 경로 | 내용 |
|---|---|
| `mx_host/` | 호스트 툴 코드 |
| `tests/` | 테스트 |
| `data/` | 예시 측정 데이터 |
| `docs/` | 데이터시트(가상) · 요구사항 |
| `tools/` | 장비 · DB 연동 스크립트 (실습용 가짜) |
| `regmap.yaml` | MX-7 레지스터맵 (가상) |
