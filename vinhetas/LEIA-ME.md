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
