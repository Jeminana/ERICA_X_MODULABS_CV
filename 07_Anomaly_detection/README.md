# 제조업 실시간 이상 탐지 시스템 구축

**한국어** | [English](#real-time-anomaly-detection-for-manufacturing)

## 📎 제출 링크 및 공개 설정

| 항목 | 링크 | 공개 설정 |
|---|---|---|
| GitHub 노트북 | [6_제조업_실시간_이상_탐지_시스템_구축_[프로젝트].ipynb](6_%E1%84%8C%E1%85%A6%E1%84%8C%E1%85%A9%E1%84%8B%E1%85%A5%E1%86%B8_%E1%84%89%E1%85%B5%E1%86%AF%E1%84%89%E1%85%B5%E1%84%80%E1%85%A1%E1%86%AB_%E1%84%8B%E1%85%B5%E1%84%89%E1%85%A1%E1%86%BC_%E1%84%90%E1%85%A1%E1%86%B7%E1%84%8C%E1%85%B5_%E1%84%89%E1%85%B5%E1%84%89%E1%85%B3%E1%84%90%E1%85%A6%E1%86%B7_%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8_%5B%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%5D%20.ipynb) | Public 저장소 (로그인 없이 열람 가능) |
| GitHub 폴더 | https://github.com/Jeminana/ERICA_X_MODULABS_CV/tree/main/07_Anomaly_detection | Public |

> 실행 환경: Google Colab, T4 GPU

---

## 📌 프로젝트 개요

**VisA** 데이터셋의 `pcb4` 카테고리를 사용해 **정상 이미지만으로 학습하는 비지도 이상 탐지** 모델 3가지를 구현하고 비교했습니다. 그중 성능이 가장 좋았던 **PaDiM**을 저장하고, **Gradio**로 이미지를 올리면 바로 정상/비정상 판정과 이상 영역 히트맵을 보여주는 실시간 추론 데모를 만들었습니다.

- 데이터셋: [VisA (Amazon Visual Anomaly)](https://github.com/amazon-science/spot-diff), `pcb4` 카테고리 (정상 1,005장 / 이상 100장, 결함 유형 27종)
- 학습: 정상 이미지 804장 (정상 데이터의 80%)
- 테스트: 정상 201장 + 이상 100장 = 301장

---

## 🔍 구현한 기능

| 단계 | 구성 요소 | 하는 일 |
|---|---|---|
| 1 | `download_visa_dataset()` / `check_visa_structure()` | VisA tar 파일을 받아 풀고, 카테고리별 정상 이미지 수를 확인 |
| 2 | `VisADataset` | `image_anno.csv`를 읽어 정상(0)/이상(1) 라벨과 결함 유형, 마스크 경로를 구성. 학습 세트에는 **정상 데이터만** 넣고, 테스트 세트에는 남은 정상 + 모든 이상 데이터를 넣음 |
| 3 | `visualize_visa_samples()` / `plot_visa_statistics()` | 샘플 이미지, 마스크, 클래스 비율, 결함 유형 분포 시각화 |
| 4 | `FeatureExtractor` | ImageNet 사전학습 **Wide-ResNet50**에 forward hook을 걸어 중간 레이어(`layer2`, `layer3`) 특징 맵을 가져옴. 가중치는 고정 |
| 5 | `PaDiM` | 특징 맵을 28×28 패치로 나누고, **패치 위치마다 정상 특징의 평균·공분산**을 저장. 테스트 시 마할라노비스 거리로 이상 점수를 계산 |
| 6 | `AutoEncoderAnomalyDetector` | 합성곱 오토인코더를 정상 이미지로 학습시키고, **재구성 오차**를 이상 점수로 사용 |
| 7 | `OneClassSVMAnomalyDetector` | 특징 맵을 평균 풀링한 벡터로 One-Class SVM을 학습, 결정 경계 밖일수록 이상 |
| 8 | `AnomalyDetectionEvaluator` | AUROC, AUPRC, Best F1 계산 및 ROC/PR 곡선, 점수 분포 비교 |
| 9 | Gradio 데모 | 학습한 PaDiM 상태를 `pickle`로 저장 → 다시 불러와 업로드 이미지에 대해 점수, 히트맵, 오버레이 이미지 출력 |

### 핵심 아이디어: PaDiM

정상 이미지에서 같은 위치(예: 왼쪽 위 패치)의 특징은 비슷한 분포를 가집니다. PaDiM은 위치마다 이 분포를 가우시안으로 근사해 두고, 테스트 이미지의 패치가 그 분포에서 얼마나 떨어져 있는지(마할라노비스 거리)를 봅니다. 그래서 **이미지 단위 점수**와 함께 **어느 위치가 이상한지 보여주는 이상 맵**을 얻을 수 있습니다.

```python
# 패치 위치별로 정상 특징의 평균과 공분산을 저장
for patch_idx in range(28 * 28):
    patch_features = all_features[patch_idx::28*28]          # [n_samples, d_reduced]
    mean = torch.mean(patch_features, dim=0)
    cov = centered.T @ centered / (n - 1)
    cov += torch.eye(cov.shape[0]).to(device) * 1e-4          # 역행렬이 불안정해지지 않도록 대각 성분 보정
```

- `layer2` + `layer3` 특징을 이어 붙이면 채널이 1,536개라서 패치마다 1536×1536 공분산을 784개 저장해야 합니다. 이를 줄이기 위해 **랜덤 프로젝션으로 100차원**으로 낮췄습니다.
- 공분산이 특이행렬이 되면 `torch.linalg.inv` 대신 `pinv`를 쓰도록 예외 처리를 했습니다.

---

## 🧪 실험 조건과 결과

### 실험 조건

| 방법 | 입력 특징 | 주요 설정 |
|---|---|---|
| PaDiM | Wide-ResNet50 `layer2`+`layer3` → 28×28 패치 | 1,536차원 → 랜덤 프로젝션 100차원, 공분산 정규화 1e-4 |
| AutoEncoder | 원본 이미지 (256×256) | 잠재 채널 128, Adam lr 1e-3, MSE loss, 50 epoch |
| One-Class SVM | Wide-ResNet50 `layer2`+`layer3` 평균 풀링 벡터 | RBF 커널, `nu=0.1`, StandardScaler |

공통: 이미지 256×256, ImageNet 정규화, 배치 16, 학습 데이터에만 RandomHorizontalFlip

### 결과 (pcb4 테스트 301장)

| 방법 | AUROC | AUPRC | Best F1 |
|---|---|---|---|
| **PaDiM** | **0.9543** | **0.8840** | **0.8571** |
| AutoEncoder | 0.9273 | 0.7881 | 0.8225 |
| One-Class SVM | 0.8155 | 0.7033 | 0.6565 |

### 결과 해석

- **PaDiM이 세 지표 모두 가장 높았습니다.** 별도 학습 없이 사전학습 특징의 통계만 저장하는데도 가장 좋았고, 학습 시간도 특징 추출 약 14초로 가장 짧았습니다.
- **AutoEncoder**는 loss가 0.512 → 약 0.029까지 내려가며 정상 이미지를 잘 복원하게 되었고, AUROC 0.93으로 생각보다 괜찮았습니다. 다만 50 epoch × 약 13초가 걸려 PaDiM보다 훨씬 오래 걸렸고, 후반부에는 loss가 0.029~0.030 근처에서 더 내려가지 않았습니다.
- **One-Class SVM**이 가장 낮았습니다. 특징 맵 전체를 평균 풀링해 이미지당 벡터 하나로 만들기 때문에, PCB의 작은 결함 정보가 평균에 묻혀 버린 것으로 보입니다. 같은 백본 특징을 쓰는 PaDiM과의 차이(AUROC 0.82 vs 0.95)가 **위치 정보를 유지하는 것이 얼마나 중요한지**를 보여줍니다.
- AUROC보다 AUPRC가 방법 간 차이를 더 크게 보여줬습니다. 테스트 세트가 정상 2 : 이상 1로 불균형해서, 이상 샘플을 정확히 골라내는 능력은 AUPRC에서 더 잘 드러납니다.

### 실시간 추론 데모 (Gradio)

- 데모용 PaDiM은 `layer1`+`layer2`+`layer3`을 사용했습니다 (1,792차원 → 100차원).
- 학습 결과(`means`, `inv_covariances`, `projection_matrix`)를 `padim_outputs/padim_model_state.pkl`로 저장하고, 앱 시작 시 한 번만 불러와 추론 때마다 다시 학습하지 않도록 했습니다.
- `predict()`를 DataLoader 대신 **이미지 텐서 하나를 바로 받도록 수정**해서 업로드 이미지 한 장을 바로 추론할 수 있게 했습니다.
- 출력: 이상 점수와 판정 결과, 이상 맵 히트맵, 원본 이미지 위 오버레이

---

## 🔬 추가 실험

이미지 단위 AUROC만으로는 "현장에서 쓸 수 있는가"를 알기 어려워서 세 가지를 더 확인했습니다. 모든 추가 실험은 데모용 PaDiM(`layer1`+`layer2`+`layer3`)으로 진행했고, 이 모델의 테스트셋 이미지 AUROC는 **0.9757**입니다. `layer2`+`layer3`만 쓴 비교 실험의 PaDiM(0.9543)보다 높아서, `layer1`의 저수준 특징이 PCB 결함 탐지에 도움이 된 것으로 보입니다.

### Test 1. 픽셀 단위 위치 정확도 (Pixel AUROC)

이상 맵을 256×256으로 업샘플링하고 가우시안 블러(σ=4)를 적용한 뒤, GT 마스크와 픽셀 단위로 비교했습니다.

| 지표 | 값 |
|---|---|
| Image AUROC | 0.9757 |
| **Pixel AUROC** | **0.9789** |

→ 판정만 맞는 것이 아니라 **히트맵이 실제 결함 위치도 잘 짚는다**는 것을 확인했습니다. 불량 이미지 3장의 원본 / GT 마스크 / 이상 맵을 같은 색 범위로 그려 눈으로도 비교했습니다.

### Test 2. 정상 데이터만으로 임계값 정하기

기존 Best F1은 테스트셋 정답을 보고 고른 임계값이라 현실에서는 쓸 수 없습니다. 그래서 테스트용 정상 201장 중 100장을 **보정(calibration) 세트**로 떼어 정상 점수의 백분위로 임계값을 정하고, 나머지 정상 101장 + 불량 100장으로 평가했습니다.

| 임계값 기준 | 임계값 | F1 | 놓친 불량 | 오탐 |
|---|---|---|---|---|
| (참고) 테스트셋에 맞춘 Best F1 | – | 0.9453 | – | – |
| **정상 95번째 백분위** | **26.54** | **0.8925** | **17 / 100** | **3 / 101** |
| 정상 99번째 백분위 | 34.93 | 0.4496 | 71 / 100 | 0 / 101 |
| 정상 100번째 백분위 (최댓값) | 35.43 | 0.4496 | 71 / 100 | 0 / 101 |

- 정상 데이터만으로 정한 95번째 백분위 임계값으로도 **F1 0.89**가 나와, 상한선(0.945)과 큰 차이가 없었습니다.
- 반대로 오탐을 0으로 만들려고 임계값을 99번째 이상으로 올리면 **불량의 71%를 놓쳤습니다.** 정상 점수 분포의 꼬리가 길어서, 임계값을 조금만 올려도 미탐이 급격히 늘어납니다.
- 이후 실험에서는 95번째 백분위 값(26.54)을 `THRESHOLD`로 사용했습니다.

### Test 3. 촬영 환경 변화에 대한 강건성

정상 이미지 50장에 촬영 환경 변화를 흉내 낸 변형을 주고, 평균 이상 점수와 오탐률(정상을 불량으로 판정한 비율)을 측정했습니다.

| 변형 | 평균 점수 | 오탐률 |
|---|---|---|
| 원본 | 17.71 | 4% |
| 어둡게 (밝기 0.7) | 17.80 | 4% |
| 밝게 (밝기 1.3) | 21.10 | 8% |
| 블러 (Gaussian σ=2) | 36.01 | **100%** |
| 회전 5° | 39.63 | **100%** |
| 가우시안 노이즈 (std 15) | 28.45 | **98%** |

- **밝기 변화에는 강했지만**, 블러·회전·노이즈에는 정상 보드를 거의 전부 불량으로 판정했습니다.
- PaDiM은 **패치 위치마다** 정상 분포를 저장하기 때문에, 5°만 돌아가도 패치가 다른 위치의 분포와 비교되어 점수가 크게 오릅니다. 블러와 노이즈도 사전학습 특징의 질감 정보를 바꿔 같은 문제를 일으킵니다.
- 즉 실제 라인에 적용하려면 **카메라 고정·정렬·초점 관리가 필수**이고, 그렇지 않으면 정렬(registration) 전처리나 변형 증강을 넣은 학습이 필요합니다.

---

## 🐛 디버깅 및 확인한 점

- **마스크 시각화 경고** — `visualize_with_mask()`에서 `Clipping input data to the valid range for imshow ... Got range [0.0..255.0]` 경고가 나왔습니다. 마스크가 0~255 값 그대로 float으로 들어가서 생긴 문제로, 255로 나눠 0~1로 맞추면 해결됩니다.
- **`tarfile.extractall` DeprecationWarning** — Python 3.14부터 기본 필터가 바뀐다는 경고입니다. `filter='data'`를 넘기면 경고 없이 안전하게 압축을 풀 수 있습니다.
- **데이터 경로 중복** — CSV의 `image` 경로가 `pcb4/Data/...`처럼 카테고리 이름으로 시작해서 `category_path / image`로 합치면 `pcb4/pcb4/...`가 됩니다. 경로가 카테고리 이름으로 시작하는지 확인하고 분기해 해결했습니다.
- **OOM 대비** — PaDiM은 학습 시 전체 특징이 `[630336, 1536]` 크기라 메모리를 많이 씁니다. `run_all_methods()`에서는 각 방법을 `try/except`로 감싸 하나가 실패해도 나머지는 계속 실행되게 했습니다.
- **`except:` → `except RuntimeError:`** — 실시간 추론용 PaDiM에서는 모든 예외를 삼키던 bare except를 역행렬 실패에 해당하는 `RuntimeError`만 잡도록 바꿨습니다.

---

## 💭 회고 (KPT)

### Keep — 잘한 점

- 세 가지 방법을 **같은 데이터 분할, 같은 평가 클래스**로 돌려서 공정하게 비교할 수 있었습니다.
- 성능 비교에서 그치지 않고, 가장 좋은 모델을 저장 → 불러오기 → Gradio 데모까지 이어서 **실제로 쓸 수 있는 형태**로 만들어 봤습니다.
- AUROC 하나만 보지 않고 AUPRC, F1, 점수 분포까지 함께 봐서 방법 간 차이를 더 정확하게 이해할 수 있었습니다.
- 추가 실험으로 **Pixel AUROC, 정상 데이터만으로 정한 임계값, 촬영 환경 변화**까지 확인해서, 숫자 하나가 아니라 "현장에서 어떻게 동작할지"를 볼 수 있었습니다.

### Problem — 아쉬운 점

- 비교 실험의 Best F1은 여전히 테스트 세트에서 고른 임계값 기준입니다. Test 2에서 보정 세트로 정한 임계값의 F1(0.8925)을 따로 구했지만, 세 방법 모두에 적용하지는 않았습니다.
- **Gradio 데모의 판정 임계값이 15로 하드코딩되어 있습니다.** Test 3에서 정상 원본 이미지의 평균 점수가 17.71이었으므로, 지금 데모는 정상 보드도 대부분 불량으로 판정할 가능성이 큽니다. 보정 세트로 구한 26.54를 써야 합니다.
- **블러·회전·노이즈에 매우 취약합니다** (오탐률 98~100%). 카메라 위치나 초점이 조금만 달라져도 쓸 수 없는 수준입니다.
- PaDiM의 **랜덤 프로젝션에 seed를 고정하지 않아** 다시 실행하면 결과가 조금씩 달라집니다. 실제로 노트북을 다시 실행했을 때 PaDiM AUROC가 0.9519 → 0.9543으로 바뀌었습니다.
- 학습/테스트 분할이 CSV 순서대로(`iloc`) 나뉘어 있어 무작위 분할이 아닙니다.
- `pcb4` 한 카테고리만 실험해서, 다른 카테고리(capsules, macaroni 등)에서도 같은 순위가 나오는지는 확인하지 못했습니다.
- 노트북에 같은 클래스(`VisADataset`, `FeatureExtractor`, `PaDiM`)가 두 번 정의되어 있어 코드가 중복됩니다.
- Gradio `share=True` 링크는 최대 1주일만 유지되어 데모를 계속 공개해 둘 수 없습니다.

### Try — 다음에 시도할 것

- 데모 임계값을 보정 세트의 95번째 백분위 값으로 바꾸고, 세 방법 모두 같은 방식으로 F1을 다시 계산
- 학습 시 회전·블러·노이즈 증강을 넣거나, 추론 전에 기준 이미지에 맞춰 정렬하는 전처리를 넣어 Test 3을 다시 실행
- `torch.manual_seed()`로 seed를 고정하고, 여러 seed의 평균과 편차로 결과 보고
- 같은 파이프라인을 VisA 다른 카테고리에도 돌려 방법별 순위가 유지되는지 비교
- 설치해 둔 `anomalib`으로 **PatchCore** 등 최신 모델을 돌려 직접 구현한 PaDiM과 비교
- 중복 정의된 클래스를 하나로 정리하고, 실시간 추론 부분을 별도 `.py` 모듈과 Hugging Face Spaces 배포로 분리

### 실행 가능한 액션

| # | 액션 | 완료 기준 | 상태 |
|---|---|---|---|
| 1 | `torch.manual_seed(42)` 추가 후 PaDiM 3회 재실행 | AUROC 평균 ± 표준편차를 표로 기록 | |
| 2 | 정상 데이터에서 검증 세트 분리, 임계값을 검증 세트로 결정 | 테스트 F1을 다시 계산해 지금 값과 비교 | ✅ Test 2 (F1 0.8925) |
| 3 | `visualize_with_mask()`에서 마스크를 `/ 255.0`으로 정규화 | Clipping 경고 사라짐 | |
| 4 | pixel-level AUROC 함수 추가 | PaDiM 히트맵에 대한 pixel AUROC 기록 | ✅ Test 1 (0.9789) |
| 5 | `capsules` 카테고리로 같은 실험 반복 | 결과 표에 행 추가 | |
| 6 | Gradio 판정 임계값 15 → `THRESHOLD`(26.54)로 교체 | 정상 샘플 업로드 시 "정상" 판정 | |
| 7 | 회전·블러·노이즈 증강 또는 정렬 전처리 적용 | Test 3 오탐률이 30% 이하로 감소 | |

<br>

---
---

# Real-Time Anomaly Detection for Manufacturing

[한국어](#제조업-실시간-이상-탐지-시스템-구축) | **English**

## 📎 Links and Visibility

| Item | Link | Visibility |
|---|---|---|
| GitHub notebook | [6_제조업_실시간_이상_탐지_시스템_구축_[프로젝트].ipynb](6_%E1%84%8C%E1%85%A6%E1%84%8C%E1%85%A9%E1%84%8B%E1%85%A5%E1%86%B8_%E1%84%89%E1%85%B5%E1%86%AF%E1%84%89%E1%85%B5%E1%84%80%E1%85%A1%E1%86%AB_%E1%84%8B%E1%85%B5%E1%84%89%E1%85%A1%E1%86%BC_%E1%84%90%E1%85%A1%E1%86%B7%E1%84%8C%E1%85%B5_%E1%84%89%E1%85%B5%E1%84%89%E1%85%B3%E1%84%90%E1%85%A6%E1%86%B7_%E1%84%80%E1%85%AE%E1%84%8E%E1%85%AE%E1%86%A8_%5B%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%5D%20.ipynb) | Public repository (no login needed) |
| GitHub folder | https://github.com/Jeminana/ERICA_X_MODULABS_CV/tree/main/07_Anomaly_detection | Public |

> Environment: Google Colab, T4 GPU

---

## 📌 Overview

Using the `pcb4` category of the **VisA** dataset, I implemented and compared three **unsupervised anomaly detection** models that are trained on normal images only. I saved the best one, **PaDiM**, and built a real-time **Gradio** demo: upload an image and it returns a normal/anomaly decision plus a heatmap of the anomalous region.

- Dataset: [VisA (Amazon Visual Anomaly)](https://github.com/amazon-science/spot-diff), `pcb4` category (1,005 normal / 100 anomalous images, 27 defect types)
- Train: 804 normal images (80% of normal data)
- Test: 201 normal + 100 anomalous = 301 images

---

## 🔍 What Was Implemented

| Step | Component | What it does |
|---|---|---|
| 1 | `download_visa_dataset()` / `check_visa_structure()` | Downloads and extracts the VisA tar file, counts normal images per category |
| 2 | `VisADataset` | Reads `image_anno.csv` to build normal(0)/anomaly(1) labels, defect types and mask paths. The train set has **normal images only**; the test set has the remaining normal images plus all anomalous ones |
| 3 | `visualize_visa_samples()` / `plot_visa_statistics()` | Visualizes sample images, masks, class ratio and defect type distribution |
| 4 | `FeatureExtractor` | Attaches forward hooks to an ImageNet-pretrained **Wide-ResNet50** to grab intermediate feature maps (`layer2`, `layer3`). Weights are frozen |
| 5 | `PaDiM` | Splits feature maps into 28×28 patches and stores **the mean and covariance of normal features at each patch position**. At test time, the anomaly score is the Mahalanobis distance |
| 6 | `AutoEncoderAnomalyDetector` | Trains a convolutional autoencoder on normal images and uses **reconstruction error** as the anomaly score |
| 7 | `OneClassSVMAnomalyDetector` | Trains a One-Class SVM on average-pooled feature vectors; the further outside the decision boundary, the more anomalous |
| 8 | `AnomalyDetectionEvaluator` | Computes AUROC, AUPRC and Best F1; plots ROC/PR curves and score distributions |
| 9 | Gradio demo | Saves the trained PaDiM state with `pickle`, reloads it, and outputs score, heatmap and overlay for an uploaded image |

### Key Idea: PaDiM

In normal images, features at the same position (e.g. the top-left patch) follow a similar distribution. PaDiM approximates that distribution with a Gaussian for every position and measures how far each test patch is from it (Mahalanobis distance). This gives both an **image-level score** and an **anomaly map showing where the problem is**.

```python
# Store mean and covariance of normal features per patch position
for patch_idx in range(28 * 28):
    patch_features = all_features[patch_idx::28*28]          # [n_samples, d_reduced]
    mean = torch.mean(patch_features, dim=0)
    cov = centered.T @ centered / (n - 1)
    cov += torch.eye(cov.shape[0]).to(device) * 1e-4          # diagonal regularization for a stable inverse
```

- Concatenating `layer2` + `layer3` gives 1,536 channels, which would mean storing 784 covariance matrices of size 1536×1536. To reduce this, I used **random projection down to 100 dimensions**.
- If a covariance matrix is singular, the code falls back from `torch.linalg.inv` to `pinv`.

---

## 🧪 Experimental Setup and Results

### Setup

| Method | Input features | Main settings |
|---|---|---|
| PaDiM | Wide-ResNet50 `layer2`+`layer3` → 28×28 patches | 1,536 dims → random projection to 100, covariance regularization 1e-4 |
| AutoEncoder | Raw image (256×256) | 128 latent channels, Adam lr 1e-3, MSE loss, 50 epochs |
| One-Class SVM | Average-pooled Wide-ResNet50 `layer2`+`layer3` vector | RBF kernel, `nu=0.1`, StandardScaler |

Common: 256×256 images, ImageNet normalization, batch size 16, RandomHorizontalFlip on training data only

### Results (pcb4, 301 test images)

| Method | AUROC | AUPRC | Best F1 |
|---|---|---|---|
| **PaDiM** | **0.9543** | **0.8840** | **0.8571** |
| AutoEncoder | 0.9273 | 0.7881 | 0.8225 |
| One-Class SVM | 0.8155 | 0.7033 | 0.6565 |

### Interpretation

- **PaDiM scored highest on all three metrics.** It only stores statistics of pretrained features with no extra training, yet it performed best, and it was also the fastest to train (about 14 seconds of feature extraction).
- **AutoEncoder** loss dropped from 0.512 to about 0.029, so it learned to reconstruct normal images well, and AUROC 0.93 was better than expected. However, 50 epochs × ~13 seconds made it much slower than PaDiM, and the loss plateaued around 0.029–0.030 in later epochs.
- **One-Class SVM** scored lowest. Average-pooling the whole feature map into one vector per image seems to wash out small PCB defects. The gap to PaDiM, which uses the same backbone features (AUROC 0.82 vs 0.95), shows **how important it is to keep spatial information**.
- AUPRC separated the methods more clearly than AUROC. The test set is imbalanced (2 normal : 1 anomalous), so the ability to pick out anomalies precisely shows up better in AUPRC.

### Real-Time Inference Demo (Gradio)

- The demo PaDiM uses `layer1`+`layer2`+`layer3` (1,792 dims → 100).
- The trained state (`means`, `inv_covariances`, `projection_matrix`) is saved to `padim_outputs/padim_model_state.pkl` and loaded once at app start, so the model is not retrained on every request.
- `predict()` was **changed to accept a single image tensor** instead of a DataLoader, so one uploaded image can be scored directly.
- Outputs: anomaly score and decision, anomaly map heatmap, overlay on the original image

---

## 🔬 Additional Tests

Image-level AUROC alone does not tell whether the model would work on a real line, so I checked three more things. All additional tests use the demo PaDiM (`layer1`+`layer2`+`layer3`), whose image AUROC on the test set is **0.9757**. That is higher than the `layer2`+`layer3` PaDiM in the comparison (0.9543), which suggests the low-level features from `layer1` help with PCB defects.

### Test 1. Pixel-Level Localization (Pixel AUROC)

I upsampled the anomaly maps to 256×256, applied a Gaussian blur (σ=4), and compared them pixel by pixel with the ground-truth masks.

| Metric | Value |
|---|---|
| Image AUROC | 0.9757 |
| **Pixel AUROC** | **0.9789** |

→ The model doesn't just get the decision right; **the heatmap also points at the actual defect location**. I also plotted image / GT mask / anomaly map for three defective images on the same color scale to check visually.

### Test 2. Setting the Threshold from Normal Data Only

The original Best F1 uses a threshold picked by looking at the test labels, which isn't possible in practice. So I held out 100 of the 201 normal test images as a **calibration set**, set the threshold from a percentile of their scores, and evaluated on the remaining 101 normal + 100 anomalous images.

| Threshold rule | Threshold | F1 | Missed defects | False alarms |
|---|---|---|---|---|
| (Reference) Best F1 tuned on test set | – | 0.9453 | – | – |
| **95th percentile of normal** | **26.54** | **0.8925** | **17 / 100** | **3 / 101** |
| 99th percentile of normal | 34.93 | 0.4496 | 71 / 100 | 0 / 101 |
| 100th percentile of normal (max) | 35.43 | 0.4496 | 71 / 100 | 0 / 101 |

- A threshold set from normal data alone (95th percentile) still reached **F1 0.89**, not far from the upper bound (0.945).
- Pushing the threshold to the 99th percentile or above to get zero false alarms **missed 71% of defects**. The normal score distribution has a long tail, so raising the threshold even slightly causes misses to jump.
- The 95th percentile value (26.54) is used as `THRESHOLD` in the next test.

### Test 3. Robustness to Imaging Conditions

I applied perturbations that mimic changes in imaging conditions to 50 normal images and measured the mean anomaly score and the false alarm rate (normal judged as defective).

| Perturbation | Mean score | False alarm rate |
|---|---|---|
| Original | 17.71 | 4% |
| Darker (brightness 0.7) | 17.80 | 4% |
| Brighter (brightness 1.3) | 21.10 | 8% |
| Blur (Gaussian σ=2) | 36.01 | **100%** |
| Rotate 5° | 39.63 | **100%** |
| Gaussian noise (std 15) | 28.45 | **98%** |

- **Brightness changes were handled well**, but blur, rotation and noise caused almost every normal board to be flagged as defective.
- PaDiM stores a normal distribution **per patch position**, so even a 5° rotation makes patches get compared against the wrong position's distribution and the score jumps. Blur and noise change the texture information in the pretrained features and cause the same problem.
- To use this on a real line, **a fixed, aligned and focused camera is essential**; otherwise an alignment (registration) step or training with these augmentations is needed.

---

## 🐛 Debugging and Findings

- **Mask visualization warning** — `visualize_with_mask()` raised `Clipping input data to the valid range for imshow ... Got range [0.0..255.0]`. The mask was passed as a float in 0–255; dividing by 255 to get 0–1 fixes it.
- **`tarfile.extractall` DeprecationWarning** — warns that the default filter changes in Python 3.14. Passing `filter='data'` extracts safely without the warning.
- **Duplicated data path** — the CSV `image` path already starts with the category name (`pcb4/Data/...`), so joining with `category_path / image` gave `pcb4/pcb4/...`. Fixed by checking whether the path starts with the category name.
- **OOM safeguard** — PaDiM's full training features are `[630336, 1536]`, which uses a lot of memory. `run_all_methods()` wraps each method in `try/except` so one failure doesn't stop the others.
- **`except:` → `except RuntimeError:`** — in the real-time PaDiM, a bare except that swallowed every error was narrowed to `RuntimeError`, which is what a failed matrix inverse raises.

---

## 💭 Retrospective (KPT)

### Keep

- Ran all three methods with **the same data split and the same evaluator**, so the comparison was fair.
- Went beyond comparing scores: saved the best model → reloaded it → built a Gradio demo, turning it into **something usable**.
- Looked at AUPRC, F1 and score distributions, not just AUROC, which gave a clearer picture of the differences between methods.
- The additional tests (**Pixel AUROC, a threshold from normal data only, imaging condition changes**) showed how the model would behave in practice, not just a single number.

### Problem

- Best F1 in the comparison is still based on a threshold chosen on the test set. Test 2 computed F1 with a calibration-set threshold (0.8925), but only for PaDiM, not all three methods.
- **The Gradio demo's decision threshold is hardcoded to 15.** In Test 3, normal original images averaged 17.71, so the current demo likely flags most normal boards as defective. It should use the calibrated value of 26.54.
- **Very sensitive to blur, rotation and noise** (98–100% false alarms). A small change in camera position or focus makes it unusable.
- **The PaDiM random projection has no fixed seed**, so results shift between runs. Re-running the notebook actually changed PaDiM AUROC from 0.9519 to 0.9543.
- The train/test split follows CSV order (`iloc`), not a random split.
- Only `pcb4` was tested, so I don't know whether the ranking holds for other categories (capsules, macaroni, etc.).
- The same classes (`VisADataset`, `FeatureExtractor`, `PaDiM`) are defined twice in the notebook.
- A Gradio `share=True` link lasts at most one week, so the demo can't stay public.

### Try

- Switch the demo threshold to the 95th percentile of the calibration set, and recompute F1 the same way for all three methods
- Add rotation/blur/noise augmentation in training, or an alignment step before inference, then re-run Test 3
- Fix the seed with `torch.manual_seed()` and report mean and std across several seeds
- Run the same pipeline on other VisA categories to see if the method ranking holds
- Use the already installed `anomalib` to run newer models such as **PatchCore** and compare with my own PaDiM
- Merge the duplicated classes, and move real-time inference into a separate `.py` module deployed on Hugging Face Spaces

### Action Items

| # | Action | Done when | Status |
|---|---|---|---|
| 1 | Add `torch.manual_seed(42)` and run PaDiM 3 times | AUROC mean ± std recorded in a table | |
| 2 | Split a validation set from normal data and set the threshold on it | Test F1 recomputed and compared with current value | ✅ Test 2 (F1 0.8925) |
| 3 | Normalize the mask with `/ 255.0` in `visualize_with_mask()` | Clipping warning gone | |
| 4 | Add a pixel-level AUROC function | Pixel AUROC recorded for PaDiM heatmaps | ✅ Test 1 (0.9789) |
| 5 | Repeat the experiment on the `capsules` category | Row added to the results table | |
| 6 | Replace the Gradio threshold 15 with `THRESHOLD` (26.54) | Normal sample upload returns "Normal" | |
| 7 | Apply rotation/blur/noise augmentation or an alignment step | Test 3 false alarm rate below 30% | |
