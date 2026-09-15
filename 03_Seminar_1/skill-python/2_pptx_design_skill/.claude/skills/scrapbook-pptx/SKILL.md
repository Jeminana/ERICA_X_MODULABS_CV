---
name: scrapbook-pptx
description: 압화 · 찢어진 종이 · 크라프트지 콜라주(Pressed Flower Scrapbook) 디자인으로 PPTX 발표 자료를 만든다. 보고서 · 논문 · PDF · 문서 내용이나 주제를 받아 10~15장 분량의 편집 가능한 .pptx(네이티브 텍스트/도형 + SVG 차트/다이어그램)와 HTML 미리보기를 생성하고 직접 검수한다. 사용자가 "pptx 만들어줘", "발표자료/슬라이드/PPT 만들어줘", "이 보고서(파일)로 슬라이드 만들어줘", "스크랩북 스타일 발표자료" 등을 요청할 때 사용한다.
---

# Scrapbook PPTX

레퍼런스 HTML 슬라이드 모음집(`templates/reference-slides.html`)의 디자인을 python-pptx 엔진으로 옮겨 PPTX를 만든다.
HTML(미리보기)을 중간 표현으로 써서 색 · 정렬 · 여백 · 겹침을 빠르게 확인하고 고친다.

## 구성

| 경로 | 역할 |
|---|---|
| `scripts/pptx_engine.py` | 디자인 엔진: 토큰, 찢어진 종이/우표 카드, 텍스트 스타일, SVG 삽입, preview.html 생성 |
| `scripts/render_preview.py` | preview.html → 슬라이드별 PNG (검수용) |
| `scripts/requirements.txt` | python-pptx, pillow, numpy, lxml, pypdfium2 |
| `templates/reference-slides.html` | 16개 레이아웃 레퍼런스 (00 스타일 가이드 + 01~15). 좌표는 px 절대 위치 |
| `examples/build_ai_labor_deck.py` | 완성 예시 12장 (한국은행 이슈노트 요약). **새 덱은 이 파일을 복사해서 시작** |
| `references/engine-api.md` | 엔진 API · 스타일 · 색 토큰 요약 |

아래에서 `<skill>`은 이 SKILL.md가 있는 디렉토리(스킬 base directory)를 뜻한다.

## 작업 순서

1. **환경 준비 (최초 1회)**
   `pip install -r "<skill>/scripts/requirements.txt"`
   Windows에서는 명령 앞에 `PYTHONIOENCODING=utf-8`(bash) 또는 `$env:PYTHONIOENCODING='utf-8'`(PowerShell).

2. **원문 파악**
   파일을 끝까지 읽고 핵심 질문 · 주장 · 수치 · 구조를 목록으로 뽑는다. 수치는 원문에 있는 것만 쓴다.
   요약본만 있거나 표/그래프 원자료가 없으면 그 한계를 사용자에게 알린다.

3. **목차 설계 (10~15장, 사용자가 분량을 정하면 그에 따름)**
   표지 → 목차 → 본문 → 마무리. 장마다 아래 카탈로그에서 레이아웃 1개를 배정한다.
   - 같은 레이아웃을 연달아 쓰지 않는다. 배경은 `kraft` / `peach` / `brown`을 번갈아 리듬을 준다.
   - 한 장 = 한 메시지. 제목은 결론이 드러나는 짧은 문장 (예: "고노출 일자리, 수도권이 주도").
   - 수치가 3개 이상 비교되면 SVG 차트, 흐름/순환/구조는 SVG 다이어그램.

4. **빌드 스크립트 작성**
   작업 디렉토리에 `<주제>_deck/build_deck.py`를 만든다. `examples/build_ai_labor_deck.py`를 복사해
   맨 위 `SKILL_SCRIPTS`를 `<skill>/scripts`의 **절대경로**로 바꾸고, SVG 정의와 슬라이드 내용을 새 주제로 교체한다.
   좌표는 `templates/reference-slides.html`의 해당 레이아웃과 예시 파일에서 가져와 텍스트 양에 맞게 조정한다.

5. **실행**
   `cd <주제>_deck && python build_deck.py` → `output/<파일명>.pptx`, `output/preview.html`, `output/assets/`

6. **검수 (반드시 모든 장을 이미지로 본다)**
   `python "<skill>/scripts/render_preview.py" output/preview.html` → `output/preview_png/slideNN.png`
   이미지를 하나씩 열어 확인하고, 문제가 있으면 스크립트를 고쳐 5~6을 반복한다.
   - 글자 넘침, 카드 밖으로 나간 텍스트, 한 글자만 남은 줄바꿈
   - 압화/고사리 장식이 글자를 가림
   - 차트 수치 · 순위 · 단위가 원문과 일치하는지
   - 다크 배경 위 글자 대비

7. **보고**
   PPTX 경로, 장별 제목과 사용한 레이아웃 표, 원문에 없는 해석을 넣은 위치(슬라이드에도 "발표자 정리" 표기),
   검수 한계(PowerPoint 실제 렌더링을 못 봤다면 그 사실)를 짧게 알린다. 수정 요청을 받으면 4~6을 반복한다.

## 레이아웃 카탈로그

번호는 `templates/reference-slides.html`의 섹션 번호, 예시 열은 `examples/build_ai_labor_deck.py`에서 같은 구조를 쓴 슬라이드.

| # | 레이아웃 | 쓰임 | 예시 |
|---|---|---|---|
| 01 | Cover | 표지: 크라프트 배경 + 대형 종이 카드 + 장부 조각 | 01 |
| 02 | Agenda | 좌측 다크 띠 + 번호 목록 5개 | 02 |
| 03 | Team / 3 circles | 원형 이미지/아이콘 3개 + 이름 · 설명 (3가지 유형 비교에도 사용) | 04 |
| 04 | Section Divider | 대형 섹션 번호 + 제목 종이띠 | — |
| 05 | Text + Key Number | 본문 카드(불릿 3개) + 핵심 수치/다이어그램 카드 | 09 |
| 06 | 4-Step Stamp Grid | 우표 카드 2×2 (단계, 신호, 항목 4개) | 08 |
| 07 | Key Message + 3 Points | 인용형 핵심 문장 + 3열 설명 | 03 |
| 08 | Chart + Explanation | 설명 카드 + SVG 차트 (다크 배경) | 06 |
| 09 | Process Timeline | 번호 원 3~4개 점선 연결 + 카드 | 10 |
| 10 | Before / After | 좌(밝은 종이) vs 우(다크 종이) 비교 + 가운데 원 | 05 |
| 11 | Photo Gallery | 폴라로이드 3장 + 캡션 | — |
| 12 | Results Strips | 원형 아이콘 + 종이띠(큰 숫자 · 지표 · 설명) 3줄 | 07 |
| 13 | Data Table | 다크 헤더 표 (행 = rect + text) | 11 |
| 14 | References | 번호 출처 목록 | — |
| 15 | Closing | 대형 인사말 + Q&A + 출처 | 12 |

## 디자인 규칙

- 캔버스 1280×720 px, 좌상단 원점. 카드 안쪽은 `with s.card(...)` 로컬 좌표(회전 자동 반영)
- 폰트: 제목 `display`(Arial Black / 맑은 고딕), 본문 Arial / 맑은 고딕. 최소 14px, 본문 16~19px
- 제목의 `{글자}` 섞기(콜라주 느낌)는 제목당 1곳
- 텍스트 분량 기준: 16px 한글은 폭 300px에 한 줄 약 18자. 카드 설명은 3~4줄 이내로 자르고, 텍스트 박스 높이는 여유 있게
- 장식(`sprig`, `fern`)은 슬라이드 가장자리나 카드 모서리에만. 글자와 겹치면 위치를 옮긴다
- 다크 배경(`brown` 슬라이드, `dark` 카드, `stamp`) 위 글자는 `color="paper2"`, 키커는 `color="ledger"`
- SVG는 PowerPoint 호환을 위해 **평면 요소만**(rect, circle, ellipse, path, line, polyline, text, g+transform).
  `<use>`, `<symbol>`, `filter`, `marker`, CSS, 외부 이미지는 쓰지 않는다. 화살촉은 path 삼각형으로(예시의 `arrowhead`)
- 차트 색: 강조 계열 `#E6BE4A`(yellow), 비교 계열 `#CDB295`(kraft light), 다크 배경 위 글자 `#F3EBDD`
- 데이터 무결성: 원문 수치만 사용, 차트 하단에 출처, 원문의 인과관계 유보 문구가 있으면 슬라이드에도 반영

## 주의

- SVG의 PNG 대체 이미지는 Edge/Chrome 헤드리스로 만든다. 브라우저가 없으면 투명 이미지로 대체되고 경고가 출력된다
  (PowerPoint 2016+는 SVG를 직접 그리므로 문제없지만 Google Slides 등에서는 그래픽이 비어 보임). 경로는 `PPTX_BROWSER` 환경변수로 지정 가능
- `output/assets`의 텍스처는 캐시된다. 엔진의 텍스처 코드를 바꿨다면 해당 `tex_*.jpg`를 지우고 다시 빌드
- 미리보기는 브라우저 렌더링이라 PowerPoint 줄바꿈과 조금 다를 수 있다. 빡빡한 텍스트 박스는 피한다
