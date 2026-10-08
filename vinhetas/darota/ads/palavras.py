"""Timestamps por palavra da trilha de voz (faster-whisper) -> palavras_X.json"""
import sys, json, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
AD = sys.argv[1]; x, sr = sf.read(f'voz_{AD}.wav', dtype='float32')
x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * 16000 / sr)), np.arange(len(x)), x).astype(np.float32)
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = m.transcribe(x, language='pt', beam_size=5, word_timestamps=True, vad_filter=False,
    initial_prompt='Da Rota Home Center. Manda a lista de material no nosso WhatsApp. Hidráulica, elétrica, ferragens. Vonder, Atlas, WD-40.')
w = [(p.word.strip(), round(p.start, 2), round(p.end, 2)) for s in segs for p in s.words]
json.dump(w, open(f'palavras_{AD}.json', 'w'), ensure_ascii=False); print(' '.join(f'{a}[{b}]' for a, b, c in w))
