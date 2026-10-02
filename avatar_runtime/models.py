from __future__ import annotations

from enum import Enum
from typing import Dict, List

from pydantic import BaseModel, Field


class AvatarState(str, Enum):
    IDLE = "idle"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    INTERRUPTED = "interrupted"


class VisemeFrame(BaseModel):
    t_ms: int
    duration_ms: int = 70
    weights: Dict[str, float] = Field(default_factory=dict)


class BehaviorFrame(BaseModel):
    t_ms: int
    blink_left: float = 0.0
    blink_right: float = 0.0
    brow_raise: float = 0.0
    head_yaw: float = 0.0
    head_pitch: float = 0.0
    gaze_x: float = 0.0
    gaze_y: float = 0.0
    breath: float = 0.0


class SpeechFrame(BaseModel):
    utterance_id: str
    text: str
    audio_url: str | None = None
    duration_ms: int
    visemes: List[VisemeFrame]
    behavior: List[BehaviorFrame]
