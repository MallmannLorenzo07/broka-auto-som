"""Monta fotos.html: estúdio fotográfico virtual (Three.js r147) para gerar as fotos de produto."""
import os
D = os.path.dirname(os.path.abspath(__file__)); L = D + '/lib/'
libs = ['three.min.js', 'Pass.js', 'CopyShader.js', 'LuminosityHighPassShader.js', 'EffectComposer.js', 'RenderPass.js', 'ShaderPass.js', 'UnrealBloomPass.js', 'RoomEnvironment.js', 'RectAreaLightUniformsLib.js']
js = '\n'.join(open(L + f).read() for f in libs) + '\n' + open(D + '/cena3d.js').read() + '\n' + open(D + '/fotos.js').read()
html = '''<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@500;900&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>html,body{margin:0;background:#000}canvas{display:block}</style></head><body><canvas id="foto"></canvas>
<script>''' + js + '''
Promise.all([document.fonts.load('900 84px Unbounded'),document.fonts.load('500 34px Unbounded'),document.fonts.load('italic 64px "Instrument Serif"')]).then(function(){window.__ready=true});
</script></body></html>'''
open(D + '/fotos.html', 'w').write(html); print('fotos.html', round(len(html) / 1e6, 2), 'MB')
