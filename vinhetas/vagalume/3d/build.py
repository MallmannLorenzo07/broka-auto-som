"""Monta vagalume3d.html: GSAP + Three.js (r147) + cena3d.js embutidos, com os tempos da narração."""
import os, json
D = os.path.dirname(os.path.abspath(__file__)); L = D + '/lib/'
libs = ['three.min.js', 'Pass.js', 'CopyShader.js', 'LuminosityHighPassShader.js', 'EffectComposer.js', 'RenderPass.js', 'ShaderPass.js', 'UnrealBloomPass.js', 'RoomEnvironment.js']
three = '\n'.join(open(L + f).read() for f in libs) + '\n' + open(D + '/cenarios.js').read() + '\n' + open(D + '/cena3d.js').read()
s = open(D + '/vagalume3d.src.html').read().replace('{{gsap}}', open(D + '/../../motion/gsap.min.js').read()).replace('{{three}}', three)
import re, base64
s = re.sub(r'\{\{foto:([^}]+)\}\}', lambda m: 'data:image/jpeg;base64,' + base64.b64encode(open(D + '/../fotos_jpg/' + m.group(1), 'rb').read()).decode(), s)
s = s.replace('{{tempos}}', json.dumps(json.load(open(D + '/../motion/tempos.json'))))
assert '{{' not in s; open(D + '/vagalume3d.html', 'w').write(s); print('vagalume3d.html', round(len(s) / 1e6, 2), 'MB')
