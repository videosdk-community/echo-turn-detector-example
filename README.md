# Echo Turn Detector

The Echo Turn Detector (TurnV2) utilizes a custom fine-tuned model from VideoSDK to accurately determine whether a user has finished speaking. This allows for precise management of conversation flow, especially in cascading pipeline setups. It operates as a server-hosted multilingual model on the VideoSDK Inference Gateway, with options for low latency (`echo-small`) or high accuracy (`echo-large`).

## Architecture

![VideoSDK AI Agents High Level Architecture](https://assets.videosdk.live/static-assets/ghost/2026/06/echo_turn_detector_architecture.png)

## Learn More

- 📖 **[Documentation](https://docs.videosdk.live/ai_agents/core-components/turn-detection)** — Full API reference, configuration options, and integration guides for the Echo Turn Detector.
- ✍️ **[Blog](https://www.videosdk.live/blog/echo-turn-detection)** — Read about how the Echo Turn Detector works, benchmarks.

## Get Started

1. Set environment variables

Copy [`.env.example`](.env.example) at the repo root to `.env` and fill in: `DEEPGRAM_API_KEY`, `ELEVENLABS_API_KEY`, `OPENAI_API_KEY`.

For VideoSDK auth, set **either** `VIDEOSDK_AUTH_TOKEN` **or** `VIDEOSDK_API_KEY` + `VIDEOSDK_SECRET_KEY` (the SDK auto-mints a JWT from the API key/secret at runtime).

Get these credentials from the [VideoSDK Dashboard](https://app.videosdk.live/dashboard/) under **API Keys**.

2. Create the environment

- On MacOS/Linux

```bash
python3 -m venv .venv
```

- On Windows

Next, Activate it! Command differ based on your environment

```bash
source .venv/bin/activate
```

3. Installation Dependencies

```bash
python -m pip install -r requirements.txt
```

4. Run Agent Worker

```bash
python main.py console
```

## Working - ECHO TURN DETECTOR

## Importing

```python
from videosdk.agents.inference import TurnV2
```

## Example Usage

**1. For lowest latency (echo-small):**

This is the default variant optimized for the fastest possible turn detection.

```python
# Initialize the Turn Detector using the echo-small model
turn_detector = TurnV2.echo_small()

# Add the Turn Detector to a pipeline
pipeline = Pipeline(
    stt=DeepgramSTT(),
    llm=OpenAILLM(),
    tts=ElevenLabsTTS(),
    vad=SileroVAD(),
    turn_detector=turn_detector
)
```

**2. For highest accuracy (echo-large):**

This variant trades a small amount of latency for improved classification accuracy.

```python
# Initialize the Turn Detector using the echo-large model
turn_detector = TurnV2.echo_large()

# Add the Turn Detector to a pipeline
pipeline = Pipeline(
    stt=DeepgramSTT(),
    llm=OpenAILLM(),
    tts=ElevenLabsTTS(),
    vad=SileroVAD(),
    turn_detector=turn_detector
)
```

## Inspecting Turn States

If you want to test or debug what the detector is doing, you can subscribe to the pipeline's `turn_state` hook. It fires every time the model classifies a turn, giving you the transcribed text and the predicted state.

```python
@pipeline.on("turn_state")
async def on_turn_state(data: dict):
    # data = {"text": str, "state": "Complete" | "Incomplete" |
    #    "Backchannel" | "Wait" }
    print(f"[TURN] state={data['state']} text={data['text']!r}")
```

The `state` field can be one of:

| State | Meaning |
| :--- | :--- |
| `Complete` | The user has finished speaking — the agent can respond. |
| `Incomplete` | The user paused but is likely still speaking. |
| `Backchannel` | A filler/acknowledgement (e.g. "uh-huh", "okay") — not a real turn. |
| `Wait` | Hold for more input before deciding. |

## Supported Languages

The `TurnV2` models support a wide range of languages. Since the model is multilingual, it automatically detects the language being spoken.

Here is a list of the supported languages:

| Language |
| :--- |
| Bengali |
| English |
| French |
| German |
| Gujarati |
| Hindi |
| Italian |
| Marathi |
| Spanish |
| Tamil |
| Telugu |
| Urdu |

## Pre-downloading Model

Unlike other detectors that require downloading models locally, the **Echo Turn Detector** is fully server-hosted on the **VideoSDK Inference Gateway**.

No local model download or setup is required. The model is ready to use instantly, reducing startup latency and agent worker resource consumption.

## VideoSDK Agents

Build and deploy production-ready AI voice & video agents with [VideoSDK](https://videosdk.live). This repo is your central hub for agent templates, feature examples, and everything you need to ship real-world AI-powered applications.

| Resource | Description |
|---|---|
| 🚀 [Use Case Examples](https://github.com/videosdk-live/agents/tree/main/use_case_examples) | Production-ready templates across Customer Support, Healthcare, Tech Support & more |
| ⚡ [Feature Examples](https://github.com/videosdk-live/agents/tree/main/examples) | Always up-to-date examples showcasing the latest VideoSDK Agent features |
| 📖 [AI Agents Docs](https://docs.videosdk.live/ai_agents/introduction) | Full guides, concepts & API references to get you started |

> ⭐ If this helps you, star this repo and [`videosdk-live/agents`](https://github.com/videosdk-live/agents) — it keeps us motivated to ship more!
