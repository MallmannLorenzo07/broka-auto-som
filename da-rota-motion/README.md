# Da Rota Home Center: motion de 30s

Vídeo vertical (1080×1920, 30 fps, formato Reels/Stories) com trilha original: **`da-rota-motion.mp4`**.

## Roteiro (120 BPM, 1 compasso = 2s)

| Tempo | Cena |
|---|---|
| 0–2s | Gancho: "Vai construir? Ou vai reformar?" sobre silhueta de obra em amarelo |
| 2–4s | Drop: logo Da Rota + "Tudo que você precisa para a sua casa" |
| 4–9s | Departamentos (1 por segundo): Materiais de construção, Hidráulica, Elétrica, Ferragens, Pisos e revestimentos |
| 9–12s | Banheiro e cozinha: duchas e torneiras + selo "Promoções do mês" |
| 12–14s | Estoque: "Seu pedido separado com agilidade" |
| 14–18s | Entrega: caminhão Da Rota na estrada até a obra, com o selo "Entregue ✓" e "Prazo cumprido à risca" |
| 18–20s | Depoimentos reais de clientes em formato de conversa no WhatsApp |
| 20–24s | Diferenciais: qualidade, equipe, prazo, pagamento |
| 24–26s | Equipe na fachada: "Conte com a gente!" |
| 26–30s | Final: logo, WhatsApp (51) 99788-7758, endereço, @darotahomecenter e site |

Textos, fotos e depoimentos foram tirados do site darotahomecenter.com.br.

## Arquivos

- `index.html`: a animação (GSAP). Abra no navegador e clique em play para ver a prévia com som.
- `trilha.py`: gera a trilha original (`assets/trilha.wav` / `.mp3`) com numpy, sincronizada com os cortes.
- `render.mjs`: renderiza quadro a quadro com Playwright/Chromium e monta o MP4 com ffmpeg.

## Como renderizar de novo

```bash
python3 trilha.py         # gera a trilha
node render.mjs           # gera da-rota-motion.mp4
node render.mjs --stills 3,10.5,27 stills/   # (opcional) quadros para conferência
```
