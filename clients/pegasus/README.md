# Pegasus client adapter

This adapter connects the React/Three.js Pegasus frontend to the KMCE Avatar Runtime v2.

## Contract

The runtime streams Server-Sent Events containing:

- speech start
- timed morph weights
- blink/gaze/head behavior
- speech end
- interruption

The renderer consumes morph weights directly instead of inferring mouth shapes from random browser-speech frequency data.

## React usage

```tsx
const avatar = useAvatarRuntime(
  import.meta.env.VITE_AVATAR_RUNTIME_URL,
  agent.id,
);

<AvatarFace
  agent={agent}
  isSpeaking={avatar.isSpeaking}
  runtimeMorphs={avatar.morphs}
  runtimeBehavior={avatar.behavior}
/>
```

When the existing TTS endpoint returns real audio, pass the same utterance text and measured/known audio duration to `avatar.speak()`. The final production implementation should start audio and the avatar timeline from one shared playback clock.

## Rollout

1. Simon only.
2. Validate mouth timing, interruption, blink/gaze, and voice identity.
3. Keep the existing analyzer-based renderer as rollback.
4. After Simon passes QA, propagate the same adapter to the other agents.
