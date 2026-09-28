# EfficientDet Object Detection Project

## 📌 프로젝트 개요 | Project Overview

이 프로젝트에서는 **EfficientDet-D0** ([zylo117/Yet-Another-EfficientDet-Pytorch](https://github.com/zylo117/Yet-Another-EfficientDet-Pytorch)) 를 사용하여 사전학습 모델로 이미지·영상을 추론하고, 직접 커스텀 데이터셋으로 모델을 학습(fine-tuning)시키는 전체 과정을 실습했습니다.

사용한 데이터셋은 Kaggle의 **Vehicle Detection Image Dataset** (`Vehicles_Detection.v8i.coco`) 이며, `Bus`, `Car`, `Motorcycle`, `Pickup`, `Truck` 다섯 개 클래스로 구성되어 있습니다. train 이미지는 **102장**뿐인 매우 작은 데이터셋입니다 (640×640, COCO 포맷, annotation 2,069개).

학습은 한 번에 끝내지 않고 **학습 범위 · learning rate · epoch을 바꿔가며 4단계로 나누어** 진행했고, 각 단계가 성능에 어떤 영향을 주는지 비교했습니다.

---

This project covers the full EfficientDet workflow: running the pretrained D0 model on images and video, dissecting its output, and fine-tuning it on a custom dataset.

The dataset is Kaggle's **Vehicle Detection Image Dataset** (`Vehicles_Detection.v8i.coco`) with five classes — `Bus`, `Car`, `Motorcycle`, `Pickup`, `Truck`. It is very small: only **102 training images** (640×640, COCO format, 2,069 annotations).

Rather than training once, I split training into **four stages that vary the trainable part, the learning rate and the epoch budget**, and compared what each change bought.

- Notebook: [4_EfficientDet_[프로젝트]_정정채.ipynb](4_EfficientDet_[프로젝트]_정정채.ipynb)
- Dataset: https://www.kaggle.com/datasets/pkdarabi/vehicle-detection-image-dataset
- Base repo: https://github.com/zylo117/Yet-Another-EfficientDet-Pytorch

---

## 🎯 배운 내용 | What I Learned

- **EfficientDet 추론 파이프라인**: `preprocess()` → `EfficientDetBackbone` → `postprocess()` → `invert_affine()` 의 전체 흐름. 특히 `invert_affine`이 letterbox 패딩된 좌표를 원본 이미지 좌표로 되돌리는 역할이라는 것
- **모델 출력의 구조**: `features`(5개 레벨의 BiFPN 특징 맵), `regression`, `classification`, `anchors` 네 가지가 따로 나오고, 실제 박스는 `BBoxTransform`(regression → 좌표)과 `ClipBoxes`(이미지 밖 clip)를 거쳐야 나온다는 것
- **Compound scaling**: `compound_coef`가 입력 해상도(`input_sizes`)와 backbone 크기를 동시에 결정하는 방식
- **COCO 포맷 데이터셋 준비**: Roboflow가 내보낸 구조를 이 repo가 요구하는 `datasets/<proj>/{train,valid,test}` + `annotations/instances_*.json` 구조로 변환
- **Anchor 설계**: 데이터셋의 bbox 통계(크기·비율)를 직접 계산해 anchor scale/ratio를 정하는 방법
- **단계적 fine-tuning**: head만 먼저 학습(`--head_only True`)해 워밍업한 뒤 backbone을 푸는 전략
- **COCO 평가 지표**: mAP@[.5:.95], AP@.5, small/medium/large 별 AP를 나누어 읽는 법

---

- **The EfficientDet inference pipeline**: `preprocess()` → backbone → `postprocess()` → `invert_affine()`, and specifically that `invert_affine` maps letterboxed coordinates back onto the original image.
- **The model's raw outputs**: `features` (five BiFPN levels), `regression`, `classification` and `anchors` come out separately — real boxes only appear after `BBoxTransform` and `ClipBoxes`.
- **Compound scaling**: how `compound_coef` sets both the input resolution and the backbone size at once.
- **Preparing a COCO dataset**: converting the Roboflow export into the `datasets/<proj>/{train,valid,test}` + `annotations/instances_*.json` layout this repo expects.
- **Anchor design**: computing bbox size/ratio statistics from the dataset to choose anchor scales and ratios.
- **Staged fine-tuning**: warming up the head alone (`--head_only True`) before unfreezing the backbone.
- **COCO metrics**: reading mAP@[.5:.95], AP@.5 and the small/medium/large breakdown separately.

---

## 🛠️ 실습 진행 방식 | How I Tackled the Practice

1. **사전학습 모델 추론** — `efficientdet-d0.pth`(COCO 90 classes)로 샘플 이미지를 추론하고, `features`/`regression`/`classification`/`anchors`의 shape을 하나씩 확인했습니다.
2. **후처리 분해** — `postprocess()`를 직접 호출해 `rois`, `class_ids`, `scores`가 나오는 과정을 확인하고 OpenCV로 시각화했습니다.
3. **영상 추론** — `soccer.mp4`를 프레임 단위로 추론해 결과 프레임을 저장하고, 다시 mp4로 합쳤습니다.
4. **데이터셋 준비** — Kaggle API로 다운로드 후, repo가 요구하는 폴더/annotation 구조로 변환했습니다. (**API 키는 노트북에 하드코딩하지 않고 `getpass`로 입력받도록** 처리했습니다.)
5. **데이터셋 통계 계산** — train 이미지의 RGB mean/std와 bbox 크기·비율 분포를 직접 계산해 `projects/my_car_detect_proj.yml`을 작성했습니다.
6. **4단계 학습** — 학습 범위 → learning rate → epoch 순서로 조건을 바꿔가며 학습했습니다 (아래).
7. **평가 및 추론** — `coco_eval.py`로 test set을 평가하고, 학습된 weight로 직접 추론해 결과를 시각화했습니다.

### 데이터셋 통계로 정한 설정 | Config derived from dataset statistics

```yaml
mean: [0.4639, 0.4724, 0.4700]     # train 102장에서 직접 계산 | computed over the 102 train images
std:  [0.1653, 0.1642, 0.1631]
anchors_scales: '[0.25, 0.5, 1.0]'
anchors_ratios: '[(0.7, 1.4), (1.0, 1.0), (1.4, 0.7)]'
obj_list: ['Bus', 'Car', 'Motorcycle', 'Pickup', 'Truck']
```

bbox 통계상 객체 중앙값 크기가 **17.7px**(640×640 기준)로 매우 작아, COCO 기본 anchor scale(`2^0, 2^(1/3), 2^(2/3)`)보다 **작은 쪽으로 내린 `[0.25, 0.5, 1.0]`** 을 사용했습니다.

The median object is only **17.7 px** on a 640×640 image, so I used anchor scales shifted *down* from the COCO defaults.

---

## 🧪 학습 조건별 실험 | Training Runs by Setting

네 번의 학습은 모두 직전 단계의 마지막 체크포인트를 이어받습니다. 이 repo에서 `--num_epochs`는 "이번 run의 epoch 수"가 아니라 **누적 목표 epoch**입니다.

All four runs resume from the previous stage's last checkpoint. In this repo `--num_epochs` is the **cumulative target epoch**, not the number of epochs for that run.

| 단계 / Stage | 학습 범위 / Trainable | lr | batch | epoch (누적) | 최종 val total loss | test mAP@[.5:.95] |
|---|---|---|---|---|---|---|
| 1 | head만 / head only | 1e-3 | 16 | 0 → 10 | 35.938 | – |
| 2 | 전체 / full model | 1e-3 | 16 | 10 → 30 | 1.889 | 0.104 |
| 3 | 전체 / full model | 1e-4 | 16 | 30 → 40 | 1.674 | – |
| 4 | 전체 / full model | 1e-4 | 16 | 40 → 80 | **1.566** | **0.280** |

```bash
# 1단계 | Stage 1 — head only warm-up
python train.py -c 0 -p my_car_detect_proj --head_only True  --lr 1e-3 --batch_size 16 \
    --load_weights weights/efficientdet-d0.pth --num_epochs 10

# 2단계 | Stage 2 — unfreeze backbone
python train.py -c 0 -p my_car_detect_proj --head_only False --lr 1e-3 --batch_size 16 \
    --load_weights logs/my_car_detect_proj/efficientdet-d0_9_80.pth --num_epochs 30

# 3단계 | Stage 3 — lower the lr
python train.py -c 0 -p my_car_detect_proj --head_only False --lr 1e-4 --batch_size 16 \
    --load_weights "{weight_path}" --num_epochs 40

# 4단계 | Stage 4 — train longer at the same lr
python train.py -c 0 -p my_car_detect_proj --head_only False --lr 1e-4 --batch_size 16 \
    --load_weights "{weight_path}" --num_epochs 80
```

### 단계별로 무엇이 달라졌나 | What each stage changed

- **1단계 (head only):** head가 COCO 90-class → 5-class로 새로 초기화되므로 classification loss가 39까지 치솟습니다. backbone을 고정한 채 head만 안정화시키는 워밍업 구간이었습니다.
- **2단계 (backbone 해제):** 가장 큰 변화. val total loss가 **35.94 → 1.89** 로 급감했습니다. 사전학습 backbone이 차량 도메인에 맞춰지면서 대부분의 학습이 여기서 일어났습니다.
- **3단계 (lr 1/10):** loss가 정체되어 lr을 1e-3 → 1e-4로 낮췄습니다. loss는 1.89 → 1.67로 내려갔지만 개선 폭은 작았습니다.
- **4단계 (epoch 연장):** lr은 3단계와 **동일**하고 epoch만 40 → 80으로 늘렸습니다. loss는 1.67 → 1.57로 소폭 내려갔지만, **mAP는 0.104 → 0.280으로 2.7배** 올랐습니다.

### 평가 결과 비교 | COCO eval: stage 2 vs. stage 4

| Metric (test set) | 2단계 / Stage 2 | 4단계 / Stage 4 |
|---|---|---|
| **AP @[.5:.95] \| all** | 0.104 | **0.280** |
| AP @.5 \| all | 0.183 | 0.464 |
| AP @.75 \| all | 0.091 | 0.285 |
| AP \| small | 0.045 | 0.196 |
| AP \| medium | 0.218 | 0.438 |
| AP \| large | 0.361 | 0.464 |
| AR @[.5:.95] \| all, maxDets=100 | 0.340 | 0.403 |

**결과:** val loss만 보면 3→4단계 개선은 1.67 → 1.57로 미미해 보이지만, 실제 검출 성능(mAP)은 이 구간에서 가장 크게 올랐습니다. **loss 곡선이 평평해 보여도 학습을 더 돌릴 가치가 있었다**는 것이 이번 실험에서 가장 인상적인 부분이었습니다. small object AP도 0.045 → 0.196으로 올랐지만, 여전히 medium/large의 절반 이하입니다.

**Result:** judged by validation loss, stage 4 looks like a marginal gain (1.67 → 1.57) — but detection quality improved most in exactly that window. A flat-looking loss curve was still worth training through. Small-object AP rose from 0.045 to 0.196, yet remains under half the medium/large numbers.

---

## 🐛 디버깅 기록 | Debugging Notes

- **`ReduceLROnPlateau(..., verbose=True)` 에러** — 최신 PyTorch에서 `verbose` 인자가 제거되어 `train.py`가 실행되지 않았습니다. `sed`로 해당 인자를 제거해 해결했습니다.
- **`size mismatch` 경고** — 사전학습 weight는 90-class head(810 채널), 우리 모델은 5-class head(45 채널)이라 head만 로드에 실패합니다. 이는 의도된 동작이며 나머지 backbone/BiFPN 가중치는 정상적으로 로드됩니다.
- **category_id 오프셋** — COCO json의 `categories`에는 supercategory인 `cars`가 id 0으로 들어 있어 `obj_list`가 6개(`['cars', 'Bus', 'Car', 'Motorcycle', 'Pickup', 'Truck']`)로 나옵니다. 실제 학습에는 `cars`를 제외한 **5개 클래스**를 사용했습니다.
- **추론 시 중복 박스** — 같은 차량에 박스가 겹쳐 그려져 `iou_threshold`를 0.2 → **0.1** 로 낮춰 NMS를 강하게 적용했습니다.
- **추론 모델 생성 시 anchor 설정** — 학습에 쓴 `ratios`/`scales`를 `EfficientDetBackbone`에 그대로 넘기지 않으면 체크포인트가 맞지 않습니다.

---

## 💭 회고 | Retrospective

**배운 점**

- **어느 단계에서 성능이 오르는지는 loss만 봐서는 알 수 없다.** 2단계에서 loss가 극적으로 떨어졌지만 mAP는 0.104에 불과했고, loss가 거의 평평했던 4단계에서 mAP가 2.7배 올랐습니다. loss와 최종 지표는 같은 것을 측정하지 않는다는 걸 체감했습니다.
- head만 먼저 학습시키는 워밍업이 왜 필요한지 숫자로 확인했습니다. 새로 초기화된 head에서 나오는 거대한 gradient가 backbone을 망가뜨리지 않도록 막아주는 단계였습니다.
- anchor를 데이터셋 통계로부터 직접 설계해 보면서, anchor가 "기본값을 쓰는 설정"이 아니라 **데이터의 객체 크기 분포에 맞춰야 하는 설계 요소**라는 것을 알게 되었습니다.

**아쉬운 점**

- **train 이미지가 102장뿐**이라 최종 mAP 0.280은 낮습니다. 데이터 양이 병목인지 학습 조건이 병목인지 구분하지 못했습니다.
- bbox 통계가 추천한 anchor(`scales [0.54, 1.0, 2.13]`, `ratios [(0.52,1.0), (0.67,1.0), (0.82,1.0)]`)와 실제로 쓴 값(`[0.25, 0.5, 1.0]`, `[(0.7,1.4), (1.0,1.0), (1.4,0.7)]`)이 다른데, 두 설정을 A/B로 비교해 보지 못했습니다.
- 3단계와 4단계를 lr·epoch 두 변수를 동시에 놓고 본 셈이라, "lr 감소"의 효과만 분리해 측정하지는 못했습니다.
- small object AP가 낮은 원인을 실패 이미지로 직접 확인하지 못했습니다.

**다음에 해보고 싶은 것**

- 통계 기반 anchor vs. 직접 정한 anchor를 같은 조건에서 비교
- `compound_coef`를 0 → 1, 2로 올려 입력 해상도(512 → 640 → 768)가 small object AP에 주는 영향 확인
- 데이터 augmentation 또는 v8/v9 데이터셋 병합으로 학습 데이터를 늘려 보기
- 같은 데이터셋에서 [YOLOv8 프로젝트](../04_YOLOv8/README.md) 결과와 정면 비교

---

**What I learned:** the loss curve and the final metric do not measure the same thing — loss collapsed in stage 2 while mAP was still only 0.104, and mAP tripled in stage 4 where loss barely moved. Warming up the head first turned out to be measurably necessary, and anchors are a design choice that should follow your data's object-size distribution, not a default to inherit.

**What I'd improve:** with only 102 training images, a final mAP of 0.280 is low, and I never separated "not enough data" from "not enough training". I also changed lr and epochs in overlapping steps, so I cannot attribute the gain to either one alone, and I never A/B tested the statistics-derived anchors against the ones I actually used.

---

## 📁 폴더 구조 | Repository Layout

```
05_EfficientDet/
├── 4_EfficientDet_[프로젝트]_정정채.ipynb   # 전체 실습 + 4단계 학습
└── README.md
```

노트북 실행 시 Colab 안에서 만들어지는 구조 | Structure created inside Colab at runtime:

```
Yet-Another-EfficientDet-Pytorch/
├── projects/my_car_detect_proj.yml         # mean/std/anchor/obj_list
├── weights/efficientdet-d0.pth             # COCO 사전학습 weight
├── datasets/my_car_detect_proj/
│   ├── annotations/instances_{train,valid,test}.json
│   └── train/ valid/ test/                 # *.jpg
└── logs/my_car_detect_proj/                # 학습 체크포인트 + tensorboard
```

> 데이터셋·가중치·체크포인트는 용량 문제로 저장소에 포함하지 않았습니다. 노트북을 위에서부터 실행하면 재생성됩니다.
> Kaggle API 키는 `getpass`로 입력받으며 노트북에 저장되지 않습니다.

---

## 📋 Peer Review Template

- 코더 : 정정채
- 리뷰어 :

### PRT(Peer Review Template)

- [ ] **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 문제에서 요구하는 최종 결과물이 첨부되었는지 확인
- [ ] **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 해당 코드 블럭을 왜 핵심적이라고 생각하는지 확인
    - 해당 코드 블럭에 doc string/annotation이 달려 있는지 확인
    - 해당 코드의 기능, 존재 이유, 작동 원리 등을 기술했는지 확인
- [ ] **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나 새로운 시도 또는 추가 실험을 수행해보았나요?**
    - 문제 원인 및 해결 과정을 잘 기록하였는지 확인
    - 프로젝트 평가 기준에 더해 추가적으로 수행한 나만의 시도, 실험이 기록되어 있는지 확인
- [ ] **4. 회고를 잘 작성했나요?**
    - 배운점과 아쉬운점, 느낀점 등이 기록되어 있는지 확인
    - 전체 코드 실행 플로우를 그래프로 그려서 이해를 돕고 있는지 확인
- [ ] **5. 코드가 간결하고 효율적인가요?**
    - 파이썬 스타일 가이드 (PEP8) 를 준수하였는지 확인
    - 코드 중복을 최소화하고 범용적으로 사용할 수 있도록 함수화/모듈화했는지 확인

### 리뷰어 회고 (참고 링크 및 코드 개선 제안)

<!-- 리뷰어의 회고를 작성합니다. -->
