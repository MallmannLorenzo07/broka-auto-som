# Vinhetas de 30 s (Marcelo Munhoz e PeD Bebidas)

- `teaser/` vinheta Marcelo Munhoz · `teaser_ped/` vinheta PeD Bebidas
- `build.py` monta o HTML (GSAP + imagens embutidas) · `audio.py` / `teaser_audio.py` mixa narração + trilha
- `motion/render.js` renderiza: `node motion/render.js teaser.html saida.mp4 mix.m4a 30`
- `kokoro/elevenlabs_tts.py` gera as falas no ElevenLabs (lê `ELEVENLABS_API_KEY` do ambiente):
  `python3 kokoro/elevenlabs_tts.py vozes` e `python3 kokoro/elevenlabs_tts.py gerar VOICE_ID teaser_ped/vo "fala 1" ...`
- `kokoro/avaliar.py` mede inteligibilidade com Whisper
