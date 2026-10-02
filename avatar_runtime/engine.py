from __future__ import annotations

import asyncio
import time
import uuid
from dataclasses import dataclass
from typing import AsyncIterator

from .behavior import build_behavior_timeline
from .models import AvatarState, SpeechFrame
from .visemes import text_to_visemes


@dataclass
class AvatarRuntimeConfig:
    agent_id: str
    display_name: str
    voice_id: str
    locale: str = "en-GB"
    frame_ms: int = 72


class AvatarRuntime:
    """
    Reusable avatar timing engine.

    The runtime owns the authoritative avatar state and produces a single
    speech timeline that the GLB renderer can consume. Audio transport and
    facial animation should be driven from this same utterance clock.
    """

    def __init__(self, config: AvatarRuntimeConfig):
        self.config = config
        self.state = AvatarState.IDLE
        self._active_utterance_id: str | None = None
        self._started_at: float | None = None

    def set_state(self, state: AvatarState) -> None:
        self.state = state

    def interrupt(self) -> None:
        self.state = AvatarState.INTERRUPTED
        self._active_utterance_id = None
        self._started_at = None

    def build_speech_frame(
        self,
        text: str,
        *,
        audio_url: str | None = None,
        duration_ms: int | None = None,
    ) -> SpeechFrame:
        visemes = text_to_visemes(text, frame_ms=self.config.frame_ms)
        inferred_duration = visemes[-1].t_ms + visemes[-1].duration_ms
        final_duration = duration_ms or inferred_duration

        return SpeechFrame(
            utterance_id=str(uuid.uuid4()),
            text=text,
            audio_url=audio_url,
            duration_ms=final_duration,
            visemes=visemes,
            behavior=build_behavior_timeline(final_duration, AvatarState.SPEAKING),
        )

    async def stream(self, frame: SpeechFrame) -> AsyncIterator[dict]:
        self.state = AvatarState.SPEAKING
        self._active_utterance_id = frame.utterance_id
        self._started_at = time.perf_counter()

        yield {
            "type": "speech_start",
            "utterance_id": frame.utterance_id,
            "agent_id": self.config.agent_id,
            "audio_url": frame.audio_url,
            "duration_ms": frame.duration_ms,
        }

        behavior_idx = 0
        for viseme in frame.visemes:
            if self._active_utterance_id != frame.utterance_id:
                yield {"type": "interrupted", "utterance_id": frame.utterance_id}
                return

            while behavior_idx + 1 < len(frame.behavior) and frame.behavior[behavior_idx + 1].t_ms <= viseme.t_ms:
                behavior_idx += 1

            yield {
                "type": "frame",
                "utterance_id": frame.utterance_id,
                "t_ms": viseme.t_ms,
                "viseme": viseme.weights,
                "behavior": frame.behavior[behavior_idx].model_dump(),
            }
            await asyncio.sleep(viseme.duration_ms / 1000.0)

        self.state = AvatarState.IDLE
        self._active_utterance_id = None
        self._started_at = None
        yield {"type": "speech_end", "utterance_id": frame.utterance_id}
