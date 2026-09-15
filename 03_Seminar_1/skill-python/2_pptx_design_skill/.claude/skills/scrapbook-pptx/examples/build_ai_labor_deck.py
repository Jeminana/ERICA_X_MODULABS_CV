"""BOK 이슈노트 제2026-25호 「AI와 지역 노동시장」 요약본 → Pressed Flower Scrapbook PPTX.

실행: python build_ai_labor_deck.py
결과: output/AI와_지역노동시장.pptx, output/preview.html
"""
import math
import sys
from pathlib import Path

# 엔진 위치: 새 덱으로 복사하면 <skill>/scripts 의 절대경로로 바꾼다
SKILL_SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SKILL_SCRIPTS))

from pptx_engine import Deck, svg_doc  # noqa: E402

deck = Deck("output")

BROWN, BROWN6, INK, PAPER2, LEDGER = "#5C2E14", "#7A4A2A", "#3B2414", "#F3EBDD", "#EFD6A0"
YELLOW, LILAC, SAGE, KRAFT_L, WHITE = "#E6BE4A", "#A98ABD", "#6D7C53", "#CDB295", "#FFFDF8"


# =====================================================================
# SVG 그래픽
# =====================================================================
def arrowhead(ex, ey, cx, cy, size=11, color=BROWN6):
    dx, dy = ex - cx, ey - cy
    length = math.hypot(dx, dy)
    ux, uy = dx / length, dy / length
    bx, by = ex - ux * size, ey - uy * size
    px, py = -uy * size * 0.55, ux * size * 0.55
    return f'<path d="M{ex:.1f} {ey:.1f} L{bx + px:.1f} {by + py:.1f} L{bx - px:.1f} {by - py:.1f} Z" fill="{color}"/>'


deck.add_svg("icon_gen", svg_doc(120, 120, (
    f'<rect x="24" y="18" width="58" height="78" rx="4" fill="{WHITE}" stroke="{BROWN}" stroke-width="3"/>'
    f'<path d="M35 38 H71 M35 50 H71 M35 62 H63 M35 74 H55" stroke="{KRAFT_L}" stroke-width="4" stroke-linecap="round"/>'
    f'<path d="M91 46 L96 59 L109 64 L96 69 L91 82 L86 69 L73 64 L86 59 Z" fill="{YELLOW}" stroke="{BROWN}" stroke-width="2"/>'
    f'<path d="M98 16 L100.5 23.5 L108 26 L100.5 28.5 L98 36 L95.5 28.5 L88 26 L95.5 23.5 Z" fill="{LILAC}"/>')))

deck.add_svg("icon_agent", svg_doc(120, 120, (
    f'<path d="M34 36 L86 36 L60 88 Z" fill="none" stroke="{BROWN6}" stroke-width="3" stroke-dasharray="6 5"/>'
    f'<circle cx="34" cy="36" r="16" fill="{YELLOW}" stroke="{BROWN}" stroke-width="3"/>'
    f'<circle cx="86" cy="36" r="16" fill="{LILAC}" stroke="{BROWN}" stroke-width="3"/>'
    f'<circle cx="60" cy="88" r="16" fill="{SAGE}" stroke="{BROWN}" stroke-width="3"/>'
    f'<path d="M52 88 L58 94 L68 82" fill="none" stroke="{WHITE}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<text x="34" y="41" font-size="14" font-weight="700" fill="{BROWN}" text-anchor="middle" font-family="Arial">1</text>'
    f'<text x="86" y="41" font-size="14" font-weight="700" fill="{BROWN}" text-anchor="middle" font-family="Arial">2</text>')))

deck.add_svg("icon_physical", svg_doc(120, 120, (
    f'<rect x="20" y="94" width="56" height="13" rx="3" fill="{BROWN6}"/>'
    f'<path d="M48 94 L40 60 L78 38" fill="none" stroke="{BROWN}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<circle cx="47" cy="92" r="7" fill="{YELLOW}" stroke="{BROWN}" stroke-width="2.5"/>'
    f'<circle cx="40" cy="60" r="7" fill="{YELLOW}" stroke="{BROWN}" stroke-width="2.5"/>'
    f'<circle cx="78" cy="38" r="6" fill="{YELLOW}" stroke="{BROWN}" stroke-width="2.5"/>'
    f'<path d="M83 33 L97 25 M85 42 L100 40" stroke="{BROWN}" stroke-width="5" stroke-linecap="round"/>'
    f'<rect x="84" y="76" width="24" height="24" fill="{KRAFT_L}" stroke="{BROWN}" stroke-width="2.5"/>')))

deck.add_svg("icon_trend", svg_doc(120, 120, (
    f'<path d="M20 98 H104 M20 98 V18" fill="none" stroke="{BROWN6}" stroke-width="3" stroke-linecap="round"/>'
    f'<polyline points="30,84 50,70 66,76 90,42" fill="none" stroke="{BROWN}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
    f'<path d="M78 41 L91 40 L90 53" fill="none" stroke="{BROWN}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
    f'<circle cx="30" cy="84" r="5" fill="{LILAC}"/><circle cx="50" cy="70" r="5" fill="{YELLOW}"/><circle cx="66" cy="76" r="5" fill="{SAGE}"/>')))


def chart_jobs():
    """지역별 취업자 중 직군 비중 (수도권 vs 비수도권), 요약본 수치만 사용."""
    x0, k = 150, 13
    o = [f'<rect x="150" y="6" width="16" height="16" fill="{YELLOW}"/>'
         f'<text x="174" y="19" font-size="15" fill="{PAPER2}">수도권</text>'
         f'<rect x="250" y="6" width="16" height="16" fill="{KRAFT_L}"/>'
         f'<text x="274" y="19" font-size="15" fill="{PAPER2}">비수도권</text>']
    for v in (0, 10, 20, 30):
        x = x0 + k * v
        o.append(f'<line x1="{x}" y1="48" x2="{x}" y2="478" stroke="{PAPER2}" stroke-opacity="0.16" stroke-width="1"/>'
                 f'<text x="{x}" y="498" font-size="13" fill="{KRAFT_L}" text-anchor="middle">{v}%</text>')

    def section(y, title, rows):
        o.append(f'<text x="0" y="{y}" font-size="15" font-weight="700" fill="{LEDGER}">{title}</text>')
        for j, (name, a, b) in enumerate(rows):
            ry = y + 16 + j * 52
            o.append(f'<text x="140" y="{ry + 23}" font-size="15" fill="{PAPER2}" text-anchor="end">{name}</text>')
            for off, val, col in ((0, a, YELLOW), (19, b, KRAFT_L)):
                o.append(f'<rect x="{x0}" y="{ry + off}" width="{val * k:.1f}" height="16" fill="{col}"/>'
                         f'<text x="{x0 + val * k + 6:.1f}" y="{ry + off + 13}" font-size="13" font-weight="700" '
                         f'fill="{PAPER2}">{val}%</text>')

    section(66, "생성형 · 에이전틱AI 노출도 높은 직군",
            [("전문가", 28.1, 18.0), ("사무직", 20.2, 15.8), ("판매직", 8.9, 8.2), ("관리자", 1.5, 1.2)])
    section(316, "피지컬AI 노출도 높은 직군",
            [("장치·기계조작", 8.1, 12.0), ("단순노무", 12.7, 14.6), ("서비스직", 12.2, 13.1)])
    o.append(f'<text x="0" y="516" font-size="12" fill="{KRAFT_L}">자료: 한국은행 BOK 이슈노트 제2026-25호 요약 · 권역별 취업자 중 직군 비중</text>')
    return svg_doc(580, 520, "".join(o))


def cycle():
    """위험요인 ①: 수도권 집중의 순환구조."""
    o = [f'<text x="180" y="30" font-size="17" font-weight="700" fill="{BROWN}" text-anchor="middle">위험요인 ① 이 만드는 순환</text>',
         f'<circle cx="180" cy="222" r="34" fill="none" stroke="{KRAFT_L}" stroke-width="2" stroke-dasharray="5 4"/>',
         f'<text x="180" y="228" font-size="17" font-weight="700" fill="{BROWN6}" text-anchor="middle">순환</text>']
    nodes = [((115, 60), YELLOW, "AI투자·인재", "수도권 집중"), ((220, 190), WHITE, "생산성·임금", "격차 확대"),
             ((115, 320), WHITE, "비수도권 청년", "수도권 유입"), ((10, 190), WHITE, "집적경제", "더욱 강화")]
    for (x, y), fill, l1, l2 in nodes:
        o.append(f'<rect x="{x}" y="{y}" width="130" height="64" rx="10" fill="{fill}" stroke="{BROWN}" stroke-width="2"/>'
                 f'<text x="{x + 65}" y="{y + 28}" font-size="14" font-weight="700" fill="{BROWN}" text-anchor="middle">{l1}</text>'
                 f'<text x="{x + 65}" y="{y + 48}" font-size="14" font-weight="700" fill="{BROWN}" text-anchor="middle">{l2}</text>')
    for (sx, sy), (cx, cy), (ex, ey) in (((245, 96), (285, 104), (285, 184)), ((285, 258), (285, 344), (251, 350)),
                                         ((115, 350), (75, 344), (75, 262)), ((75, 186), (75, 102), (109, 94))):
        o.append(f'<path d="M{sx} {sy} Q{cx} {cy} {ex} {ey}" fill="none" stroke="{BROWN6}" stroke-width="3"/>'
                 + arrowhead(ex, ey, cx, cy))
    o.append(f'<text x="180" y="424" font-size="12" fill="#7B6552" text-anchor="middle">AI투자와 숙련노동의 높은 보완성 → 격차 확대의 순환</text>')
    return svg_doc(360, 440, "".join(o))


deck.add_svg("chart_jobs", chart_jobs())
deck.add_svg("cycle", cycle())


def chip(s, x, y, label, fill="ledger", color="brown800"):
    w = 24 + sum(14 if ord(ch) > 0x2E80 else 8.5 for ch in label)
    s.rect(x, y, w, 28, fill=fill, radius=14, text=label, style="small", size=14, bold=True, color=color, lh=1.2)
    return w


# =====================================================================
# 01 표지
# =====================================================================
s = deck.slide("kraft")
s.scrap("ledger", 780, -40, 560, 300, 4)
s.scrap("dark", -50, 520, 440, 260, -3)
with s.card("paper", 170, 110, 840, 490, -1.2):
    s.text(90, 70, 660, 22, "BOK 이슈노트 제2026-25호 · 한국은행 지역경제조사팀", "kicker")
    s.text(90, 104, 700, 210, ["{A}I와 지역", "노동{시}장"], "display", size=92, lh=1.08)
    s.text(90, 326, 680, 40, "지역간 격차 확대 위험과 새로운 기회", size=26, lh=1.3)
    s.line(90, 396, 510, 396)
    s.text(90, 414, 640, 26, "**요약 발표** · 2026. 09. 15", "small", color="muted")
s.svg("sprig", -50, -80, 240, 500, 165)
s.svg("fern", 950, -10, 90, 400, 14)
s.svg("sprig", 990, 290, 270, 560, -10)

# =====================================================================
# 02 목차
# =====================================================================
s = deck.slide("peach")
s.scrap("dark", -70, -40, 480, 800, 2)
s.text(70, 226, 300, 22, "CONTENTS", "kicker", color="ledger")
s.text(70, 254, 320, 100, "목{차}", "display", size=84, color="paper2")
s.text(70, 372, 300, 90, ["한국은행 BOK 이슈노트", "요약본의 핵심 10개 항목을", "다섯 부분으로 정리했습니다."],
       "small", color="paper2")
s.scrap("ledger", 350, 570, 300, 200, -6)
agenda = [("연구 질문과 AI 유형", "세 가지 AI 유형과 노출도라는 잣대"),
          ("직업별 · 지역별 AI 노출도", "누가, 어디서 AI에 더 많이 노출되는가"),
          ("AI 확산과 지역 노동시장 변화", "취업자수 · 인력부족 · 임금의 초기 징후"),
          ("위험요인과 기회요인", "격차를 키우는 힘과 줄이는 힘"),
          ("정책적 시사점", "지역이 준비해야 할 세 가지 과제")]
with s.card("paper", 520, 62, 690, 596, 0.8):
    for i, (t, d) in enumerate(agenda):
        y = 46 + i * 104
        s.oval(52, y, 46, 46, f"{i + 1:02d}")
        s.text(118, y - 3, 520, 28, t, "h3")
        s.text(118, y + 26, 520, 26, d, "small", color="muted")
        if i < len(agenda) - 1:
            s.line(52, y + 76, 638, y + 76)
s.svg("sprig", 230, 420, 210, 440, -14)

# =====================================================================
# 03 연구 질문
# =====================================================================
s = deck.slide("brown")
s.scrap("ledger", -50, -40, 440, 130, -4)
s.text(120, 110, 600, 22, "01 · 연구 질문", "kicker", color="ledger")
s.text(120, 136, 900, 70, "무엇을 {물}었나", "display", color="paper2")
with s.card("paper", 90, 236, 1100, 434, 0.5):
    s.text(56, 38, 988, 50, "“AI 확산은 지역간 노동시장 격차를 키울까, 줄일까?”", size=30, bold=True, color="brown800",
           align="c", lh=1.4)
    s.line(56, 116, 1044, 116)
    steps = [("STEP 1", "AI를 세 유형으로 구분", "생성형 · 에이전틱 · 피지컬. AI 유형에 따라 활용 방식과 영향이 다를 수 있기 때문입니다."),
             ("STEP 2", "직업별·지역별 노출도", "유형별 AI 활용가능성(노출도)을 **국내 최초로** 직업별 · 지역별로 산출했습니다."),
             ("STEP 3", "고용지표와의 관계", "AI 확산 이후 취업자수 등 지역별 고용지표가 노출도와 어떤 관계를 보이는지 초기 징후를 살폈습니다.")]
    for i, (k, t, d) in enumerate(steps):
        x = 56 + i * 340
        s.text(x, 146, 300, 20, k, "kicker")
        s.text(x, 172, 300, 32, t, "h3")
        s.text(x, 212, 300, 140, d, "small")
        if i:
            s.line(x - 20, 146, x - 20, 350)
    s.text(56, 384, 988, 22, "* 초기 징후 분석으로, AI가 고용지표 변화의 원인이라고 인과관계를 단정하기는 어렵습니다.", "caption")
s.svg("fern", 0, 430, 90, 400, -15)
s.svg("sprig", 1070, -60, 230, 480, 190)

# =====================================================================
# 04 AI 세 유형과 직업별 노출도
# =====================================================================
s = deck.slide("peach")
s.scrap("ledger", 900, -50, 460, 230, 5)
s.scrap("kraft", -40, 610, 1360, 200, -1.5)
with s.card("paper", 110, 66, 1060, 566, -0.6):
    s.text(0, 34, 1060, 64, "{세} 가지 AI, 다른 일자리", "display", align="c")
    s.text(0, 104, 1060, 26, "직업별 AI노출도 = 그 직업의 업무에 AI를 활용할 수 있는 가능성", "small", color="muted", align="c")
    types = [("icon_gen", "생성형 AI", "GENERATIVE", "문서작성 · 정보처리 비중이 높은 일", "사무직 · 판매직 · 전문가"),
             ("icon_agent", "에이전틱 AI", "AGENTIC", "여러 단계의 업무를 스스로 수행", "관리직 > 사무직 > 판매직"),
             ("icon_physical", "피지컬 AI", "PHYSICAL", "로봇 · 기계로 물리적 작업을 수행", "장치·기계조작 · 단순노무")]
    for i, (ic, name, en, desc, jobs) in enumerate(types):
        cx = 190 + i * 340
        s.oval(cx - 80, 150, 160, 160, fill="white", line="paper2", line_w=6, shadow=True)
        s.svg(ic, cx - 52, 178, 104, 104)
        s.text(cx - 150, 330, 300, 34, name, "h3", size=24, align="c")
        s.text(cx - 150, 368, 300, 20, en, "kicker", align="c")
        s.text(cx - 150, 398, 300, 26, desc, "small", color="muted", align="c")
        s.rect(cx - 140, 440, 280, 88, fill="tint", radius=10)
        s.text(cx - 130, 452, 260, 20, "노출도 높은 직군", "caption", align="c")
        s.text(cx - 130, 476, 260, 40, jobs, "h3", size=19, align="c")
s.svg("sprig", -40, 370, 200, 420, 16)
s.svg("sprig", 1150, 380, 200, 420, -18)

# =====================================================================
# 05 지역별 AI 노출도
# =====================================================================
s = deck.slide("kraft")
with s.card("paper2", 370, 36, 540, 118, -1.5):
    s.text(0, 0, 540, 118, "지역별 {A}I 노출도", "display", size=46, align="c", anchor="m")
with s.card("paper", 90, 190, 500, 476, -1):
    s.text(42, 38, 416, 20, "수도권이 높은 유형", "kicker")
    s.text(42, 62, 416, 40, "생성형 · 에이전틱 AI", "h2")
    s.text(42, 124, 416, 26, "생성형 AI 노출도 순위", "h3", size=18)
    s.text(42, 154, 416, 34, "① 서울   ② 세종   ③ 경기   ④ 인천", size=22, bold=True)
    s.text(42, 206, 416, 26, "에이전틱 AI 노출도 순위", "h3", size=18)
    s.text(42, 236, 416, 34, "① 서울   ② 세종   ③ 경기   ④ 대전", size=22, bold=True)
    s.line(42, 298, 458, 298)
    s.text(42, 316, 416, 130, "두 유형 모두 **1~3위가 서울 · 세종 · 경기**로 같습니다. 지식서비스업이 몰려 있어 "
                              "사무직 · 전문가 일자리가 많은 곳입니다.", "small")
with s.card("dark", 690, 190, 500, 476, 1, shadow=True):
    s.text(42, 38, 416, 20, "비수도권이 높은 유형", "kicker", color="ledger")
    s.text(42, 62, 416, 40, "피지컬 AI", "h2", color="paper2")
    s.text(42, 124, 416, 26, "피지컬 AI 노출도 순위", "h3", size=18, color="paper2")
    s.text(42, 154, 416, 34, "① 경북   ② 전남   ③ 충북   ④ 울산", size=22, bold=True, color="paper2")
    s.line(42, 216, 458, 216, color="stitch")
    s.text(42, 234, 416, 150, "제조업과 농림어업 비중이 큰 지역일수록 높습니다. 장치 · 기계조작, 단순노무, "
                              "서비스직 일자리가 많기 때문입니다.", "small", color="paper2")
s.oval(598, 386, 84, 84, "VS", fill="yellow", line="paper2", line_w=5, color="brown900", size=24, shadow=True)
s.svg("sprig", -70, 540, 160, 340, 28)
s.svg("fern", 1196, 390, 80, 360, -8)

# =====================================================================
# 06 차이는 일자리 구성에서 (차트)
# =====================================================================
s = deck.slide("brown")
s.scrap("kraft", -60, 330, 150, 480, 4)
s.text(110, 48, 1000, 70, "차이는 {일}자리 구성에서", "display", size=50, color="paper2")
with s.card("paper", 90, 156, 520, 508, -1):
    s.text(44, 38, 432, 20, "02 · 지역별 노출도의 배경", "kicker")
    s.text(44, 64, 432, 40, "권역별 취업자의 직군 비중", "h2", size=26)
    s.text(44, 112, 432, 130, "수도권에는 생성형 · 에이전틱 AI 노출도가 높은 **전문가 · 사무직** 일자리가, 비수도권에는 "
                              "피지컬AI 노출도가 높은 **장치·기계조작 · 단순노무** 일자리가 더 많습니다.", "small")
    s.text(44, 248, 432, 80, "배경에는 수도권의 지식서비스업 집중과 비수도권의 높은 제조업 · 농림어업 비중이 있습니다.", "small")
    s.rect(44, 352, 432, 112, fill="tint")
    s.rect(44, 352, 6, 112, fill="brown800")
    s.text(66, 366, 396, 86, "**가장 큰 차이** · 전문가 비중이 수도권 28.1%, 비수도권 18.0%로 **10.1%p** 벌어져 있습니다.",
           "small", size=17, lh=1.55)
s.svg("chart_jobs", 650, 104, 580, 520)
s.svg("fern", 1196, 440, 80, 340, -10)

# =====================================================================
# 07 고노출 일자리, 수도권이 주도 (핵심 수치)
# =====================================================================
s = deck.slide("peach")
s.scrap("kraft", -70, -50, 210, 830, 3)
s.scrap("ledger", 930, 560, 420, 220, -5)
s.text(280, 36, 600, 20, "03 · AI 확산과 지역 노동시장", "kicker")
s.text(280, 60, 820, 70, "고노출 일자리, {수}도권이 주도", "display", size=50)
rows = [(176, 280, -0.8, "l", "icon_gen", "80.8%", "생성형AI 고노출 증가분 중 수도권",
         "2023년 이후 3년간 24.7만명 증가 · 수도권 19.9만명"),
        (336, 200, 0.8, "r", "icon_agent", "88.3%", "에이전틱AI 고노출 증가분 중 수도권",
         "2025년 중 10.5만명 증가 · 수도권 9.3만명"),
        (496, 280, -0.6, "l", "icon_trend", "+1.0%p", "수도권: 노출도 0.1 상승 시 고용증가율",
         "비수도권은 통계적으로 유의한 관계가 없었습니다")]
for y, x, r, side, ic, big, t, d in rows:
    with s.card("paper", x, y, 770, 118, r):
        bx = 120 if side == "l" else 40
        s.text(bx, 0, 210, 118, big, "display", size=46, anchor="m")
        s.text(bx + 220, 22, 400 if side == "l" else 390, 30, t, "h3", size=19)
        s.text(bx + 220, 56, 400 if side == "l" else 390, 50, d, "small", color="muted", lh=1.5)
    cx = x - 90 if side == "l" else x + 700
    s.oval(cx, y - 10, 138, 138, fill="white", line="paper2", line_w=6, shadow=True)
    s.svg(ic, cx + 26, y + 16, 86, 86)
s.text(280, 640, 620, 24, "* AI 확산 초기의 징후로, AI가 고용지표 변화의 원인이라고 단정하기는 어렵습니다.", "caption")
s.svg("fern", 30, 30, 90, 390, 5)
s.svg("sprig", 1070, 40, 220, 460, -10)

# =====================================================================
# 08 그 밖의 초기 징후 (우표 카드)
# =====================================================================
s = deck.slide("peach")
s.scrap("kraft", -90, -50, 270, 830, 2)
s.scrap("kraft", 1150, -50, 240, 830, -2)
s.text(180, 40, 920, 70, "그 밖의 {초}기 징후", "display", align="c")
s.text(180, 112, 920, 26, "고노출 일자리 증가와 함께 나타난 신호들", "small", color="muted", align="c")
signals = [(220, 184, -1, "인력부족 · 임금", "수도권",
            "에이전틱AI 고노출 일자리가 늘었는데도 수도권 기업이 느끼는 인력부족이 더 컸고, 임금은 수도권 중심으로 오를 조짐입니다."),
           (660, 184, 1, "미스매치 신호", "해석",
            "전문성 · 실무경험 수요는 늘었지만 맞는 인력 공급이 부족합니다. 전문성에 대한 임금프리미엄이 커질 가능성을 시사합니다."),
           (220, 446, 0.8, "20대 청년층", "예외",
            "고노출 일자리가 수도권 · 비수도권 모두 줄어 격차 확대가 뚜렷하지 않았습니다. 대학교육이 지식축적 중심이라 역량을 갖추기 어렵기 때문으로 보입니다."),
           (660, 446, -1.2, "피지컬AI 직군", "장기 감소",
            "노출도가 높은 직업의 취업자수는 생성형 · 에이전틱과 달리 수도권 · 비수도권 모두에서 오랫동안 꾸준히 줄어 왔습니다.")]
for n, (x, y, r, t, tag, d) in enumerate(signals, 1):
    with s.stamp(x, y, 410, 228, r, badge=n):
        s.text(30, 34, 240, 30, t, "h3", color="paper2")
        tw = 24 + sum(14 if ord(ch) > 0x2E80 else 8.5 for ch in tag)
        chip(s, 380 - tw, 36, tag)
        s.text(30, 78, 350, 140, d, "small", color="paper2", lh=1.55)
s.svg("sprig", 0, 250, 200, 440, 6)
s.svg("sprig", 1090, 280, 200, 440, -8)

# =====================================================================
# 09 위험요인
# =====================================================================
s = deck.slide("peach")
s.scrap("kraft", 860, -50, 470, 830, 3)
s.scrap("ledger", 830, 500, 480, 290, -8)
with s.card("paper", 60, 56, 770, 608, -0.8):
    s.text(56, 44, 600, 20, "04 · 위험요인", "kicker")
    s.text(56, 68, 660, 70, "격차를 {키}우는 힘", "display", size=52)
    risks = [("수도권 집적경제 강화",
              "지식서비스(종사자 수도권 비중 **71.9%**)와 반도체 제조업(**74.4%**)이 이미 수도권에 몰려 있습니다. "
              "AI투자는 숙련인재와 보완성이 커 수도권에 더 집중될 수 있습니다."),
             ("피지컬AI발 지방 고용 감소",
              "피지컬AI 발전이 빨라지면 노출도가 높은 비수도권에서 제조 · 숙박음식 · 운수업을 중심으로 고용이 줄 우려가 있습니다."),
             ("AI 준비도 격차",
              "인적자본 · 혁신활동으로 평가한 지역별 “AI 준비도”가 서울 · 경기 등에서 비수도권보다 크게 높습니다.")]
    for i, (t, d) in enumerate(risks):
        y = 164 + i * 140
        s.oval(56, y, 46, 46, str(i + 1))
        s.text(120, y + 7, 590, 30, t, "h3")
        s.text(120, y + 42, 590, 90, d, "small")
with s.card("paper2", 884, 96, 370, 452, 2):
    s.svg("cycle", 5, 6, 360, 440)
s.svg("sprig", 1120, 520, 160, 340, -8)

# =====================================================================
# 10 기회요인
# =====================================================================
s = deck.slide("kraft")
s.scrap("ledger", -40, 652, 1360, 130, 1)
s.text(110, 44, 600, 20, "04 · 기회요인", "kicker", color="brown800")
s.text(110, 68, 800, 70, "격차를 {줄}이는 힘", "display")
centers = (215, 640, 1065)
s.line(centers[0], 236, centers[-1], 236, color="brown800", width=3)
for i, cx in enumerate(centers):
    s.oval(cx - 36, 200, 72, 72, str(i + 1), size=24, line="paper2", line_w=4)
opps = [(-1, "인재 · R&D 분산", "수도권 집적의 완화",
         "암묵지(문서화되지 않은 경험 · 정보)의 AI화가 진전되면 사람 간 대면과 집적의 필요성이 줄어들 수 있습니다.",
         "✔ 피지컬AI R&D가 산업현장에서 이뤄지며 지방 제조업의 지식서비스화 촉진"),
        (0.8, "서비스업 상향평준화", "지방 서비스업 생산성 개선",
         "AI가 인적자본이 부족한 비수도권 서비스업의 생산성을 더 크게 끌어올리고 공급제약을 완화할 수 있습니다.",
         "✔ 지역 안의 서비스 소비 성장 기대"),
        (-0.6, "청년 유출 완화", "지방의 양질 일자리 증가",
         "청년층의 수도권 취업경쟁이 치열한 가운데 비수도권에 상대적으로 좋은 일자리가 늘면 청년 유출이 줄 수 있습니다.",
         "✔ 전제: 비수도권의 양질 일자리 확대")]
for (r, tag, t, d, note), cx in zip(opps, centers):
    with s.card("paper", cx - 180, 300, 360, 336, r):
        chip(s, 28, 28, tag)
        s.text(28, 70, 304, 32, t, "h3")
        s.text(28, 110, 304, 130, d, "small")
        s.line(28, 252, 332, 252)
        s.text(28, 264, 304, 50, note, "caption")
s.svg("sprig", 1150, -130, 150, 320, 200)

# =====================================================================
# 11 정책적 시사점 (표)
# =====================================================================
s = deck.slide("brown")
s.scrap("kraft", -40, 610, 1360, 200, -2)
with s.card("paper", 90, 50, 1100, 620, -0.4):
    s.text(56, 40, 600, 20, "05 · 정책적 시사점", "kicker")
    s.text(56, 64, 760, 64, "지역이 준비할 {세} 가지 과제", "display", size=46)
    s.text(700, 104, 344, 20, "‘연결되는 위험 · 기회’는 발표자 정리", "caption", align="r")
    cols = [(56, 230), (286, 400), (686, 358)]
    y0 = 150
    s.rect(56, y0, 988, 48, fill="brown800")
    for (x, w), h in zip(cols, ["정책 과제", "추진 방향", "연결되는 위험 · 기회"]):
        s.text(x + 18, y0, w - 36, 48, h, size=17, bold=True, color="paper2", anchor="m")
    policy = [("1", ["지역 서비스업", "전문화"], "**AI 교육시스템 강화**와 혁신성장 지원으로 지역 서비스업의 전문성을 높입니다.",
               ["기회 ② 서비스업 생산성 개선", "위험 ③ AI 준비도 격차"]),
              ("2", ["제조업의", "지식서비스화"], "**주력 제조업과 연계한 서비스 특화**와 스타트업 육성을 추진합니다.",
               ["위험 ② 피지컬AI발 고용 감소", "기회 ① 산업현장 중심 R&D"]),
              ("3", ["거점대학의", "AI 허브화"], "**선택과 집중**에 기초해 지역 거점대학에 대한 투자를 확대합니다.",
               ["위험 ① 인재의 수도권 집적", "기회 ③ 청년 유출 완화"])]
    for i, (n, t, d, links) in enumerate(policy):
        y = y0 + 48 + i * 130
        if i % 2:
            s.rect(56, y, 988, 130, fill="tint")
        s.oval(74, y + 45, 40, 40, n, size=16)
        s.text(128, y, 150, 130, t, "h3", size=19, anchor="m")
        s.text(304, y, 364, 130, d, "small", size=17, anchor="m", lh=1.55)
        s.text(704, y, 322, 130, links, "small", size=16, anchor="m", color="brown800", space=6)
        s.line(56, y + 130, 1044, y + 130)
s.svg("sprig", 1150, 380, 180, 380, -14)
s.svg("fern", 10, 440, 90, 380, -12)

# =====================================================================
# 12 마무리
# =====================================================================
s = deck.slide("brown")
s.scrap("kraft", 790, -50, 560, 820, 4)
with s.card("paper", 110, 84, 960, 552, -1):
    s.text(90, 60, 700, 260, ["{감}사", "합니{다}"], "display", size=124, lh=1.0)
    s.line(90, 346, 550, 346)
    s.text(90, 368, 400, 20, "Q & A", "kicker")
    s.text(90, 394, 600, 26, "궁금한 점을 편하게 질문해 주세요", "small")
    s.text(90, 436, 580, 60, "출처: 한국은행, BOK 이슈노트 제2026-25호 「AI와 지역 노동시장 – 지역간 격차 확대 위험과 "
                             "새로운 기회」, 지역경제조사팀, 2026.9 (요약본 기준)", "caption")
s.svg("sprig", 820, 110, 320, 660, -6)
s.svg("fern", 1140, 320, 100, 440, 10)

path = deck.save("AI와_지역노동시장.pptx")
print(f"저장 완료: {path} ({len(deck.slides)}장)")
