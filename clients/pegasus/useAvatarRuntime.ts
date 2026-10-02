import { useCallback, useEffect, useRef, useState } from 'react';
import {
  AvatarBehavior,
  AvatarRuntimeEvent,
  AvatarState,
  MorphWeights,
  interruptAvatar,
  streamAvatarSpeech,
} from './avatarRuntimeClient';

const ZERO_BEHAVIOR: AvatarBehavior = {
  t_ms: 0,
  blink_left: 0,
  blink_right: 0,
  brow_raise: 0,
  head_yaw: 0,
  head_pitch: 0,
  gaze_x: 0,
  gaze_y: 0,
  breath: 0,
};

export function useAvatarRuntime(baseUrl: string, agentId: string) {
  const [state, setState] = useState<AvatarState>('idle');
  const [morphs, setMorphs] = useState<MorphWeights>({});
  const [behavior, setBehavior] = useState<AvatarBehavior>(ZERO_BEHAVIOR);
  const abortRef = useRef<AbortController | null>(null);

  const stop = useCallback(async () => {
    abortRef.current?.abort();
    abortRef.current = null;
    setMorphs({});
    setBehavior(ZERO_BEHAVIOR);
    setState('interrupted');
    try {
      await interruptAvatar(baseUrl, agentId);
    } finally {
      setState('idle');
    }
  }, [baseUrl, agentId]);

  const speak = useCallback(async (
    text: string,
    options: { audioUrl?: string; durationMs?: number } = {},
  ) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    const onEvent = (event: AvatarRuntimeEvent) => {
      if (event.type === 'speech_start') {
        setState('speaking');
      } else if (event.type === 'frame') {
        setMorphs(event.viseme);
        setBehavior(event.behavior);
      } else if (event.type === 'speech_end') {
        setMorphs({});
        setState('idle');
      } else if (event.type === 'interrupted') {
        setMorphs({});
        setState('interrupted');
      }
    };

    try {
      await streamAvatarSpeech(
        baseUrl,
        agentId,
        {
          text,
          audio_url: options.audioUrl,
          duration_ms: options.durationMs,
        },
        onEvent,
        controller.signal,
      );
    } catch (error) {
      if (!controller.signal.aborted) throw error;
    }
  }, [baseUrl, agentId]);

  useEffect(() => () => abortRef.current?.abort(), []);

  return {
    state,
    isSpeaking: state === 'speaking',
    morphs,
    behavior,
    speak,
    stop,
  };
}
