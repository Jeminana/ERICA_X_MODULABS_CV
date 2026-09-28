# YOLOv8 Object Detection Project

## 📌 프로젝트 개요 | Project Overview

이 프로젝트에서는 **YOLOv8 (Ultralytics)** 을 사용하여 사전학습 모델로 객체를 탐지하고, 직접 커스텀 데이터셋으로 모델을 학습(fine-tuning)시키는 전체 과정을 실습했습니다.

사용한 데이터셋은 Roboflow Universe의 **stamp** 데이터셋(version 10)이며, `shoes`와 `stamp` 두 개의 클래스로 구성되어 있습니다 (train 1,100장 / valid 273장 / test 193장).

기본 실습에 더해, 모델 크기와 confidence threshold가 탐지 성능에 어떤 영향을 주는지 확인하기 위한 추가 실험을 진행했습니다.

---

This project covers the full YOLOv8 workflow: running a pretrained detector, understanding its output format, and fine-tuning the model on a custom dataset.

The dataset is the **stamp** dataset (version 10) from Roboflow Universe, with two classes, `shoes` and `stamp` (1,100 train / 273 valid / 193 test images).

On top of the given practice, I ran additional experiments to see how model size and the confidence threshold affect detection performance.

- Notebook: [3_YOLOv8__프로젝트_.ipynb](3_YOLOv8__프로젝트_.ipynb)
- Dataset: [stamp/](stamp/) — https://universe.roboflow.com/warisara-kaewsuwan-cf2hs/stamp-bcrhe (CC BY 4.0)

---

## 🎯 배운 내용 | What I Learned

- **YOLOv8 추론 파이프라인**: `YOLO('yolov8n.pt')` 로드 → `model.predict()` → `Results` 객체 구조 이해
- **Bounding box 포맷**: 같은 박스를 `xyxy`, `xywh`, `xyxyn`, `xywhn` 네 가지로 표현하는 방식과, 정규화 좌표가 픽셀 좌표를 이미지 크기로 나눈 값이라는 것을 직접 계산해 확인
- **`boxes.data` 텐서 구조**: `[x1, y1, x2, y2, conf, cls]` 한 줄이 하나의 탐지 결과
- **커스텀 시각화**: Ultralytics 기본 시각화 대신 OpenCV + matplotlib으로 직접 박스와 라벨 그리기
- **클래스 필터링과 crop**: 특정 클래스만 남기거나, 탐지된 영역을 잘라 별도 이미지로 저장하여 다음 모델의 입력으로 넘기는 방법
- **커스텀 학습**: `data.yaml` 구조(train/val/test 경로, `nc`, `names`)와 `model.train()` / `model.val()` 사용법
- **평가 지표 해석**: Precision, Recall, mAP@.5, mAP@.5:.95 의 의미와 차이

---

- **The YOLOv8 inference pipeline**: loading a pretrained model, calling `predict()`, and reading the `Results` object.
- **Bounding box formats**: the same box written as `xyxy`, `xywh`, `xyxyn`, `xywhn` — I verified by hand that the normalized versions are the pixel values divided by width/height.
- **The `boxes.data` tensor**: each row is `[x1, y1, x2, y2, conf, cls]`.
- **Custom visualization** with OpenCV + matplotlib instead of the built-in plotting.
- **Class filtering and cropping**: keeping only the classes a scenario needs, and cropping detections into separate images to feed another model.
- **Custom training**: the `data.yaml` structure and the `model.train()` / `model.val()` API.
- **Reading metrics**: what Precision, Recall, mAP@.5 and mAP@.5:.95 actually tell you.

---

## 🛠️ 실습 진행 방식 | How I Tackled the Practice

1. **사전학습 모델 확인** — `yolov8n.pt`로 샘플 이미지(bus.jpg)를 추론하고, 결과 이미지와 `Results` 객체를 확인했습니다.
2. **출력 구조 분해** — `boxes.xyxy`, `boxes.xywh`와 정규화 좌표를 직접 나눠 계산해 보며 포맷 간 관계를 검증했습니다.
3. **직접 시각화** — OpenCV로 박스를 그리고, `class 0 (person)`만 필터링해 confidence와 함께 라벨을 표시했습니다.
4. **객체 crop** — COCO YAML에서 `bus` 클래스 ID를 찾아 해당 영역만 잘라 `bus_crops/`에 저장했습니다.
5. **데이터셋 다운로드** — Roboflow API로 stamp 데이터셋을 YOLOv8 포맷으로 내려받았습니다. **API 키는 노트북에 하드코딩하지 않고 Colab Secrets(`userdata.get`)로 처리**했습니다.
6. **학습 및 평가** — `yolov8n.pt`를 20 epochs, imgsz 640, batch 16으로 학습한 뒤 `model.val()`로 평가했습니다.
7. **테스트 이미지 추론** — 학습된 모델로 test 이미지를 예측하고 결과를 저장·시각화했습니다.

### 기본 학습 결과 | Baseline training result (yolov8n, 20 epochs)

| Class | Images | Instances | Precision | Recall | mAP@.5 | mAP@.5:.95 |
|-------|--------|-----------|-----------|--------|--------|------------|
| all   | 273    | 952       | 0.979     | 0.903  | 0.982  | 0.656      |
| shoes | 204    | 408       | 0.962     | 0.815  | 0.968  | 0.719      |
| stamp | 273    | 544       | 0.996     | 0.991  | 0.995  | 0.592      |

`stamp` 클래스는 모양이 일정해 거의 완벽하게 탐지된 반면, `shoes`는 Recall이 0.815로 낮아 놓치는 객체가 더 많았습니다. 다만 mAP@.5:.95는 `shoes`가 더 높은데, 이는 탐지에 성공한 박스의 위치 정밀도는 `shoes` 쪽이 더 정확했다는 뜻입니다.

The `stamp` class is nearly perfectly detected — it has a consistent shape. `shoes` has lower recall (0.815), so more objects are missed, but its mAP@.5:.95 is *higher*, meaning the boxes it does find are localized more precisely.

---

## 🧪 추가 실험 | Additional Experiments

기본 실습 이후, 직접 세 가지 질문을 세우고 실험했습니다. 학습 결과가 Colab 세션 종료로 사라지지 않도록 **Google Drive에 저장**하도록 구성했습니다.

### A. 모델 크기 비교 | Model Size Comparison

`yolov8n`, `yolov8s`, `yolov8m`을 동일 조건(20 epochs, imgsz 640, batch 16)으로 각각 학습하고, 파라미터 수·학습 시간·추론 속도·정확도를 비교했습니다.

| model | params (M) | file (MB) | train time (min) | inference (ms/img) | mAP50 | mAP50-95 | precision | recall |
|-------|-----------|-----------|------------------|--------------------|-------|----------|-----------|--------|
| yolov8n | 3.011 | 6.247 | 7.418 | 4.575 | 0.984 | 0.631 | 0.951 | 0.947 |
| yolov8s | 11.136 | 22.517 | 8.507 | 9.293 | 0.984 | 0.634 | 0.965 | 0.913 |
| yolov8m | 25.857 | 52.029 | 12.647 | 20.886 | 0.980 | 0.631 | 0.953 | 0.914 |

**결과:** 모델을 키워도 정확도는 거의 오르지 않았습니다 (mAP50-95 기준 0.631 → 0.634 → 0.631). 반면 파라미터는 8.6배, 추론 시간은 4.6배 늘어났습니다. 클래스가 2개뿐이고 객체 모양이 단순한 데이터셋에서는 **가장 작은 `yolov8n`이 가장 합리적인 선택**이라는 결론을 얻었습니다.

**Result:** Scaling the model up bought essentially no accuracy (mAP50-95: 0.631 → 0.634 → 0.631) while costing 8.6× the parameters and 4.6× the inference time. For a 2-class dataset with simple object shapes, the smallest model is the right choice.

### B. Confidence Threshold 실험 | Confidence Threshold Sweep

`yolov8n` best weight로 test set 전체를 `conf=0.01`로 한 번만 추론해 두고, threshold를 바꿔가며 **TP / FP / FN을 직접 계산**했습니다. IoU 매칭(`iou_thr=0.5`)과 Precision/Recall/F1 계산 함수를 직접 구현해, 지표가 어떤 값에서 나오는지 확인했습니다.

| conf | TP | FP (false alarms) | FN (missed) | precision | recall | F1 |
|------|----|-------------------|-------------|-----------|--------|-----|
| 0.05 | 616 | 37 | 17  | 0.943 | 0.973 | 0.958 |
| 0.10 | 608 | 30 | 25  | 0.953 | 0.961 | 0.957 |
| 0.25 | 598 | 20 | 35  | 0.968 | 0.945 | 0.956 |
| 0.50 | 593 | 13 | 40  | 0.979 | 0.937 | 0.957 |
| 0.70 | 581 | 5  | 52  | 0.991 | 0.918 | 0.953 |
| 0.90 | 153 | 1  | 480 | 0.994 | 0.242 | 0.389 |

**결과:** threshold를 올릴수록 precision은 오르고 recall은 떨어지는 전형적인 trade-off가 나타났습니다. 흥미로운 점은 **0.05 ~ 0.70 구간에서 F1이 0.953~0.958로 거의 평평하다**는 것입니다. 즉 이 범위 안에서는 threshold를 어디에 두든 전체 성능은 비슷하고, **"놓치는 것을 줄일지(낮은 threshold) / 오탐을 줄일지(높은 threshold)"를 목적에 따라 고르는 문제**였습니다. 반면 0.9에서는 recall이 0.242로 급락하며 F1이 무너졌습니다.

**Result:** The expected precision/recall trade-off shows up, but F1 stays almost flat (0.953–0.958) across 0.05–0.70. Within that range the threshold is a product decision — fewer misses vs. fewer false alarms — not an accuracy decision. At 0.9 the model collapses (recall 0.242).

### C. Valid vs Test 비교 | Valid vs Test (미완료 / not completed)

세 번째로 valid set과 test set의 점수를 비교해 과적합 여부를 확인하려 했으나, 이 실험은 노트북에서 실행하지 못했습니다. 다만 B 실험의 test set 기준 precision/recall이 valid 점수와 비슷한 수준으로 나온 것으로 보아, 심한 과적합은 없는 것으로 보입니다.

I planned to compare valid vs. test scores to check for overfitting, but did not get to run it. The test-set precision/recall from experiment B land in the same range as the validation scores, which suggests no severe overfitting.

---

## 💭 회고 | Retrospective

**배운 점**

- 모델을 더 크게 만드는 것이 항상 답은 아니라는 것을 숫자로 확인했습니다. 데이터셋 난이도에 비해 모델이 이미 충분하면, 크기를 키우는 비용은 그대로 손해입니다.
- TP/FP/FN을 직접 구현해 보면서 precision, recall, F1이 실제로 어떤 계산에서 나오는지 체감할 수 있었습니다. 라이브러리가 계산해 주는 mAP만 볼 때와는 이해의 깊이가 달랐습니다.
- confidence threshold는 "정답이 하나 있는 하이퍼파라미터"가 아니라 **사용 목적에 따라 정하는 값**이라는 것을 알게 되었습니다.

**아쉬운 점**

- 실험 C(valid vs test 비교)를 끝내지 못했습니다.
- 모든 실험을 20 epochs로 고정했는데, 더 큰 모델은 더 오래 학습해야 성능이 나올 수도 있어 비교가 완전히 공정하다고 보기는 어렵습니다.
- `shoes` 클래스의 recall이 낮은 원인(가려짐? 크기? 라벨 품질?)을 실제 실패 이미지로 분석해 보지 못했습니다.

**다음에 해보고 싶은 것**

- 실패 케이스(FN) 이미지를 직접 확인해 `shoes` recall이 낮은 이유 분석
- epochs, augmentation, imgsz를 바꿔가며 학습 조건 실험
- IoU threshold를 바꿔가며 mAP@.5와 mAP@.5:.95의 차이를 더 깊이 확인

---

**What I learned:** a bigger model is not automatically a better one — and I have the numbers to show it. Implementing TP/FP/FN matching by hand made the metrics concrete in a way that reading mAP off a library never did. The confidence threshold turned out to be a decision about which kind of error you prefer, not a value with one correct answer.

**What I'd improve:** I didn't finish experiment C; I kept epochs fixed at 20 for every model size, which may under-train the larger models; and I never looked at the actual failure images behind the low `shoes` recall.

---

## 📁 폴더 구조 | Repository Layout

```
04_YOLOv8/
├── 3_YOLOv8__프로젝트_.ipynb   # 전체 실습 + 추가 실험
├── stamp/                      # Roboflow stamp dataset (v10)
│   ├── data.yaml               # nc: 2, names: ['shoes', 'stamp']
│   ├── train/ valid/ test/
│   └── README.dataset.txt / README.roboflow.txt
└── README.md
```

> `runs/`, `*.pt`, `bus_crops/`, 예측 결과 이미지는 [.gitignore](.gitignore)로 제외되어 있습니다.
> Roboflow API 키는 Colab Secrets로 관리하며 노트북에 저장되지 않습니다.

