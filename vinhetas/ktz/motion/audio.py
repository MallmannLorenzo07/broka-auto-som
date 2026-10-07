"""Áudio do motion KTZ (~60 s): narração (Chatterbox, voz clonada de narrador LibriVox em domínio público) +
trilha sintetizada aqui: pad em Ré maior (Dmaj7 → Bm7 → Gmaj7 → A), pulso suave a 84 BPM, arpejo, whooshes e impacto final."""
import os, json, wave, numpy as np
from corte import ler, SR
D = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(D + '/plano.json')); T = P['T']
DUR = T['fim']; N = int(DUR * SR); t = np.arange(N) / SR; rng = np.random.default_rng(7)
def put(dst, x, at, g=1.0):
    i = int(at * SR); n = min(len(x), N - i)
    if n > 0: dst[i:i + n] += x[:n] * g

voz = np.zeros(N, np.float32)
for k, at in enumerate(P['vo']):
    if at is not None: put(voz, ler(f"{D}/../{os.environ.get('VODIR', 'vo')}/{k}.wav"), at)
voz = np.tanh(voz * 1.2) / np.tanh(1.2)

B = 60 / 84
acordes = [[146.83, 185.0, 220.0, 277.18], [123.47, 146.83, 185.0, 220.0], [98.0, 146.83, 196.0, 246.94], [110.0, 164.81, 220.0, 277.18]]
pad = np.zeros(N, np.float32); L = 8 * B
for j in range(int(DUR // L) + 1):
    a = acordes[j % 4]; i0 = int(j * L * SR); i1 = min(N, int((j + 1) * L * SR + 1.5 * SR))
    s = t[i0:i1] - j * L; env = np.clip(s / 1.8, 0, 1) * np.clip((L + 1.5 - s) / 1.8, 0, 1); y = np.zeros_like(s)
    for f in a:
        for d in (-.6, .6): y += np.sin(2 * np.pi * (f + d) * s) + .15 * np.sin(4 * np.pi * (f + d) * s)
        y += .5 * np.sin(np.pi * f * s)
    pad[i0:i1] += y * env
pad = np.convolve(pad, np.ones(60) / 60, 'same'); pad /= np.abs(pad).max()

def kick():
    n = int(.5 * SR); s = np.arange(n) / SR; f = 42 + 80 * np.exp(-s * 26)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 7)).astype(np.float32)
def hat():
    n = int(.05 * SR); x = rng.standard_normal(n); x = x - np.convolve(x, np.ones(6) / 6, 'same')
    return (x * np.exp(-np.arange(n) / SR * 80) * .4).astype(np.float32)
def pluck(f):
    n = int(1.2 * SR); s = np.arange(n) / SR
    return ((np.sin(2 * np.pi * f * s) + .3 * np.sin(4 * np.pi * f * s) + .1 * np.sin(6 * np.pi * f * s)) * np.exp(-s * 4.5) * np.clip(s / .004, 0, 1)).astype(np.float32)
def whoosh(dur=1.0):
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float32); y = np.zeros(n, np.float32); acc = 0.; c = np.linspace(.02, .3, n) ** 1.4
    for i in range(n): acc += c[i] * (x[i] - acc); y[i] = acc
    return y * np.sin(np.linspace(0, np.pi, n)) ** 2
def boom(g):
    n = int(3.0 * SR); s = np.arange(n) / SR; f = 30 + 50 * np.exp(-s * 5)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 1.4) * g + rng.standard_normal(n) * np.exp(-s * 8) * .15 * g).astype(np.float32)

ritmo = np.zeros(N, np.float32); arp = np.zeros(N, np.float32); K = kick(); H = hat()
notas = [[293.66, 369.99, 440.0, 554.37], [246.94, 293.66, 369.99, 440.0], [196.0, 293.66, 392.0, 493.88], [220.0, 329.63, 440.0, 554.37]]
for k in range(int(DUR / B) + 1):
    tb = k * B
    if T['s3'] - .1 <= tb < T['s10'] - B: put(ritmo, K, tb, .55 if k % 2 == 0 else .35)
    if T['s5'] <= tb < T['s9']: put(ritmo, H, tb + B / 2, .45)
    if T['s2'] <= tb < T['s10'] - B:
        nt = notas[int(tb // L) % 4]
        for h in range(2): put(arp, pluck(nt[(2 * k + h) % 4] * 2), tb + h * B / 2, .5)
sfx = np.zeros(N, np.float32)
for c in ['s2', 's3', 's4', 's5', 's6', 's7', 's8', 's9']: put(sfx, whoosh(), T[c] - .5, .22)
put(sfx, boom(.5), T['s3']); put(sfx, boom(.9), T['s10'])
put(sfx, boom(.35), T['s8'])

envv = np.convolve(np.abs(voz), np.ones(12000) / 12000, 'same')
ativo = np.convolve((envv > .01).astype(np.float32), np.ones(int(.45 * SR)))[:N] > 0
duck = np.convolve(np.where(ativo, .4, 1.0), np.ones(16000) / 16000, 'same')
fade = np.clip(t / 1.2, 0, 1) * np.clip((DUR - t) / 2.0, 0, 1)
musica = (pad * .15 + ritmo * .42 + arp * .06) * duck
mix = (voz * .95 + musica + sfx * .5) * fade
mix /= max(1., np.abs(mix).max() / .95)
with wave.open(D + '/mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok', round(DUR, 2), 's')
