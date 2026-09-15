# pptx_engine API

```python
import sys
from pathlib import Path
sys.path.insert(0, r"<skill>/scripts")          # 스킬 scripts 경로
from pptx_engine import Deck, svg_doc

deck = Deck("output")                            # 텍스처 + 기본 SVG(sprig, fern) 준비
deck.add_svg("chart", svg_doc(580, 520, body))   # assets/chart.svg + PNG 대체 이미지

s = deck.slide("kraft")                          # 배경: kraft | peach | brown
s.scrap("ledger", 780, -40, 560, 300, rot=4)     # 찢어진 종이: paper | paper2 | kraft | ledger | dark

with s.card("paper", 170, 110, 840, 490, rot=-1.2):   # 종이 카드 + 안쪽 로컬 좌표
    s.text(90, 70, 660, 22, "KICKER", "kicker")
    s.text(90, 104, 700, 210, ["{A}I와 지역", "노동시장"], "display", size=92, lh=1.08)
    s.line(90, 396, 510, 396)                     # 점선 구분선

with s.stamp(220, 184, 410, 228, rot=-1, badge=1):   # 우표형 다크 카드
    s.text(30, 34, 240, 30, "제목", "h3", color="paper2")

s.oval(52, 46, 46, 46, "01")                     # 번호 원 (기본: brown800 바탕, paper2 글자)
s.rect(44, 352, 432, 112, fill="tint", radius=10) # 박스 (text= 로 가운데 글자 가능)
s.svg("sprig", 990, 290, 270, 560, rot=-10)      # SVG 그래픽
deck.save("파일명.pptx")                          # + output/preview.html
```

## 메서드

| 메서드 | 인자 |
|---|---|
| `Deck(out_dir)` | 출력 폴더 (assets/ 자동 생성) |
| `deck.add_svg(name, svg_text)` | `svg_doc(w, h, body)`로 만든 SVG 문자열 등록 |
| `deck.slide(bg)` | `"kraft"`, `"peach"`, `"brown"` |
| `deck.save(pptx_name, preview_name="preview.html")` | 저장 경로 반환 |
| `s.scrap(kind, x, y, w, h, rot=0, shadow=None)` | paper/paper2는 기본 그림자 |
| `s.card(kind, x, y, w, h, rot=0, shadow=None)` | context manager, 안쪽 좌표 = 카드 좌상단 기준 |
| `s.stamp(x, y, w, h, rot=0, badge=None)` | context manager, 우표 카드 + 번호 배지 |
| `s.text(x, y, w, h, content, style="body", align="l", anchor="t", **kw)` | 아래 스타일/옵션 참고 |
| `s.rect(x, y, w, h, fill="paper", line=None, line_w=1, dash=False, radius=0, shadow=False, text=None, **text_kw)` | `fill=None`이면 투명 |
| `s.oval(x, y, w, h, text=None, fill="brown800", line=None, line_w=1, shadow=False, **text_kw)` | |
| `s.line(x1, y1, x2, y2, color="rule", width=2, dash=True)` | |
| `s.svg(name, x, y, w, h, rot=0)` | 카드 안에서 쓰면 카드 회전도 반영 |

## 텍스트

- `content`: 문자열 또는 문단 리스트 (리스트 = 줄바꿈된 문단)
- 인라인 표기: `**굵게**`, `{섞기 글자}`(제목 콜라주용: 작고 다른 색), `^^강조^^`(굵은 갈색 / 다크 위 ledger)
- 옵션: `size`(px), `bold`, `color`(토큰 또는 hex), `lh`(행간 배수), `space`(문단 뒤 px), `font`("latin" | "display"), `spacing`(자간 em), `mix_color`

| style | size | 굵기 | 색 | 행간 |
|---|---|---|---|---|
| `display` | 54 | Arial Black | brown800 | 1.06 |
| `h2` | 28 | bold | brown800 | 1.3 |
| `h3` | 21 | bold | brown800 | 1.35 |
| `body` | 19 | | ink | 1.65 |
| `small` | 16 | | ink | 1.6 |
| `caption` | 14 | | muted | 1.5 |
| `kicker` | 14 | bold, 자간 .18em | brown600 | 1.2 |

## 색 토큰

`brown900 #4A2410` · `brown800 #5C2E14` · `brown600 #7A4A2A` · `kraft #B39373` · `kraft_light #CDB295` ·
`paper #EAE0CC` · `paper2 #F3EBDD` · `peach #F8E7D3` · `ledger #EFD6A0` · `ink #3B2414` · `muted #7B6552` ·
`yellow #E6BE4A` · `lilac #A98ABD` · `sage #6D7C53` · `white #FFFDF8` · `up #5E7A3A` · `down #A2452B` ·
`tint #E1D4BD`(종이 위 옅은 박스) · `stitch #8F6B55`(다크 위 점선) · `rule #CDBBA3`(종이 위 점선)

## 자주 쓰는 패턴 (examples/build_ai_labor_deck.py)

- `chip(s, x, y, label)`: 둥근 라벨 (폭 자동 추정)
- `arrowhead(ex, ey, cx, cy)`: SVG 곡선 끝 화살촉 (marker 대신)
- 아이콘 SVG 120×120: 원(`s.oval(..., fill="white", line="paper2", line_w=6, shadow=True)`) 위에 `s.svg(icon, ...)`
- 표: 헤더 `s.rect(fill="brown800")` + 열마다 `s.text(anchor="m")`, 짝수 행 `fill="tint"`, 행 사이 `s.line`
