from avatar_runtime.agents import SIMON
from avatar_runtime.models import AvatarState


def test_simon_profile():
    assert SIMON.config.agent_id == "simon"
    assert SIMON.config.locale == "en-GB"


def test_build_speech_frame():
    frame = SIMON.build_speech_frame("Hello Kimberly")
    assert frame.duration_ms > 0
    assert frame.visemes
    assert frame.behavior


def test_interrupt_state():
    SIMON.set_state(AvatarState.SPEAKING)
    SIMON.interrupt()
    assert SIMON.state == AvatarState.INTERRUPTED
