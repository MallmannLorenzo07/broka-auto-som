# Vinhetas de 30 s (Marcelo Munhoz e PeD Bebidas)

- `teaser/` vinheta Marcelo Munhoz · `teaser_ped/` vinheta PeD Bebidas
- `build.py` monta o HTML (GSAP + imagens embutidas) · `audio.py` / `teaser_audio.py` mixa narração + trilha
- `motion/render.js` renderiza: `node motion/render.js teaser.html saida.mp4 mix.m4a 30`
- `kokoro/elevenlabs_tts.py` gera as falas no ElevenLabs (lê `ELEVENLABS_API_KEY` do ambiente):
  `python3 kokoro/elevenlabs_tts.py vozes` e `python3 kokoro/elevenlabs_tts.py gerar VOICE_ID teaser_ped/vo "fala 1" ...`
- `kokoro/avaliar.py` mede inteligibilidade com Whisper

## Voz gratuita (sem conta): Chatterbox Multilingual
- Licença MIT, uso comercial liberado. Clona o timbre de `refs/miramontes.wav`, um trecho de narrador brasileiro do LibriVox (domínio público).
- Instalação: `uv venv -p 3.11 cb && . cb/bin/activate && uv pip install --extra-index-url https://download.pytorch.org/whl/cpu torch==2.6.0+cpu torchaudio==2.6.0+cpu chatterbox-tts "setuptools<81"`
- Gerar candidatos: `python kokoro/lote.py config.json` (veja `vozes`, `seeds`, `falas`; `out`/`refs` com caminhos absolutos)
- Escolher a melhor tomada por fala (Whisper): `python3 kokoro/escolher.py config.json teaser_ped/vo_cb`
- Falas finais em `teaser/vo_cb/` e `teaser_ped/vo_cb/`

## ElevenLabs (plano gratuito)
- No gratuito, a API só aceita as vozes padrão (vozes da biblioteca e Voice Design exigem plano pago). Usamos "Brian" (`nPczCjzI2devNBz1zQrb`) com `eleven_multilingual_v2`; o `eleven_v3` erra falas curtas (lê "Pê e Dê" em inglês).
- `ELEVENLABS_API_KEY=... EL_MODEL=eleven_multilingual_v2 python3 kokoro/elevenlabs_tts.py gerar nPczCjzI2devNBz1zQrb teaser_ped/vo_el "fala 1" ...`
- Mixar com essas falas: `VODIR=vo_el python3 teaser_ped/audio.py` (padrão `vo_cb` = Chatterbox)
- Plano gratuito: uso não comercial e com crédito ao ElevenLabs.

## KTZ Construtora (motion de ~1 min)
- `ktz/motion/ktz.src.html` (cenas), `plano.py` (encaixa cenas na narração e grava `tempos.json`/`plano.json`), `audio.py` (trilha + voz), `build.py` (monta `ktz.html`)
- Ordem: `python3 ktz/motion/plano.py && python3 ktz/motion/audio.py && python3 ktz/motion/build.py`, depois `node motion/render.js $PWD/ktz/motion/ktz.html saida.mp4 ktz/motion/mix.m4a 30` (mix.wav → m4a com ffmpeg loudnorm)
- Falas escolhidas em `ktz/vo/` (as falas 4 e 14 ficam só na tela, para caber em ~1 min)
- Versão ElevenLabs (voz Brian): `VODIR=vo_el ALVO=64 python3 ktz/motion/plano.py && VODIR=vo_el python3 ktz/motion/audio.py` (falas em `ktz/vo_el/`)
- Para celular: áudio AAC-LC estéreo 44,1 kHz e vídeo H.264 Main 4.0 (`-profile:v main -level:v 4.0 -ar 44100 -ac 2 -movflags +faststart`)
