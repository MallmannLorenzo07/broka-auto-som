"""Pontua candidatos {voz}_{fala}_{seed}.wav com Whisper e escolhe a melhor voz e a melhor tomada de cada fala.
Uso: python3 escolher.py config.json destino_dir"""
import sys, json, glob, re, unicodedata, shutil, collections, numpy as np, soundfile as sf
from faster_whisper import WhisperModel
cfg = json.load(open(sys.argv[1])); dst = sys.argv[2]
NUM = [('39', 'trinta e nove'), ('210', 'duzentos e dez'), ('910', 'novecentas e dez'), ('900 e 10', 'novecentas e dez'), ('200', 'duzentos'), ('2 mil', 'duas mil'), ('2000', 'duas mil')]
def norm(s):
    s = s.lower()
    for a, b in NUM: s = s.replace(a, b)
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\bp\.? ?e\.? ?d\b|\bp e d\b|\bpid\b|\bped\b', 'pe e de', s)
    return re.findall(r'[a-z]+', s)
def wer(r, h):
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        p, d[0] = d[0], i
        for j in range(1, len(h) + 1): p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (r[i - 1] != h[j - 1]))
    return d[-1] / len(r)
m = WhisperModel('small', device='cpu', compute_type='int8'); res = {}
for f in sorted(glob.glob(cfg['out'] + '/*.wav')):
    v, i, s = f.split('/')[-1][:-4].rsplit('_', 2); i = int(i)
    x, sr = sf.read(f, dtype='float32'); dur = len(x) / sr
    x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * 16000 / sr)), np.arange(len(x)), x).astype(np.float32)
    segs, info = m.transcribe(x, language='pt', beam_size=5, condition_on_previous_text=False); segs = list(segs)
    txt = ' '.join(z.text.strip() for z in segs); lp = -sum(z.avg_logprob for z in segs) / max(1, len(segs))
    nw = len(norm(cfg['falas'][i])); w = wer(norm(cfg['falas'][i]), norm(txt))
    # pontuação: erros de palavra pesam mais; incerteza desempata; fala corrida demais (>3,3 palavras/s) é penalizada
    score = w * 3 + lp + max(0, nw / dur - 3.3) * .3
    res[(v, i, s)] = (score, w, lp, dur, txt)
porvoz = collections.defaultdict(float)
for v in cfg['vozes']:
    for i in range(len(cfg['falas'])): porvoz[v] += min(res[(v, i, s)][0] for (vv, ii, s) in res if vv == v and ii == i)
for v, sc in sorted(porvoz.items(), key=lambda a: a[1]): print(f'voz {v:12} {sc:.3f}')
best = min(porvoz, key=porvoz.get); import os; os.makedirs(dst, exist_ok=True)
for i in range(len(cfg['falas'])):
    c = sorted((res[k], k) for k in res if k[0] == best and k[1] == i)
    (sc, w, lp, dur, txt), k = c[0]
    shutil.copy(f"{cfg['out']}/{k[0]}_{k[1]}_{k[2]}.wav", f'{dst}/{i}.wav')
    print(f'{i} seed{k[2]} WER {w:4.0%} inc {lp:.3f} {dur:4.2f}s | {txt}')
