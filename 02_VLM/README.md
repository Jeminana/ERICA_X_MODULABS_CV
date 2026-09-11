\- 코더 : VLM

\- 리뷰어 : 나즈미





\# PRT(Peer Review Template)

\- \[ ] \*\*1. 프로젝트 개요\*\*

&#x20;   - 본 프로젝트에서는 이미지에서 주변의 주행 상황을 분석하여 차량이 \*\*Go 또는 Stop\*\*을 결정할 수 있도록 Vision-Language Model(VLM)을 적용하였습니다.

&#x20;   - 모델은 이미지를 관찰하고, 해당 상황에서 발생할 수 있는 충돌 위험을 바탕으로 객관식 질문에 답하도록 구성하였습니다.

\- \[ ]  \*\*1. Project Overview\*\*

&#x20;   - This project applied a Vision-Language Model(VLM) to determine vehicle movement wether to Go or Stop by analyzing surrounding driving situations from images.

&#x09;	- Model will observes images and answer a multiple-choice question based in the possible collision risk in the scene.

&#x20; 

\- \[ ] \*\*2. 모델 및 방법\*\*

&#x20;   - 본 프로젝트에서는 기본 VLM 모델로 \*\*Gemma\*\*를 사용하였습니다.

&#x20;   - VLM에는 다음과 같은 입력이 주어집니다.

&#x20;       - 10장의 주행 상황 이미지

&#x20;       - 의사결정 과정을 설명하는 prompt

&#x20;       - 4개의 선택지: Go, Stop, Cannot be determined, None of the above

\- \[ ]  \*\*2. Model and Method\*\*

&#x20;   - Gemma is used as the original VLM model in this project

VLM will receive:

&#x09;- 10 images of driving situation

&#x09;- prompt explaining decision making workflow

&#x09;- 4 possible choices: Go, Stop, Cannot be determined, and None of the above

&#x20;

\- \[ ] \*\*3. 결과\*\*

&#x20;   - 정확도: \*\*80%\*\*

&#x20;   - 자세한 결과는 코드에 기록하였습니다.

\- \[ ]  \*\*3. Result\*\*

&#x20;	Accuracy: 80% (detail is in the code)

&#x20;

\- \[ ] \*\*4. 추가 실험\*\*

&#x20;   - 모델이 상황을 더 구체적으로 이해할 수 있도록 prompt에 상세한 설명을 추가하여 테스트하였습니다.

&#x20;   - 다른 VLM 모델인 \*\*Qwen3-VL\*\*을 적용하여 기존 모델과 결과를 비교하였습니다.

\- \[ ]  \*\*4. Additional Test\*\*

&#x20;   - Modify prompt to see how model work with more detail specific explaination 

&#x20;   - Applied different VLM Model (Qwen3-VL)

&#x20;

\- \[ ] \*\*5. 한계점 및 개선 방향\*\*

&#x20;   - 실험 과정에서 package 간의 호환성 문제가 발생하였으며, 호환 가능한 안정적인 버전의 package를 설치하여 문제를 해결하였습니다.

&#x20;   - 제한된 GPU 런타임으로 인해 주어진 시간 내에 더 많은 실험을 진행하지 못했습니다.

&#x20;   - 향후에는 다양한 prompt를 추가로 테스트하여 모델의 성능을 더욱 향상시키고, 다른 VLM 모델도 적용해 보고 싶습니다.

&#x20;   - 또한 장애물을 마주했을 때 차량이 선택할 수 있는 행동을 더 다양하게 표현할 수 있도록 다른 형태의 객관식 질문과 선택지도 실험해 보고 싶습니다.

\- \[ ]  \*\*5. Limitation and Improvement\*\*

* There is an errors occur during experiment which is compatibality of package and can be easily solve by installing other stable package
* Due to limited runtime GPU, I cannot run more test within given time but I would like to try other prompt to achive much better model and also try using other VLM. Also I would like to test different multiple-choice question which I think can give more option to vehicle when confronting obstacles. 



