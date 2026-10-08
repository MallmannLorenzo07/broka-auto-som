import re, os, base64
D = os.path.dirname(os.path.abspath(__file__))
s = open(D + '/cenas.src.html').read().replace('{{gsap}}', open(D + '/../../motion/gsap.min.js').read())
s = re.sub(r'\{\{img:([^}]+)\}\}', lambda m: 'data:image/jpeg;base64,' + base64.b64encode(open(D + '/img/' + m.group(1), 'rb').read()).decode(), s)
open(D + '/cenas.html', 'w').write(s); print('ok', round(len(s) / 1e6, 2), 'MB')
