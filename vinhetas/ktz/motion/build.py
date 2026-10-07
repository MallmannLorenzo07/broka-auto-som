"""Monta ktz.html: GSAP + imagens embutidas + tempos (tempos.json, gerado pelo plano a partir da narração)."""
import re, os, json, base64, mimetypes
D = os.path.dirname(os.path.abspath(__file__)); IMG = D + '/../img/'
T = json.load(open(D + '/tempos.json'))
s = open(D + '/ktz.src.html').read().replace('{{gsap}}', open(D + '/../../motion/gsap.min.js').read()).replace('{{tempos}}', json.dumps(T))
mt = lambda f: 'image/svg+xml' if f.endswith('.svg') else (mimetypes.guess_type(f)[0] or 'image/webp')
s = re.sub(r'\{\{img:([^}]+)\}\}', lambda m: f'data:{mt(m.group(1))};base64,' + base64.b64encode(open(IMG + m.group(1), 'rb').read()).decode(), s)
assert '{{' not in s; open(D + '/ktz.html', 'w').write(s); print('ktz.html', round(len(s) / 1e6, 2), 'MB')
