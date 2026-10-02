from __future__ import annotations

import math
from typing import List

from .models import AvatarState, BehaviorFrame


def build_behavior_timeline(duration_ms: int, state: AvatarState, step_ms: int = 80) -> List[BehaviorFrame]:
    frames: List[BehaviorFrame] = []
    for t in range(0, max(duration_ms, step_ms), step_ms):
        phase = t / 1000.0

        # Small deterministic movements keep the avatar alive without jitter.
        head_yaw = math.sin(phase * 0.55) * (0.010 if state == AvatarState.SPEAKING else 0.006)
        head_pitch = math.sin(phase * 0.37) * 0.005
        gaze_x = math.sin(phase * 0.23) * 0.04
        gaze_y = math.cos(phase * 0.19) * 0.02
        breath = (math.sin(phase * 2.0) + 1.0) * 0.5

        # Deterministic blink every ~3.7 seconds.
        blink_phase = (t % 3700)
        blink = 1.0 if 0 <= blink_phase <= 120 else 0.0

        frames.append(
            BehaviorFrame(
                t_ms=t,
                blink_left=blink,
                blink_right=blink,
                brow_raise=0.08 if state == AvatarState.LISTENING else 0.02,
                head_yaw=head_yaw,
                head_pitch=head_pitch,
                gaze_x=gaze_x,
                gaze_y=gaze_y,
                breath=breath,
            )
        )
    return frames
