"""Monta vagalume.html: GSAP embutido + tempos.json."""
import os, json
D = os.path.dirname(os.path.abspath(__file__))
s = open(D + '/vagalume.src.html').read().replace('{{gsap}}', open(D + '/../../motion/gsap.min.js').read()).replace('{{tempos}}', json.dumps(json.load(open(D + '/tempos.json'))))
assert '{{' not in s; open(D + '/vagalume.html', 'w').write(s); print('vagalume.html', round(len(s) / 1e6, 2), 'MB')
