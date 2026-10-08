"""Legenda queimada estilo Reels (ASS): blocos de até 3 palavras, palavra falada em amarelo.
Fica na faixa y≈1080–1230 (dentro da área útil do Meta). Pula as cenas que já têm o texto na tela."""
import sys, json, re
AD = sys.argv[1]
PULA = {'A': [(22.4, 31.1)], 'B': [(0, 2.6), (10.3, 15.3)]}[AD]
FIX = {'wonder,': 'Vonder,', 'presso': 'Preço'}
w = json.load(open(f'palavras_{AD}.json'))
p = []
for t, a, b in w:
    t = FIX.get(t.lower(), t)
    if t == '-40.' and p and p[-1][0] == 'WD': p[-1] = ('WD-40.', p[-1][1], b); continue
    if not any(x <= a < y for x, y in PULA): p.append((t, a, b))
CURTAS = {'e', 'o', 'a', 'de', 'no', 'na', 'do', 'da', 'com', 'seu', 'sua', 'como', 'ou'}
blocos, cur = [], []
for i, x in enumerate(p):
    cur.append(x)
    prox = p[i + 1] if i + 1 < len(p) else None
    if len(cur) == 3 and prox and cur[-1][0].lower() in CURTAS: cur.pop(); blocos.append(cur); cur = [x]; continue
    if len(cur) == 3 or re.search(r'[,.?!]$', x[0]) or not prox or prox[1] - x[2] > .5: blocos.append(cur); cur = []
def ts(s): h = int(s // 3600); m = int(s % 3600 // 60); return f'{h}:{m:02d}:{s % 60:05.2f}'
lim = lambda a: min([y for x, y in PULA if y > a] + [99])
ev = []
for k, bl in enumerate(blocos):
    fim_bl = bl[-1][2] + .25
    if k + 1 < len(blocos): fim_bl = min(fim_bl + .4, blocos[k + 1][0][1])
    for j, (t, a, b) in enumerate(bl):
        ini = a
        fim = bl[j + 1][1] if j + 1 < len(bl) else fim_bl
        partes = [(r'{\c&H1FDCFD&}' if jj == j else r'{\c&HFFFFFF&}') + re.sub(r'[,.]$', '', tt).upper() for jj, (tt, _, _) in enumerate(bl)]
        ev.append(f'Dialogue: 0,{ts(max(0, ini))},{ts(min(fim, lim(a)))},L,,0,0,0,,' + (r'{\fad(60,0)}' if j == 0 else '') + ' '.join(partes))
cab = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: L,Anton,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,4,2,60,60,700,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
open(f'leg_{AD}.ass', 'w').write(cab + '\n'.join(ev) + '\n'); print(AD, len(blocos), 'blocos', len(ev), 'eventos')
