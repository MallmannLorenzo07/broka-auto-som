"""Áudio da vinheta de 30 s: narração (Chatterbox Multilingual, MIT, voz clonada de narrador LibriVox em domínio público) + trilha sintetizada aqui (pad, batida 100 BPM, riser, impacto, whooshes)."""
import wave, os, numpy as np
D = os.path.dirname(os.path.abspath(__file__)); SR = 48000; DUR = 30.0; N = int(DUR * SR)
t = np.arange(N) / SR
def ler(f):
    import soundfile as sf
    x, sr = sf.read(f, dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * SR / sr)), np.arange(len(x)), x).astype(np.float32)
    h = int(.05 * SR); e = np.array([np.sqrt(np.mean(x[j:j + h] ** 2)) for j in range(0, len(x), h)])
    on = np.where(e > .01)[0]; ini, fim = on[0], on[-1]
    for a, b in zip(on[:-1], on[1:]):      # pausa > 0,4 s seguida de pouco som (< 0,7 s) = respiração/ruído no fim: corta
        if b - a > 8 and (on > a).sum() < 14: fim = a; break
    x = x[max(0, ini * h - 1200): (fim + 1) * h + 2400].copy(); x[-2400:] *= np.linspace(1, 0, 2400)
    return x / np.abs(x).max() * .9
def put(dst, x, at, g=1.0):
    i = int(at * SR); n = min(len(x), N - i)
    if n > 0: dst[i:i + n] += x[:n] * g

# narração
VO = [0.9, 3.3, 7.2, 12.1, 14.0, 16.9, 24.3]
voz = np.zeros(N, np.float32)
for k, at in enumerate(VO): put(voz, ler(f'{D}/vo_cb/{k}.wav'), at)
voz = np.tanh(voz * 1.7) / np.tanh(1.7)

rng = np.random.default_rng(3)
B = 0.6
# pad (Lá menor → Fá → Dó → Sol), 2 compassos por acorde
acordes = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
pad = np.zeros(N, np.float32); L = 4.8
for j in range(int(DUR // L) + 1):
    a = acordes[j % 4]; i0 = int(j * L * SR); i1 = min(N, int((j + 1) * L * SR + SR))
    s = t[i0:i1] - j * L; env = np.clip(s / 1.2, 0, 1) * np.clip((L + 1 - s) / 1.2, 0, 1); y = np.zeros_like(s)
    for f in a:
        for d in (-0.7, 0.7): y += np.sin(2 * np.pi * (f + d) * s) + 0.2 * np.sin(4 * np.pi * (f + d) * s)
        y += 0.6 * np.sin(np.pi * f * s)
    pad[i0:i1] += y * env
pad = np.convolve(pad, np.ones(40) / 40, 'same'); pad /= np.abs(pad).max()

def kick():
    n = int(.42 * SR); s = np.arange(n) / SR; f = 45 + 95 * np.exp(-s * 28)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 7.5)).astype(np.float32)
def hat():
    n = int(.06 * SR); x = rng.standard_normal(n); x = x - np.convolve(x, np.ones(6) / 6, 'same')
    return (x * np.exp(-np.arange(n) / SR * 70) * .5).astype(np.float32)
def whoosh(dur=.8):
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float32); y = np.zeros(n, np.float32); acc = 0.; c = np.linspace(.02, .4, n) ** 1.4
    for i in range(n): acc += c[i] * (x[i] - acc); y[i] = acc
    return y * np.sin(np.linspace(0, np.pi, n)) ** 2
ritmo = np.zeros(N, np.float32); K = kick(); Hh = hat()
for k in range(int(DUR / B) + 1):
    tb = k * B
    batida = (3.0 <= tb < 12.0) or (16.8 <= tb < 22.2)
    if batida: put(ritmo, K, tb, .9)
    if batida and tb >= 6.6: put(ritmo, Hh, tb + B / 2, .55)
    if 22.8 <= tb < 23.4: put(ritmo, K, tb, .5); put(ritmo, K, tb + B / 2, .45)   # aceleração antes do impacto
# riser antes do clímax
n = int(1.8 * SR); s = np.arange(n) / SR; x = rng.standard_normal(n).astype(np.float32)
ris = np.zeros(n, np.float32); acc = 0.; c = np.linspace(.01, .6, n) ** 2
for i in range(n): acc += c[i] * (x[i] - acc); ris[i] = acc
ris = ris * (s / s[-1]) ** 2 * .9 + .25 * np.sin(2 * np.pi * np.cumsum(200 + 700 * (s / s[-1]) ** 2) / SR) * (s / s[-1]) ** 2
sfx = np.zeros(N, np.float32); put(sfx, ris[-int(.75 * SR):].astype(np.float32), 23.4 - .75)   # riser curto: não cobre o fim da fala
# impactos
def boom(g):
    n = int(2.2 * SR); s = np.arange(n) / SR; f = 32 + 60 * np.exp(-s * 6)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 1.9) * g + rng.standard_normal(n) * np.exp(-s * 9) * .25 * g).astype(np.float32)
put(sfx, boom(1.0), 23.4); put(sfx, boom(.55), 13.95); put(sfx, boom(.4), 3.0)
for c in [6.6, 8.85, 10.55, 12.0, 16.8]: put(sfx, whoosh(), c - .45, .28)

envv = np.convolve(np.abs(voz), np.ones(12000) / 12000, 'same')
ativo = np.convolve((envv > .01).astype(np.float32), np.ones(int(.45 * SR)))[:N] > 0   # segura o ducking 0,45 s após cada fala
duck = np.convolve(np.where(ativo, .4, 1.0), np.ones(16000) / 16000, 'same')
fade = np.clip(t / 1.0, 0, 1) * np.clip((DUR - t) / 1.6, 0, 1)
musica = (pad * .16 + ritmo * .5) * duck
mix = (voz * .95 + musica + sfx * .55) * fade
mix /= max(1., np.abs(mix).max() / .95)
with wave.open(D + '/mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok')
