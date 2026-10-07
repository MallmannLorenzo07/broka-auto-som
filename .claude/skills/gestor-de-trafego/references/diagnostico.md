# Diagnóstico de Performance

## Índice
1. Método: decomposição do funil
2. Antes de diagnosticar: checagens de sanidade
3. Árvores de diagnóstico por sintoma
4. Como analisar um export (CSV/planilha)
5. Leitura de prints
6. Erros comuns de diagnóstico

---

## 1. Método: decomposição do funil

Todo CPA pode ser decomposto assim:

```
CPA = CPM ÷ (1000 × CTR × CVR)
     onde CTR = cliques/impressões e CVR = conversões/cliques

ROAS = (CTR × CVR × Ticket × 1000) ÷ CPM
```

Logo, uma variação de CPA vem de **um ou mais** destes fatores:
- **CPM** (custo do leilão): concorrência, sazonalidade, qualidade/relevância do anúncio, público estreito, posicionamento.
- **CTR** (atratividade do criativo): hook, oferta, fadiga, público errado.
- **CVR** (página + oferta + intenção do clique): landing page, preço, frete, checkout, velocidade, qualidade do tráfego.
- **Ticket/AOV** (só para ROAS): mix de produtos, cupons, upsell.

**Como fazer na prática:** monte uma tabela período atual × anterior (mesma duração, de preferência com o mesmo dia da semana) e calcule a variação % de cada elo. O elo com maior variação negativa é o primeiro suspeito.

| Métrica | Anterior | Atual | Δ% |
|---|---|---|---|
| CPM | | | |
| CTR (link) | | | |
| CPC | | | |
| Taxa de conversão (clique → compra) | | | |
| CPA | | | |
| Ticket médio | | | |
| ROAS | | | |

Para funis com etapas intermediárias, quebre o CVR: clique → visualização da página → adição ao carrinho → início do checkout → compra. Assim você localiza a etapa exata da perda.
- **Clique no link → visualização da página** baixo (< 70–80%): site lento, redirect, pixel quebrado, clique acidental (Audience Network).
- **Visualização → carrinho** baixo: oferta, preço, página de produto, desalinhamento entre anúncio e página.
- **Carrinho → checkout** baixo: frete, prazo, cadastro obrigatório.
- **Checkout → compra** baixo: meios de pagamento, parcelamento, PIX/boleto não pago, erro técnico.

## 2. Antes de diagnosticar: checagens de sanidade

Verifique isto antes de concluir que "a campanha piorou":
1. **Rastreamento:** o evento ainda dispara? Houve mudança no site, tema, checkout, domínio ou GTM? Compare o número da plataforma com o backend (Shopify, Nuvemshop, Hotmart, CRM).
2. **Atribuição:** a janela de atribuição mudou? A comparação está usando a mesma janela? Lembre que os dados dos últimos 1–3 dias ainda vão subir (conversões atrasadas são atribuídas à data da impressão/clique).
3. **Mudanças recentes:** edição relevante (orçamento, público, criativo, lance) reinicia o aprendizado. Peça o histórico de alterações.
4. **Fatores externos:** sazonalidade (Black Friday encarece o CPM de outubro a novembro, a virada do mês muda o poder de compra, feriados), concorrente agressivo, ruptura de estoque, mudança de preço, problema no site, greve dos Correios ou de transportadora.
5. **Volume:** com poucas conversões, a variação pode ser ruído. 10 → 7 vendas não é tendência.
6. **Pagamento pendente:** boleto e PIX não pagos inflam "compras" no pixel se o evento dispara na geração do pedido, e não na aprovação.

## 3. Árvores de diagnóstico por sintoma

### CPA subiu / ROAS caiu
1. **CPM subiu?**
   - Sim, em todas as campanhas → leilão/sazonalidade. Ação: aceitar temporariamente, segurar verba nos dias mais caros, reforçar criativos de alta relevância e ajustar a expectativa do cliente.
   - Sim, só numa campanha → público saturado/estreito, baixa relevância do anúncio, sobreposição de públicos. Ação: ampliar público, renovar criativos, consolidar conjuntos.
2. **CTR caiu?**
   - Com frequência subindo → **fadiga criativa**. Ação: novos criativos (ângulos novos, não só variações de cor).
   - Sem frequência alta → criativo fraco para o público atual ou mudança de posicionamento. Ação: testar hooks, revisar o placement.
3. **CVR caiu (CTR estável)?**
   - Problema de site/oferta/rastreamento. Checar velocidade, checkout, estoque, preço, frete, cupom expirado, evento de pixel.
   - Mudou a qualidade do tráfego? (Advantage+ expandiu para posicionamentos de baixa intenção, Display/parceiros no Google, PMax puxando tráfego de marca ou de Display.)
4. **Ticket caiu?** Mix de produtos, cupom agressivo, campanha de produto barato ganhando verba.

### Campanha não gasta / gasta pouco
- Lance/custo-alvo muito restritivo (Cost Cap, tCPA ou tROAS altos demais). Ação: afrouxar o alvo em 15–25% ou trocar para menor custo/Maximizar conversões.
- Público muito pequeno ou muitas exclusões.
- Criativo com baixa relevância ou em análise/reprovado (checar status e qualidade).
- Orçamento fragmentado demais (vários conjuntos com R$ 20/dia).
- Google: palavras-chave de baixo volume, "volume de pesquisa baixo", Índice de Qualidade baixo, limitado por lance, conversão marcada como secundária, aprovação limitada.
- Problema de pagamento/limite da conta.

### Gasta mas não converte
- Evento de otimização errado (otimizando para clique/visualização da página em vez de compra).
- Pixel/CAPI não está recebendo a conversão (checar Gerenciador de Eventos/Diagnóstico de tag).
- Tráfego de baixa qualidade: Audience Network, apps no Display, parceiros de pesquisa. Excluir ou separar.
- Desalinhamento entre anúncio e página (promessa diferente, produto diferente).
- Oferta não competitiva (preço, frete, prova social).
- Volume insuficiente para sair do aprendizado (CPA alvo × 50 > verba semanal). Ação: otimizar para um evento mais alto no funil (Adicionar ao carrinho/Iniciar checkout) ou consolidar.

### CTR alto, conversão baixa
- O criativo gera curiosidade, mas não qualifica (clickbait). Ajustar a promessa e mostrar o preço/produto no anúncio.
- Página não entrega o que o anúncio promete, ou está lenta (> 3s no mobile).
- Público errado: muito engajamento de quem não compra (ex.: público jovem para produto caro).

### CTR baixo, conversão boa
- O criativo filtra bem, mas atrai pouca gente. Testar hooks mais fortes mantendo a oferta. Esse cenário costuma ser bom para escalar com mais criativos do mesmo ângulo.

### Leads baratos, mas não fecham
- Formulário instantâneo com "volume maior" → mudar para "maior intenção", adicionar perguntas qualificadoras e uma tela de revisão.
- Otimizar para lead qualificado: enviar eventos do CRM (lead qualificado, venda) via API de Conversões/conversões offline e otimizar para eles quando houver volume.
- Comercial demorando para responder (tempo de resposta > 5 min derruba a conversão). Isso é processo, não mídia, mas impacta o resultado e vale apontar para o cliente.

### Resultado caiu "do nada" no Meta
- Checar: alteração de política/conta restrita, criativos reprovados, problema de domínio/eventos (Gerenciador de Eventos), mudança no site, bugs da plataforma (comunidade de gestores costuma reportar), sazonalidade, mudança na atribuição.
- Não reestruturar a conta inteira por 1–2 dias ruins. Olhe janelas de 7 dias.

### Google: impressões caíram
- Parcela de impressões perdida por classificação (lance/qualidade) vs. orçamento.
- Concorrente novo (Informações do leilão).
- Mudança no volume de busca (sazonalidade, Google Trends).
- Palavras negativas bloqueando demais. Anúncios reprovados.

## 4. Como analisar um export (CSV/planilha)

1. Rode o script:
   ```bash
   python scripts/analisar_campanhas.py <arquivo> [--cpa-alvo X | --roas-alvo Y | --ticket T --margem M]
   ```
2. Leia o **resumo** (totais, CPA/ROAS consolidados, concentração de verba).
3. Leia os **alertas** por linha: PAUSAR (gasto sem retorno), ESCALAR (abaixo da meta com volume), FADIGA (frequência alta), CTR BAIXO, ACIMA DO EQUILÍBRIO.
4. Cruze com o contexto antes de recomendar: os candidatos a pausar estão em aprendizado? São campanhas de topo de funil (que naturalmente têm CPA maior, mas alimentam o remarketing)?
5. Entregue a resposta: **top 3 ações por impacto financeiro** (quanto de verba está sendo desperdiçada/realocada), depois o detalhe.

Se o script não reconhecer colunas, ele lista as colunas encontradas. Nesse caso, peça ao usuário para exportar com as colunas padrão (veja abaixo) ou faça a análise manualmente.

**Colunas recomendadas para exportar no Meta:** Nome da campanha/conjunto/anúncio, Valor usado, Impressões, Alcance, Frequência, Cliques no link, Resultados, Custo por resultado, Compras, Valor de conversão da compra, Adições ao carrinho, Finalizações de compra iniciadas.
**No Google Ads:** Campanha, Custo, Impr., Cliques, Conversões, Valor conv., Parcela de impressões de pesquisa.

## 5. Leitura de prints

Quando o usuário mandar print do gerenciador:
- Transcreva os números relevantes numa tabela antes de analisar. Isso evita erro de leitura e deixa claro o que foi entendido.
- Se algo estiver ilegível ou cortado, diga o que não foi possível ler em vez de chutar.
- Observe também: status de veiculação ("Aprendizado", "Aprendizado limitado"), período selecionado, janela de atribuição, nível (campanha/conjunto/anúncio).

## 6. Erros comuns de diagnóstico

- Comparar períodos de durações diferentes ou com eventos diferentes (semana de Black Friday × semana comum).
- Julgar o topo de funil pelo CPA de último clique. Olhe também o impacto no remarketing e no faturamento total (MER).
- Pausar o anúncio "mais caro" que, na verdade, é o que traz mais volume.
- Ignorar que o Meta atribui por data de impressão/clique: os dias recentes sempre parecem piores.
- Otimizar só pelo ROAS da plataforma quando ele diverge muito do faturamento real. Use o MER (faturamento total ÷ investimento total) como verdade de negócio.
- Mexer em várias variáveis ao mesmo tempo e não saber o que funcionou.
