"""컴퓨터 비전 객체 탐지 개요 → Pressed Flower Scrapbook PPTX (10장).

실행: python build_deck.py
결과: output/객체탐지_개요.pptx, output/preview.html
"""
import sys
from pathlib import Path

SKILL_SCRIPTS = Path(r"C:\hy-edu\ERICA_X_MODULABS_CV\03_Seminar_1\skill-python\2_pptx_design_skill\.claude\skills\scrapbook-pptx\scripts")
sys.path.insert(0, str(SKILL_SCRIPTS))

from pptx_engine import Deck, svg_doc  # noqa: E402

deck = Deck("output")

BROWN, BROWN6, INK, PAPER2, LEDGER = "#5C2E14", "#7A4A2A", "#3B2414", "#F3EBDD", "#EFD6A0"
YELLOW, LILAC, SAGE, KRAFT_L, WHITE = "#E6BE4A", "#A98ABD", "#6D7C53", "#CDB295", "#FFFDF8"


# =====================================================================
# SVG 그래픽
# =====================================================================
def frame():
    return (f'<rect x="14" y="20" width="92" height="80" rx="6" fill="{WHITE}" stroke="{BROWN}" stroke-width="3"/>'
            f'<path d="M20 94 L48 62 L66 80 L80 68 L100 94 Z" fill="{KRAFT_L}"/>'
            f'<circle cx="84" cy="40" r="8" fill="{YELLOW}"/>')


deck.add_svg("icon_cls", svg_doc(120, 120, frame() + (
    f'<rect x="30" y="4" width="60" height="24" rx="12" fill="{SAGE}" stroke="{BROWN}" stroke-width="2"/>'
    f'<text x="60" y="21" font-size="13" font-weight="700" fill="{WHITE}" text-anchor="middle" font-family="Arial">CAT</text>')))

deck.add_svg("icon_det", svg_doc(120, 120, frame() + (
    f'<rect x="24" y="48" width="40" height="46" fill="none" stroke="{BROWN}" stroke-width="3.5"/>'
    f'<rect x="24" y="38" width="30" height="12" fill="{BROWN}"/>'
    f'<rect x="68" y="30" width="30" height="30" fill="none" stroke="{LILAC}" stroke-width="3.5"/>'
    f'<rect x="68" y="20" width="22" height="11" fill="{LILAC}"/>')))

deck.add_svg("icon_seg", svg_doc(120, 120, (
    f'<rect x="14" y="20" width="92" height="80" rx="6" fill="{WHITE}" stroke="{BROWN}" stroke-width="3"/>'
    f'<path d="M24 92 C22 70 34 52 50 56 C62 58 66 76 62 92 Z" fill="{YELLOW}" fill-opacity="0.85" stroke="{BROWN}" stroke-width="2"/>'
    f'<path d="M66 60 C70 36 94 32 98 50 C102 66 90 74 78 72 C72 71 66 68 66 60 Z" fill="{LILAC}" fill-opacity="0.85" stroke="{BROWN}" stroke-width="2"/>'
    f'<path d="M20 92 H100" stroke="{SAGE}" stroke-width="4"/>')))


def chart_speed_acc():
    """YOLOv1 논문 Table 1 (PASCAL VOC 2007, 실시간/비실시간 검출기) 수치만 사용."""
    models = [("Fast R-CNN", 70.0, 0.5, False), ("Faster R-CNN VGG-16", 73.2, 7, False),
              ("Faster R-CNN ZF", 62.1, 18, False), ("YOLO", 63.4, 45, True), ("Fast YOLO", 52.7, 155, True)]
    x0 = 190
    o = [f'<rect x="190" y="4" width="16" height="16" fill="{YELLOW}"/>'
         f'<text x="214" y="17" font-size="15" fill="{PAPER2}">1-Stage (YOLO)</text>'
         f'<rect x="360" y="4" width="16" height="16" fill="{KRAFT_L}"/>'
         f'<text x="384" y="17" font-size="15" fill="{PAPER2}">2-Stage (R-CNN 계열)</text>']

    def section(y, title, idx, vmax, unit, fmt):
        k = 330 / vmax
        o.append(f'<text x="0" y="{y}" font-size="15" font-weight="700" fill="{LEDGER}">{title}</text>')
        for j, m in enumerate(models):
            name, val, fast = m[0], m[idx], m[3]
            ry = y + 14 + j * 40
            col = YELLOW if fast else KRAFT_L
            o.append(f'<text x="{x0 - 12}" y="{ry + 18}" font-size="14" fill="{PAPER2}" text-anchor="end">{name}</text>'
                     f'<rect x="{x0}" y="{ry + 4}" width="{max(val * k, 2):.1f}" height="20" fill="{col}"/>'
                     f'<text x="{x0 + max(val * k, 2) + 8:.1f}" y="{ry + 19}" font-size="14" font-weight="700" '
                     f'fill="{PAPER2}">{fmt(val)}{unit}</text>')

    section(56, "속도 · FPS (클수록 빠름)", 2, 155, " FPS", lambda v: f"{v:g}")
    section(304, "정확도 · mAP (클수록 정확)", 1, 80, "%", lambda v: f"{v:.1f}")
    o.append(f'<text x="0" y="532" font-size="12" fill="{KRAFT_L}">자료: Redmon et al. (2016) YOLOv1 논문 Table 1 · PASCAL VOC 2007 · 논문 보고치</text>')
    return svg_doc(580, 540, "".join(o))


deck.add_svg("chart_speed", chart_speed_acc())


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
    s.text(90, 70, 660, 22, "COMPUTER VISION · OBJECT DETECTION", "kicker")
    s.text(90, 104, 700, 210, ["객체 {탐}지", "한눈에 보기"], "display", size=88, lh=1.1)
    s.text(90, 326, 680, 40, "무엇이, 어디에 있는지 찾는 기술의 구조와 흐름", size=26, lh=1.3)
    s.line(90, 396, 510, 396)
    s.text(90, 414, 640, 26, "**개요 발표** · 2026. 09. 15", "small", color="muted")
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
s.text(70, 372, 300, 90, ["객체 탐지의 개념부터", "대표 모델까지", "다섯 부분으로 정리했습니다."],
       "small", color="paper2")
s.scrap("ledger", 350, 570, 300, 200, -6)
agenda = [("객체 탐지란", "분류 · 탐지 · 분할은 무엇이 다른가"),
          ("탐지 모델의 구조", "백본 → 넥 → 헤드 → 후처리"),
          ("2-Stage와 1-Stage", "정확도와 속도 사이의 선택"),
          ("핵심 개념", "IoU · NMS · 앵커 · mAP"),
          ("대표 모델", "Faster R-CNN · YOLOv8 · EfficientDet · DETR")]
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
# 03 객체 탐지란 (Key Message + 3 Points)
# =====================================================================
s = deck.slide("brown")
s.scrap("ledger", -50, -40, 440, 130, -4)
s.text(120, 110, 600, 22, "01 · 객체 탐지란", "kicker", color="ledger")
s.text(120, 136, 900, 70, "무엇이, {어}디에", "display", color="paper2")
with s.card("paper", 90, 236, 1100, 434, 0.5):
    s.text(56, 38, 988, 50, "“이미지 속 물체가 무엇이고, 어디에 있는가?”", size=30, bold=True, color="brown800",
           align="c", lh=1.4)
    s.line(56, 116, 1044, 116)
    outs = [("OUTPUT 1", "클래스 · 무엇", "사람, 자동차, 불량품처럼 미리 정한 범주 중 어느 것인지 예측합니다."),
            ("OUTPUT 2", "바운딩 박스 · 어디", "물체를 감싸는 사각형의 위치와 크기(x, y, w, h)를 좌표로 예측합니다."),
            ("OUTPUT 3", "신뢰도 · 얼마나", "그 박스에 해당 물체가 있을 확률 점수로, 기준값 아래는 걸러냅니다.")]
    for i, (k, t, d) in enumerate(outs):
        x = 56 + i * 340
        s.text(x, 146, 300, 20, k, "kicker")
        s.text(x, 172, 300, 32, t, "h3")
        s.text(x, 212, 300, 140, d, "small")
        if i:
            s.line(x - 20, 146, x - 20, 350)
    s.text(56, 384, 988, 22, "* 한 이미지에 물체가 여러 개일 수 있어, 모델은 이 세 가지를 물체마다 한 묶음씩 출력합니다.", "caption")
s.svg("fern", 0, 430, 90, 400, -15)
s.svg("sprig", 1070, -60, 230, 480, 190)

# =====================================================================
# 04 분류 · 탐지 · 분할 (3 circles)
# =====================================================================
s = deck.slide("peach")
s.scrap("ledger", 900, -50, 460, 230, 5)
s.scrap("kraft", -40, 610, 1360, 200, -1.5)
with s.card("paper", 110, 66, 1060, 566, -0.6):
    s.text(0, 34, 1060, 64, "{세} 가지 비전 과제", "display", align="c")
    s.text(0, 104, 1060, 26, "같은 사진이라도 무엇을 얼마나 자세히 알고 싶은지에 따라 과제가 달라집니다", "small",
           color="muted", align="c")
    tasks = [("icon_cls", "이미지 분류", "CLASSIFICATION", "사진 전체에 라벨 하나", "ResNet · EfficientNet"),
             ("icon_det", "객체 탐지", "DETECTION", "물체마다 박스 + 라벨", "YOLO · Faster R-CNN"),
             ("icon_seg", "분할", "SEGMENTATION", "픽셀 단위로 물체 윤곽", "Mask R-CNN · SAM")]
    for i, (ic, name, en, desc, models) in enumerate(tasks):
        cx = 190 + i * 340
        s.oval(cx - 80, 150, 160, 160, fill="white", line="paper2", line_w=6, shadow=True)
        s.svg(ic, cx - 52, 178, 104, 104)
        s.text(cx - 150, 330, 300, 34, name, "h3", size=24, align="c")
        s.text(cx - 150, 368, 300, 20, en, "kicker", align="c")
        s.text(cx - 150, 398, 300, 26, desc, "small", color="muted", align="c")
        s.rect(cx - 140, 440, 280, 88, fill="tint", radius=10)
        s.text(cx - 130, 452, 260, 20, "대표 모델", "caption", align="c")
        s.text(cx - 130, 476, 260, 40, models, "h3", size=19, align="c")
s.svg("sprig", -40, 370, 200, 420, 16)
s.svg("sprig", 1150, 380, 200, 420, -18)

# =====================================================================
# 05 탐지 모델 구조 (Process Timeline)
# =====================================================================
s = deck.slide("kraft")
s.scrap("ledger", -40, 652, 1360, 130, 1)
s.text(110, 44, 600, 20, "02 · 탐지 모델의 구조", "kicker", color="brown800")
s.text(110, 68, 900, 70, "이미지가 박스가 되는 {4}단계", "display", size=50)
centers = (205, 495, 785, 1075)
s.line(centers[0], 206, centers[-1], 206, color="brown800", width=3)
for i, cx in enumerate(centers):
    s.oval(cx - 36, 170, 72, 72, str(i + 1), size=24, line="paper2", line_w=4)
stages = [(-1, "BACKBONE", "백본", "CNN 등으로 이미지에서 모양 · 질감 같은 특징 맵을 뽑습니다.", "예: ResNet, CSPDarknet"),
          (0.8, "NECK", "넥", "해상도가 다른 특징 맵을 섞어 크고 작은 물체를 함께 봅니다.", "예: FPN, BiFPN"),
          (-0.6, "HEAD", "헤드", "특징 맵의 위치마다 클래스 점수와 박스 좌표를 예측합니다.", "예: YOLO Head"),
          (1, "POST", "후처리", "겹치는 박스를 NMS로 정리하고 신뢰도 낮은 박스를 버립니다.", "예: NMS, 임계값")]
for (r, en, t, d, note), cx in zip(stages, centers):
    with s.card("paper", cx - 132, 284, 264, 316, r):
        chip(s, 24, 26, en)
        s.text(24, 68, 216, 34, t, "h3", size=24)
        s.text(24, 112, 216, 130, d, "small")
        s.line(24, 244, 240, 244)
        s.text(24, 256, 216, 44, note, "caption")
s.svg("sprig", 1150, -130, 150, 320, 200)

# =====================================================================
# 06 2-Stage vs 1-Stage (Before / After)
# =====================================================================
s = deck.slide("peach")
with s.card("paper2", 340, 36, 600, 118, -1.5):
    s.text(0, 0, 600, 118, "2-Stage vs {1}-Stage", "display", size=46, align="c", anchor="m")
with s.card("paper", 90, 190, 500, 476, -1):
    s.text(42, 38, 416, 20, "03 · 두 번 보고 정확하게", "kicker")
    s.text(42, 62, 416, 40, "2-Stage 탐지기", "h2")
    s.text(42, 124, 416, 26, "① 후보 영역 제안", "h3", size=19)
    s.text(42, 154, 416, 56, "물체가 있을 법한 후보 영역(RPN)을 먼저 골라냅니다.", "small")
    s.text(42, 216, 416, 26, "② 영역별 분류 · 박스 보정", "h3", size=19)
    s.text(42, 246, 416, 56, "고른 영역마다 클래스를 판단하고 박스 위치를 다듬습니다.", "small")
    s.line(42, 318, 458, 318)
    s.text(42, 336, 416, 60, "**강점** 정확도가 높은 편  ·  **약점** 느린 편", "small")
    s.text(42, 384, 416, 30, "대표: R-CNN · Fast R-CNN · Faster R-CNN", "small", color="muted")
with s.card("dark", 690, 190, 500, 476, 1, shadow=True):
    s.text(42, 38, 416, 20, "03 · 한 번에 빠르게", "kicker", color="ledger")
    s.text(42, 62, 416, 40, "1-Stage 탐지기", "h2", color="paper2")
    s.text(42, 124, 416, 26, "한 번의 신경망 계산으로 끝", "h3", size=19, color="paper2")
    s.text(42, 154, 416, 150, "후보 영역 단계 없이, 이미지를 격자로 나눈 각 위치에서 클래스와 박스를 "
                              "동시에 예측합니다. 영상처럼 실시간 처리가 필요한 곳에 알맞습니다.", "small", color="paper2")
    s.line(42, 318, 458, 318, color="stitch")
    s.text(42, 336, 416, 60, "**강점** 빠르고 구조가 단순  ·  **약점** 작은 물체에 불리했음",
           "small", color="paper2")
    s.text(42, 384, 416, 30, "대표: YOLO · SSD · RetinaNet · EfficientDet", "small", color="ledger")
s.oval(598, 386, 84, 84, "VS", fill="yellow", line="paper2", line_w=5, color="brown900", size=24, shadow=True)
s.svg("sprig", -70, 540, 160, 340, 28)
s.svg("fern", 1196, 390, 80, 360, -8)

# =====================================================================
# 07 속도와 정확도 (Chart + Explanation)
# =====================================================================
s = deck.slide("brown")
s.scrap("kraft", -60, 330, 150, 480, 4)
s.text(110, 44, 1000, 70, "속도와 {정}확도의 줄다리기", "display", size=50, color="paper2")
with s.card("paper", 90, 150, 520, 516, -1):
    s.text(44, 38, 432, 20, "03 · 속도와 정확도", "kicker")
    s.text(44, 64, 432, 40, "같은 데이터, 같은 논문의 비교", "h2", size=26)
    s.text(44, 112, 432, 110, "YOLO는 2-Stage 방식인 Faster R-CNN보다 mAP가 낮지만, **초당 45장**을 처리해 "
                              "실시간 영상 탐지를 가능하게 했습니다.", "small")
    s.text(44, 236, 432, 90, "반대로 정확도가 가장 높은 Faster R-CNN VGG-16은 초당 7장에 그쳤습니다.", "small")
    s.rect(44, 344, 432, 124, fill="tint")
    s.rect(44, 344, 6, 124, fill="brown800")
    s.text(66, 358, 396, 100, "**발표자 정리** · 이후 모델들은 이 줄다리기에서 두 마리 토끼를 잡는 방향으로 발전해 왔습니다.",
           "small", size=17, lh=1.55)
s.svg("chart_speed", 650, 116, 580, 540)
s.svg("fern", 1196, 440, 80, 340, -10)

# =====================================================================
# 08 핵심 개념 (4 Stamp Grid)
# =====================================================================
s = deck.slide("peach")
s.scrap("kraft", -90, -50, 270, 830, 2)
s.scrap("kraft", 1150, -50, 240, 830, -2)
s.text(180, 40, 920, 70, "성능을 {읽}는 네 가지 개념", "display", align="c", size=50)
s.text(180, 112, 920, 26, "탐지 결과를 이해하고 평가할 때 꼭 나오는 용어들", "small", color="muted", align="c")
concepts = [(220, 184, -1, "IoU", "겹침 정도",
             "예측 박스와 정답 박스의 교집합 넓이를 합집합 넓이로 나눈 값입니다. 1에 가까울수록 잘 맞습니다."),
            (660, 184, 1, "NMS", "중복 제거",
             "같은 물체에 겹친 박스 중 점수가 가장 높은 것만 남기고, IoU가 기준보다 큰 나머지를 지웁니다."),
            (220, 446, 0.8, "Anchor", "기준 박스",
             "미리 정한 크기 · 비율의 박스에서 차이만 예측합니다. YOLOv8처럼 앵커 없이 예측하는 방식도 있습니다."),
            (660, 446, -1.2, "mAP", "평가 지표",
             "클래스별 정밀도-재현율 곡선 아래 넓이(AP)의 평균입니다. COCO는 IoU 0.5~0.95 기준을 평균합니다.")]
for n, (x, y, r, t, tag, d) in enumerate(concepts, 1):
    with s.stamp(x, y, 410, 228, r, badge=n):
        s.text(30, 34, 240, 30, t, "h3", color="paper2")
        tw = 24 + sum(14 if ord(ch) > 0x2E80 else 8.5 for ch in tag)
        chip(s, 380 - tw, 36, tag)
        s.text(30, 78, 350, 140, d, "small", color="paper2", lh=1.55)
s.svg("sprig", 0, 250, 200, 440, 6)
s.svg("sprig", 1090, 280, 200, 440, -8)

# =====================================================================
# 09 대표 모델 (Data Table)
# =====================================================================
s = deck.slide("kraft")
s.scrap("ledger", -40, 610, 1360, 200, -2)
with s.card("paper", 90, 40, 1100, 640, -0.4):
    s.text(56, 40, 600, 20, "05 · 대표 모델", "kicker")
    s.text(56, 64, 760, 64, "대표 모델 {한}눈에", "display", size=46)
    cols = [(56, 250), (306, 190), (496, 548)]
    y0 = 150
    s.rect(56, y0, 988, 48, fill="brown800")
    for (x, w), h in zip(cols, ["모델 · 발표", "방식", "핵심 아이디어"]):
        s.text(x + 18, y0, w - 36, 48, h, size=17, bold=True, color="paper2", anchor="m")
    models = [("1", ["Faster R-CNN", "2015"], "2-Stage", "후보 영역 제안(RPN)을 신경망 안에 넣어 R-CNN 계열을 빠르게 만들었습니다."),
              ("2", ["EfficientDet", "2020 · Google"], "1-Stage", "**BiFPN**으로 특징을 섞고, 해상도 · 깊이 · 너비를 함께 키우는 복합 스케일링을 씁니다."),
              ("3", ["DETR", "2020 · Meta"], "Transformer", "물체 집합을 한 번에 예측해 **앵커와 NMS 없이** 탐지합니다."),
              ("4", ["YOLOv8", "2023 · Ultralytics"], "1-Stage", "**앵커 없는(anchor-free)** 헤드로 탐지 · 분할 · 포즈를 한 프레임워크에서 지원합니다.")]
    rh = 100
    for i, (n, t, kind, d) in enumerate(models):
        y = y0 + 48 + i * rh
        if i % 2:
            s.rect(56, y, 988, rh, fill="tint")
        s.oval(74, y + (rh - 40) / 2, 40, 40, n, size=16)
        s.text(128, y, 170, rh, t, "h3", size=19, anchor="m")
        s.text(324, y, 160, rh, kind, "small", size=17, bold=True, color="brown800", anchor="m")
        s.text(514, y, 512, rh, d, "small", size=17, anchor="m", lh=1.55)
        s.line(56, y + rh, 1044, y + rh)
s.svg("sprig", 1150, 380, 180, 380, -14)

# =====================================================================
# 10 마무리
# =====================================================================
s = deck.slide("brown")
s.scrap("kraft", 790, -50, 560, 820, 4)
with s.card("paper", 110, 84, 960, 552, -1):
    s.text(90, 60, 700, 260, ["{감}사", "합니{다}"], "display", size=124, lh=1.0)
    s.line(90, 346, 550, 346)
    s.text(90, 368, 400, 20, "Q & A", "kicker")
    s.text(90, 394, 600, 26, "궁금한 점을 편하게 질문해 주세요", "small")
    s.text(90, 436, 600, 80, "참고: Ren et al. 2015 (Faster R-CNN) · Redmon et al. 2016 (YOLO) · Tan et al. 2020 "
                             "(EfficientDet) · Carion et al. 2020 (DETR) · Ultralytics YOLOv8 문서 (2023)", "caption")
s.svg("sprig", 820, 110, 320, 660, -6)
s.svg("fern", 1140, 320, 100, 440, 10)

path = deck.save("객체탐지_개요.pptx")
print(f"저장 완료: {path} ({len(deck.slides)}장)")
