# Stable Diffusion으로 합성 데이터 생성하기

**한국어** | [English](#synthetic-data-generation-with-stable-diffusion)

## 📎 제출 링크 및 공개 설정

| 항목 | 링크 | 공개 설정 |
|---|---|---|
| GitHub 노트북 | [8_1_Stable_diffusion_실습.ipynb](8_1_Stable_diffusion_%E1%84%89%E1%85%B5%E1%86%AF%E1%84%89%E1%85%B3%E1%86%B8.ipynb) | Public 저장소 (로그인 없이 열람 가능) |
| GitHub 폴더 | https://github.com/Jeminana/ERICA_X_MODULABS_CV/tree/main/08_Gen_Synthetic_data | Public |

> 실행 환경: Google Colab, CUDA GPU, `diffusers==0.33.1`, `transformers==4.52.4`

---

## 📌 프로젝트 개요

Hugging Face `diffusers`의 **Stable Diffusion v1.5**로 두 가지 이미지 생성 방식을 실습했습니다.

1. **Text-to-Image** — 텍스트 프롬프트만으로 새 이미지를 생성
2. **Inpainting** — 기존 이미지에 마스크를 씌우고, 마스크 영역만 프롬프트에 맞게 다시 그림

Inpainting은 정상 제품 이미지의 일부에 결함(녹, 페인트 벗겨짐 등)을 그려 넣어 **불량 데이터를 합성**하는 용도로 쓸 수 있어서, 이상 탐지([07_Anomaly_detection](../07_Anomaly_detection))처럼 불량 데이터가 부족한 문제에 활용할 수 있는지 확인하는 것이 목적이었습니다.

---

## 🔍 구현한 기능

| 단계 | 구성 요소 | 하는 일 |
|---|---|---|
| 1 | 환경 설정 | `diffusers`, `transformers` 버전 고정, GPU 확인 |
| 2 | `StableDiffusionPipeline` | `stable-diffusion-v1-5/stable-diffusion-v1-5`를 fp16으로 불러와 텍스트로 이미지 생성 |
| 3 | `StableDiffusionInpaintPipeline` | `stable-diffusion-v1-5/stable-diffusion-inpainting`을 불러와 마스크 영역만 다시 생성 |
| 4 | 마스크 생성 | `PIL.ImageDraw`로 흰색 타원 마스크를 그림 (흰색 = 다시 그릴 영역) |
| 5 | `display_image()` | 원본, 마스크, 결과 이미지를 matplotlib으로 시각화하고 `.png`로 저장 |

### 주요 파라미터

| 파라미터 | 의미 |
|---|---|
| `prompt` / `negative_prompt` | 생성할 내용 / 피하고 싶은 내용 |
| `num_inference_steps` | 노이즈 제거 단계 수. 클수록 디테일이 좋아지지만 느려짐 |
| `guidance_scale` | 프롬프트를 얼마나 강하게 따를지 (CFG). 너무 크면 이미지가 부자연스러워짐 |
| `generator.manual_seed()` | 초기 노이즈를 고정해 같은 결과를 다시 얻기 위함 |

---

## 🧪 실험 조건과 결과

| Test | 방식 | 입력 | 프롬프트 | 주요 설정 |
|---|---|---|---|---|
| 1 | Text-to-Image | – | `A photo of man riding a horse in the moon wearing astronaut outfits` | steps 30, guidance 8.5, seed 7 |
| 2 | Inpainting | `product1.jpg` (기하학 패턴 벽) + 중앙 작은 원 마스크 `(220,220)-(300,300)` | `peeling paint and rust` | steps 50, guidance 7.5, seed 없음 |
| 3 | Inpainting | Unsplash 해변 사진 + 큰 타원 마스크 `(50,50)-(460,460)` | `A treasure chest buried in the sand` | steps 50, guidance 8.5, seed 1234 |

### Test 1. Text-to-Image (seed 42 → 7)

- 달 표면 위의 우주비행사는 사실적으로 잘 생성되었습니다.
- 하지만 **말(horse)이 이미지에 없습니다.** "말을 탄 우주비행사"처럼 흔하지 않은 조합은 SD v1.5가 일부 단어를 무시하는 경우가 많습니다.
- seed를 42에서 7로 바꿔 재현성을 실험했습니다. `torch.Generator`에 seed를 고정하면 같은 초기 노이즈에서 시작하므로 같은 결과가 나옵니다. 다만 노트북에는 seed 7 결과만 남아 있어 두 seed의 결과를 나란히 비교할 수는 없습니다.

### Test 2. 다른 이미지로 Inpainting

- 기하학 패턴이 칠해진 벽 사진에 중앙 원형 마스크를 씌우고 녹과 벗겨진 페인트를 그리려 했습니다.
- **결과 이미지에서 결함이 거의 보이지 않았습니다.** 원본과 결과의 평균 픽셀 차이가 약 4/255로, VAE로 인코딩·디코딩하면서 생기는 정도의 차이만 있었습니다.
- 원인으로 보이는 것:
  - 마스크가 80×80 픽셀로 이미지의 약 2%밖에 안 돼서, 주변의 깨끗한 벽 문맥이 결과를 강하게 끌어당김
  - `peeling paint and rust`처럼 짧은 프롬프트와 guidance 7.5로는 주변 문맥을 이기지 못함
  - seed를 고정하지 않아 같은 조건으로 다시 비교할 수 없음

### Test 3. 마스크 크기와 위치 변경

- 마스크를 이미지 대부분을 덮는 큰 타원으로 바꾸고, 해변 사진에 보물상자를 그렸습니다.
- **보물상자가 해변의 빛과 원근에 맞게 자연스럽게 생성되었습니다.** 마스크 바깥의 수평선, 하늘 일부는 그대로 유지되었습니다.
- 다만 마스크 안에 있던 **하늘과 구름도 함께 다시 그려져** 원본과 구름 모양이 달라졌습니다. 마스크가 크면 원하지 않는 영역까지 바뀝니다.
- Test 2와 비교하면, **마스크 크기가 생성 결과에 큰 영향을 준다**는 것을 확인했습니다. 마스크가 너무 작으면 아무것도 안 바뀌고, 너무 크면 배경까지 바뀝니다.

---

## 🐛 디버깅 및 확인한 점

- **라이브러리 버전 확인** — `pip install` 출력에는 `transformers` 5.19.0이 보이지만 import한 버전은 4.52.4였습니다. `diffusers 0.33.1`과 호환되도록 두 버전을 명시적으로 고정했습니다.
- **Text-to-Image 코드에 결함 생성용 이름이 남아 있음** — 변수명이 `prompt_defect`, 저장 파일명이 `generated_defect_0.png`이고, negative prompt에 `normal, no defect`가 들어 있습니다. 원래 결함 이미지 생성용 템플릿을 그대로 쓰고 프롬프트만 바꿔서 생긴 것으로, 우주비행사 이미지에는 의미가 없는 설정입니다.
- **셀 실행 순서** — Test 2 결과 이미지에 `Generated Image` 제목이 붙어 있는데, 이 제목은 Test 3 셀에서 다시 정의한 `display_image()`에서 나옵니다. Test 3 셀을 먼저 실행한 뒤 Test 2를 다시 실행한 것으로, 위에서 아래로 순서대로 실행하면 출력이 달라질 수 있습니다.
- **같은 모델 중복 로딩** — Test 2와 Test 3에서 같은 inpainting 파이프라인을 두 번 불러와 GPU 메모리를 더 사용합니다.
- **마크다운 메모와 코드 불일치** — 노트에는 Test 1의 `num_steps`를 50으로 바꿨다고 되어 있지만, 최종 코드는 30입니다.

---

## 💭 회고 (KPT)

### Keep — 잘한 점

- Text-to-Image와 Inpainting을 모두 실행해 보고, **각 방식이 언제 잘 되고 언제 안 되는지** 결과 이미지로 직접 확인했습니다.
- seed, 입력 이미지, 마스크 크기를 바꿔 보면서 **어떤 파라미터가 결과에 영향을 주는지** 비교했습니다.
- `diffusers`와 `transformers` 버전을 고정해서 다시 실행해도 같은 환경이 되도록 했습니다.
- 파이프라인 로딩을 `try/except`로 감싸고, 이미지 다운로드 실패 시 대체 이미지를 그리도록 해서 셀이 중간에 멈추지 않게 했습니다.

### Problem — 아쉬운 점

- **본래 목적인 결함 합성(Test 2)이 실패했습니다.** 녹·페인트 벗겨짐이 거의 생기지 않아, 이 설정으로는 불량 데이터로 쓸 수 없습니다.
- Test 1에서 **프롬프트의 말(horse)이 빠졌는데**, 프롬프트를 바꿔 다시 시도하지는 않았습니다. seed 42와 7의 결과도 나란히 남겨 두지 않았습니다.
- 각 테스트마다 **여러 조건을 동시에 바꿔서**(이미지, 마스크, 프롬프트, guidance, seed) 어떤 변화가 결과를 만든 것인지 정확히 알 수 없습니다.
- 결과를 눈으로만 비교했고, 정량 지표(CLIP score 등)는 없습니다.
- Test 2는 seed를 고정하지 않아 재현할 수 없습니다.
- 변수명·파일명·negative prompt에 결함 템플릿이 남아 있고, 셀 실행 순서가 뒤섞여 있습니다.

### Try — 다음에 시도할 것

- 결함 합성: 마스크를 키우거나 `strength`를 1.0에 가깝게 두고, guidance를 10~12로 올리고, `close-up of rusty corroded metal surface, flaking paint`처럼 구체적인 프롬프트 사용
- Test 1: `riding a horse`를 프롬프트 앞쪽에 두거나 강조해서 다시 생성, 또는 SDXL처럼 프롬프트를 더 잘 따르는 모델과 비교
- 한 번에 **파라미터 하나만** 바꾸는 표(steps 20/30/50, guidance 5/7.5/10)를 만들어 그리드로 비교
- 하나의 inpainting 파이프라인을 재사용하고, 위에서 아래로 한 번에 다시 실행해 출력 정리
- 합성한 결함 이미지를 07의 PaDiM에 넣어 실제로 이상으로 판정되는지 확인

### 실행 가능한 액션

| # | 액션 | 완료 기준 | 상태 |
|---|---|---|---|
| 1 | Test 2를 seed 고정 + 마스크 크기 3종(80/160/240px)으로 재실행 | 결함이 보이는 최소 마스크 크기를 표로 기록 | |
| 2 | 결함 프롬프트 구체화 + guidance 7.5/10/12 비교 | 결함이 보이는 조건 1개 이상 확인 | |
| 3 | Test 1 프롬프트 수정 후 seed 3개로 생성 | 말이 포함된 이미지 비율 기록 | |
| 4 | `prompt_defect`, `generated_defect_*`, `normal, no defect` 정리 | Text-to-Image 코드에 결함 관련 이름이 남지 않음 | |
| 5 | inpainting 파이프라인 1회만 로딩, 노트북 전체 재실행 | Restart & Run All에서 에러 없이 순서대로 출력 | |
| 6 | 합성 결함 이미지를 PaDiM으로 평가 | 이상 점수가 정상 95번째 백분위(26.54)를 넘는지 기록 | |

<br>

---
---

# Synthetic Data Generation with Stable Diffusion

[한국어](#stable-diffusion으로-합성-데이터-생성하기) | **English**

## 📎 Links and Visibility

| Item | Link | Visibility |
|---|---|---|
| GitHub notebook | [8_1_Stable_diffusion_실습.ipynb](8_1_Stable_diffusion_%E1%84%89%E1%85%B5%E1%86%AF%E1%84%89%E1%85%B3%E1%86%B8.ipynb) | Public repository (no login needed) |
| GitHub folder | https://github.com/Jeminana/ERICA_X_MODULABS_CV/tree/main/08_Gen_Synthetic_data | Public |

> Environment: Google Colab, CUDA GPU, `diffusers==0.33.1`, `transformers==4.52.4`

---

## 📌 Overview

I used **Stable Diffusion v1.5** from Hugging Face `diffusers` to practice two ways of generating images.

1. **Text-to-Image** — generate a new image from a text prompt alone
2. **Inpainting** — mask part of an existing image and redraw only the masked region to match a prompt

Inpainting can paint defects (rust, peeling paint, etc.) onto part of a normal product image to **synthesize defective samples**. The goal was to see whether this could help problems that lack defect data, like anomaly detection ([07_Anomaly_detection](../07_Anomaly_detection)).

---

## 🔍 What Was Implemented

| Step | Component | What it does |
|---|---|---|
| 1 | Environment setup | Pins `diffusers` and `transformers` versions, checks the GPU |
| 2 | `StableDiffusionPipeline` | Loads `stable-diffusion-v1-5/stable-diffusion-v1-5` in fp16 and generates images from text |
| 3 | `StableDiffusionInpaintPipeline` | Loads `stable-diffusion-v1-5/stable-diffusion-inpainting` and regenerates only the masked region |
| 4 | Mask creation | Draws a white ellipse mask with `PIL.ImageDraw` (white = region to redraw) |
| 5 | `display_image()` | Shows the original, mask and result with matplotlib and saves them as `.png` |

### Key Parameters

| Parameter | Meaning |
|---|---|
| `prompt` / `negative_prompt` | What to generate / what to avoid |
| `num_inference_steps` | Number of denoising steps. More steps give more detail but are slower |
| `guidance_scale` | How strongly to follow the prompt (CFG). Too high makes images look unnatural |
| `generator.manual_seed()` | Fixes the initial noise so the same result can be reproduced |

---

## 🧪 Experimental Setup and Results

| Test | Method | Input | Prompt | Main settings |
|---|---|---|---|---|
| 1 | Text-to-Image | – | `A photo of man riding a horse in the moon wearing astronaut outfits` | 30 steps, guidance 8.5, seed 7 |
| 2 | Inpainting | `product1.jpg` (geometric painted wall) + small center circle mask `(220,220)-(300,300)` | `peeling paint and rust` | 50 steps, guidance 7.5, no seed |
| 3 | Inpainting | Unsplash beach photo + large ellipse mask `(50,50)-(460,460)` | `A treasure chest buried in the sand` | 50 steps, guidance 8.5, seed 1234 |

### Test 1. Text-to-Image (seed 42 → 7)

- The astronaut on the lunar surface came out realistic.
- However, **there is no horse in the image.** For unusual combinations like "an astronaut riding a horse", SD v1.5 often ignores part of the prompt.
- I changed the seed from 42 to 7 to test reproducibility. Fixing the seed on `torch.Generator` starts from the same initial noise, so it gives the same result. However, only the seed 7 output is kept in the notebook, so the two seeds can't be compared side by side.

### Test 2. Inpainting on a Different Image

- I masked a circle in the center of a geometric painted wall photo and tried to draw rust and peeling paint.
- **The defect is barely visible in the result.** The mean pixel difference between original and result is about 4/255, roughly what VAE encoding/decoding alone would cause.
- Likely causes:
  - The mask is 80×80 pixels, only about 2% of the image, so the surrounding clean wall pulls the result strongly toward "no change"
  - A short prompt like `peeling paint and rust` with guidance 7.5 can't overcome the surrounding context
  - No fixed seed, so the same condition can't be re-compared

### Test 3. Changing Mask Size and Position

- I switched to a large ellipse mask covering most of the image and drew a treasure chest on a beach photo.
- **The treasure chest was generated naturally, matching the lighting and perspective of the beach.** The horizon and parts of the sky outside the mask were kept.
- However, **the sky and clouds inside the mask were redrawn too**, so the clouds differ from the original. A large mask changes areas you didn't intend to change.
- Compared with Test 2, this showed that **mask size has a big effect on the result**. Too small and nothing changes; too large and the background changes as well.

---

## 🐛 Debugging and Findings

- **Library version check** — the `pip install` output shows `transformers` 5.19.0, but the imported version was 4.52.4. I pinned both versions explicitly to stay compatible with `diffusers 0.33.1`.
- **Defect-generation names left in the Text-to-Image code** — the variable is `prompt_defect`, the saved file is `generated_defect_0.png`, and the negative prompt contains `normal, no defect`. These come from reusing a defect-image template and only changing the prompt, and they make no sense for an astronaut image.
- **Cell execution order** — the Test 2 output images have a `Generated Image` title, which comes from the `display_image()` redefined in the Test 3 cell. Test 3 was run before Test 2 was re-run, so running the notebook top to bottom may give different output.
- **Same model loaded twice** — Test 2 and Test 3 each load the same inpainting pipeline, using extra GPU memory.
- **Markdown note doesn't match the code** — the note says Test 1's `num_steps` was changed to 50, but the final code uses 30.

---

## 💭 Retrospective (KPT)

### Keep

- Ran both Text-to-Image and Inpainting and checked from the actual images **when each method works and when it doesn't**.
- Changed the seed, input image and mask size to see **which parameters affect the result**.
- Pinned `diffusers` and `transformers` versions so the environment can be reproduced.
- Wrapped pipeline loading in `try/except` and drew a fallback image when the download fails, so cells don't stop halfway.

### Problem

- **The original goal, defect synthesis (Test 2), failed.** Almost no rust or peeling paint appeared, so these settings can't produce usable defect data.
- In Test 1 **the horse from the prompt was missing**, and I didn't retry with a different prompt. I also didn't keep the seed 42 and seed 7 outputs side by side.
- Each test **changed several conditions at once** (image, mask, prompt, guidance, seed), so it's unclear which change caused which effect.
- Results were only compared by eye, with no quantitative metric (e.g. CLIP score).
- Test 2 has no fixed seed and can't be reproduced.
- Variable names, file names and the negative prompt still carry the defect template, and the cells were run out of order.

### Try

- Defect synthesis: use a larger mask or keep `strength` near 1.0, raise guidance to 10–12, and use a more specific prompt such as `close-up of rusty corroded metal surface, flaking paint`
- Test 1: move or emphasize `riding a horse` earlier in the prompt and regenerate, or compare with a model that follows prompts better, such as SDXL
- Build a table that changes **one parameter at a time** (steps 20/30/50, guidance 5/7.5/10) and compare in a grid
- Reuse one inpainting pipeline and re-run the notebook top to bottom to clean up outputs
- Feed synthesized defect images into the PaDiM model from 07 to see whether they are actually flagged as anomalies

### Action Items

| # | Action | Done when | Status |
|---|---|---|---|
| 1 | Re-run Test 2 with a fixed seed and 3 mask sizes (80/160/240px) | Smallest mask size that shows a defect recorded in a table | |
| 2 | Make the defect prompt specific and compare guidance 7.5/10/12 | At least one condition where the defect is visible | |
| 3 | Rewrite the Test 1 prompt and generate with 3 seeds | Share of images that include a horse recorded | |
| 4 | Clean up `prompt_defect`, `generated_defect_*`, `normal, no defect` | No defect-related names left in the Text-to-Image code | |
| 5 | Load the inpainting pipeline once and re-run the whole notebook | Restart & Run All finishes without errors, outputs in order | |
| 6 | Evaluate synthesized defect images with PaDiM | Record whether the score exceeds the normal 95th percentile (26.54) | |
