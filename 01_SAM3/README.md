# SAM3 Object Detection Project

## 📌 프로젝트 개요 | Project Overview

이 프로젝트에서는 **SAM3 (Segment Anything Model 3)**를 직접 구현하고, 텍스트 프롬프트를 사용하여 모델이 객체를 탐지하고 분할하는 방법을 학습했습니다.

기본적인 SAM3 구현뿐만 아니라, 다양한 이미지, 객체 프롬프트, confidence threshold에 따라 SAM3의 탐지 결과가 어떻게 달라지는지 확인하기 위해 추가 실험을 진행했습니다.

---

This project focuses on learning how to implement **SAM3 (Segment Anything Model 3)** and understanding how the model detects and segments objects using text prompts.

In addition to the basic implementation, I conducted several experiments to better understand how SAM3 behaves with different images, object prompts, and confidence thresholds.

---

## 🧪 실험 | Experiments

### 1. 다양한 차량 종류 객체 탐지 | Object Detection with Different Vehicle Types

SAM3가 서로 다른 종류의 차량을 어떻게 탐지하는지 확인하기 위해 여러 종류의 차량이 포함된 이미지를 사용하여 테스트했습니다.

또한 특정 차량 종류를 탐지할 수 있는지 확인하기 위해 `"vehicle"`과 `"car"` 프롬프트를 사용하여 결과를 비교했습니다.

**결과:**

- `"vehicle"` → 45개 객체 탐지
- `"car"` → 13개 객체 탐지

실험을 통해 SAM3가 크기가 서로 다른 자동차뿐만 아니라 일부가 가려진 자동차도 식별할 수 있음을 확인했습니다.

---

I tested SAM3 using an image containing several types of vehicles.

The purpose was to observe how SAM3 detects a general category such as `"vehicle"` and whether it can also detect a more specific category such as `"car"`.

**Results:**

- `"vehicle"` → 45 objects detected
- `"car"` → 13 objects detected

The experiment showed that SAM3 was able to identify cars of different sizes, including some vehicles that were partially hidden.

---

### 2. Confidence Threshold 테스트 | Confidence Threshold Test

두 번째 실험에서는 **confidence threshold가 객체 탐지 결과에 어떤 영향을 미치는지** 확인했습니다.

Threshold를 **0.7에서 0.3으로 낮추었을 때 `"car"`로 탐지된 객체의 수가 증가하는 것**을 확인할 수 있었습니다.

**결과:**

- Threshold `0.7` → 9개 객체 탐지
- Threshold `0.3` → 24개 객체 탐지

Threshold가 `0.7`일 때는 `0.918`, `0.953`, `0.961`과 같이 대부분 높은 confidence score를 가진 객체들이 탐지되었습니다.

반면 threshold를 `0.3`으로 낮추었을 때는 더 많은 객체가 탐지되었지만, `0.30~0.50` 정도의 낮은 confidence score를 가진 객체들도 포함되었습니다.

이를 통해 **confidence threshold를 낮추면 더 많은 객체를 탐지할 수 있지만, 신뢰도가 낮은 탐지 결과도 증가할 수 있다는 것**을 확인했습니다.

---

I tested how the **confidence threshold** affects object detection.

When the threshold was decreased from `0.7` to `0.3`, the number of objects detected as `"car"` increased.

**Results:**

- Threshold `0.7` → 9 objects detected
- Threshold `0.3` → 24 objects detected

At a threshold of `0.7`, most detected objects had high confidence scores, such as `0.918`, `0.953`, and `0.961`.

At a lower threshold of `0.3`, more objects were detected, including detections with lower confidence scores around `0.30–0.50`.

This experiment showed that **lowering the confidence threshold can increase the number of detected objects, but it can also include detections with lower confidence.**

---

## 💡 배운 점 | What I Learned

이 프로젝트를 통해 다음과 같은 내용을 학습했습니다.

- SAM3를 설정하고 구현하는 방법
- SAM3가 텍스트 프롬프트를 사용하여 객체를 탐지하고 분할하는 방법
- SAM3를 새로운 이미지에 적용하는 방법
- 서로 다른 프롬프트가 객체 탐지 결과에 미치는 영향
- Confidence threshold가 객체 탐지 결과에 미치는 영향

---

Through this project, I learned:

- How to set up and implement SAM3
- How SAM3 uses text prompts to detect and segment objects
- How to apply SAM3 to different images
- How different prompts can affect detection results
- How the confidence threshold affects object detection

---

## ⚠️ 어려웠던 점 | Challenges

이 프로젝트를 진행하면서 가장 어려웠던 점 중 하나는 **SAM3 구현 과정에서 사용되는 일부 코드를 이해하는 것**이었습니다.

또한 기존 예제뿐만 아니라 **다른 이미지나 새로운 상황에 SAM3를 어떻게 적용해야 하는지** 이해하는 과정에서도 어려움이 있었습니다.

하지만 다양한 이미지, 프롬프트, confidence threshold를 직접 변경하고 테스트하면서 SAM3의 동작 방식을 더 잘 이해할 수 있었습니다.

---

One of the main challenges during this project was understanding some parts of the SAM3 implementation and code.

I also had difficulty at first understanding how to apply the model to different images and how to design additional test scenarios beyond the original example.

By experimenting with different images, prompts, and confidence thresholds, I was able to understand the model better.

---

## 🚀 향후 계획 | Future Work

앞으로 SAM3를 활용하여 더 다양한 실험을 진행해 보고 싶습니다.

- 일부가 가려진 객체에 대한 탐지 성능 테스트
- 더 복잡하고 어려운 이미지에서의 테스트
- 모델의 탐지 성능을 개선할 수 있는 방법 탐색
- 다양한 텍스트 프롬프트와 confidence threshold 실험
- 다양한 제품 및 분야에서 SAM3를 활용할 수 있는 방법 탐색

향후에는 SAM3가 **컴퓨터 비전 시스템, 자율주행 및 자율 시스템, 로봇, 교통 분석 등 다양한 분야에서 어떻게 활용될 수 있는지** 알아보고 싶습니다.

---

In the future, I would like to conduct more experiments with SAM3, such as:

- Testing objects that are partially hidden or occluded
- Testing more difficult and complex images
- Exploring ways to improve the model's detection performance
- Experimenting with different text prompts and confidence thresholds
- Investigating how SAM3 can be applied to different products and fields

I would also like to explore how SAM3 can be applied to areas such as **computer vision systems, autonomous systems, robotics, traffic analysis, and other real-world applications.**

---

## 📚 결론 | Conclusion

이번 프로젝트를 통해 SAM3를 직접 구현하고 테스트하면서 **객체 탐지와 분할이 어떻게 이루어지는지 실습을 통해 이해할 수 있었습니다.**

또한 추가 실험을 통해 이미지, 텍스트 프롬프트, confidence threshold와 같은 요소를 변경하면 객체 탐지 결과에도 영향을 줄 수 있다는 것을 확인했습니다.

---

Through this project, I gained practical experience implementing and testing SAM3 and developed a better understanding of how object detection and segmentation work.

The additional experiments also showed that changing factors such as the input image, text prompt, and confidence threshold can affect the object detection results.

&#x20;   # 리뷰어의 회고를 작성합니다.

&#x20;   # 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.

&#x20;   # 코드 리뷰를 통해 개선한 코드가 있다면 코드와 간략한 설명을 첨부합니다.

