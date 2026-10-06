"""Monta a linha do tempo (sincroniza animação com a narração), a música, os efeitos e a mixagem final."""
import json, sys, numpy as np, soundfile as sf
from scipy import signal

SP = sys.argv[1]
VO = f"{SP}/audio/vo"
SR = 44100
FPS = 30
DUR_ANIM = 24.0
rng = np.random.default_rng(7)

# ---------------- linha do tempo ----------------
meta = json.load(open(f"{VO}/meta.json"))
SYNC = {"c2b": 3.95, "c2c": 4.55}          # alinhado com as "pancadas" da cena 2
for m in meta:
    m["cue"] = SYNC.get(m["key"], m["cue"])
BOUNDS = [3.1, 6.3, 12.2, 16.8, 19.9]

events = [(m["cue"], "line", m) for m in meta] + [(b, "bound", None) for b in BOUNDS]
events.sort(key=lambda e: e[0])
keys = [(0.0, 0.0)]
last_end = 0.0
for a, kind, m in events:
    pa, po = keys[-1]
    o = po + (a - pa)
    if kind == "line":
        o = max(o, last_end + 0.12)
        m["out"] = o
        last_end = o + m["dur"]
    else:
        o = max(o, last_end + 0.25)
    keys.append((a, o))
pa, po = keys[-1]
keys.append((DUR_ANIM, max(po + (DUR_ANIM - pa), last_end + 1.6)))
KA = np.array([k[0] for k in keys]); KO = np.array([k[1] for k in keys])
OUT_DUR = float(KO[-1])
def a2o(a): return float(np.interp(a, KA, KO))
def o2a(o): return float(np.interp(o, KO, KA))
N = int(round(OUT_DUR * FPS))
json.dump([round(o2a(i / FPS), 4) for i in range(N)], open(f"{SP}/ad/timeline.json", "w"))
print("duração final: %.2f s, %d quadros" % (OUT_DUR, N))
for m in meta: print(f'  {m["key"]}: {m["out"]:.2f}s  "{m["text"]}"')

L = int(OUT_DUR * SR) + SR
def T(n): return np.arange(n) / SR
def place(buf, x, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]
    if x.ndim == 1:
        lg, rg = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        x = np.stack([x * lg, x * rg], 1) * np.sqrt(2)
    buf[i:i + len(x)] += x * gain
def lp(x, fc, order=2): return signal.sosfilt(signal.butter(order, fc, "low", fs=SR, output="sos"), x, axis=0)
def hp(x, fc, order=2): return signal.sosfilt(signal.butter(order, fc, "high", fs=SR, output="sos"), x, axis=0)
def bp(x, lo, hi, order=2): return signal.sosfilt(signal.butter(order, [lo, hi], "band", fs=SR, output="sos"), x, axis=0)
def env(n, a, d):
    t = T(n); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-np.maximum(0, t - a) / d)
def reverb(x, sec=1.6, mix=0.25):
    n = int(sec * SR); ir = rng.standard_normal((n, 2)) * np.exp(-T(n) / (sec / 6))[:, None]
    ir = lp(ir, 6000); ir /= np.abs(ir).sum(0) ** 0.5 * 4
    if x.ndim == 1: x = np.stack([x, x], 1)
    wet = np.stack([signal.fftconvolve(x[:, c], ir[:, c])[: len(x)] for c in range(2)], 1)
    return x * (1 - mix) + wet * mix
def saw(f, n, det=0.0):
    ph = np.cumsum(np.full(n, f * (1 + det)) / SR) + rng.random()
    return 2 * (ph % 1) - 1

# ---------------- música (128 BPM, Lá menor) ----------------
BPM = 128; BEAT = 60 / BPM; BAR = 4 * BEAT
drop = a2o(3.1)            # a batida entra na cena 2
end_hit = a2o(19.9)        # pancada na cena final
music = np.zeros((L, 2))
def note(n): return 440 * 2 ** ((n - 69) / 12)
PROG = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [64, 67, 72]), (55, [62, 67, 71])]  # Am F C G

def kick():
    n = int(.45 * SR); t = T(n); f = 45 + 110 * np.exp(-t * 28)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    x[:200] += rng.standard_normal(200) * np.linspace(.6, 0, 200)
    return np.tanh(x * 1.6)
def clap():
    n = int(.3 * SR); x = bp(rng.standard_normal(n), 900, 4500) * 3
    e = sum(env(n, .001, .012) * (np.arange(n) >= int(d * SR)) for d in (0, .012, .024)) + env(n, .03, .09) * .8
    return x * e
def hat(open_=False):
    n = int((.18 if open_ else .05) * SR); return hp(rng.standard_normal(n), 7000) * env(n, .001, .06 if open_ else .015)
def bassnote(f, d):
    n = int(d * SR); x = lp(saw(f, n) + saw(f, n, .005), 420, 2) + np.sin(2 * np.pi * f / 2 * T(n)) * .6
    return x * env(n, .005, d * .9)
def chord(notes, d, fc):
    n = int(d * SR); x = sum(saw(note(k), n, dt) for k in notes for dt in (-.006, 0, .006)) / 9
    return lp(x, fc, 2) * np.minimum(1, T(n) / .08) * np.minimum(1, (d - T(n)) / .15).clip(0)
def pluck(f, d=.22):
    n = int(d * SR); x = saw(f, n) * .5 + np.sign(np.sin(2 * np.pi * f * T(n))) * .3
    return lp(x, 3500, 2) * env(n, .002, .07)

pump = np.ones(L)          # "sidechain" da batida
t = 0.0; bar = 0
while t < OUT_DUR + BAR:
    root, ch = PROG[bar % 4]
    pre = t < drop
    # pad e arpejo o tempo todo (filtrado na introdução)
    fc = 900 + 3000 * min(1, t / max(drop, .1)) if pre else 3800
    place(music, chord(ch, BAR, fc), t, .16 if pre else .13, 0)
    for s in range(16):
        k = ch[[0, 1, 2, 1][s % 4]] + (12 if s % 8 >= 4 else 0)
        place(music, pluck(note(k)), t + s * BEAT / 4, .07 if pre else .06, (-.4, .4)[s % 2])
    if not pre:
        for b in range(4):
            tb = t + b * BEAT
            place(music, kick(), tb, .55)
            i = int(tb * SR); n = int(BEAT * SR)
            if i < L: pump[i:i + n] = np.minimum(pump[i:i + n], (1 - .55 * np.exp(-T(n)[: L - i] / .09))[:n])
            if b in (1, 3): place(music, clap(), tb, .32)
            place(music, hat(), tb + BEAT / 2, .16, .3)
            place(music, hat(), tb + BEAT / 4, .06, -.3); place(music, hat(), tb + 3 * BEAT / 4, .06, -.3)
            for e8 in range(2):
                place(music, bassnote(note(root - 12), BEAT / 2 * .9), tb + e8 * BEAT / 2, .30)
    t += BAR; bar += 1
music[:, 0] *= pump; music[:, 1] *= pump

# subida antes da batida entrar
n = int(drop * SR) if drop < 4 else int(2.5 * SR)
r = bp(rng.standard_normal(n), 2000, 9000) * np.linspace(0, 1, n) ** 2
place(music, r, drop - n / SR, .18)
# final: corta a batida, deixa só um acorde longo com cauda
fade_at = OUT_DUR - 1.4
i = int(fade_at * SR)
music[i:] *= np.exp(-T(L - i) / .25)[:, None]
place(music, reverb(chord([57, 64, 69, 72], 2.5, 2500), 2.5, .45), fade_at, .35)
music = reverb(music, 1.2, .12)

# ---------------- efeitos ----------------
sfx = np.zeros((L, 2))
def whoosh(d=.75, lo=300, hi=5000):
    n = int(d * SR); x = rng.standard_normal(n); out = np.zeros(n); y = 0.0
    fc = lo * (hi / lo) ** np.sin(np.linspace(0, np.pi, n))
    al = 1 - np.exp(-2 * np.pi * fc / SR)
    for k in range(n): y += al[k] * (x[k] - y); out[k] = y
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    pan = np.linspace(-.8, .8, n)
    return np.stack([out * e * np.cos((pan + 1) * np.pi / 4), out * e * np.sin((pan + 1) * np.pi / 4)], 1) * 2.2
def impact(d=1.2):
    n = int(d * SR); t = T(n)
    x = np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-t * 18)) / SR) * np.exp(-t * 3.2)
    x += lp(rng.standard_normal(n), 1800) * np.exp(-t * 14) * .8
    return reverb(np.tanh(x * 1.4), 1.8, .3)
def pop(f0=1000, f1=320):
    n = int(.09 * SR); t = T(n); f = f1 + (f0 - f1) * np.exp(-t * 60)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .002, .03)
def tap():
    n = int(.04 * SR); return (np.sin(2 * np.pi * 2200 * T(n)) * .5 + hp(rng.standard_normal(n), 3000)) * env(n, .0005, .008)
def tick():
    n = int(.02 * SR); return hp(rng.standard_normal(n), 4000) * env(n, .0003, .004)
def ding():
    n = int(.8 * SR); t = T(n)
    x = (np.sin(2 * np.pi * 1318.5 * t) * env(n, .002, .25) + .7 * np.sin(2 * np.pi * 1975.5 * t) * env(n, .002, .3) * (t > .09))
    return reverb(x, 1.2, .3)
def rise(d=.6):
    n = int(d * SR); t = T(n); f = 200 * (8 ** (t / d))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * (t / d) ** 2 * .5

# transições (cortinas): o meio da cortina cai na fronteira da cena
for b in BOUNDS:
    w = whoosh(); place(sfx, w, a2o(b) - len(w) / SR / 2, .55)
    place(sfx, impact(.7), a2o(b) + .02, .22)
# cena 1
w = whoosh(.6, 400, 6000); place(sfx, w, 0.0, .45)                  # faixa vermelha
place(sfx, whoosh(.5, 600, 4000), a2o(.35), .3)                       # logo girando
place(sfx, impact(), a2o(.7), .36); place(sfx, impact(), a2o(1.0), .35)
place(sfx, pop(700, 250), a2o(1.5), .35)
# cena 2: pancadas
for h in (3.35, 3.95, 4.55): place(sfx, impact(), a2o(h), .38)
place(sfx, whoosh(.5, 800, 3000), a2o(5.1), .2)
# cena 3: celular sobe, rolagem e balões
place(sfx, whoosh(.9, 200, 2500), a2o(6.5), .5)
for s in (7.6, 9.1, 10.6): place(sfx, whoosh(.6, 1500, 6000), a2o(s), .12)
for c in (8.45, 9.95, 11.45): place(sfx, pop(), a2o(c), .5)
# cena 4: chips, toques, mensagem
for i in range(10): place(sfx, tick(), a2o(12.5 + i * .06), .25, (-.5, .5)[i % 2])
for tp in (13.35, 13.8, 14.25): place(sfx, tap(), a2o(tp), .7); place(sfx, pop(1200, 600), a2o(tp) + .01, .25)
place(sfx, whoosh(.5, 500, 4000), a2o(14.55), .35)
t0, t1 = a2o(14.9), a2o(16.2); tt = t0
while tt < t1: place(sfx, tick(), tt, .18, rng.uniform(-.3, .3)); tt += rng.uniform(.045, .08)
place(sfx, ding(), t1 + .05, .35)
# cena 5: barras e troca
place(sfx, rise(.7), a2o(17.45), .18)
place(sfx, tap(), a2o(18.45), .7); place(sfx, rise(.6), a2o(18.5), .15)
# cena 6
place(sfx, whoosh(.6, 400, 6000), a2o(19.95), .4)
place(sfx, impact(1.6), a2o(20.35), .4)
for c in (20.9, 22.0): place(sfx, pop(900, 300), a2o(c), .45)
place(sfx, whoosh(.4, 1000, 5000), a2o(21.3), .25)

# ---------------- narração ----------------
vo = np.zeros((L, 2))
for m in meta:
    x, sr = sf.read(f'{VO}/{m["key"]}.wav')
    if sr != SR: x = signal.resample_poly(x, SR, sr)
    x = x / (np.abs(x).max() + 1e-9)               # o tratamento de locutor já foi feito no vo.py
    place(vo, x, m["out"], .95)
vo = reverb(vo, .4, .03)                       # quase seco, como estúdio de locução

# ducking: a música abaixa quando o locutor fala
e = np.abs(vo).max(1)
e = signal.sosfilt(signal.butter(1, 6, "low", fs=SR, output="sos"), e)
e = np.clip(e / (e.max() + 1e-9) * 3, 0, 1)
duck = 1 - .68 * e
mix = music * duck[:, None] * .7 + sfx * .9 + vo
mix = mix[: int(OUT_DUR * SR)]
mix /= np.abs(mix).max() / .89
sf.write(f"{SP}/ad/mix.wav", mix, SR, subtype="PCM_24")
sf.write(f"{SP}/ad/music_only.wav", (music * .85)[: int(OUT_DUR * SR)] / (np.abs(music).max() + 1e-9) * .8, SR, subtype="PCM_16")
print("áudio ok")

# conferência de equilíbrio: narração x música durante as falas
def rms(x): return 20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-9)
md = (music * duck[:, None] * .7)[: len(mix)]
for m in meta[:4] + meta[-3:]:
    a, b = int(m["out"] * SR), int((m["out"] + m["dur"]) * SR)
    print(f'{m["key"]}: voz {rms(vo[a:b]):.1f} dB | música {rms(md[a:b]):.1f} dB | efeitos {rms(sfx[a:b]):.1f} dB')
