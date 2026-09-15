"""주요 시장 지표 조회 스크립트.

Yahoo Finance(yfinance)에서 아래 지표의 최신 값을 가져와 정리해 출력한다.
- S&P500, 나스닥, 다우존스, 코스피, 코스닥
- 미국채 10년물 금리, 금 가격, 원/달러 환율

사용법:
    python market_indicators.py            # 표 형태로 출력
    python market_indicators.py --json     # JSON 출력
    python market_indicators.py --csv out.csv
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from unicodedata import east_asian_width

try:
    import yfinance as yf
except ImportError:  # pragma: no cover
    sys.exit("yfinance가 필요합니다.  pip install -r requirements.txt")


@dataclass(frozen=True)
class Indicator:
    name: str
    ticker: str
    unit: str
    fmt: str = "{:,.2f}"


INDICATORS = [
    Indicator("S&P 500", "^GSPC", "pt"),
    Indicator("나스닥 종합", "^IXIC", "pt"),
    Indicator("다우존스", "^DJI", "pt"),
    Indicator("코스피", "^KS11", "pt"),
    Indicator("코스닥", "^KQ11", "pt"),
    Indicator("미국채 10년물 금리", "^TNX", "%", "{:,.3f}"),
    Indicator("금 (선물)", "GC=F", "USD/oz"),
    Indicator("원/달러 환율", "KRW=X", "KRW", "{:,.2f}"),
]


def fetch(ind: Indicator) -> dict:
    """지표 1건의 최근 종가와 전일 대비 변동을 조회한다."""
    row = {
        "name": ind.name,
        "ticker": ind.ticker,
        "unit": ind.unit,
        "date": None,
        "price": None,
        "prev_close": None,
        "change": None,
        "change_pct": None,
        "error": None,
    }
    try:
        # 휴장일/연휴를 감안해 넉넉히 10일치를 받아 마지막 2개 종가를 사용한다.
        hist = yf.Ticker(ind.ticker).history(period="10d", interval="1d")
        closes = hist["Close"].dropna()
        if closes.empty:
            row["error"] = "데이터 없음"
            return row

        last = float(closes.iloc[-1])
        row["date"] = closes.index[-1].strftime("%Y-%m-%d")
        row["price"] = last

        if len(closes) >= 2:
            prev = float(closes.iloc[-2])
            row["prev_close"] = prev
            row["change"] = last - prev
            row["change_pct"] = (last - prev) / prev * 100 if prev else None
    except Exception as exc:  # 개별 지표 실패가 전체를 막지 않도록 한다.
        row["error"] = f"{type(exc).__name__}: {exc}"
    return row


def fetch_all() -> list[dict]:
    return [fetch(ind) for ind in INDICATORS]


def _w(text: str) -> int:
    """한글 등 전각 문자를 2칸으로 세는 표시 폭."""
    return sum(2 if east_asian_width(ch) in "WF" else 1 for ch in text)


def _ljust(text: str, width: int) -> str:
    return text + " " * max(0, width - _w(text))


def _rjust(text: str, width: int) -> str:
    return " " * max(0, width - _w(text)) + text


def render_table(rows: list[dict]) -> str:
    fmt_by_ticker = {i.ticker: i.fmt for i in INDICATORS}
    header = (
        _ljust("지표", 20) + _ljust("티커", 10) + _ljust("기준일", 12)
        + _rjust("현재값", 14) + _rjust("전일대비", 12) + _rjust("등락률", 10) + "  단위"
    )
    lines = [
        f"■ 주요 시장 지표  (조회: {datetime.now().astimezone():%Y-%m-%d %H:%M:%S %Z})",
        "",
        header,
        "-" * _w(header),
    ]

    for r in rows:
        if r["error"]:
            lines.append(_ljust(r["name"], 20) + _ljust(r["ticker"], 10) + f"조회 실패 - {r['error']}")
            continue

        fmt = fmt_by_ticker[r["ticker"]]
        price = fmt.format(r["price"])
        if r["change"] is None:
            change = pct = "-"
        else:
            sign = "+" if r["change"] >= 0 else ""
            change = sign + fmt.format(r["change"])
            pct = f"{sign}{r['change_pct']:.2f}%"

        lines.append(
            _ljust(r["name"], 20) + _ljust(r["ticker"], 10) + _ljust(r["date"], 12)
            + _rjust(price, 14) + _rjust(change, 12) + _rjust(pct, 10) + f"  {r['unit']}"
        )

    lines.append("")
    lines.append("* 미국 지수/금은 현지 거래일, 코스피·코스닥은 한국 거래일 기준 종가입니다.")
    return "\n".join(lines)


def write_csv(rows: list[dict], path: str) -> None:
    import csv

    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="주요 시장 지표 조회 (Yahoo Finance)")
    parser.add_argument("--json", action="store_true", help="JSON으로 출력")
    parser.add_argument("--csv", metavar="PATH", help="결과를 CSV 파일로 저장")
    args = parser.parse_args()

    rows = fetch_all()

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        print(render_table(rows))

    if args.csv:
        write_csv(rows, args.csv)
        print(f"\nCSV 저장 완료: {args.csv}")

    return 1 if all(r["error"] for r in rows) else 0


if __name__ == "__main__":
    raise SystemExit(main())
