# Planejamento de Mídia, Orçamento, Proposta e Onboarding

## Índice
1. Briefing/diagnóstico inicial do cliente
2. Viabilidade (a conta antes do plano)
3. Plano de mídia por fases
4. Distribuição de orçamento
5. Projeção e metas
6. Sazonalidade no Brasil
7. Proposta comercial e precificação do serviço
8. Onboarding (primeiros 30 dias)
9. Rotina de gestão

---

## 1. Briefing inicial do cliente

Perguntas que mais mudam a estratégia:
- **Negócio:** o que vende, para quem, onde (região), diferenciais, concorrentes.
- **Números:** ticket médio, margem de contribuição, LTV/recompra, faturamento atual, % que vem do digital.
- **Objetivo:** vendas online, leads, mensagens, visitas à loja, agendamentos. Meta numérica e prazo.
- **Histórico:** já anunciou? Quanto investia, CPA/ROAS, o que funcionou e o que não funcionou. Acesso às contas (Business Manager, Google Ads, GA4, GTM, plataforma de e-commerce/CRM).
- **Estrutura:** site/landing, checkout, meios de pagamento, capacidade de atendimento (quantos leads o time consegue atender?), estoque, prazo de entrega.
- **Ativos criativos:** fotos, vídeos, depoimentos, criadores, identidade visual, quem produz.
- **Restrições:** verba mensal, políticas do setor, aprovações, LGPD.

## 2. Viabilidade

Sempre calcule antes de prometer:
1. **CPA máximo** = ticket × margem (ou, para leads: valor do cliente × margem × taxa de fechamento × taxa de qualificação).
2. **Verba necessária** = meta de vendas × CPA esperado.
3. **CPA esperado:** histórico da conta, ou estimativa por funil (CPM × CTR × CVR), sempre com cenários pessimista/realista/otimista.
4. Compare: se o CPA esperado > CPA máximo, o plano precisa mudar **a oferta** (ticket, bundle, upsell, recorrência) ou **a conversão** (site, atendimento), não só a mídia.

Use `scripts/calculadora.py` (`equilibrio`, `projecao`, `orcamento`, `leads`, `ltv`) e mostre a conta.

## 3. Plano de mídia por fases

**Fase 1 — Fundação (semanas 1–2)**
- Rastreamento (pixel + CAPI, GA4, conversões Google, UTMs).
- Auditoria do site/landing (velocidade, oferta, prova social, checkout).
- Estrutura enxuta de campanhas, criativos iniciais (3–5 ângulos).
- Campanhas de fundo de funil primeiro (Pesquisa/marca, remarketing) para gerar caixa e sinal.

**Fase 2 — Validação (semanas 3–6)**
- Teste de criativos/ângulos e ofertas.
- Sair do aprendizado, achar o CPA/ROAS real.
- Primeiras otimizações (negativas, pausas, realocação).

**Fase 3 — Escala (mês 2+)**
- Escalar vencedores (vertical + horizontal).
- Novos canais (TikTok, YouTube, Demand Gen).
- Produção contínua de criativos, CRO, LTV (e-mail/WhatsApp para recompra).

## 4. Distribuição de orçamento

Pontos de partida (ajuste por nicho e histórico):

| Cenário | Distribuição sugerida |
|---|---|
| E-commerce iniciante | 60–70% Meta (prospecção ampla + Advantage+), 20–30% Google (Shopping/PMax + marca), 5–10% remarketing/testes |
| Serviço local | 50–70% Google Pesquisa, 30–50% Meta (raio + WhatsApp) |
| B2B | 50–60% Google Pesquisa, 20–30% LinkedIn, 10–20% Meta remarketing/conteúdo |
| Infoproduto perpétuo | 70–85% Meta, 10–20% YouTube/Google (marca + VSL) |
| Lançamento | Captação 50–60%, aquecimento 10–20%, carrinho aberto 25–35% |

- **Regra 70/20/10:** 70% no que já funciona, 20% em otimizações/expansões, 10% em testes novos.
- Verba mínima por campanha para gerar aprendizado (veja `meta-ads.md` §4). Se a verba total é pequena, **concentre** em um canal/campanha.
- **Pacing:** acompanhe o gasto vs. o planejado semanalmente; antecipe ajustes em datas comerciais.

## 5. Projeção e metas

Monte 3 cenários com premissas explícitas:
```
| Cenário | CPM | CTR | CVR | CPA | Vendas | Receita | ROAS |
| Pessimista | ... |
| Realista | ... |
| Otimista | ... |
```
- Projeções de mês 1 devem ser conservadoras (aprendizado + testes).
- Defina **metas de processo** além das de resultado (n° de criativos testados, rastreamento ok, tempo de resposta do comercial).

## 6. Sazonalidade no Brasil

| Período | Efeito |
|---|---|
| Janeiro | Pós-festas, volta às aulas (material escolar), liquidações; CPM mais baixo |
| Fevereiro/Março | Carnaval (queda de atenção em alguns nichos); Dia do Consumidor (15/03) |
| Abril/Maio | Páscoa; **Dia das Mães** (2ª maior data do varejo) |
| Junho | Dia dos Namorados (12/06); festas juninas |
| Julho | Férias; liquidações de inverno |
| Agosto | Dia dos Pais (2º domingo) |
| Setembro | Semana do Brasil/"Black Friday de setembro"; Dia do Cliente (15/09) |
| Outubro | Dia das Crianças (12/10); CPM começa a subir |
| Novembro | **Black Friday** (CPM no pico; aquecimento/lista de espera em outubro) |
| Dezembro | Natal (prazos de entrega!), 13º salário; CPM alto até ~20/12 |

- **Dias do mês:** muitos nichos vendem mais no começo do mês (salário) e perto do dia 20 (vale/adiantamento).
- Black Friday: capte leads/lista antes (CPM mais barato), crie criativos com antecedência, use ajustes sazonais no Google e não teste coisas novas na semana de pico.

## 7. Proposta comercial e precificação do serviço

**Modelos de cobrança comuns:**
- Fee fixo mensal (mais comum): referência pelo escopo (n° de plataformas, campanhas, relatórios, reuniões, criativos inclusos).
- Fee + % da verba (ex.: fee mínimo + 10–20% do investimento acima de X).
- Fee + bônus por performance (meta de CPA/ROAS/faturamento). Exige rastreamento confiável e definição clara.
- Setup/implementação cobrado à parte (rastreamento, estrutura, auditoria).

**Estrutura da proposta:**
1. Diagnóstico (o que vimos: oportunidades e problemas).
2. Objetivo e metas (com viabilidade mostrada).
3. Estratégia (canais, fases, funil).
4. Escopo (o que está e o que não está incluso: criativos, landing page, CRM, gestão de redes sociais…).
5. Cronograma (primeiros 90 dias).
6. Rotina de relatórios e reuniões.
7. Investimento (fee + verba de mídia recomendada, separados).
8. Responsabilidades do cliente (acessos, aprovações, atendimento de leads, envio de dados de venda).
9. Prazo de contrato/aviso prévio.

**Alinhamento de expectativa:** deixe claro que o mês 1 é de aprendizado, que o resultado depende também da oferta, do site e do atendimento, e que a verba de mídia é paga direto às plataformas.

## 8. Onboarding (primeiros 30 dias)

- [ ] Acessos: Business Manager (parceiro), conta de anúncios, página/IG, pixel, catálogo; Google Ads (MCC), GA4, GTM, Merchant Center; plataforma de e-commerce/CRM; Search Console.
- [ ] Forma de pagamento da conta de anúncio no nome do cliente.
- [ ] Auditoria de rastreamento (veja `rastreamento.md`) e correções.
- [ ] Auditoria da conta (veja os checklists em `meta-ads.md` §13 e `google-ads.md` §9).
- [ ] Pesquisa de concorrentes e de avatar; banco de ângulos.
- [ ] Briefing e pedido dos primeiros criativos.
- [ ] Estrutura inicial no ar, com nomenclatura e UTMs.
- [ ] Dashboard/relatório configurado (Looker Studio, Supermetrics, Reportei, planilha).
- [ ] Reunião de kickoff com metas, rotina e responsáveis definidos.

## 9. Rotina de gestão

**Diário (5–15 min/conta):** gasto vs. orçamento, anomalias (gasto travado, CPA disparado, reprovação), saldo/pagamento.
**2–3x por semana:** pausas e escalas, termos de pesquisa (Google), frequência e fadiga, novos criativos.
**Semanal:** análise por ângulo/criativo, realocação de verba, matriz de testes, relatório curto para o cliente.
**Mensal:** relatório completo, revisão de metas, planejamento do mês seguinte (sazonalidade), auditoria de rastreamento.
**Trimestral:** revisão de estratégia, novos canais, teste de incrementalidade, renegociação de metas/escopo.
