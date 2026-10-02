from __future__ import annotations

from .engine import AvatarRuntime, AvatarRuntimeConfig


SIMON = AvatarRuntime(
    AvatarRuntimeConfig(
        agent_id="simon",
        display_name="Simon",
        voice_id="fenrir",
        locale="en-GB",
        frame_ms=72,
    )
)

AGENTS = {
    "simon": SIMON,
}


def get_agent_runtime(agent_id: str) -> AvatarRuntime:
    try:
        return AGENTS[agent_id.lower()]
    except KeyError as exc:
        raise KeyError(f"Unknown avatar agent: {agent_id}") from exc
