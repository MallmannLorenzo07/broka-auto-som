"""Corte das falas: tira silêncio e respiração do fim e normaliza."""
import numpy as np, soundfile as sf
SR = 48000

def ler(f):
    x, sr = sf.read(f, dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * SR / sr)), np.arange(len(x)), x).astype(np.float32)
    h = int(.05 * SR); e = np.array([np.sqrt(np.mean(x[j:j + h] ** 2)) for j in range(0, len(x), h)])
    on = np.where(e > .01)[0]; ini, fim = on[0], on[-1]
    for a, b in zip(on[:-1], on[1:]):      # pausa > 0,4 s seguida de pouco som (< 0,7 s) = respiração/ruído no fim: corta
        if b - a > 8 and (on > a).sum() < 14: fim = a; break
    x = x[max(0, ini * h - 1200): (fim + 1) * h + 2400].copy(); x[-2400:] *= np.linspace(1, 0, 2400)
    return x / np.abs(x).max() * .9
