"""Áudio dos anúncios Meta Ads da Da Rota: trilha original remontada em trechos (crossfade 80 ms),
narração ElevenLabs posicionada nos cortes e ducking da trilha sob a voz.
Uso: python3 mix_ads.py VIDEO_ORIGINAL A|B  -> mix_A.wav / mix_B.wav + voz_A.wav (só a voz, para legendar)"""
import sys, subprocess, numpy as np, soundfile as sf
from corte import ler, SR
F, AD = sys.argv[1], sys.argv[2]
def trecho(x, a, b):
    y = x[int(a * SR): int(b * SR) if b else None].copy(); f = int(.012 * SR); y[:f] *= np.linspace(0, 1, f); y[-f:] *= np.linspace(1, 0, f); return y
if AD == 'A':      # 31 s: gancho original, WhatsApp, categorias, tintas/marcas, pedido+entrega, oferta, CTA
    DUR = 31.0
    musica = [(0, 2), (2, 6.8), (4, 9), (4, 9), (12, 18), (20, 23.6), (24, 30)]
    def falas(put):
        intro = ler('../y/a/0.wav'); put(trecho(intro, 0, .9), .12); put(trecho(intro, .98, None), 1.05)
        put(ler('v0/0.wav'), 2.3)                                    # manda a lista no WhatsApp...
        cat = ler('../y/a/1.wav')
        for (a, b), at in zip([(0, 1.2), (1.42, 2.12), (2.17, 2.9), (2.95, 3.66), (3.7, None)], [6.82, 7.8, 8.8, 9.8, 10.8]): put(trecho(cat, a, b), at)
        put(ler('../z/a/0.wav'), 11.95)                              # tintas, ferramentas e marcas
        put(ler('../vo/9.wav'), 16.88); put(ler('../vo/10.wav'), 18.92)
        put(ler('v0/1.wav'), 22.95)                                  # preço bom e várias formas de pagamento
        put(ler('v0/2.wav'), 26.6)                                   # chama a Da Rota no WhatsApp agora
else:              # 15,2 s: gancho "obra parada?", entrega, por que comprar, CTA
    DUR = 15.2
    musica = [(0, 2.6), (14, 18), (20, 24), (24, 30)]
    def falas(put):
        put(ler('v1/3.wav'), .15); put(ler('v0/4.wav'), 2.75); put(ler('v1/5.wav'), 6.85); put(ler('v0/2.wav'), 10.8)
N = int(DUR * SR)
orig = np.frombuffer(subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', F, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True).stdout, np.float32).reshape(-1, 2)
X = int(.08 * SR); trilha = np.zeros((N, 2), np.float32); pos = 0
for a, b in musica:
    s = orig[int(a * SR):int(b * SR)].copy(); n = len(s)
    if pos > 0: s[:X] *= np.linspace(0, 1, X)[:, None]; trilha[pos - X:pos] *= np.linspace(1, 0, X)[:, None]; pos -= X
    m = min(n, N - pos); trilha[pos:pos + m] += s[:m]; pos += m
trilha *= np.clip((DUR - np.arange(N) / SR) / 1.0, 0, 1)[:, None]
voz = np.zeros(N, np.float32)
def put(x, at): i = int(at * SR); n = min(len(x), N - i); voz[i:i + n] += x[:n]
falas(put)
env = np.convolve(np.abs(voz), np.ones(2400) / 2400, 'same')
ativo = np.convolve((env > .01).astype(np.float32), np.ones(int(.25 * SR)))[:N] > 0
duck = np.convolve(np.where(ativo, .32, 1.0), np.ones(4800) / 4800, 'same').astype(np.float32)
mix = trilha * duck[:, None] + (voz * .95)[:, None]; mix /= max(1., np.abs(mix).max() / .97)
sf.write(f'mix_{AD}.wav', mix, SR); sf.write(f'voz_{AD}.wav', voz, SR); print(AD, 'ok', DUR, 's')
