"""Locução do motion Da Rota com ElevenLabs + mixagem com a trilha.

Gera cada fala separadamente (mesma voz e mesmas configurações), encaixa cada uma
no início da sua cena, abaixa a música enquanto a voz fala (ducking) e grava
assets/mix.wav, que o render.mjs usa no lugar da trilha pura.

Uso:
  ELEVENLABS_API_KEY=... python3 locucao.py           # gera as falas e a mixagem
  ELEVENLABS_VOICE_ID=... (opcional) escolhe a voz; sem ela, procura na sua conta
                          uma voz em português e, se não achar, usa a padrão abaixo
  python3 locucao.py --mix                            # só refaz a mixagem com as falas já baixadas
  python3 locucao.py --simular                        # testa a mixagem com uma "voz" sintética
"""
import json, os, subprocess, sys, urllib.request, urllib.error, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VOZ_DIR = os.path.join(HERE, 'assets', 'voz')
SR = 44100
DUR = 30.0
API = 'https://api.elevenlabs.io/v1'
MODEL = os.environ.get('ELEVENLABS_MODEL', 'eleven_multilingual_v2')
VOZ_PADRAO = 'nPczCjzI2devNBz1zQrb'  # "Brian", voz premade multilíngue

# (início em s, fim máximo em s, texto) — casado com as cenas do index.html
FALAS = [
    (0.10, 1.95, 'Vai construir? Ou vai reformar?'),
    (2.15, 4.05, 'Da Rota Home Center! Tudo pra sua casa.'),
    (4.15, 8.95, 'Materiais de construção, hidráulica, elétrica, ferragens, pisos e revestimentos.'),
    (9.10, 11.95, 'E acabamento completo pro banheiro e pra cozinha.'),
    (12.10, 13.95, 'Seu pedido, separado com agilidade...'),
    (14.15, 17.90, 'e entregue direto na sua obra, no prazo combinado.'),
    (18.10, 19.90, 'Quem compra, aprova!'),
    (20.15, 23.85, 'Qualidade, um time pronto pra te ajudar e várias formas de pagamento.'),
    (24.10, 25.95, 'Conte com a Da Rota!'),
    (26.30, 29.70, 'Chama no WhatsApp e peça seu orçamento! Da Rota Home Center.'),
]

CONFIG_VOZ = {'stability': 0.38, 'similarity_boost': 0.8, 'style': 0.45,
              'use_speaker_boost': True, 'speed': 1.08}


def api(path, data=None):
    key = os.environ.get('ELEVENLABS_API_KEY')
    if not key:
        sys.exit('Defina ELEVENLABS_API_KEY no ambiente (configurações do ambiente) para gerar a locução.')
    req = urllib.request.Request(API + path, method='POST' if data else 'GET',
                                 data=json.dumps(data).encode() if data else None,
                                 headers={'xi-api-key': key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        sys.exit(f'ElevenLabs respondeu {e.code}: {e.read().decode(errors="ignore")[:400]}')


def escolher_voz():
    if os.environ.get('ELEVENLABS_VOICE_ID'):
        return os.environ['ELEVENLABS_VOICE_ID'], 'ELEVENLABS_VOICE_ID'
    vozes = json.loads(api('/voices')).get('voices', [])
    for v in vozes:
        txt = json.dumps(v.get('labels', {})).lower() + ' ' + (v.get('name') or '').lower()
        if any(k in txt for k in ('brazil', 'brasil', 'portugu', 'pt-br')):
            return v['voice_id'], v.get('name')
    return VOZ_PADRAO, 'Brian (padrão)'


def decodificar(mp3):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', mp3, '-f', 's16le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<i2').astype(np.float64) / 32768


def aparar(x, lim=0.02):
    idx = np.where(np.abs(x) > lim)[0]
    if not len(idx):
        return x
    a, b = max(0, idx[0] - int(0.01 * SR)), min(len(x), idx[-1] + int(0.06 * SR))
    return x[a:b]


def acelerar(x, fator):
    """Acelera sem mudar o tom (atempo do ffmpeg)."""
    p = subprocess.run(['ffmpeg', '-loglevel', 'error', '-f', 's16le', '-ar', str(SR), '-ac', '1', '-i', '-',
                        '-af', f'atempo={fator:.4f}', '-f', 's16le', '-'],
                       input=(np.clip(x, -1, 1) * 32767).astype('<i2').tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, '<i2').astype(np.float64) / 32768


def gerar_falas():
    os.makedirs(VOZ_DIR, exist_ok=True)
    voz, nome = escolher_voz()
    print(f'voz: {nome} ({voz}), modelo: {MODEL}')
    for i, (_, _, texto) in enumerate(FALAS):
        corpo = {'text': texto, 'model_id': MODEL, 'voice_settings': CONFIG_VOZ, 'seed': 42,
                 'previous_text': FALAS[i - 1][2] if i else None,
                 'next_text': FALAS[i + 1][2] if i + 1 < len(FALAS) else None}
        audio = api(f'/text-to-speech/{voz}?output_format=mp3_44100_128', corpo)
        with open(os.path.join(VOZ_DIR, f'fala-{i + 1:02d}.mp3'), 'wb') as f:
            f.write(audio)
        print(f'  fala {i + 1:02d} ok: {texto}')


def voz_simulada(d):
    """Ruído modulado em sílabas, só para testar a mixagem sem gastar créditos."""
    t = np.arange(int(d * SR)) / SR
    rng = np.random.default_rng(1)
    n = np.fft.irfft(np.fft.rfft(rng.standard_normal(len(t))) * (np.fft.rfftfreq(len(t), 1 / SR) < 3000), len(t))
    return n / np.abs(n).max() * (0.5 + 0.5 * np.sin(2 * np.pi * 4.5 * t)) ** 2 * 0.5


def ler_wav(p):
    with wave.open(p) as w:
        x = np.frombuffer(w.readframes(w.getnframes()), '<i2').astype(np.float64) / 32768
        return x.reshape(-1, w.getnchannels())


def mixar(simular=False):
    musica = ler_wav(os.path.join(HERE, 'assets', 'trilha.wav'))
    N = len(musica)
    voz = np.zeros(N)
    for i, (ini, fim, texto) in enumerate(FALAS):
        if simular:
            x = voz_simulada(len(texto) / 16)
        else:
            x = aparar(decodificar(os.path.join(VOZ_DIR, f'fala-{i + 1:02d}.mp3')))
        caber = fim - ini
        if len(x) / SR > caber:
            fator = len(x) / SR / caber
            if fator > 1.3:
                print(f'  aviso: fala {i + 1} tem {len(x) / SR:.2f}s para {caber:.2f}s (acelerada {fator:.2f}x)')
            x = acelerar(x, min(fator, 1.6))
        x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * 0.16  # nivela as falas entre si
        a = int(ini * SR)
        x = x[: N - a]
        fade = int(0.02 * SR)
        x[-fade:] *= np.linspace(1, 0, fade)
        voz[a:a + len(x)] += x
        print(f'  fala {i + 1:02d}: {ini:5.2f}s → {ini + len(x) / SR:5.2f}s (limite {fim:.2f}s)')

    # ducking: envelope da voz (ataque rápido, soltura lenta) abaixa a música ~9 dB
    env = np.abs(voz)
    k = int(0.03 * SR)
    env = np.convolve(env, np.ones(k) / k, 'same')
    env = np.minimum(env / (env.max() + 1e-9) * 4, 1)
    rel = np.exp(-1 / (0.25 * SR))
    atk = np.exp(-1 / (0.02 * SR))
    g = np.empty(N)
    s = 0.0
    for n in range(N):  # seguidor de envelope simples
        c = atk if env[n] > s else rel
        s = c * s + (1 - c) * env[n]
        g[n] = s
    duck = 1 - 0.65 * g

    # leve presença na voz (realce em ~3 kHz) e mix
    X = np.fft.rfft(voz)
    f = np.fft.rfftfreq(N, 1 / SR)
    X *= 1 + 0.4 * np.exp(-((f - 3200) / 1500) ** 2)
    X *= 1 / np.sqrt(1 + (90 / (f + 1e-9)) ** 4)  # corta graves abaixo de ~90 Hz
    voz = np.fft.irfft(X, N)
    mix = musica * duck[:, None] + voz[:, None] * np.array([1.0, 1.0])
    mix /= max(1.0, np.abs(mix).max() / 0.98)

    bruto = os.path.join(HERE, 'assets', 'mix-bruto.wav')
    with wave.open(bruto, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype('<i2').tobytes())
    out = os.path.join(HERE, 'assets', 'mix.wav')
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', bruto,
                    '-af', 'loudnorm=I=-14:TP=-1.2:LRA=9', '-ar', str(SR), out], check=True)
    os.remove(bruto)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', out, '-b:a', '192k',
                    os.path.join(HERE, 'assets', 'mix.mp3')], check=True)
    print('ok ->', out)


if __name__ == '__main__':
    if '--simular' in sys.argv:
        mixar(simular=True)
    else:
        if '--mix' not in sys.argv:
            gerar_falas()
        mixar()
