import re, os, base64, mimetypes
D = os.path.dirname(os.path.abspath(__file__)); IMG = D + '/../ped/deck/img/'
s = open(D + '/teaser.src.html').read().replace('{{gsap}}', open(D + '/../motion/gsap.min.js').read())
mt = lambda f: mimetypes.guess_type(f)[0] or 'image/webp'
s = re.sub(r'\{\{img:([^}]+)\}\}', lambda m: f'data:{mt(m.group(1))};base64,' + base64.b64encode(open(IMG + m.group(1), 'rb').read()).decode(), s)
assert '{{' not in s; open(D + '/teaser.html', 'w').write(s); print('teaser.html', round(len(s)/1e6, 2), 'MB')
