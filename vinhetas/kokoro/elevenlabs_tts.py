"""Gera falas no ElevenLabs a partir da variável de ambiente ELEVENLABS_API_KEY (nunca colar a chave no chat).

Uso:
  python elevenlabs_tts.py vozes                       # lista as vozes da conta (nome, id, idioma)
  python elevenlabs_tts.py gerar VOICE_ID saida_dir "fala 1" "fala 2" ...
Gera saida_dir/0.wav, 1.wav ... (PCM 16 bits, 44,1 kHz) e imprime a duração de cada uma.
"""
import os, sys, json, wave, urllib.request

KEY = os.environ.get('ELEVENLABS_API_KEY')
if not KEY:
    sys.exit('ELEVENLABS_API_KEY não encontrada no ambiente.')
API = 'https://api.elevenlabs.io/v1'

def req(path, body=None, accept='application/json'):
    r = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                               headers={'xi-api-key': KEY, 'Content-Type': 'application/json', 'Accept': accept},
                               method='POST' if body else 'GET')
    with urllib.request.urlopen(r, timeout=120) as resp:
        return resp.read()

if sys.argv[1] == 'vozes':
    for v in json.loads(req('/voices'))['voices']:
        lab = v.get('labels') or {}
        print(f"{v['name']:28} {v['voice_id']}  {lab.get('language','')} {lab.get('accent','')} {lab.get('gender','')}")
elif sys.argv[1] == 'gerar':
    voz, out, falas = sys.argv[2], sys.argv[3], sys.argv[4:]
    os.makedirs(out, exist_ok=True)
    for i, txt in enumerate(falas):
        pcm = req(f'/text-to-speech/{voz}?output_format=pcm_44100', {
            'text': txt, 'model_id': 'eleven_multilingual_v2', 'language_code': 'pt',
            'voice_settings': {'stability': 0.55, 'similarity_boost': 0.8, 'style': 0.15, 'use_speaker_boost': True, 'speed': 0.95}},
            accept='audio/pcm')
        with wave.open(f'{out}/{i}.wav', 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100); w.writeframes(pcm)
        print(i, round(len(pcm) / 2 / 44100, 2), txt)
