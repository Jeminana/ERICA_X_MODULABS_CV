# PRD — 이한양 개인 포트폴리오 웹사이트

- **문서 버전**: v1.0 (2026-09-08)
- **작성 근거**: [resume_sample.docx](resume_sample.docx)
- **작성자**: 이한양 (한양대학교 인공지능학과 4학년)

---

## 1. 배경 및 목적

졸업(2026년)을 앞두고 AI Engineer 직군으로 취업 지원을 준비 중이다. 이력서 PDF와 GitHub 링크만으로는
프로젝트의 맥락과 기여도를 전달하기 어렵기 때문에, **채용 담당자가 1~2분 안에 "이 사람이 무엇을 할 수 있는가"를
파악할 수 있는 단일 페이지 포트폴리오 사이트**를 만든다.

### 성공 정의
| 목표 | 지표 |
|---|---|
| 지원 서류에 링크 1줄로 대체 가능 | 이력서/자소서/GitHub 프로필에 URL 게시 |
| 빠른 파악 | 첫 화면(스크롤 없이)에서 이름·직군·핵심 기술 스택 노출 |
| 프로젝트 이해 | 각 프로젝트의 문제 → 해결 → 기술 → 결과가 카드 하나로 완결 |
| 접근성 | 모바일에서도 레이아웃 깨짐 없음, Lighthouse 성능/접근성 90+ |

---

## 2. 타깃 사용자

| 사용자 | 상황 | 니즈 |
|---|---|---|
| **P1. 채용 담당자 / 현업 엔지니어** | 지원서에 첨부된 링크를 데스크톱에서 짧게 확인 | 기술 스택, 프로젝트 규모, 코드(GitHub) 확인 |
| **P2. 교수 / 랩실 / 인턴 담당자** | 추천서·인턴 지원 검토 | 전공 이수 과목, 학술 활동, 학업 성실도 |
| **P3. 본인** | 프로젝트 추가 시 | 파일 한 곳만 수정하면 반영되는 구조 |

P1이 최우선. 모든 디자인/정보 우선순위는 P1 기준으로 결정한다.

---

## 3. 범위

### In Scope (v1)
- 원페이지(single-page) 반응형 정적 사이트, 상단 고정 내비게이션 + 스크롤 앵커 이동
- Hero / About / Skills / Projects / Activities / Education / Contact 7개 섹션
- 프로젝트 상세는 카드 확장(아코디언) 또는 모달로 표현 — 별도 라우팅 없음
- 다크/라이트 모드 토글
- 이력서 PDF 다운로드 버튼
- 콘텐츠는 코드가 아닌 **데이터 파일(`src/data/*.ts` 또는 `content/*.json`)로 분리**

### Out of Scope (v1)
- 백엔드 서버, 데이터베이스, 로그인
- 블로그/CMS, 댓글, 방명록
- 다국어(영문) 버전 → v2 후보
- 문의 폼(서버 필요) → `mailto:` 링크로 대체
- 방문자 분석 대시보드 자체 구현 (필요 시 GA4 스크립트 삽입으로 갈음)

---

## 4. 정보 구조 (IA)

```
Header (고정)  Logo(이한양) · About · Skills · Projects · Contact · [Resume PDF] · [🌙/☀️]
│
├─ 1. Hero          이름 / AI ENGINEER / 한 줄 소개 / CTA(프로젝트 보기, GitHub)
├─ 2. About         이력서 요약문 전문 + 핵심 키워드 뱃지 3~4개
├─ 3. Skills        3개 그룹 카드 (Language / AI·ML / Tools)
├─ 4. Projects      프로젝트 카드 2개 (최신순) — 사이트의 핵심 섹션
├─ 5. Activities    타임라인 2건 (동아리, 서머 스터디)
├─ 6. Education     학교/전공/기간/학점/이수 과목
└─ 7. Contact       GitHub · Email · Phone + Footer
```

---

## 5. 섹션별 요구사항

### 5.1 Hero
- **표시**: `이한양` / `AI ENGINEER` / 요약 1문장(예: "AI 시스템의 전체 과정을 이해하고 직접 구현하는 AI Engineer를 목표로 합니다.")
- **CTA**: `프로젝트 보기`(#projects 스크롤), `GitHub`(새 탭)
- 스크롤 없이 화면에 이름·직군·CTA가 모두 보여야 한다 (뷰포트 높이 100vh 이하 권장)

### 5.2 About
- 이력서 요약 문단 전문 노출
- 하단에 키워드 뱃지: `PyTorch` `NLP / Transformer` `LLM · RAG` `Computer Vision`

### 5.3 Skills
데이터 원문 그대로 3개 그룹으로 렌더링:

| 그룹 | 항목 |
|---|---|
| Programming Language | Python, C++ |
| AI / ML | PyTorch, Scikit-Learn, Hugging Face Transformers, NLP, Computer Vision, LLM, RAG |
| Tools | Git, GitHub, Docker, FastAPI, Streamlit, Jupyter Notebook |

- 각 항목은 pill 형태 뱃지. **숙련도 %·별점 표시는 하지 않는다**(근거 없는 수치는 신뢰도를 떨어뜨림).

### 5.4 Projects — 최우선 섹션
카드 1장에 담기는 필드:

| 필드 | 예시 |
|---|---|
| 제목 | 한양대 학사정보 RAG 챗봇 |
| 기간 · 유형 | 2026.03 – 2026.05 · 팀 프로젝트 |
| 한 줄 요약 | 학사 안내 문서를 검색해 질문에 답하는 RAG 챗봇 |
| 상세 설명 | 이력서의 불릿 3~5개 |
| Tech Stack | 뱃지 목록 |
| 링크 | GitHub (Demo 있으면 추가) |
| 썸네일 | 이미지 또는 그라디언트 플레이스홀더 (16:9) |

**등록 프로젝트 (최신순)**
1. **한양대 학사정보 RAG 챗봇** (2026.03–05, 팀)
   - 학사 공지·PDF를 Chunk 분할 + Embedding 후 Vector DB 저장
   - 질문 관련 문서 검색 후 LLM이 근거 기반 답변하도록 RAG Pipeline 구현
   - Chunk Size / Top-K 값에 따른 검색 정확도 비교 실험
   - FastAPI + Streamlit 웹 데모 구현
   - Stack: Python, LangChain, Hugging Face, FAISS, FastAPI, Streamlit
   - GitHub: `https://github.com/example-hanyang-ai/hyu-rag-chatbot`
2. **딥러닝 기반 음식 이미지 분류 및 영양정보 추천 시스템** (2025.09–12, 팀)
   - 음식 이미지 분류 후 영양정보를 제공하는 AI 서비스
   - 공개 데이터셋 전처리 및 Augmentation
   - ResNet 기반 Transfer Learning 분류 모델 구축
   - Accuracy / Precision / Recall / F1-score 기반 성능 평가
   - 모델을 API화하여 웹에서 이미지 업로드·추론 가능하도록 구현
   - Stack: Python, PyTorch, torchvision, ResNet, FastAPI, Streamlit
   - GitHub: `https://github.com/example-hanyang-ai/food-vision-demo`

**동작**: 카드 클릭 시 상세 불릿 펼침. 기본 상태에서는 요약 + 스택 + 링크만 노출.

### 5.5 Activities (타임라인)
1. **AI 학술동아리** — 한양대학교 인공지능학과, 2025.03–2025.12
   - 논문/기술 스터디, PyTorch로 CNN·RNN·Transformer 구현, Hugging Face 사전학습 모델 Fine-tuning
2. **교내 AI Summer Study — 생성형 AI & LLM 스터디**, 2025.07–2025.08
   - Transformer/LLM 구조 학습, Prompt Engineering·RAG 실습, LangChain LLM Application 개발

### 5.6 Education
- 한양대학교 인공지능학과 학사과정, 2023.03 – 현재
- 2026년 현재 4학년 재학 / 학점(전공) 3.0 / 4.5
- 관련 과목: 인공지능, 머신러닝, 딥러닝, 자연어처리, 컴퓨터비전, 자료구조, 알고리즘, 확률 및 통계

### 5.7 Contact
- GitHub `https://github.com/example-hanyang-ai` (새 탭)
- Email `lee.hanyang@example.com` (`mailto:`)
- Phone `010-0000-0000`
- **개인정보 주의**: 전화번호는 공개 웹에 노출하면 스팸 위험이 있으므로 **기본은 이메일·GitHub만 노출**하고,
  전화번호는 데이터 파일의 플래그(`showPhone: false`)로 제어한다.
- 이메일은 크롤러 대비로 텍스트 직접 노출 대신 클릭 시 조합 방식 사용(선택).

---

## 6. 비기능 요구사항

| 항목 | 요구 |
|---|---|
| 반응형 | 360px(모바일) / 768px(태블릿) / 1280px(데스크톱) 3개 브레이크포인트 |
| 성능 | Lighthouse Performance ≥ 90, 이미지 WebP·lazy loading |
| 접근성 | 시맨틱 태그(`header/nav/section/footer`), 이미지 `alt`, 본문 대비비 4.5:1 이상, 키보드 탭 이동 가능 |
| SEO | `<title>이한양 · AI Engineer`, meta description, Open Graph 이미지(링크 공유 시 카드 표시) |
| 브라우저 | 최신 Chrome / Edge / Safari, 모바일 Safari·Chrome |
| 유지보수 | 콘텐츠 수정 시 데이터 파일만 편집 — 컴포넌트 코드 수정 불필요 |

---

## 7. 디자인 가이드

- **톤**: 기술 중심, 절제된 미니멀. 과한 애니메이션·화려한 색상 지양.
- **컬러**: 뉴트럴 배경(라이트 `#FAFAFA` / 다크 `#0E0E10`) + 액센트 1색(예: 한양대 블루 계열 또는 딥 인디고). 액센트는 CTA·링크·뱃지에만 사용.
- **타이포**: 한글 Pretendard, 영문/코드 Inter 또는 JetBrains Mono. 본문 16px / 행간 1.7.
- **레이아웃**: 최대 폭 1120px 중앙 정렬, 섹션 상하 패딩 96px(데스크톱) / 64px(모바일).
- **모션**: 스크롤 진입 시 fade-up 정도만. `prefers-reduced-motion` 존중.

---

## 8. 기술 스택 (제안)

| 영역 | 선택 | 이유 |
|---|---|---|
| 프레임워크 | **Next.js (App Router) + TypeScript** | SEO/OG 태그 처리 용이, 정적 export 가능, 취업 시 어필되는 스택 |
| 스타일 | Tailwind CSS | 반응형·다크모드 구현 속도 |
| 배포 | Vercel (GitHub 연동 자동 배포) | 무료, 커스텀 도메인 연결 가능 |
| 콘텐츠 | `src/data/resume.ts` 단일 소스 | 이력서 내용 = 타입 지정된 객체 하나 |

> **대안**: 학습 부담을 줄이려면 `index.html + CSS + 최소 JS` 단일 파일 정적 사이트 + GitHub Pages 배포로도 v1 요구사항을 모두 충족할 수 있다. 확장 계획이 없다면 이쪽이 더 빠르다.

### 디렉터리(안)
```
web/
├─ src/
│  ├─ app/            layout.tsx, page.tsx, globals.css
│  ├─ components/     Hero, About, Skills, Projects, ProjectCard, Activities, Education, Contact, Header, ThemeToggle
│  └─ data/resume.ts  ← 모든 이력 콘텐츠
└─ public/            resume.pdf, og-image.png, projects/*.webp
```

---

## 9. 개발 단계

| 단계 | 산출물 | 완료 조건 |
|---|---|---|
| M1. 세팅 | 프로젝트 초기화, Tailwind, 폰트, 다크모드 토큰 | 빈 페이지가 로컬에서 뜸 |
| M2. 데이터 | `resume.ts` 타입 + 이력서 전체 내용 입력 | 이력서 항목 100% 반영 |
| M3. 섹션 구현 | Hero → Projects → Skills → 나머지 순 | 데스크톱에서 전 섹션 렌더링 |
| M4. 반응형·다크모드 | 3개 브레이크포인트 대응 | 360px에서 가로 스크롤 없음 |
| M5. 마감 | OG 이미지, meta, resume.pdf, 접근성 점검 | Lighthouse 90+ |
| M6. 배포 | Vercel 배포 + 도메인 | 공개 URL에서 정상 동작 |

---

## 10. 확인이 필요한 사항 (Open Questions)

1. `resume_sample.docx`의 이름·이메일·GitHub·전화번호는 **샘플 값**으로 보인다. 실제 값으로 교체 필요.
2. 전화번호를 사이트에 공개할 것인가? (기본값: 비공개)
3. 프로젝트 썸네일/데모 스크린샷 이미지 확보 가능 여부. 없으면 플레이스홀더로 진행.
4. 배포 도메인: `이름.vercel.app` 무료 도메인 vs 커스텀 도메인 구매.
5. 영문 버전 필요 여부(외국계·글로벌 기업 지원 시 v2 우선순위 상승).

---

## 11. 향후 확장 (v2+)

- 영문/국문 언어 토글
- 프로젝트 상세 페이지 분리(`/projects/[slug]`) 및 회고 글 추가
- 이력서 PDF 자동 생성(사이트 데이터 → PDF)
- 조회수/유입 경로 분석(GA4 또는 Vercel Analytics)
