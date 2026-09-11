\# 🚗 VLM Driving Decision Project



\*\*코더 (Coder):\*\* VLM  

\*\*리뷰어 (Reviewer):\*\* 나즈미



\---



\## 1. 📌 프로젝트 개요 | Project Overview



본 프로젝트에서는 이미지에서 주변의 주행 상황을 분석하여 차량이 \*\*Go 또는 Stop\*\*을 결정할 수 있도록 Vision-Language Model(VLM)을 적용하였습니다.



모델은 이미지를 관찰하고, 해당 상황에서 발생할 수 있는 충돌 위험을 바탕으로 객관식 질문에 답하도록 구성하였습니다.



> This project applies a Vision-Language Model (VLM) to analyze driving scenes and determine whether a vehicle should \*\*Go or Stop\*\*.

>

> The model observes each image and answers a multiple-choice question based on the possible collision risk in the scene.



\---



\## 2. 🤖 모델 및 방법 | Model \& Method



본 프로젝트에서는 기본 VLM 모델로 \*\*Gemma\*\*를 사용하였습니다.



VLM에는 다음과 같은 입력이 주어집니다.



\- 🖼️ \*\*10장\*\*의 주행 상황 이미지

\- 💬 의사결정 과정을 설명하는 Prompt

\- 🔤 \*\*4개의 선택지\*\*

&#x20; - Go

&#x20; - Stop

&#x20; - Cannot be determined

&#x20; - None of the above



> \*\*Gemma\*\* was used as the primary VLM for this project.

>

> The model receives 10 driving-scene images, a prompt explaining the decision-making criteria, and four possible choices.



\---



\## 3. 📊 실험 결과 | Results



\### Gemma



| Model | Accuracy | Correct | Total |

|:---:|:---:|:---:|:---:|

| \*\*Gemma\*\* | \*\*80%\*\* | \*\*8\*\* | \*\*10\*\* |



자세한 예측 결과와 reasoning은 프로젝트 notebook에 기록하였습니다.



> The Gemma model achieved \*\*80% accuracy (8/10)\*\*.  

> Detailed predictions and reasoning are available in the project notebook.



\---



\## 4. 🧪 추가 실험 | Additional Experiments



\### 4.1 Prompt 수정



모델이 상황을 더 구체적으로 이해할 수 있도록 안전, 충돌 위험, 불확실한 상황에 대한 설명을 추가하여 Prompt를 수정하였습니다.



수정 후에도 정확도는 \*\*80%\*\*로 유지되었습니다.



> The prompt was modified by adding more detailed instructions about safety, collision risks, and uncertain situations.

>

> The modified prompt maintained an accuracy of \*\*80%\*\*.



\### 4.2 다른 VLM 적용 — Qwen3-VL



동일한 Prompt를 사용하여 \*\*Qwen3-VL\*\* 모델도 테스트하였습니다.



| Model | Accuracy | Correct | Total |

|:---:|:---:|:---:|:---:|

| \*\*Gemma\*\* | \*\*80%\*\* | \*\*8\*\* | \*\*10\*\* |

| \*\*Qwen3-VL\*\* | \*\*70%\*\* | \*\*7\*\* | \*\*10\*\* |



동일한 이미지와 Prompt를 사용하더라도 VLM에 따라 결과가 달라질 수 있음을 확인하였습니다.



> Qwen3-VL was tested using the same prompt and achieved \*\*70% accuracy (7/10)\*\*.

>

> This experiment showed that different VLMs can produce different decisions even when given the same images and prompt.



\---



\## 5. ⚠️ 한계점 및 개선 방향 | Limitations \& Improvements



\### Package 호환성



실험 과정에서 package 간의 호환성 문제가 발생하였습니다.  

호환 가능한 안정적인 버전의 package를 설치하여 문제를 해결하였습니다.



> A package compatibility issue occurred during the experiment.  

> The problem was resolved by installing a compatible and stable package version.



\### GPU Runtime



제한된 GPU runtime으로 인해 주어진 시간 내에 더 많은 실험을 진행하지 못했습니다.



향후에는:



\- 다양한 Prompt를 추가로 테스트

\- 다른 VLM 모델 비교

\- 다양한 객관식 질문 및 선택지 실험

\- Stop 상황에서 발생하는 오류 분석



등을 진행하여 성능을 개선해 보고 싶습니다.



> Due to the limited GPU runtime, I could not conduct more experiments within the given time.

>

> In future experiments, I would like to test different prompt strategies, compare additional VLMs, and explore different multiple-choice questions that provide more possible actions when the vehicle encounters obstacles.



\---



\## 🔄 Project Flow



```text

Driving Image

&#x20;     ↓

Prompt + Multiple Choices

&#x20;     ↓

Vision-Language Model

&#x20;     ↓

Image \& Prompt Analysis

&#x20;     ↓

Go / Stop Decision

&#x20;     ↓

Compare with Ground Truth

&#x20;     ↓

Calculate Accuracy

