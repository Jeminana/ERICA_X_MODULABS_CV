# Seminar 2 — Hugging Face CLI와 Colab GPU를 활용한 Vision AI 에이전트

# Seminar 2 — Vision AI Agent with Hugging Face CLI and Colab GPU

## 개요

이번 세미나에서는 **Hugging Face CLI**와 **Colab GPU**를 이용해 Vision AI 작업을 진행하고, 이 과정을 **AI 에이전트**가 수행할 수 있도록 연결하는 방법을 배웠습니다. 작업 공간으로는 **GitHub Codespaces**를 사용했습니다.

노트북을 열어 셀을 하나씩 실행하는 대신, Codespaces 터미널에서 명령어로 모델을 받고(`hf`), Colab GPU를 만들어 노트북을 원격 실행한 뒤(`colab`), 실행 결과가 담긴 출력 노트북(`*_output.ipynb`)을 돌려받았습니다. 이렇게 명령어로 이루어진 흐름이기 때문에 셸 스크립트와 에이전트 Skill로 묶어 자동화할 수 있습니다.

실습 주제는 Hugging Face의 사전학습 모델(`facebook/deit-tiny-patch16-224`)을 받아 GPU에서 추론하고, 병·그릇·캔·컵·접시 5개 클래스로 파인튜닝하는 것이었습니다.

## Overview

In this seminar, we learned how to run Vision AI tasks with the **Hugging Face CLI** and a **Colab GPU**, and how to hook that process up so an **AI agent** can carry it out. **GitHub Codespaces** served as the workspace.

Instead of opening a notebook and running cells one by one, we used commands in the Codespaces terminal to download the model (`hf`), create a Colab GPU and execute the notebooks remotely (`colab`), and get back output notebooks (`*_output.ipynb`) containing the results. Because the whole flow is made of commands, it can be wrapped in a shell script and an agent Skill and automated.

The practice task was to download a pretrained Hugging Face model (`facebook/deit-tiny-patch16-224`), run inference on a GPU, and fine-tune it on five classes: bottle, bowl, can, cup and plate.

### 사용한 도구 | Tools

| 도구 Tool | 역할 Role | 실행 위치 Where |
|---|---|---|
| GitHub Codespaces | 작업 공간: 편집, 다운로드, 데이터 준비 · Workspace: editing, downloads, data prep | 클라우드 CPU · Cloud CPU |
| Hugging Face CLI (`hf`) | 모델 파일 다운로드 · Downloading model files | Codespaces |
| Colab CLI (`colab`) | GPU 생성·파일 전송·노트북 실행·회수·종료 · Create GPU, transfer files, run notebooks, retrieve, stop | 명령은 Codespaces, 연산은 Colab · Commands in Codespaces, compute in Colab |
| Transformers · PyTorch | 모델 추론과 학습 · Model inference and training | Colab T4 GPU |
| Agent Skill (`.agents/skills/`) | 위 과정을 에이전트가 실행하도록 안내 · Instructions that let an agent run the above | AI 코딩 도구 · AI coding tool |

---

## 폴더 구성 | Folder Layout

```
06_Seminar_2/
├── 01_gpu_inference_output.ipynb    ← 01번을 Colab GPU에서 실행한 결과
├── 02_gpu_finetuning_output.ipynb   ← 02번을 Colab GPU에서 실행한 결과
└── vision-ai-notebook-main/         ← 수업 저장소 (환경 설정, 노트북, 스크립트)
    ├── .devcontainer/               ← Codespaces 환경 자동 설정
    └── hf_colab_gpu/notebooks/
        ├── 00_hf_download_and_data.ipynb
        ├── 01_gpu_inference.ipynb
        └── 02_gpu_finetuning.ipynb
```

폴더 밖에 있는 두 파일이 **최종 결과물**입니다. `vision-ai-notebook-main/` 안의 00·01·02번 노트북은 실행 전 원본입니다.

The two files outside the folder are the **final outputs**. The 00·01·02 notebooks inside `vision-ai-notebook-main/` are the original, unexecuted versions.

---

## 1. 전체 흐름 | The Workflow

세 노트북은 각각 따로 실행하는 것이 아니라 하나의 흐름으로 이어집니다. **00번이 준비한 모델과 데이터를 가지고 01번과 02번이 결과를 만듭니다.**

The three notebooks are not independent — they form one pipeline. **Notebooks 01 and 02 produce their outputs from the model and data that notebook 00 prepares.**

```
[Codespaces CPU]                          [Colab T4 GPU]
00_hf_download_and_data.ipynb
  ├─ hf download → 모델 파일 3개
  └─ 데이터 분할 → train/val/test .npz
         │
         │  colab upload (모델·데이터 전송)
         ▼
  colab exec -f 01_gpu_inference.ipynb  ──►  실행  ──►  01_gpu_inference_output.ipynb
  colab exec -f 02_gpu_finetuning.ipynb ──►  실행  ──►  02_gpu_finetuning_output.ipynb
         │
         │  colab download (결과 회수) → colab stop (세션 종료)
```

| 노트북 | 실행 위치 | 하는 일 |
|---|---|---|
| 00 · HF CLI와 데이터 준비 | Codespaces CPU | `hf download`로 모델을 받고, 이미지를 train 500 / val 100 / test 200장으로 분할 |
| 01 · GPU 추론 | Colab GPU | `pipeline()`과 직접 작성된 추론 함수로 Top-5 예측 비교 |
| 02 · GPU 파인튜닝 | Colab GPU | 분류 헤드 학습 → 마지막 Transformer 블록까지 파인튜닝 → 저장·재로딩 검증 |

---

## 2. Codespaces 환경 설정 | Setting Up Codespaces

저장소를 Fork한 뒤 **Code → Codespaces → Create codespace on main**으로 클라우드 개발 환경을 만들었습니다. `.devcontainer/devcontainer.json`이 Dockerfile과 `scripts/setup.sh`를 연결해 Python 가상환경(`.venv`)과 Jupyter 커널 `Vision AI (Codespaces CPU)`를 자동으로 만들어 줍니다.

After forking the repo, we created a cloud dev environment via **Code → Codespaces → Create codespace on main**. `.devcontainer/devcontainer.json` wires the Dockerfile and `scripts/setup.sh` together, which automatically builds the Python venv (`.venv`) and the `Vision AI (Codespaces CPU)` Jupyter kernel.

```bash
source .venv/bin/activate
python scripts/doctor.py   # 환경 점검 | environment check
```

---

## 3. 00번 — 모델 다운로드와 데이터 준비 | Notebook 00 — Model Download & Data Prep

Codespaces의 CPU 커널에서 00번을 실행해 Hugging Face CLI로 모델을 받고 데이터를 준비했습니다. GPU가 필요 없는 작업이므로 Codespaces에서 처리합니다.

Notebook 00 runs on the Codespaces CPU kernel: it downloads the model with the Hugging Face CLI and prepares the data. No GPU is needed for this step.

```bash
hf download facebook/deit-tiny-patch16-224 config.json preprocessor_config.json pytorch_model.bin \
  --revision b3428f18dcc7b543470d07f14b4a4157815d1880 \
  --local-dir hf_colab_gpu/models/deit-tiny
```

---

## 4. Colab CLI로 GPU에서 01·02번 실행 | Running 01 & 02 on a Colab GPU via CLI

핵심은 **Codespaces 터미널에서 `colab` 명령으로 원격 GPU를 조작한다**는 점입니다. Codespaces에서 Run All을 누른다고 GPU에 연결되지 않으며, `colab exec -f`로 노트북 자체를 Colab에 보내야 합니다.

The key idea is that **the remote GPU is driven with `colab` commands from the Codespaces terminal**. Pressing Run All in Codespaces does not connect to a GPU — the notebook itself has to be sent to Colab with `colab exec -f`.

```bash
# 1) 로그인 + T4 세션 생성 | log in and create a T4 session
colab --auth oauth2 sessions
colab new -s hf-vision-gpu --gpu T4

# 2) GPU 라이브러리 설치, 모델·데이터 업로드 | install libs, upload model & data
colab upload -s hf-vision-gpu <local path> content/vision-ai/<remote path>

# 3) 노트북 실행 → *_output.ipynb 생성 | execute notebooks → *_output.ipynb
colab exec -s hf-vision-gpu -f hf_colab_gpu/notebooks/01_gpu_inference.ipynb --timeout 1800
colab exec -s hf-vision-gpu -f hf_colab_gpu/notebooks/02_gpu_finetuning.ipynb --timeout 1800

# 4) 결과 회수 후 세션 종료 | download results, then stop the session
colab download -s hf-vision-gpu content/vision-ai/hf_colab_gpu/results/gpu/report.json hf_colab_gpu/results/gpu/report.json
colab stop -s hf-vision-gpu
```

`colab exec`는 셀에서 오류가 나도 종료 코드만으로는 알 수 없기 때문에, 생성된 `*_output.ipynb`를 열어 모든 셀이 오류 없이 실행되었는지 직접 확인해야 합니다. 또한 Colab 사용량(CU)은 세션이 켜져 있는 동안 소모되므로 실습 후 반드시 `colab stop`으로 종료합니다.

`colab exec` can finish even when a cell fails, so the exit code alone isn't enough — the generated `*_output.ipynb` has to be opened to confirm every cell ran cleanly. Colab compute units are consumed while a session is alive, so the session is always stopped with `colab stop` afterwards.

---

## 5. Vision AI 에이전트 — 셸 스크립트와 Skill | Vision AI Agent — Shell Script & Skills

위의 명령어 흐름을 **셸 파일 하나로 묶고, 그 셸 파일을 AI 에이전트가 호출하도록 Skill로 등록**하는 방법도 배웠습니다. 순서는 **Skill → 셸 파일 → Colab CLI → Python `pipeline()`** 입니다.

We also learned how to **wrap the command flow above into a single shell script, and register that script as a Skill an AI agent can call**. The chain is **Skill → shell script → Colab CLI → Python `pipeline()`**.

```bash
# 로그인·GPU 생성 없이 실행 계획만 확인 | show the plan only, no login or GPU
bash hf_colab_gpu/run_pipeline_colab.sh --dry-run

# 새 Colab T4 → Hub 모델 추론 → 결과 회수 → 세션 종료
# new Colab T4 → Hub model inference → retrieve results → stop session
bash hf_colab_gpu/run_pipeline_colab.sh
```

저장소의 `.agents/skills/`에는 두 개의 Skill이 들어 있습니다.

The repo ships two Skills under `.agents/skills/`:

| Skill | 하는 일 What it does |
|---|---|
| `vision-colab` | HF CLI로 모델 준비 → Colab GPU 세션에서 01·02 노트북 실행 → 결과 회수 → 세션 종료까지의 전체 과정 · The full flow: prepare the model with HF CLI → run notebooks 01·02 on a Colab GPU session → retrieve results → stop the session |
| `vision-pipeline-inference` | `run_pipeline_colab.sh`를 호출해 이미지 한 장을 Colab T4에서 추론 · Calls `run_pipeline_colab.sh` to classify a single image on a Colab T4 |

Skill은 새로운 프로그램이 아니라 **에이전트가 읽는 작업 지침**입니다. 예를 들어 에이전트에게 다음과 같이 요청할 수 있습니다.

A Skill isn't a new program — it's **a set of instructions the agent reads**. For example, the agent can be asked:

> `$vision-pipeline-inference`로 00번에서 준비한 cup 이미지를 새 Colab T4에서 추론해 줘. 결과 JSON을 회수하고 이번에 만든 세션이 종료됐는지도 확인해 줘.
>
> Use `$vision-pipeline-inference` to classify the cup image prepared in notebook 00 on a new Colab T4. Retrieve the result JSON and confirm the session I created has been stopped.

Google 로그인은 본인이 직접 해야 하며, Skill 파일에 토큰이나 계정 정보를 적지 않습니다.

The Google login has to be done by the user, and no tokens or account details go into the Skill files.

---

## 6. 실행 결과 | Results

두 출력 노트북 모두 **Tesla T4 GPU**에서 오류 없이 끝까지 실행되었습니다 (`torch 2.8.0+cu126`, `transformers 4.57.6`).

Both output notebooks ran to completion without errors on a **Tesla T4 GPU** (`torch 2.8.0+cu126`, `transformers 4.57.6`).

### 01 · GPU 추론 | GPU Inference

- 원본 모델은 ImageNet 1,000개 라벨로 학습되어 있어, 컵 이미지를 넣어도 `face powder 5.01%`, `eggnog 4.10%` 같은 엉뚱한 라벨이 나왔습니다.
- `pipeline()` 결과와 직접 작성된 추론 함수의 Top-5 결과가 **완전히 일치**하는 것을 확인했습니다.
- 32×32 저해상도 이미지이고 "cup" 라벨 자체가 우리 데이터와 맞지 않기 때문에, 파인튜닝이 필요하다는 점을 보여 주는 단계입니다.

---

- The original model predicts ImageNet's 1,000 labels, so a cup image came out as `face powder 5.01%`, `eggnog 4.10%` and similar off-target labels.
- The Top-5 from `pipeline()` and from the hand-written inference functions **matched exactly**.
- With 32×32 images and a label set that doesn't match ours, this step shows why fine-tuning is needed.

### 02 · GPU 파인튜닝 | GPU Fine-tuning

| 단계 Stage | 학습 파라미터 Trainable params | Validation | Test |
|---|---|---|---|
| 분류 헤드만 학습 Head only | 965 | 83.0% | 80.0% |
| 마지막 블록 + 헤드 파인튜닝 Last block + head | 446,213 | 85.0% | 81.0% |

- Macro F1: **0.800 → 0.809**
- 모델 저장 후 다시 불러왔을 때 출력 차이 **0.0** — 저장·재로딩 검증 통과

- Macro F1: **0.800 → 0.809**
- Save-and-reload check passed with a maximum output difference of **0.0**.

---

## 배운 점 | What I Learned

- **작업 공간과 연산 공간의 분리**: 편집·다운로드·데이터 준비는 Codespaces(CPU), 무거운 연산은 Colab(GPU)에서 하고, 둘을 CLI로 연결하는 방식
- **노트북을 명령어로 실행하기**: 셀을 직접 누르지 않고 `colab exec -f`로 노트북 전체를 원격 실행해 결과가 담긴 출력 노트북을 받는 방법
- **devcontainer**: 저장소에 환경 설정을 함께 넣어 두면 누구든 Codespace를 열었을 때 같은 환경이 재현된다는 점
- **`hf download` vs `from_pretrained`**: 전자는 파일을 받는 것이고, 후자는 받은 파일을 Python 모델로 읽는 것
- **클라우드 자원 관리**: 세션을 만들고, 결과를 회수하고, 반드시 종료하는 흐름
- **에이전트로 자동화하기**: 명령어로 된 작업은 셸 스크립트로 묶고 Skill로 등록하면 AI 에이전트가 같은 과정을 대신 실행할 수 있다는 점

---

- **Separating workspace from compute**: editing, downloading and data prep happen in Codespaces (CPU), heavy compute happens in Colab (GPU), and the CLI connects the two.
- **Running notebooks from the command line**: executing a whole notebook remotely with `colab exec -f` and getting back an output notebook with the results, instead of clicking through cells.
- **devcontainer**: keeping the environment config in the repo means anyone opening a Codespace gets the same environment.
- **`hf download` vs `from_pretrained`**: the first fetches files; the second loads those files into a Python model.
- **Managing cloud resources**: create a session, retrieve the results, and always shut it down.
- **Automating with an agent**: once a task is made of commands, it can be wrapped in a shell script and registered as a Skill so an AI agent can run the same process.

---

- 수업 저장소 | Course repo: [vision-ai-notebook-main/](vision-ai-notebook-main/) ([README](vision-ai-notebook-main/README.md), [단계별 안내 | step-by-step guide](vision-ai-notebook-main/hf_colab_gpu/README.md))
