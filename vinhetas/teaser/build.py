import re, os, base64, mimetypes
D = os.path.dirname(os.path.abspath(__file__)); IMG = D + '/../deck/img/'
s = open(D + '/teaser.src.html').read()
s = s.replace('{{gsap}}', open(D + '/../motion/gsap.min.js').read())
s = re.sub(r'\{\{img:([^}]+)\}\}', lambda m: f'data:{mimetypes.guess_type(m.group(1))[0]};base64,' + base64.b64encode(open(IMG + m.group(1), 'rb').read()).decode(), s)
assert '{{' not in s
open(D + '/teaser.html', 'w').write(s); print('teaser.html', round(len(s) / 1e6, 2), 'MB')
