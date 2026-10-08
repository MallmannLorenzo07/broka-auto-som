"""Da Rota: narração ElevenLabs (voz Brian) sincronizada com os cortes do vídeo, sobre a trilha original com ducking."""
import sys, subprocess, numpy as np, soundfile as sf
from corte import ler, SR
F = sys.argv[1]; DUR = 30.0; N = int(DUR * SR)
trilha = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', F, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).reshape(-1, 2)[:N]
trilha = np.pad(trilha, ((0, N - len(trilha)), (0, 0)))
voz = np.zeros(N, np.float32)
def put(x, at): i = int(at * SR); n = min(len(x), N - i); voz[i:i + n] += x[:n]
def trecho(x, a, b):   # recorte em segundos com fade curto
    y = x[int(a * SR): int(b * SR) if b else None].copy(); f = int(.012 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y
intro = ler('y/a/0.wav'); put(trecho(intro, 0, .9), .12); put(trecho(intro, .98, None), 1.05)
cat = ler('y/a/1.wav')
for (a, b), at in zip([(0, 1.2), (1.42, 2.12), (2.17, 2.9), (2.95, 3.66), (3.7, None)], [4.02, 5.0, 6.0, 7.0, 8.0]): put(trecho(cat, a, b), at)
for i, at in [(2, 2.15), (8, 9.12), (9, 12.08), (10, 14.12), (11, 18.08), (12, 20.04), (13, 24.22), (14, 26.15)]: put(ler(f'vo/{i}.wav'), at)
env = np.convolve(np.abs(voz), np.ones(2400) / 2400, 'same')
ativo = np.convolve((env > .01).astype(np.float32), np.ones(int(.25 * SR)))[:N] > 0
duck = np.convolve(np.where(ativo, .32, 1.0), np.ones(4800) / 4800, 'same').astype(np.float32)
mix = trilha * duck[:, None] + (voz * .95)[:, None]
mix /= max(1., np.abs(mix).max() / .97)
sf.write('mix.wav', mix, SR); print('ok')
