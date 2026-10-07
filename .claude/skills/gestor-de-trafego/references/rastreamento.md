# Rastreamento e Mensuração

## Índice
1. Arquitetura recomendada
2. Meta: Pixel + API de Conversões
3. Google: tag, conversões, enhanced conversions, GA4
4. UTMs e parâmetros
5. Conversões offline / CRM
6. Diagnóstico de discrepâncias
7. Privacidade e LGPD

---

## 1. Arquitetura recomendada

```
Site/Checkout ──► GTM (web) ──► Pixel Meta / Google Tag / TikTok Pixel / GA4
        │
        └──► Servidor (CAPI direto da plataforma, GTM server-side ou gateway) ──► Meta CAPI / Google / TikTok Events API
CRM ──► eventos offline (lead qualificado, venda) ──► Meta CAPI / Google Ads (importação) / TikTok
```

- **Plataformas de e-commerce** (Shopify, Nuvemshop, VTEX, Tray, WooCommerce, Yampi) e **de infoproduto** (Hotmart, Kiwify, Eduzz) têm integrações nativas de pixel/CAPI. Prefira o nativo, bem configurado, a gambiarras.
- **GTM server-side** (Stape, Google Cloud, outros) para contas maiores: mais controle, melhor qualidade de dados, primeira parte.

## 2. Meta: Pixel + API de Conversões

**Eventos padrão:** PageView, ViewContent, AddToCart, InitiateCheckout, AddPaymentInfo, Purchase (com `value` e `currency`), Lead, CompleteRegistration, Contact, Schedule, Subscribe.

**Checklist:**
- [ ] Pixel e CAPI enviando os mesmos eventos com **`event_id` igual** para desduplicação (Gerenciador de Eventos mostra a taxa de desduplicação).
- [ ] **Qualidade da correspondência (EMQ):** envie e-mail, telefone, nome, cidade/estado/CEP (com hash), `fbp`, `fbc`, IP e user agent. Meta: ≥ 6, idealmente 8+ para a Purchase.
- [ ] `fbc` capturado a partir do `fbclid` da URL (preserve-o em redirects).
- [ ] Purchase dispara **uma vez**, na página de obrigado/aprovação, com o valor correto (sem frete/imposto duplicado e na mesma moeda).
- [ ] Boleto/PIX: idealmente, Purchase só na aprovação (via CAPI do servidor/checkout). Se o pixel dispara na geração, separe "pedido gerado" de "compra aprovada".
- [ ] Domínio verificado no Business Manager.
- [ ] Testar com a ferramenta **Testar eventos** e com a extensão Meta Pixel Helper.
- [ ] Diagnóstico do Gerenciador de Eventos sem alertas críticos.

## 3. Google: tag, conversões, enhanced conversions, GA4

- **Google Tag** (gtag ou GTM) com o vinculador de conversões; auto-tagging (`gclid`) ativo.
- Conversões do **Google Ads nativas** para o lance (mais precisas); importação do GA4 é opção, mas cuidado com duplicidade (não marque as duas como principais).
- **Enhanced conversions** (web e para leads): envia e-mail/telefone com hash.
- **Modo de consentimento v2** quando há banner de cookies (obrigatório para tráfego do EEE; boa prática no Brasil com LGPD).
- **GA4:** eventos de e-commerce recomendados (`view_item`, `add_to_cart`, `begin_checkout`, `purchase` com `transaction_id`), vínculo com Google Ads e Merchant Center, filtros de tráfego interno, retenção de dados em 14 meses.
- **Valor dinâmico** e `transaction_id` na compra para evitar duplicadas.
- Ligações: número de encaminhamento do Google e conversões de ligação pelo site.

## 4. UTMs e parâmetros

**Padrão sugerido (Meta, nos parâmetros de URL do anúncio):**
```
utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}
```
**TikTok:** `utm_source=tiktok&utm_medium=paid_social&utm_campaign=__CAMPAIGN_NAME__&utm_content=__CID_NAME__&utm_term=__AID_NAME__`
**Google:** auto-tagging (`gclid`) + modelo de acompanhamento opcional: `{lpurl}?utm_source=google&utm_medium=cpc&utm_campaign={campaignid}&utm_content={creative}&utm_term={keyword}`

- Padronize em minúsculas, sem espaços (use `_` ou `-`).
- Para WhatsApp: mensagem pré-preenchida com um código do anúncio, ou link intermediário com UTM → redirect para wa.me registrando o clique.
- Ferramentas de atribuição de terceiros (Utmify, Triple Whale, Hyros, Northbeam, entre outras) ajudam a cruzar UTMs com vendas; o Brasil tem várias específicas para infoproduto e e-commerce.

## 5. Conversões offline / CRM

- **Meta:** API de Conversões com eventos do CRM (`Lead` → `QualifiedLead`/`Purchase` com `action_source = system_generated` ou `crm`, conforme a integração). Integrações nativas: RD Station, HubSpot, Kommo, Zapier, Make.
- **Google:** importação por GCLID (guardar o gclid no formulário/CRM) ou enhanced conversions for leads (por e-mail/telefone com hash). Janela de importação: até 90 dias após o clique.
- **Valor:** envie o valor real da venda para permitir otimização por valor.
- **Frequência:** diária ou automática; atrasos longos reduzem a utilidade para o algoritmo.

## 6. Diagnóstico de discrepâncias

| Sintoma | Causas prováveis |
|---|---|
| Plataforma mostra mais vendas que o backend | Duplicidade (pixel + CAPI sem event_id; Purchase na página de obrigado recarregada), boleto/PIX não pago contado, view-through, atribuição a múltiplas plataformas (cada uma reivindica a venda) |
| Plataforma mostra menos que o backend | CAPI ausente, bloqueadores/iOS, checkout em domínio externo sem pixel, redirect perdendo parâmetros, vendas de outros canais (orgânico, e-mail) |
| GA4 ≠ Google Ads | Modelos de atribuição e data de crédito diferentes (GA4 atribui na data da conversão; o Ads, na data do clique), conversões entre dispositivos, consentimento |
| Soma das plataformas > faturamento real | Normal: cada plataforma reivindica crédito. Use o **MER** e testes de incrementalidade como verdade |

**Regra:** a "verdade" de negócio é o backend (faturamento, pedidos pagos, clientes novos). As plataformas servem para otimização relativa (qual anúncio/conjunto é melhor), não como contabilidade.

## 7. Privacidade e LGPD

- Base legal para coletar/usar dados (consentimento ou legítimo interesse, conforme o caso); política de privacidade atualizada.
- Banner de cookies com gestão de consentimento quando aplicável.
- Listas de clientes: envie sempre com hash (as plataformas fazem o hash ao subir, mas evite compartilhar planilhas em texto puro com terceiros).
- Contrato com o cliente definindo quem é controlador/operador dos dados.
