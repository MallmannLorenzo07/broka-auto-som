"""Trilha original do motion Da Rota (30 s, 120 BPM), sintetizada do zero com numpy.

Cada compasso dura 2 s, então os cortes do vídeo caem no tempo da música.
Progressão C - G - Am - F (pop animado), com efeitos sincronizados às cenas.
Uso: python3 trilha.py  -> assets/trilha.wav e assets/trilha.mp3 (se houver ffmpeg)
"""
import os, subprocess, wave
import numpy as np

SR = 44100
DUR = 30.0
BPM = 120
BEAT = 60 / BPM
N = int(SR * DUR)
rng = np.random.default_rng(7)
HERE = os.path.dirname(os.path.abspath(__file__))

dry = np.zeros((N, 2))   # canal direto
send = np.zeros((N, 2))  # vai para o reverb
kicks = []               # instantes do bumbo (para o sidechain)


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(d):
    return np.arange(int(SR * d)) / SR


def add(sig, t0, gain=1.0, pan=0.0, rev=0.0):
    i = int(round(t0 * SR))
    if i >= N:
        return
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    st = np.stack([sig * l, sig * r], 1) * gain * np.sqrt(2)
    dry[i:i + len(sig)] += st
    if rev:
        send[i:i + len(sig)] += st * rev


def fft_filter(x, lo=None, hi=None, order=2):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR) + 1e-9
    g = np.ones_like(f)
    if hi:
        g /= np.sqrt(1 + (f / hi) ** (2 * order))
    if lo:
        g /= np.sqrt(1 + (lo / f) ** (2 * order))
    return np.fft.irfft(X * g, len(x))


def sweep_noise(d, f0, f1, q=1.4):
    """Ruído com filtro passa-faixa que varre de f0 a f1 (whoosh / riser)."""
    n = int(SR * d)
    out = np.zeros(n)
    hop = 1024
    win = np.hanning(hop * 2)
    noise = rng.standard_normal(n + hop * 2)
    for s in range(0, n, hop):
        k = s / max(n - 1, 1)
        fc = f0 * (f1 / f0) ** k
        seg = fft_filter(noise[s:s + hop * 2] * win, lo=fc / q, hi=fc * q)
        e = min(n, s + hop * 2)
        out[s:e] += seg[: e - s]
    return out / (np.abs(out).max() + 1e-9)


def saw(f, d, harm=14, detune=0.0):
    t = tt(d)
    out = np.zeros_like(t)
    for k in range(1, harm + 1):
        if f * k > 15000:
            break
        out += np.sin(2 * np.pi * f * k * (1 + detune) * t + k) / k
    return out


def env(d, a=0.005, dec=0.2, sus=0.0, rel=0.05):
    t = tt(d)
    e = np.where(t < a, t / a, sus + (1 - sus) * np.exp(-(t - a) / dec))
    r = int(rel * SR)
    if r and len(e) > r:
        e[-r:] *= np.linspace(1, 0, r)
    return e


# ---------- instrumentos ----------
def kick(t0, g=1.0):
    d = 0.45
    t = tt(d)
    f = 45 + 110 * np.exp(-t / 0.035)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t / 0.16)
    s[:200] += rng.standard_normal(200) * np.linspace(.6, 0, 200)
    add(np.tanh(s * 1.6), t0, 0.9 * g)
    kicks.append(t0)


def clap(t0, g=1.0):
    d = 0.35
    n = rng.standard_normal(int(SR * d))
    n = fft_filter(n, lo=900, hi=2600)
    t = tt(d)
    e = np.exp(-t / 0.06)
    for off in (0.0, 0.011, 0.022):
        e += np.where(t >= off, np.exp(-(t - off) / 0.006), 0) * 0.7
    add(n * e / 3, t0 - 0.022, 0.55 * g, 0.0, rev=0.35)


def hat(t0, open_=False, g=1.0, pan=0.0):
    d = 0.22 if open_ else 0.06
    n = fft_filter(rng.standard_normal(int(SR * d)), lo=7000)
    n *= np.exp(-tt(d) / (0.07 if open_ else 0.015))
    add(n, t0, (0.32 if open_ else 0.2) * g, pan)


def snare(t0, g=1.0):
    d = 0.18
    t = tt(d)
    n = fft_filter(rng.standard_normal(len(t)), lo=1500, hi=9000) * np.exp(-t / 0.05)
    tone = np.sin(2 * np.pi * 190 * t) * np.exp(-t / 0.04)
    add(n * .8 + tone * .5, t0, 0.42 * g, 0, rev=0.2)


def bass(t0, m, d, g=1.0):
    s = saw(hz(m), d, harm=10) * 0.55 + np.sin(2 * np.pi * hz(m) * tt(d)) * 0.8
    s = fft_filter(s, hi=900)
    add(s * env(d, 0.004, 0.18, 0.55, 0.03), t0, 0.42 * g)


def stab(t0, notes, d=0.24, g=1.0):
    s = sum(saw(hz(m), d, 16, dt) for m in notes for dt in (-0.006, 0, 0.006))
    s = fft_filter(s, hi=3200)
    s *= env(d, 0.003, 0.09, 0.2, 0.04)
    add(s, t0, 0.075 * g, -0.25, rev=0.35)
    add(s, t0 + 0.012, 0.075 * g, 0.25, rev=0.35)


def pad(t0, notes, d, g=1.0):
    s = sum(saw(hz(m), d, 6, dt) for m in notes for dt in (-0.004, 0.004))
    s = fft_filter(s, hi=1400)
    a = min(0.4, d / 3)
    s *= env(d, a, 99, 1.0, min(0.5, d / 3))
    add(s, t0, 0.04 * g, 0, rev=0.5)


def pluck(t0, m, g=1.0, pan=0.0):
    d = 0.32
    t = tt(d)
    f = hz(m)
    s = (np.sign(np.sin(2 * np.pi * f * t)) * 0.4 + np.sin(2 * np.pi * f * t)) * np.exp(-t / 0.09)
    s = fft_filter(s, hi=4500)
    add(s, t0, 0.12 * g, pan, rev=0.25)
    add(s, t0 + BEAT * 0.75, 0.05 * g, -pan, rev=0.25)  # eco pontuado


def impact(t0, g=1.0):
    d = 2.2
    t = tt(d)
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t / 0.08)) / SR) * np.exp(-t / 0.55)
    crash = fft_filter(rng.standard_normal(len(t)), lo=3000) * np.exp(-t / 0.7) * 0.35
    add(np.tanh(boom * 1.4) * 0.9 + crash, t0, 0.8 * g, 0, rev=0.4)


def whoosh(tc, d=0.5, g=1.0, up=True):
    s = sweep_noise(d, 400 if up else 5000, 5000 if up else 400)
    e = np.sin(np.pi * np.linspace(0, 1, len(s))) ** 1.5
    pan = np.linspace(-0.8, 0.8, len(s))
    i = int((tc - d / 2) * SR)
    for ch, w in ((0, np.cos((pan + 1) * np.pi / 4)), (1, np.sin((pan + 1) * np.pi / 4))):
        seg = s * e * w * 0.38 * g
        a = max(i, 0)
        dry[a:i + len(seg), ch] += seg[a - i:][: N - a]
        send[a:i + len(seg), ch] += seg[a - i:][: N - a] * 0.3


def pop(t0, m=84, g=1.0):
    d = 0.12
    t = tt(d)
    f = hz(m) * (1 + 0.6 * np.exp(-t / 0.01))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.035)
    add(s, t0, 0.22 * g, 0, rev=0.2)


def horn(t0, d=0.16):
    s = (saw(311, d, 12) + saw(392, d, 12)) * env(d, 0.01, 99, 1, 0.03)
    add(fft_filter(s, lo=200, hi=2500), t0, 0.12, 0.3, rev=0.15)


def riser(t0, d, g=1.0):
    s = sweep_noise(d, 300, 7000, 1.6) * np.linspace(0, 1, int(SR * d)) ** 2
    t = tt(d)
    tone = np.sin(2 * np.pi * np.cumsum(200 * (8 ** (t / d))) / SR) * (t / d) ** 2 * 0.25
    add(s * 0.5 + tone, t0, 0.5 * g, 0, rev=0.3)


# ---------- arranjo ----------
CH = {  # acordes (voicing) e baixo
    'C': ([60, 64, 67], 36), 'G': ([59, 62, 67], 43),
    'Am': ([57, 60, 64], 45), 'F': ([57, 60, 65], 41),
}
prog = ['C', 'G', 'Am', 'F']


def chord_at(t):
    if t < 2:
        return 'F' if t < 1 else 'G'
    if t >= 26:
        return 'C' if t < 28 else 'G'
    return prog[int((t - 2) // 2) % 4]


def groove(a, b, kick_on=True, lead=True, closed=True):
    t = a
    while t < b - 1e-6:
        beat = round((t - 2) / BEAT)
        name = chord_at(t)
        notes, root = CH[name]
        if kick_on:
            kick(t)
        if beat % 2 == 1 or not kick_on and beat % 4 == 3:
            clap(t)
        hat(t + BEAT / 2, open_=True, pan=0.2)
        if closed:
            for k in (1, 3):
                hat(t + k * BEAT / 4, g=0.8, pan=-0.3)
        # baixo em colcheias, pulsando
        bass(t + BEAT / 2, root, BEAT / 2 * 0.9)
        bass(t, root - 12 if beat % 2 == 0 else root, BEAT / 2 * 0.8, 0.7)
        stab(t + BEAT / 2, [n + 12 for n in notes], g=0.9)
        if lead:
            arp = [notes[0] + 12, notes[2] + 12, notes[1] + 12, notes[2] + 12]
            for k in range(4):
                if not (beat % 2 == 1 and k == 3):
                    pluck(t + k * BEAT / 4, arp[k] + (12 if k == 0 and beat % 4 == 2 else 0), pan=0.3 if k % 2 else -0.3)
        t += BEAT


# intro 0–2: pad + chimbal crescente + virada + riser
pad(0, [53, 57, 60, 65], 1.0, 2.6)
pad(1, [55, 59, 62, 67], 1.0, 2.6)
for k in range(16):
    hat(k * BEAT / 4, g=0.25 + k / 20, pan=-0.2)
for k in range(8):
    snare(1 + k * BEAT / 4, 0.25 + k * 0.09)
riser(0, 2.0, 1.3)
pop(0.05, 72, 0.6)
pop(1.15, 76, 0.6)
bass(0, 41, 0.9, 0.6); bass(1, 43, 0.9, 0.6)

# drop 2 – 18
impact(2.0, 1.1)
groove(2, 4, lead=False, closed=False)
groove(4, 18)
for t in range(2, 18, 2):
    pad(t, CH[chord_at(t)][0], 2.0, 0.8)

# transições
for t in (4, 6, 8, 9, 14, 18, 24):
    whoosh(t, 0.5)
for t in (5, 7):
    whoosh(t, 0.3, 0.7, up=False)
impact(12.0, 0.7)
for i, t in enumerate((9.25, 9.5, 9.75, 10.0)):
    pop(t, 79 + i * 2)
pop(10.3, 91, 1.2)
horn(14.7); horn(14.92)
kick(17.0, 1.1)
for i, m in enumerate((84, 88, 91, 96)):  # "plim" de entregue
    pop(17.05 + i * 0.06, m, 0.8)

# 18–20: respiro (sem bumbo) + notificações do chat + virada
groove(18, 19, kick_on=False, lead=False, closed=False)
pad(18, CH['Am'][0], 2.0, 1.1)
for t in (18.4, 18.85, 19.3):
    pop(t, 88); pop(t + 0.06, 93)
for k in range(8):
    snare(19 + k * BEAT / 4, 0.3 + k * 0.1)
riser(18.8, 1.2, 0.7)
bass(19, 45, 0.9, 0.6)

# 20–29: volta tudo
impact(20.0, 1.0)
groove(20, 29)
for t in range(20, 28, 2):
    pad(t, CH[chord_at(t)][0], 2.0, 0.8)
pad(28, CH['G'][0], 1.0, 0.8)
for t in (20.5, 21.0, 21.5, 22.0):
    pop(t, 86, 0.8)
impact(26.0, 1.1)

# final: acorde de C sustentado
impact(29.0, 1.0)
kick(29.0, 1.1)
pad(29.0, [48, 55, 60, 64, 67, 72], 1.0, 2.2)
stab(29.0, [72, 76, 79], d=0.9, g=1.4)
bass(29.0, 36, 0.95, 1.0)

# ---------- sidechain, reverb, master ----------
sc = np.ones(N)
t = np.arange(N) / SR
for k in kicks:
    i = int(k * SR)
    j = min(N, i + int(0.3 * SR))
    sc[i:j] = np.minimum(sc[i:j], 1 - 0.55 * np.exp(-(t[i:j] - k) / 0.1))

ir_len = int(1.6 * SR)
ir = rng.standard_normal((ir_len, 2)) * np.exp(-np.arange(ir_len) / SR / 0.45)[:, None]
ir = np.stack([fft_filter(ir[:, c], lo=250, hi=6000) for c in range(2)], 1)
ir /= np.sqrt((ir ** 2).sum(0))
L = 1 << int(np.ceil(np.log2(N + ir_len)))
wet = np.stack([np.fft.irfft(np.fft.rfft(send[:, c], L) * np.fft.rfft(ir[:, c], L), L)[:N] for c in range(2)], 1)

mix = dry + wet * 0.5
mix[:, 0] *= 0.35 + 0.65 * sc  # leve bombeado geral
mix[:, 1] *= 0.35 + 0.65 * sc
mix = fft_filter(mix[:, 0], lo=28), fft_filter(mix[:, 1], lo=28)
mix = np.stack(mix, 1)
mix /= np.abs(mix).max()
mix = np.tanh(mix * 1.6) / np.tanh(1.6)       # saturação / limitador suave
fade = int(0.35 * SR)
mix[-fade:] *= np.linspace(1, 0, fade)[:, None] ** 2
mix *= 0.66

out = os.path.join(HERE, 'assets', 'trilha.wav')
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 32767).astype('<i2').tobytes())
print('ok ->', out)
try:
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-b:a', '192k',
                    os.path.join(HERE, 'assets', 'trilha.mp3')], check=True)
    print('ok -> assets/trilha.mp3')
except (OSError, subprocess.CalledProcessError):
    pass
