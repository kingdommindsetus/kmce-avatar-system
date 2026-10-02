from __future__ import annotations

import json

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from avatar_runtime.agents import get_agent_runtime
from avatar_runtime.models import AvatarState

app = FastAPI(title="KMCE Avatar Runtime", version="0.2.0")


class SpeechRequest(BaseModel):
    text: str
    audio_url: str | None = None
    duration_ms: int | None = None


class StateRequest(BaseModel):
    state: AvatarState


@app.get("/health")
async def health():
    return {"ok": True, "service": "kmce-avatar-runtime", "version": "0.2.0"}


@app.get("/agents/{agent_id}")
async def agent_status(agent_id: str):
    try:
        runtime = get_agent_runtime(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return {
        "agent_id": runtime.config.agent_id,
        "display_name": runtime.config.display_name,
        "voice_id": runtime.config.voice_id,
        "locale": runtime.config.locale,
        "state": runtime.state,
    }


@app.post("/agents/{agent_id}/state")
async def set_state(agent_id: str, request: StateRequest):
    try:
        runtime = get_agent_runtime(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    runtime.set_state(request.state)
    return {"ok": True, "agent_id": agent_id, "state": runtime.state}


@app.post("/agents/{agent_id}/interrupt")
async def interrupt(agent_id: str):
    try:
        runtime = get_agent_runtime(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    runtime.interrupt()
    return {"ok": True, "agent_id": agent_id, "state": runtime.state}


@app.post("/agents/{agent_id}/speech")
async def speech(agent_id: str, request: SpeechRequest):
    try:
        runtime = get_agent_runtime(agent_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    frame = runtime.build_speech_frame(
        request.text,
        audio_url=request.audio_url,
        duration_ms=request.duration_ms,
    )

    async def event_stream():
        async for event in runtime.stream(frame):
            yield f"data: {json.dumps(event)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
