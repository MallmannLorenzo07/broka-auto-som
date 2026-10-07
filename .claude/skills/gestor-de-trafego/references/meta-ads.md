# Meta Ads (Facebook + Instagram)

> As plataformas mudam nomes e recursos com frequência. Se o usuário citar um recurso que não bate com o que está aqui, confie na tela dele e adapte.

## Índice
1. Como o algoritmo funciona hoje (e o que isso muda na estratégia)
2. Objetivos e eventos de otimização
3. Estruturas de conta recomendadas
4. Orçamento: CBO (Advantage+ orçamento) vs ABO
5. Públicos
6. Estratégias de lance
7. Fase de aprendizado
8. Testes de criativo
9. Escala
10. Posicionamentos
11. Atribuição e leitura de resultados
12. Campanhas de mensagem (WhatsApp/Direct) e cadastro
13. Checklist de auditoria de conta Meta

---

## 1. Como o algoritmo funciona hoje

- O sistema de entrega do Meta (com o motor de recuperação de anúncios conhecido como **Andromeda**) usa o **criativo como principal sinal de segmentação**. Cada criativo diferente encontra pessoas diferentes. Por isso:
  - **Diversidade de criativos** (ângulos, formatos, personas e mensagens realmente diferentes) vale mais que 10 variações da mesma peça.
  - Públicos amplos + bons criativos tendem a superar interesses muito recortados.
  - Variações quase idênticas competem entre si e são tratadas como o mesmo anúncio.
- **Consolidação** ajuda: menos campanhas e conjuntos com mais verba e mais sinais. Fragmentar demais trava o aprendizado.
- **Qualidade do sinal** (pixel + API de Conversões com boa qualidade de correspondência) impacta diretamente a performance.

## 2. Objetivos e eventos de otimização

| Objetivo | Use para | Evento típico |
|---|---|---|
| Vendas | E-commerce, infoproduto, qualquer conversão no site | Compra (ou Iniciar checkout/Adicionar ao carrinho se faltar volume) |
| Cadastros (Leads) | Formulário instantâneo, página de captura, WhatsApp/Messenger | Lead, Cadastro concluído, lead qualificado via CRM |
| Engajamento | Mensagens, visualização de vídeo, engajamento com publicação | Conversas iniciadas, ThruPlay |
| Tráfego | Raramente para performance. Útil para alimentar público ou para blog | Visualização da página de destino (nunca "cliques no link" se der para evitar) |
| Reconhecimento | Alcance/frequência controlada, branding local | Alcance |
| Promoção do app | Instalações e eventos no app | Instalação, evento in-app |

**Regra prática do evento:** escolha o evento mais fundo no funil que gere **≥ 50 conversões por semana por conjunto** (ou que fique perto disso). Se compra não tem volume, otimize para Iniciar checkout e migre depois.

## 3. Estruturas de conta recomendadas

### Conta pequena (até ~R$ 3–5 mil/mês)
```
Campanha 1 — Vendas | Advantage+ orçamento (CBO)
  └─ Conjunto 1: público amplo (Advantage+ público), 4–8 criativos de ângulos diferentes
Campanha 2 (opcional, se houver volume de visitantes) — Remarketing
  └─ Conjunto: visitantes 30d + engajados 30–60d, excluindo compradores 180d
```
Com verba pequena, **não fragmente**. Uma campanha bem alimentada costuma vencer três passando fome.

### Conta média/grande
```
1. Teste de criativos (ABO): 1 conjunto por conceito/ângulo, 3–5 variações cada, verba fixa
2. Escala (CBO ou Advantage+ vendas): vencedores dos testes, público amplo
3. Remarketing/retargeting (opcional; o Advantage+ já cobre parte disso)
4. Campanhas táticas: lançamento, promoção, catálogo (DPA)
```
- **Advantage+ campanhas de vendas** (antiga Advantage+ Shopping): automação máxima, ótima para e-commerce com catálogo e sinal bom. Você controla o orçamento, o criativo e o limite de gasto com clientes existentes (definindo o público de clientes atuais).
- **Catálogo (anúncios dinâmicos):** obrigatório para e-commerce com muitos SKUs. Use para remarketing e para prospecção ampla.

### Nomenclatura padrão (sugira ao usuário)
`[Objetivo]_[Funil]_[Público]_[Ângulo/Oferta]_[Data]`. Exemplo: `VENDAS_TOF_AMPLO_DORprovaSocial_2610`. Facilita os relatórios e a análise por ângulo.

## 4. Orçamento: CBO vs ABO

| | CBO (Advantage+ orçamento da campanha) | ABO (orçamento no conjunto) |
|---|---|---|
| Melhor para | Escala, conjuntos já validados | Testes controlados, garantir verba por variante |
| Prós | O algoritmo distribui para onde converte mais barato | Controle, comparação justa |
| Contras | Pode "abandonar" conjuntos antes de testá-los | Mais trabalho, pode desperdiçar verba em perdedores |

- No CBO, use **limites de gasto por conjunto** (mínimo/máximo) quando precisar forçar teste ou conter um conjunto.
- **Orçamento mínimo saudável por conjunto:** idealmente ≥ CPA alvo × 50 ÷ 7 por dia para sair do aprendizado. Quando não for possível, ≥ 1–2x o CPA alvo por dia já dá sinal razoável.
- Orçamento diário vs. vitalício: o diário é o padrão. O vitalício é útil em lançamentos/promoções com data, com programação de horários.

## 5. Públicos

- **Advantage+ público (amplo com sugestões):** padrão atual. As sugestões de idade/interesse são "dicas", não limites. Restrinja apenas o que é obrigatório (idade mínima legal, localização).
- **Controles de público:** localização, idade mínima e exclusões rígidas (ex.: excluir clientes). Use quando o negócio exige.
- **Interesses:** ainda úteis para contas novas sem sinal ou nichos muito específicos. Teste-os contra o público amplo.
- **Personalizados:** visitantes do site, engajamento IG/FB, lista de clientes (hash), visualizações de vídeo, formulário aberto/enviado, conversas no WhatsApp.
- **Semelhantes (lookalike):** perderam força com o Advantage+, mas ainda funcionam como sugestão e em contas com boa base (ex.: LAL 1–3% de compradores de alto valor).
- **Exclusões:** compradores recentes (dependendo do ciclo de recompra), funcionários, leads já convertidos.
- **Sobreposição:** conjuntos com públicos sobrepostos competem no leilão. Consolide.

**Contas locais (raio):** use raio em torno do endereço; 5–15 km para serviços urbanos, maior para cidades pequenas. Com raio pequeno, o público fica pequeno: use público aberto (sem interesses) e criativos com referência local (nome do bairro ou da cidade).

## 6. Estratégias de lance

| Estratégia | Quando usar |
|---|---|
| **Maior volume (menor custo)** | Padrão. Sempre comece por aqui. |
| **Meta de custo por resultado (Cost Cap)** | Quando precisa proteger CPA e aceita menos volume. Defina perto do CPA real (± 10–20%), não do sonho. |
| **Limite de lance (Bid Cap)** | Controle rígido do lance no leilão. Avançado, exige verba alta e acompanhamento. |
| **Meta de ROAS (ROAS mínimo)** | E-commerce com valores de compra confiáveis e volume. |
| **Maximizar valor** | Otimizar receita em vez de número de compras (ticket variável). |

Lances com controle de custo **gastam menos** se o alvo for agressivo. Não é bug, é a regra funcionando.

## 7. Fase de aprendizado

- Sai do aprendizado com **~50 eventos de otimização em 7 dias** após a última edição significativa.
- **Edições que reiniciam o aprendizado:** mudança de público, posicionamento, evento de otimização, estratégia de lance, adicionar criativo novo (no nível do conjunto), pausar por 7+ dias, mudança grande de orçamento (saltos fortes).
- **Aprendizado limitado** = não vai chegar a 50/semana com a configuração atual. Soluções: consolidar conjuntos, aumentar orçamento, ampliar o público, subir o evento no funil.
- Evite julgar conjunto com menos de 3–4 dias ou menos de 1–2x o CPA alvo em gasto (salvo desastre óbvio).

## 8. Testes de criativo

**Método recomendado (simples e robusto):**
1. Campanha de teste em ABO (ou CBO com conjuntos separados e gasto mínimo).
2. **1 conjunto = 1 conceito/ângulo**, com 3–5 variações (hooks, formatos).
3. Verba por conjunto suficiente para gerar dados: idealmente gastar 2–3x o CPA alvo por conceito antes de decidir.
4. Métricas de triagem precoce (antes de ter conversões):
   - **Hook rate** (visualizações de 3s ÷ impressões): referência > 25–30%.
   - **Hold rate** (ThruPlay ou 15s ÷ 3s): referência > 8–15% dependendo da duração.
   - **CTR (link)**: referência > 1% (varia muito por nicho).
   - **CPC (link)** e **custo por adição ao carrinho**.
5. Vencedores (CPA ≤ meta com volume) → **mover para a campanha de escala usando o mesmo ID de publicação** (preserva a prova social: comentários, curtidas).

**O que testar (ordem de impacto):** conceito/ângulo > formato (UGC, estático, carrossel, VSL) > hook > copy > CTA/detalhes visuais.

**Teste A/B nativo** do Meta: útil para perguntas específicas (ex.: público amplo vs. interesses), mas é mais caro e lento. Para criativos, a estrutura acima é mais prática.

## 9. Escala

**Vertical (aumentar verba):**
- 20–30% a cada 48–72h em campanhas estáveis. Aumentos maiores (50–100%) funcionam em contas com muito sinal, com risco de instabilidade de 2–3 dias.
- Escalar em CBO/Advantage+ é mais suave do que em conjuntos ABO pequenos.
- Use regras automatizadas ("se CPA < X nos últimos 3 dias, aumentar 20%").

**Horizontal:**
- Duplicar o vencedor para novos públicos, ângulos, países/regiões, posicionamentos.
- Novos criativos do ângulo vencedor (iterações).
- Novas ofertas/kits/bundles.

**Sinais de que a escala bateu no teto:** CPM e frequência sobem, o CPA marginal (custo da conversão adicional) piora muito. Calcule o **CPA marginal**: (gasto novo − gasto antigo) ÷ (conversões novas − conversões antigas). O CPA médio esconde isso.

**Escala bem-sucedida depende de produção de criativos.** Planeje 3–10 criativos novos por semana em contas com verba de R$ 30 mil+/mês.

## 10. Posicionamentos

- Padrão: **Advantage+ posicionamentos** (automático).
- Exceções: excluir **Audience Network** se houver muito clique de baixa qualidade (CTR alto e visualização da página baixa); separar Reels/Stories quando o criativo é só vertical.
- Garanta criativos em **9:16 (Stories/Reels)**, **4:5 (Feed)** e **1:1**, com zona segura (texto fora das bordas de UI).

## 11. Atribuição e leitura de resultados

- Configuração padrão: **7 dias após o clique + 1 dia após a visualização**. Para comparar períodos, mantenha sempre a mesma janela.
- A Meta tem descontinuado janelas de visualização longas nos relatórios. Se o usuário perceber números diferentes em relatórios antigos, essa é uma possível causa.
- A coluna "Comparar configurações de atribuição" mostra quanto vem de clique e quanto vem de visualização. Muita conversão de 1 dia view em remarketing = possível inflação (a pessoa compraria de qualquer jeito).
- **Atribuição incremental** (quando disponível na conta) otimiza para conversões que não ocorreriam sem o anúncio. Vale testar em contas maduras.
- Valide sempre com o backend e com o **MER** (faturamento total ÷ investimento total em mídia).
- Teste de incrementalidade/lift: em contas grandes, pedir *Conversion Lift* ao Meta ou fazer teste geográfico (holdout por região).

## 12. Campanhas de mensagem (WhatsApp/Direct) e cadastro

**Clique para WhatsApp (muito usado no Brasil):**
- Objetivo **Engajamento → Mensagens** ou **Vendas/Cadastros com WhatsApp como destino**. Otimizar para "conversas iniciadas" gera volume. Para qualidade, quando houver integração, otimize para lead/compra via **API de Conversões para mensagens** (exige WhatsApp Business Platform ou um CRM integrado).
- Mensagem de boas-vindas e perguntas frequentes configuradas para qualificar.
- Métrica real: **custo por conversa → taxa de resposta → custo por venda.** Peça ao cliente que marque as vendas (etiquetas no WhatsApp Business ou CRM).
- Tempo de resposta é crítico. Lead de WhatsApp esfria em minutos.

**Formulário instantâneo (Lead Ads):**
- "Maior volume" = mais leads, menor qualidade. "Maior intenção" = adiciona tela de confirmação.
- Perguntas qualificadoras (orçamento, prazo, região), condicionais quando fizer sentido.
- Integrar com o CRM (Zapier, RD Station, integração nativa) para resposta imediata.
- Enviar status do lead de volta (qualificado/venda) via CAPI para otimizar a qualidade.

## 13. Checklist de auditoria de conta Meta

- [ ] Pixel + API de Conversões ativos, com desduplicação (event_id) e boa **Qualidade de correspondência do evento** (EMQ ≥ 6, idealmente 8+).
- [ ] Eventos priorizados corretamente, domínio verificado.
- [ ] Valor e moeda enviados na compra; valores coerentes com o backend.
- [ ] Estrutura enxuta (sem dezenas de conjuntos com verba baixa).
- [ ] Conjuntos fora do "aprendizado limitado" ou com plano para isso.
- [ ] Diversidade de criativos (≥ 3 ângulos diferentes ativos), com formatos verticais.
- [ ] Frequência controlada (prospecção < 2–3 em 7 dias; remarketing tolera mais).
- [ ] Sobreposição de públicos baixa, exclusões de compradores aplicadas.
- [ ] Nomenclatura padronizada e UTMs em todos os anúncios.
- [ ] Atribuição consistente e conferência com o backend/MER.
- [ ] Qualidade da conta: sem restrições, com a política de anúncios respeitada (saúde, finanças, emagrecimento e antes/depois são categorias sensíveis).
- [ ] Página de destino rápida no mobile, coerente com o anúncio.
