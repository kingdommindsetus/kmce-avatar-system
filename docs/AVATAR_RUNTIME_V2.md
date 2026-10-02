# Pegasus / KMCE Avatar Runtime v2

## Objective

Create one reusable realtime avatar engine for every Pegasus agent.

The runtime separates four concerns:

1. **Identity** — locked agent appearance and voice profile.
2. **Speech timing** — one authoritative utterance clock.
3. **Facial animation** — visemes plus jaw/mouth morph targets.
4. **Behavior** — listening, thinking, speaking, gaze, blink, head motion, interruption.

## Simon is the reference implementation

Simon is the first production reference agent. Once his runtime passes visual QA, the same engine is reused for Marie, IRIS, Mark, Cammy, Evan, Tube, Lucy, Snake, Alice, Echo, and Booker.

## Runtime states

- `idle`
- `listening`
- `thinking`
- `speaking`
- `interrupted`

## API

Run locally:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Health:

```http
GET /health
```

Simon status:

```http
GET /agents/simon
```

Set state:

```http
POST /agents/simon/state
Content-Type: application/json

{"state":"listening"}
```

Generate synchronized speech events:

```http
POST /agents/simon/speech
Content-Type: application/json

{
  "text": "Good evening, Kimberly. Simon online.",
  "audio_url": "/audio/simon-001.wav"
}
```

The response is Server-Sent Events. Each frame includes:

- `t_ms`
- viseme morph weights
- blink values
- gaze
- head yaw/pitch
- breath signal

## Accuracy note

The bundled text-to-viseme mapper is a deterministic fallback. It is better than random frequency-driven mouth movement because it produces repeatable mouth shapes, but it is not phoneme-perfect.

The production path is:

**TTS audio + provider timing metadata → same utterance clock → GLB morph targets**

When a TTS provider exposes phoneme/word timestamps, those timestamps should replace the fallback mapper without changing the renderer contract.

## Next integration

Pegasus frontend should consume these events and drive:

- `jawOpen`
- `viseme_aa`
- `viseme_oh`
- `viseme_ee`
- `viseme_mbp`
- `mouthSmile`
- blink / eye look
- head micro-motion

Audio playback and facial animation must begin from the same utterance start event. On interruption, audio and animation queues are both flushed.
