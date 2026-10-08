"""Da Rota v3 (47,5 s): vídeo original + 2 cenas novas (tintas/ferramentas/marcas e dicas do Instagram).
Trilha original remontada em trechos com crossfade; narração ElevenLabs reposicionada."""
import sys, subprocess, numpy as np, soundfile as sf
from corte import ler, SR
F = sys.argv[1]; DUR = 47.5; N = int(DUR * SR)
orig = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', F, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).reshape(-1, 2)
def seg(a, b): return orig[int(a * SR):int(b * SR)].copy()
X = int(.08 * SR); trilha = np.zeros((N, 2), np.float32); pos = 0
for a, b in [(0, 9), (4, 9), (9, 24), (19.5, 24), (12, 16), (24, 30), (24, 28)]:   # (4–9) e (19,5–24) preenchem as cenas novas
    s = seg(a, b); n = len(s)
    if pos > 0: s[:X] *= np.linspace(0, 1, X)[:, None]; trilha[pos - X:pos] *= np.linspace(1, 0, X)[:, None]; pos -= X
    m = min(n, N - pos); trilha[pos:pos + m] += s[:m]; pos += m
trilha *= np.clip((DUR - np.arange(N) / SR) / 1.5, 0, 1)[:, None]
voz = np.zeros(N, np.float32)
def put(x, at): i = int(at * SR); n = min(len(x), N - i); voz[i:i + n] += x[:n]
def trecho(x, a, b):
    y = x[int(a * SR): int(b * SR) if b else None].copy(); f = int(.012 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y
intro = ler('y/a/0.wav'); put(trecho(intro, 0, .9), .12); put(trecho(intro, .98, None), 1.05)
cat = ler('y/a/1.wav')
for (a, b), at in zip([(0, 1.2), (1.42, 2.12), (2.17, 2.9), (2.95, 3.66), (3.7, None)], [4.02, 5.0, 6.0, 7.0, 8.0]): put(trecho(cat, a, b), at)
put(ler('vo/2.wav'), 2.15)
put(ler('z/a/0.wav'), 9.15)                                   # nova: tintas, ferramentas e marcas
for i, at in [(8, 14.12), (9, 17.08), (10, 19.12), (11, 23.08), (12, 25.0)]: put(ler(f'vo/{i}.wav'), at)
put(ler('z/a/1.wav'), 29.3)                                   # nova: dicas no Instagram
put(ler('w/a/0.wav'), 33.75)                                  # nova: 6 anos
put(ler('vo/13.wav'), 37.72)
put(ler('z/a/2.wav'), 39.62)                                  # final com o número falado
env = np.convolve(np.abs(voz), np.ones(2400) / 2400, 'same')
ativo = np.convolve((env > .01).astype(np.float32), np.ones(int(.25 * SR)))[:N] > 0
duck = np.convolve(np.where(ativo, .32, 1.0), np.ones(4800) / 4800, 'same').astype(np.float32)
mix = trilha * duck[:, None] + (voz * .95)[:, None]; mix /= max(1., np.abs(mix).max() / .97)
sf.write('mix_v3.wav', mix, SR); print('ok', round(len(voz[np.abs(voz) > 0]) / SR, 1), 's de voz')
