"""Áudio do pitch VAGALUME (60 s): narração ElevenLabs + trilha sintetizada aqui.
Relógio no gancho, tensão no "pico e queda", sininho + impacto na revelação, groove a 100 BPM na apresentação,
trilha despida no "outro lado" e retorno no fecho."""
import os, json, wave, numpy as np
from corte import ler, SR
D = os.path.dirname(os.path.abspath(__file__)); P = json.load(open(D + '/plano.json')); T = P['T']
DUR = T['fim']; N = int(DUR * SR); t = np.arange(N) / SR; rng = np.random.default_rng(11)
def put(dst, x, at, g=1.0):
    i = int(at * SR); n = min(len(x), N - i)
    if n > 0 and i >= 0: dst[i:i + n] += x[:n] * g
def env(a, b, ra=.8, rb=.8):  # envelope liga em a, desliga em b
    return np.clip((t - a) / ra, 0, 1) * np.clip((b - t) / rb, 0, 1)

voz = np.zeros(N, np.float32)
for k, at in enumerate(P['vo']): put(voz, ler(f'{D}/../vo/{k}.wav'), at)
voz = np.tanh(voz * 1.2) / np.tanh(1.2)

B = .6   # 100 BPM
# acordes (Fá menor → Ré bemol → Lá bemol → Mi bemol)
AC = [[174.61, 207.65, 261.63], [138.59, 174.61, 207.65], [207.65, 261.63, 311.13], [155.56, 196.0, 233.08]]
def pad_track(oct=1.0):
    y = np.zeros(N, np.float32); L = 8 * B
    for j in range(int(DUR // L) + 1):
        a = AC[j % 4]; i0 = int(j * L * SR); i1 = min(N, int((j + 1) * L * SR + SR)); s = t[i0:i1] - j * L
        e = np.clip(s / 1.2, 0, 1) * np.clip((L + 1 - s) / 1.2, 0, 1); z = np.zeros_like(s)
        for f in a:
            for d in (-.8, .8): z += np.sin(2 * np.pi * (f * oct + d) * s) + .2 * np.sin(4 * np.pi * (f * oct + d) * s)
        y[i0:i1] += z * e
    y = np.convolve(y, np.ones(50) / 50, 'same'); return y / np.abs(y).max()
pad = pad_track()
sub = np.zeros(N, np.float32)
for j in range(int(DUR // (8 * B)) + 1):
    f = AC[j % 4][0] / 2; i0 = int(j * 8 * B * SR); i1 = min(N, int((j + 1) * 8 * B * SR)); s = t[i0:i1] - j * 8 * B
    sub[i0:i1] = np.sin(2 * np.pi * f * s) * np.clip(s / .05, 0, 1)

def kick(g=1.):
    n = int(.45 * SR); s = np.arange(n) / SR; f = 45 + 110 * np.exp(-s * 30)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 8) * g).astype(np.float32)
def clap():
    n = int(.25 * SR); s = np.arange(n) / SR; x = rng.standard_normal(n)
    e = sum(np.exp(-np.clip(s - d, 0, None) * 40) * (s >= d) for d in (0, .012, .024)) * np.exp(-s * 12)
    x = x - np.convolve(x, np.ones(4) / 4, 'same'); return (x * e * .5).astype(np.float32)
def hat(o=False):
    n = int((.18 if o else .05) * SR); x = rng.standard_normal(n); x = x - np.convolve(x, np.ones(6) / 6, 'same')
    return (x * np.exp(-np.arange(n) / SR * (18 if o else 75)) * .35).astype(np.float32)
def pluck(f, dur=.9, k=5.):
    n = int(dur * SR); s = np.arange(n) / SR
    return ((np.sin(2 * np.pi * f * s) + .4 * np.sin(4 * np.pi * f * s) + .15 * np.sin(6 * np.pi * f * s)) * np.exp(-s * k) * np.clip(s / .003, 0, 1)).astype(np.float32)
def sino(f):
    n = int(2.5 * SR); s = np.arange(n) / SR
    return (sum(np.sin(2 * np.pi * f * m * s) * a for m, a in [(1, 1), (2.76, .5), (5.4, .25), (8.9, .1)]) * np.exp(-s * 2.2)).astype(np.float32)
def tique():
    n = int(.03 * SR); s = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2400 * s) * np.exp(-s * 300)).astype(np.float32)
def whoosh(dur=.9, sobe=True):
    n = int(dur * SR); x = rng.standard_normal(n).astype(np.float32); y = np.zeros(n, np.float32); acc = 0.
    c = np.linspace(.02, .35, n) ** 1.4 if sobe else np.linspace(.35, .02, n) ** 1.4
    for i in range(n): acc += c[i] * (x[i] - acc); y[i] = acc
    return y * np.sin(np.linspace(0, np.pi, n)) ** 2
def boom(g):
    n = int(2.6 * SR); s = np.arange(n) / SR; f = 32 + 70 * np.exp(-s * 6)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-s * 1.6) * g + rng.standard_normal(n) * np.exp(-s * 10) * .2 * g).astype(np.float32)
def sweep(f0, f1, dur, g=1.):
    n = int(dur * SR); s = np.arange(n) / SR; f = f0 * (f1 / f0) ** (s / dur)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.linspace(0, np.pi, n)) * g).astype(np.float32)

bat = np.zeros(N, np.float32); arp = np.zeros(N, np.float32); fx = np.zeros(N, np.float32)
# 1) relógio
for k in range(int(T['s2'] / .5) + 1): put(fx, tique(), .4 + k * .5, .5 if k % 2 == 0 else .3)
# 2) tensão: batida de coração + sobe no pico + despenca na queda
for k in range(12):
    tb = T['s2'] + .3 + k * .75
    if tb < T['s3'] - .3: put(bat, kick(.7), tb); put(bat, kick(.45), tb + .22)
put(fx, sweep(120, 900, T['queda'] - T['pico'] + .3, .25), T['pico'])
put(fx, sweep(700, 60, 1.3, .35), T['queda'] + .5)
# 3) revelação: silêncio, sininhos subindo, impacto
for j, f in enumerate([1046.5, 1318.5, 1568.0, 2093.0, 2637.0]): put(fx, sino(f), T['junta'] + .25 * j, .18)
put(fx, whoosh(1.4), T['lata'] - 1.3, .35); put(fx, boom(1.0), T['lata']); put(fx, sino(1568.0), T['nome'], .25)
# 4–6) groove da apresentação; 7) despido; 8) volta
for k in range(int(DUR / B) + 2):
    tb = k * B; bar = k % 4
    groove = T['s4'] - .05 <= tb < T['s7'] - .3 or T['s8'] + .3 <= tb < DUR - 3
    if groove:
        put(bat, kick(.9 if bar in (0, 2) else .0), tb)
        if bar in (1, 3): put(bat, clap(), tb, .55)
        put(bat, hat(), tb + B / 2, .5); put(bat, hat(), tb, .25)
        if bar == 3: put(bat, hat(True), tb + B * .75, .3)
    if T['s3'] + 1.5 <= tb < DUR - 3 and not (T['s7'] - .3 <= tb < T['s8']):
        nt = AC[int(tb // (8 * B)) % 4]
        for h in range(2): put(arp, pluck(nt[(k * 2 + h) % 3] * 4, .5, 7.), tb + h * B / 2, .5)
    if T['s7'] <= tb < T['s8'] - .5:
        nt = AC[int(tb // (8 * B)) % 4]
        if k % 2 == 0: put(arp, pluck(nt[(k // 2) % 3] * 2, 1.6, 2.5), tb, .9)
for c in ['s2', 's4', 's5', 's6', 's7', 's8']: put(fx, whoosh(), T[c] - .45, .25)
put(fx, boom(.4), T['s8'] + .2); put(fx, sino(2093.0), T['s8'] + .3, .2)
for c in ['k1', 'k2', 'k3', 'k4', 'c1', 'c2', 'c3', 'c4', 'i1', 'i2', 'i3']: put(fx, pluck(1760, .3, 18), T[c], .12)

# níveis por trecho
trilha = (pad * (.10 + .08 * env(T['s3'], DUR + 1)) + sub * .12 * env(T['s4'], T['s7'], .3, .3)
          + sub * .12 * env(T['s8'], DUR - 2, .3, 1.5)) * (1 - .55 * env(T['s2'], T['s3'], .3, .3))
envv = np.convolve(np.abs(voz), np.ones(12000) / 12000, 'same')
ativo = np.convolve((envv > .01).astype(np.float32), np.ones(int(.45 * SR)))[:N] > 0
duck = np.convolve(np.where(ativo, .42, 1.0), np.ones(16000) / 16000, 'same')
fade = np.clip(t / 1.0, 0, 1) * np.clip((DUR - t) / 2.2, 0, 1)
musica = (trilha + bat * .42 + arp * .07) * duck
mix = (voz * .95 + musica + fx * .5) * fade
mix /= max(1., np.abs(mix).max() / .95)
with wave.open(D + '/mix.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
print('ok', DUR)
