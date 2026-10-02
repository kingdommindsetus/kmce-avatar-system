export type AvatarState = 'idle' | 'listening' | 'thinking' | 'speaking' | 'interrupted';

export type MorphWeights = Partial<Record<
  'jawOpen' | 'viseme_aa' | 'viseme_oh' | 'viseme_ee' | 'viseme_mbp' | 'mouthSmile',
  number
>>;

export interface AvatarBehavior {
  t_ms: number;
  blink_left: number;
  blink_right: number;
  brow_raise: number;
  head_yaw: number;
  head_pitch: number;
  gaze_x: number;
  gaze_y: number;
  breath: number;
}

export interface AvatarFrameEvent {
  type: 'frame';
  utterance_id: string;
  t_ms: number;
  viseme: MorphWeights;
  behavior: AvatarBehavior;
}

export interface SpeechStartEvent {
  type: 'speech_start';
  utterance_id: string;
  agent_id: string;
  audio_url?: string | null;
  duration_ms: number;
}

export interface SpeechEndEvent {
  type: 'speech_end' | 'interrupted';
  utterance_id: string;
}

export type AvatarRuntimeEvent = AvatarFrameEvent | SpeechStartEvent | SpeechEndEvent;

export interface SpeechRequest {
  text: string;
  audio_url?: string;
  duration_ms?: number;
}

export async function streamAvatarSpeech(
  baseUrl: string,
  agentId: string,
  request: SpeechRequest,
  onEvent: (event: AvatarRuntimeEvent) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${baseUrl.replace(/\/$/, '')}/agents/${agentId}/speech`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(request),
    signal,
  });

  if (!response.ok || !response.body) {
    throw new Error(`Avatar runtime failed: ${response.status}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const chunks = buffer.split('\n\n');
    buffer = chunks.pop() ?? '';

    for (const chunk of chunks) {
      const line = chunk.split('\n').find((item) => item.startsWith('data: '));
      if (!line) continue;
      onEvent(JSON.parse(line.slice(6)) as AvatarRuntimeEvent);
    }
  }
}

export async function interruptAvatar(baseUrl: string, agentId: string): Promise<void> {
  await fetch(`${baseUrl.replace(/\/$/, '')}/agents/${agentId}/interrupt`, { method: 'POST' });
}
