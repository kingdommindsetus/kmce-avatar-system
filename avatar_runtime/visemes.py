from __future__ import annotations

import re
from typing import Dict, List

from .models import VisemeFrame


# GLB morph targets supported by the current Pegasus avatar rig.
REST = {}
AA = {"jawOpen": 0.72, "viseme_aa": 1.0}
AE = {"jawOpen": 0.56, "viseme_aa": 0.78, "viseme_ee": 0.18}
AH = {"jawOpen": 0.66, "viseme_aa": 0.88}
EE = {"jawOpen": 0.22, "viseme_ee": 1.0}
IH = {"jawOpen": 0.24, "viseme_ee": 0.72}
OH = {"jawOpen": 0.48, "viseme_oh": 1.0}
OU = {"jawOpen": 0.30, "viseme_oh": 0.88}
MBP = {"viseme_mbp": 1.0}
FV = {"jawOpen": 0.12, "viseme_ee": 0.24}
TH = {"jawOpen": 0.18, "viseme_aa": 0.16}

LETTER_TO_VISEME: Dict[str, Dict[str, float]] = {
    "a": AA,
    "e": EE,
    "i": IH,
    "o": OH,
    "u": OU,
    "m": MBP,
    "b": MBP,
    "p": MBP,
    "f": FV,
    "v": FV,
}

DIGRAPHS = {
    "th": TH,
    "oo": OU,
    "oh": OH,
    "ee": EE,
}


def text_to_visemes(text: str, frame_ms: int = 72) -> List[VisemeFrame]:
    """
    Deterministic fallback viseme timeline.

    This is intentionally not presented as phoneme-perfect alignment.
    When the TTS provider exposes word/phoneme timestamps, those timestamps
    should replace this approximation while keeping the same output schema.
    """
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    frames: List[VisemeFrame] = []
    cursor = 0
    i = 0

    while i < len(normalized):
        if normalized[i].isspace():
            frames.append(VisemeFrame(t_ms=cursor, duration_ms=frame_ms, weights=REST))
            cursor += frame_ms
            i += 1
            continue

        pair = normalized[i : i + 2]
        if pair in DIGRAPHS:
            weights = DIGRAPHS[pair]
            i += 2
        else:
            weights = LETTER_TO_VISEME.get(normalized[i], REST)
            i += 1

        frames.append(VisemeFrame(t_ms=cursor, duration_ms=frame_ms, weights=weights))
        cursor += frame_ms

    if not frames:
        frames.append(VisemeFrame(t_ms=0, duration_ms=frame_ms, weights=REST))

    return frames
