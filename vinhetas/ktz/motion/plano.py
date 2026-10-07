"""Encaixa as cenas na narração: mede cada fala (mesmo corte do áudio), acha o tempo das palavras-chave com Whisper
e grava tempos.json (para o HTML) e plano.json (para o áudio). Ajusta as pausas para o total dar ~60 s."""
import os, sys, json, unicodedata, numpy as np
from corte import ler, SR
D = os.path.dirname(os.path.abspath(__file__)); VO = D + '/../' + os.environ.get('VODIR', 'vo'); ALVO = float(os.environ.get('ALVO', 65.5))
SEM_FALA = json.loads(os.environ.get('SEM_FALA', '{"4": 2.0, "14": 3.0}')); SEM_FALA = {int(k): v for k, v in SEM_FALA.items()}   # falas cortadas para caber em ~1 min: a cena fica só com texto na tela (segundos de tela)

dur = [len(ler(f'{VO}/{i}.wav')) / SR for i in range(18)]
from faster_whisper import WhisperModel
wm = WhisperModel('small', device='cpu', compute_type='int8')
def sem(s): return unicodedata.normalize('NFKD', s.lower()).encode('ascii', 'ignore').decode()
def palavras(i):
    x = ler(f'{VO}/{i}.wav'); x = np.interp(np.linspace(0, len(x) - 1, int(len(x) * 16000 / SR)), np.arange(len(x)), x).astype(np.float32)
    segs, _ = wm.transcribe(x, language='pt', beam_size=5, word_timestamps=True)
    return [(sem(w.word).strip(' .,:?!'), w.start) for s in segs for w in s.words]
def quando(i, chave, fr):
    ws = palavras(i)
    for w, t in ws:
        if chave in w: return t
    print(f'  fala {i}: "{chave}" não achada em {[w for w, _ in ws]} → {fr:.0%} da fala'); return dur[i] * fr

# posição (s, desde o início da fala) das palavras que disparam animações
K = {'ktz5': quando(5, 'ganha', .55) - .55, 'arq': quando(10, 'arquiteto', .3), 'fut': quando(10, 'futuro', .55), 'inv': quando(10, 'investidor', .82),
     'meta': quando(12, 'meta', .1), 'insta': quando(12, 'instagram', .55), 'goog': quando(13, 'google', .1), 'site': quando(13, 'site', .5),
     'ag': [quando(15, w, f) for w, f in [('estrategia', .2), ('publicos', .4), ('conteudo', .58), ('site', .74), ('investimento', .88)]]}
print('durações', [round(d, 2) for d in dur]); print('chaves', K)

def montar(k):
    g = lambda x: max(x * k, .35)          # pausas flexíveis (mínimo de 0,35 s)
    T, V = {}, [0.0] * 18
    def fala(i, t):
        if i in SEM_FALA: V[i] = None; return t + SEM_FALA[i]
        V[i] = t; return t + dur[i]
    T['s1'] = 0; e = fala(0, 1.0)
    T['s2'] = e + g(.7); e = fala(1, T['s2'] + .6); T['s2stag'] = round(min(.7, dur[1] / 4), 2); T['s2p'] = e - .2
    T['s3'] = e + g(.9); T['n1'] = T['s3'] + .5; e = fala(2, T['n1'] + .15)
    T['n2'] = e + g(.55); e = fala(3, T['n2'] + .15)
    T['n3'] = e + g(.55); e = fala(4, T['n3'] + .15)
    T['s4'] = e + g(.9); e = fala(5, T['s4'] + .7); T['s4b'] = V[5] + K['ktz5']
    T['s5'] = e + g(.9); T['j1'] = T['s5'] + 1.0; e = fala(6, T['j1'])
    T['j2'] = e + g(.4); e = fala(7, T['j2']); T['j3'] = e + g(.4); e = fala(8, T['j3']); T['j4'] = e + g(.4); e = fala(9, T['j4'])
    T['s6'] = e + g(1.0); e = fala(10, T['s6'] + .8)
    T['p1'], T['p2'], T['p3'] = V[10] + K['arq'] - .1, V[10] + K['fut'] - .1, V[10] + K['inv'] - .1
    e = fala(11, e + g(.45)); T['mapa'] = V[11] - .2
    T['s7'] = e + g(1.0); e = fala(12, T['s7'] + .8); T['e1'], T['e2'] = V[12] + K['meta'] - .1, V[12] + K['insta'] - .1
    e = fala(13, e + g(.45)); T['e3'], T['e4'] = V[13] + K['goog'] - .1, V[13] + K['site'] - .1; T['e5'] = T['e4'] + 1.1
    T['s8'] = e + g(1.4); T['s8h'] = T['s8'] + .75; e = fala(14, T['s8'] + .6); T['s8scroll'] = e - .3
    T['s9'] = e + g(1.3); e = fala(15, T['s9'] + .8)
    for j in range(5): T[f'a{j + 1}'] = V[15] + K['ag'][j] - .15
    T['s10'] = e + g(1.0); e = fala(16, T['s10'] + .7); T['f1'] = V[16] - .1
    e = fala(17, e + .6); T['f2'] = V[17] - .1
    T['fim'] = e + 3.2
    return T, V
lo, hi = .3, 3.0
for _ in range(40):
    k = (lo + hi) / 2; T, V = montar(k)
    if T['fim'] > ALVO: hi = k
    else: lo = k
T, V = montar(lo); T['fim'] = ALVO if abs(T['fim'] - ALVO) < .3 else T['fim']
T = {a: round(b, 3) for a, b in T.items()}
json.dump(T, open(D + '/tempos.json', 'w')); json.dump({'vo': [None if v is None else round(v, 3) for v in V], 'dur': dur, 'T': T}, open(D + '/plano.json', 'w'))
print('fator de pausa', round(lo, 2), 'fim', T['fim']); print(json.dumps(T))
