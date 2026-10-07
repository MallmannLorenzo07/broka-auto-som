# Métricas, Fórmulas e Referências

## Fórmulas essenciais

| Métrica | Fórmula |
|---|---|
| CPM | Investimento ÷ Impressões × 1000 |
| CTR | Cliques ÷ Impressões × 100 |
| CPC | Investimento ÷ Cliques |
| Taxa de conversão (CVR) | Conversões ÷ Cliques × 100 (ou ÷ sessões, se for a métrica do site) |
| CPA / CPL / CAC (mídia) | Investimento ÷ Conversões |
| ROAS | Receita atribuída ÷ Investimento |
| MER (Marketing Efficiency Ratio) | Faturamento total ÷ Investimento total em mídia |
| aMER / nCAC | Faturamento de clientes novos ÷ mídia · Mídia ÷ clientes novos |
| Frequência | Impressões ÷ Alcance |
| Ticket médio (AOV) | Receita ÷ Pedidos |
| Margem de contribuição | (Preço − custo do produto − impostos − taxas de pagamento − frete subsidiado − comissões) ÷ Preço |
| **ROAS de equilíbrio** | 1 ÷ Margem de contribuição |
| **CPA máximo (equilíbrio)** | Ticket × Margem de contribuição |
| CPA alvo para lucro X% | Ticket × (Margem − X) |
| LTV (margem) | Ticket × Margem × Compras por ano × Anos de vida |
| CAC máximo por LTV | LTV ÷ 3 (regra comum LTV:CAC ≥ 3) |
| Payback do CAC | CAC ÷ (Ticket × Margem × compras por mês) |
| ROI | (Lucro gerado − Investimento) ÷ Investimento |
| CPA via funil | CPM ÷ (10 × CTR% × CVR%) |
| CPA marginal | Δ Investimento ÷ Δ Conversões |
| Hook rate | Visualizações de 3s ÷ Impressões |
| Hold rate | ThruPlays (ou 15s) ÷ Visualizações de 3s |
| Custo por lead qualificado | Investimento ÷ Leads qualificados |
| Custo por venda (leads) | CPL ÷ (taxa de qualificação × taxa de fechamento) |

### Exemplo de ROAS de equilíbrio
Produto R$ 200; custo R$ 70; impostos 10% (R$ 20); gateway 5% (R$ 10); frete subsidiado R$ 15.
Margem = (200 − 70 − 20 − 10 − 15) ÷ 200 = 42,5% → **ROAS de equilíbrio = 2,35** · **CPA máximo = R$ 85**.

Lembre: ROAS da plataforma ≠ ROAS real (atribuição, cancelamentos, boletos não pagos, devoluções). Ajuste o alvo por um fator de segurança (ex.: alvo de plataforma 20–30% acima do equilíbrio) ou calibre pelo MER.

## Faixas de referência (Brasil, aproximadas)

> **São só referências de mercado** para orientar a conversa. Variam muito por nicho, oferta, sazonalidade, criativo e período. O histórico da própria conta é sempre o melhor benchmark. Ao citar, deixe claro que é referência e não meta.

**Meta Ads**
| Métrica | Faixa comum |
|---|---|
| CPM | R$ 10–40 (sobe muito em out–dez; nichos competitivos passam disso) |
| CTR (link) | 0,8%–2% (prospecção); remarketing costuma ser maior |
| CPC (link) | R$ 0,50–3,00 |
| Taxa de conversão e-commerce (clique → compra) | 0,8%–3% |
| Frequência prospecção (7 dias) | < 2–3 saudável |
| Custo por conversa no WhatsApp | R$ 3–30 (nicho e região) |
| CPL formulário B2C | R$ 5–40 |

**Google Ads**
| Métrica | Faixa comum |
|---|---|
| CTR Pesquisa | 3%–10% (marca muito mais alto) |
| CPC Pesquisa | R$ 0,50–10 (jurídico, saúde, finanças e B2B podem passar de R$ 15–30) |
| Taxa de conversão Pesquisa (lead) | 3%–10% |
| Taxa de conversão Shopping | 0,8%–2,5% |

**E-commerce geral**
- Taxa de conversão do site: 0,5%–2% (média), 2–4% (bom).
- Taxa de abandono de carrinho: 70%–80%.
- Página de destino: carregamento mobile < 3s.

## Significância e volume mínimo

- Para comparar a taxa de conversão de duas variantes com segurança, você precisa de dezenas de conversões por variante (idealmente 30–100+), dependendo da diferença.
- Regra prática de decisão para anúncio: gastar pelo menos **2–3x o CPA alvo** antes de concluir que ele não converte.
- Para CTR (mais volume), algumas milhares de impressões por variante já dão um sinal útil.
- Use intervalos: "CPA entre R$ 40 e R$ 60 com o volume atual" é mais honesto que "CPA R$ 50".
- Teste rápido de proporções (aproximação z): z = (p1 − p2) ÷ √(p(1−p)(1/n1 + 1/n2)), com p = taxa combinada. |z| > 1,96 ≈ 95% de confiança.

## Glossário rápido

TOF/MOF/BOF (topo/meio/fundo de funil) · LAL (lookalike/semelhante) · CBO/ABO (orçamento na campanha/no conjunto) · CAPI (API de Conversões) · EMQ (qualidade de correspondência do evento) · IS (parcela de impressões) · QS (Índice de Qualidade) · tCPA/tROAS (CPA/ROAS desejado) · DPA (anúncio dinâmico de produto) · UGC (conteúdo gerado por usuário/criador) · VSL (vídeo de vendas) · MER (eficiência de marketing) · LTV (valor do cliente no tempo) · AOV (ticket médio) · SQL/MQL (lead qualificado para vendas/marketing).
