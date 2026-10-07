"""VAGALUME: encaixa as cenas na narração (ElevenLabs) e grava tempos.json (HTML) e plano.json (áudio). Total ~60 s."""
import os, json, unicodedata, numpy as np
from corte import ler, SR
D = os.path.dirname(os.path.abspath(__file__)); VO = D + '/../vo'; ALVO = 60.0; NF = 17
dur = [len(ler(f'{VO}/{i}.wav')) / SR for i in range(NF)]
from faster_whisper import WhisperModel
wm = WhisperModel('small', device='cpu', compute_type='int8')
def sem(s): return unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()
def quando(i, chave, fr):
    x = ler(f'{VO}/{i}.wav'); x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * 16000 / SR)), np.arange(len(x)), x).astype(np.float32)
    segs, _ = wm.transcribe(x, language='pt', beam_size=5, word_timestamps=True)
    ws = [(sem(w.word).strip(' .,:?!'), w.start) for s in segs for w in s.words]
    for w, t in ws:
        if chave in w: return t
    print(f'  fala {i}: "{chave}" não achada em {[w for w, _ in ws]} → {fr:.0%}'); return dur[i] * fr
K = {'juros': quando(2, 'depois', .55), 'hib': quando(5, 'bisco', .4), 'lim': quando(5, 'limao', .7), 'doze': quando(8, '12', .5),
     'desce': quando(10, 'desce', .55)}
print('durações', [round(d, 2) for d in dur]); print('chaves', K)

def montar(k):
    g = lambda x: max(x * k, .3)
    T, V = {}, [0.0] * NF
    def fala(i, t): V[i] = t; return t + dur[i]
    T['s1'] = 0; e = fala(0, 1.4); T['relogio'] = 1.2; e = fala(1, e + g(.5)); T['t1'] = V[1] - .1
    T['s2'] = e + g(.6); e = fala(2, T['s2'] + .6); T['pico'] = V[2] + .2; T['queda'] = V[2] + K['juros']
    T['s3'] = e + g(.7); T['junta'] = T['s3'] + .1; T['lata'] = T['s3'] + 1.7; e = fala(3, T['s3'] + 1.8); T['nome'] = V[3] + .45
    e = fala(4, e + g(.35)); T['slogan'] = V[4] - .1
    T['s4'] = e + g(.7); e = fala(5, T['s4'] + .6); T['i1'] = V[5] - .1; T['i2'] = V[5] + K['hib'] - .25; T['i3'] = V[5] + K['lim'] - .2
    e = fala(6, e + g(.35)); T['i4'] = V[6] - .1
    T['s5'] = e + g(.7); e = fala(7, T['s5'] + .5); T['k1'] = V[7] - .1
    e = fala(8, e + g(.3)); T['k2'] = V[8] - .1; T['k3'] = V[8] + K['doze'] - .15
    e = fala(9, e + g(.3)); T['k4'] = V[9] - .1
    T['s6'] = e + g(.7); e = fala(10, T['s6'] + .7); T['curva'] = V[10] - .2; T['desce'] = V[10] + K['desce']
    T['s7'] = e + g(.8); e = fala(11, T['s7'] + .5)
    for j, i in enumerate(range(12, 16)):
        e = fala(i, e + g(.4)); T[f'c{j + 1}'] = V[i] - .15
    T['s8'] = e + g(.8); e = fala(16, T['s8'] + 1.3); T['fnome'] = V[16] - .2; T['fslogan'] = V[16] + .9
    T['fim'] = e + 2.6
    return T, V
lo, hi = .3, 3.0
for _ in range(40):
    k = (lo + hi) / 2; T, V = montar(k)
    if T['fim'] > ALVO: hi = k
    else: lo = k
T, V = montar(lo); T['fim'] = round(max(T['fim'], ALVO - .3), 3)
T = {a: round(b, 3) for a, b in T.items()}
json.dump(T, open(D + '/tempos.json', 'w')); json.dump({'vo': [round(v, 3) for v in V], 'dur': dur, 'T': T}, open(D + '/plano.json', 'w'))
print('fator de pausa', round(lo, 2), 'fim', T['fim']); print(json.dumps(T))
