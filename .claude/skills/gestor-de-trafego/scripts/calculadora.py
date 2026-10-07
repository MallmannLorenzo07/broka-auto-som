#!/usr/bin/env python3
"""Calculadora de tráfego pago: viabilidade, projeção, orçamento, leads, LTV e escala.

Exemplos:
  python calculadora.py equilibrio --ticket 297 --margem 0.45
  python calculadora.py equilibrio --ticket 200 --custo-produto 70 --impostos 10 --taxas 5 --frete 15
  python calculadora.py projecao --orcamento 10000 --cpm 25 --ctr 1.2 --cvr 2 --ticket 180
  python calculadora.py orcamento --vendas 100 --cpa 60
  python calculadora.py leads --vendas 20 --taxa-qualificacao 40 --taxa-fechamento 15 --cpl 25 --ticket 5000 --margem 0.3
  python calculadora.py ltv --ticket 150 --margem 0.5 --compras-ano 3 --anos 2
  python calculadora.py escala --orcamento 300 --passo 20 --dias 3 --alvo 1500

Percentuais (ctr, cvr, taxas, impostos) em % (1.2 = 1,2%). Margem em fração (0.45) ou % (45).
"""
import argparse


def brl(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n(v, c=2):
    return f"{v:,.{c}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def frac(m):
    return m / 100 if m is not None and m > 1 else m


def equilibrio(a):
    if a.margem is None:
        if a.custo_produto is None:
            raise SystemExit("Informe --margem ou --custo-produto (com --impostos/--taxas/--frete opcionais).")
        custos = a.custo_produto + a.ticket * (a.impostos + a.taxas) / 100 + a.frete
        margem = (a.ticket - custos) / a.ticket
        print("## Margem de contribuição")
        print(f"Ticket {brl(a.ticket)} − produto {brl(a.custo_produto)} − impostos {n(a.impostos, 1)}% "
              f"− taxas {n(a.taxas, 1)}% − frete {brl(a.frete)} = {brl(a.ticket - custos)} → **{n(margem * 100, 1)}%**\n")
    else:
        margem = frac(a.margem)
    if margem <= 0:
        raise SystemExit("Margem ≤ 0: cada venda já dá prejuízo antes da mídia. Reveja preço/custos.")
    roas_eq = 1 / margem
    cpa_max = a.ticket * margem
    print("## Equilíbrio")
    print(f"- **ROAS de equilíbrio:** 1 ÷ {n(margem, 3)} = **{n(roas_eq)}**")
    print(f"- **CPA máximo (lucro zero):** {brl(a.ticket)} × {n(margem * 100, 1)}% = **{brl(cpa_max)}**")
    print("\n## Alvos para lucro após mídia")
    print("| Lucro desejado (% do ticket) | CPA alvo | ROAS alvo |")
    print("|---|---|---|")
    for lucro in (5, 10, 15, 20):
        m_rest = margem - lucro / 100
        if m_rest <= 0:
            continue
        print(f"| {lucro}% | {brl(a.ticket * m_rest)} | {n(1 / m_rest)} |")
    print("\nObs.: o ROAS da plataforma costuma divergir do real (atribuição, cancelamentos, boletos/PIX não pagos). "
          "Use margem de segurança ou calibre pelo MER.")


def projecao(a):
    ctr, cvr = a.ctr / 100, a.cvr / 100
    print("## Projeção")
    print(f"Premissas: orçamento {brl(a.orcamento)}, CPM {brl(a.cpm)}, CTR {n(a.ctr)}%, CVR {n(a.cvr)}%"
          + (f", ticket {brl(a.ticket)}" if a.ticket else "") + "\n")
    print("| Cenário | Impressões | Cliques | CPC | Conversões | CPA |" + (" Receita | ROAS |" if a.ticket else ""))
    print("|---|---|---|---|---|---|" + ("---|---|" if a.ticket else ""))
    for nome, f_cpm, f_ctr, f_cvr in (("Pessimista", 1.2, 0.8, 0.8), ("Realista", 1, 1, 1), ("Otimista", 0.9, 1.15, 1.2)):
        cpm = a.cpm * f_cpm
        imp = a.orcamento / cpm * 1000
        cl = imp * ctr * f_ctr
        conv = cl * cvr * f_cvr
        linha = f"| {nome} | {n(imp, 0)} | {n(cl, 0)} | {brl(a.orcamento / cl)} | {n(conv, 1)} | {brl(a.orcamento / conv) if conv else '—'} |"
        if a.ticket:
            rec = conv * a.ticket
            linha += f" {brl(rec)} | {n(rec / a.orcamento)} |"
        print(linha)
    print("\nCenários: pessimista = CPM +20%, CTR e CVR −20%; otimista = CPM −10%, CTR +15%, CVR +20%.")


def orcamento(a):
    verba = a.vendas * a.cpa
    print("## Orçamento necessário")
    print(f"{n(a.vendas, 0)} conversões × CPA {brl(a.cpa)} = **{brl(verba)}** no período")
    print(f"- Por dia (30 dias): {brl(verba / 30)}")
    semana = verba / 30 * 7
    print(f"- Conversões por semana: {n(a.vendas / 30 * 7, 1)} "
          + ("(≥ 50/semana: dá para sair do aprendizado em 1 conjunto)" if a.vendas / 30 * 7 >= 50
             else "(< 50/semana: concentre em poucos conjuntos ou otimize para um evento mais alto do funil)"))
    print(f"- Verba semanal: {brl(semana)}")
    if a.ticket:
        print(f"- Receita esperada: {brl(a.vendas * a.ticket)} · ROAS {n(a.vendas * a.ticket / verba)}")


def leads(a):
    q, f = a.taxa_qualificacao / 100, a.taxa_fechamento / 100
    leads_nec = a.vendas / (q * f)
    print("## Funil de leads")
    print(f"{n(a.vendas, 0)} vendas ÷ ({n(a.taxa_qualificacao, 0)}% qualificação × {n(a.taxa_fechamento, 0)}% fechamento) "
          f"= **{n(leads_nec, 0)} leads** ({n(leads_nec * q, 0)} qualificados)")
    if a.cpl:
        verba = leads_nec * a.cpl
        print(f"- Verba: {n(leads_nec, 0)} × CPL {brl(a.cpl)} = **{brl(verba)}**")
        print(f"- Custo por lead qualificado: {brl(a.cpl / q)} · **Custo por venda: {brl(a.cpl / (q * f))}**")
    if a.ticket and a.margem:
        m = frac(a.margem)
        cpv_max = a.ticket * m
        print(f"- Custo por venda máximo (ticket × margem): {brl(cpv_max)} → **CPL máximo: {brl(cpv_max * q * f)}**")


def ltv(a):
    m = frac(a.margem)
    valor = a.ticket * m * a.compras_ano * a.anos
    print("## LTV")
    print(f"{brl(a.ticket)} × {n(m * 100, 0)}% × {n(a.compras_ano, 1)} compras/ano × {n(a.anos, 1)} anos = **{brl(valor)}** de margem por cliente")
    print(f"- CAC máximo (LTV:CAC 3:1): **{brl(valor / 3)}** · no limite (1:1): {brl(valor)}")
    print(f"- CPA de equilíbrio na 1ª compra: {brl(a.ticket * m)}")
    print(f"- Payback se o CAC for 1,5x a margem da 1ª compra: {n(1.5 * 12 / a.compras_ano, 1)} meses")


def escala(a):
    print("## Cronograma de escala")
    print(f"Aumentos de {n(a.passo, 0)}% a cada {a.dias} dias até {brl(a.alvo)}/dia\n")
    print("| Dia | Orçamento diário |")
    print("|---|---|")
    v, d = a.orcamento, 0
    print(f"| {d} | {brl(v)} |")
    while v < a.alvo and d < 365:
        d += a.dias
        v = min(v * (1 + a.passo / 100), a.alvo)
        print(f"| {d} | {brl(v)} |")
    print(f"\nTempo total: ~{d} dias. Só avance se o CPA dos últimos 3 dias estiver dentro da meta; "
          "se piorar >20%, segure ou volte um degrau.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("equilibrio", help="ROAS/CPA de equilíbrio e alvos")
    p.add_argument("--ticket", type=float, required=True)
    p.add_argument("--margem", type=float)
    p.add_argument("--custo-produto", type=float)
    p.add_argument("--impostos", type=float, default=0, help="%% sobre o preço")
    p.add_argument("--taxas", type=float, default=0, help="gateway/marketplace/plataforma, %% sobre o preço")
    p.add_argument("--frete", type=float, default=0, help="frete subsidiado por pedido (R$)")
    p.set_defaults(f=equilibrio)

    p = sub.add_parser("projecao", help="projeção por funil (CPM→CTR→CVR)")
    for k in ("orcamento", "cpm", "ctr", "cvr"):
        p.add_argument(f"--{k}", type=float, required=True)
    p.add_argument("--ticket", type=float)
    p.set_defaults(f=projecao)

    p = sub.add_parser("orcamento", help="verba necessária para uma meta")
    p.add_argument("--vendas", type=float, required=True, help="meta de conversões no mês")
    p.add_argument("--cpa", type=float, required=True)
    p.add_argument("--ticket", type=float)
    p.set_defaults(f=orcamento)

    p = sub.add_parser("leads", help="funil de leads até a venda")
    p.add_argument("--vendas", type=float, required=True)
    p.add_argument("--taxa-qualificacao", type=float, required=True, help="%%")
    p.add_argument("--taxa-fechamento", type=float, required=True, help="%%")
    p.add_argument("--cpl", type=float)
    p.add_argument("--ticket", type=float)
    p.add_argument("--margem", type=float)
    p.set_defaults(f=leads)

    p = sub.add_parser("ltv", help="LTV e CAC máximo")
    p.add_argument("--ticket", type=float, required=True)
    p.add_argument("--margem", type=float, required=True)
    p.add_argument("--compras-ano", type=float, required=True)
    p.add_argument("--anos", type=float, default=1)
    p.set_defaults(f=ltv)

    p = sub.add_parser("escala", help="cronograma de aumento de orçamento")
    p.add_argument("--orcamento", type=float, required=True, help="orçamento diário atual")
    p.add_argument("--alvo", type=float, required=True, help="orçamento diário desejado")
    p.add_argument("--passo", type=float, default=20, help="%% por degrau")
    p.add_argument("--dias", type=int, default=3, help="dias entre aumentos")
    p.set_defaults(f=escala)

    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
