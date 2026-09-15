---
name: market-snapshot
description: Yahoo Finance에서 주요 시장 지표(S&P500, 나스닥, 다우존스, 코스피, 코스닥, 미국채 10년물 금리, 금 가격, 원/달러 환율)의 최신 값을 조회해 표와 해설로 정리한다. 사용자가 현재 마켓 상황, 증시·환율·금리·금값 현황, 시장 스냅샷, "오늘 시장 어때?" 같은 요청을 할 때 사용한다.
---

# Market Snapshot

주요 시장 지표 8종의 최신 종가와 전일 대비 변동을 조회하고, 사람이 읽기 쉬운 표와 짧은 해설로 정리한다.

## 실행 방법

1. 이 SKILL.md가 있는 디렉토리(스킬 base directory)의 `scripts/market_indicators.py`를 JSON 모드로 실행한다.

   ```bash
   PYTHONIOENCODING=utf-8 python "<skill base dir>/scripts/market_indicators.py" --json
   ```

   - Windows PowerShell이라면: `$env:PYTHONIOENCODING='utf-8'; python "<skill base dir>\scripts\market_indicators.py" --json`
   - `yfinance가 필요합니다` 오류가 나면 `pip install -r "<skill base dir>/scripts/requirements.txt"` 실행 후 재시도한다.
   - 사용자가 CSV 저장을 원하면 `--csv <경로>` 옵션을 추가한다.

2. JSON 결과의 각 항목 필드: `name`, `ticker`, `unit`, `date`(기준일), `price`, `prev_close`, `change`, `change_pct`, `error`.

## 결과 정리 형식

1. **제목**: `시장 스냅샷 (조회 시각 YYYY-MM-DD HH:MM KST)`
2. **표**: 지표 | 현재값 | 전일대비 | 등락률 | 기준일
   - 천 단위 콤마, 소수점 2자리(미국채 금리는 3자리)
   - 등락률 앞에 🔺(상승) / 🔻(하락) 표시
   - 단위 표기: 금리 `%`, 금 `$…/oz`, 환율 `…원`
   - 미국채 10년물 금리는 전일대비를 `%p`로만 쓰고 등락률 칸은 `-`로 둔다. (금리의 % 변화율은 %p와 혼동되기 쉬움)
   - `error`가 있는 항목은 "조회 실패"로 표시하고 사유를 짧게 적는다.
3. **해설** (3~5문장):
   - 미국 증시 / 한국 증시 전반의 방향
   - 가장 크게 움직인 지표
   - 원/달러 환율 상승 = 원화 약세, 금리·금 흐름 등 지표 간 연관성
   - 투자 권유나 가격 예측은 하지 않는다.
4. **주의사항**: 기준일이 지표마다 다를 수 있음을 알린다(미국 지수는 현지 거래일 기준이라 한국 시간 낮에는 전날 종가). 장중 지표는 실시간으로 조금씩 변한다.

## 참고

- 데이터 출처: Yahoo Finance (yfinance), 지연 시세일 수 있음
- 티커: `^GSPC`, `^IXIC`, `^DJI`, `^KS11`, `^KQ11`, `^TNX`, `GC=F`, `KRW=X`
- 지표를 추가/변경하려면 `scripts/market_indicators.py`의 `INDICATORS` 목록을 수정한다.
