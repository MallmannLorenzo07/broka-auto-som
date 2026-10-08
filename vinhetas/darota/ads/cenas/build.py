import os
D = os.path.dirname(os.path.abspath(__file__))
s = open(D + '/ads.src.html').read().replace('{{gsap}}', open(D + '/../../../motion/gsap.min.js').read())
open(D + '/ads.html', 'w').write(s); print('ok', round(len(s) / 1e6, 2), 'MB')
