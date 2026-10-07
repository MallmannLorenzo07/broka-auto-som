#!/usr/bin/env python3
"""Analisa exports de campanhas (Meta Ads, Google Ads, TikTok Ads) em CSV ou XLSX.

Reconhece colunas em português e inglês, aceita números no formato brasileiro
("R$ 1.234,56") ou americano ("1,234.56"), agrega linhas repetidas (ex.: export
com quebra por dia), calcula CPM, CTR, CPC, CVR, CPA, ROAS e sinaliza ações.

Uso:
  python analisar_campanhas.py export.csv --cpa-alvo 80
  python analisar_campanhas.py export.csv --roas-alvo 3
  python analisar_campanhas.py export.csv --ticket 250 --margem 0.4
  python analisar_campanhas.py export.csv --col conversoes="Leads no site" --json
"""
import argparse
import csv
import io
import json
import re
import sys
import unicodedata

# ---------------------------------------------------------------- colunas
# Para cada campo: lista de (padrões que o cabeçalho deve conter, padrões proibidos),
# em ordem de prioridade. O cabeçalho é normalizado (minúsculo, sem acento).
CAMPOS = {
    "nome": [
        (["nome do anuncio"], []), (["ad name"], []),
        (["termo de pesquisa"], ["tipo", "status"]), (["search term"], ["type", "status"]),
        (["palavra-chave"], ["tipo", "status", "id"]), (["keyword"], ["type", "status", "id"]),
        (["nome do conjunto"], []), (["ad set name"], []), (["grupo de anuncios"], ["id", "status", "tipo"]),
        (["ad group"], ["id", "status", "type"]), (["nome da campanha"], []), (["campaign name"], []),
        (["campanha"], ["id", "tipo", "status", "orcamento", "veiculacao"]),
        (["campaign"], ["id", "type", "status", "budget", "delivery"]),
    ],
    "gasto": [
        (["valor usado"], []), (["amount spent"], []), (["valor gasto"], []),
        (["custo"], ["por", "/", "conv", "cpc", "medio"]), (["cost"], ["per", "/", "conv", "avg"]),
        (["investimento"], []), (["spend"], ["per"]), (["gasto"], ["por"]),
    ],
    "impressoes": [
        (["impressoes"], ["parcela", "custo", "por", "%", "taxa"]), (["impr"], ["parcela", "%", "share", "taxa"]),
        (["impressions"], ["share", "cost", "per", "%"]),
    ],
    "alcance": [(["alcance"], ["custo", "por"]), (["reach"], ["cost", "per"])],
    "frequencia": [(["frequencia"], []), (["frequency"], [])],
    "cliques": [
        (["cliques no link"], ["custo", "taxa", "ctr", "cpc", "unico", "saida"]),
        (["link clicks"], ["cost", "rate", "ctr", "cpc", "unique", "outbound"]),
        (["cliques de destino"], ["custo", "taxa", "unico"]), (["destination clicks"], ["cost", "rate", "unique"]),
        (["cliques"], ["custo", "taxa", "ctr", "cpc", "todos", "unico", "%"]),
        (["clicks"], ["cost", "rate", "ctr", "cpc", "all", "unique", "%"]),
    ],
    "conversoes": [
        (["compras"], ["valor", "custo", "roas", "taxa", "por"]), (["purchases"], ["value", "cost", "roas", "rate", "per"]),
        (["conversoes"], ["valor", "custo", "taxa", "todas", "visualizacao", "por", "/"]),
        (["conversions"], ["value", "cost", "rate", "all", "view", "per", "/"]),
        (["conv."], ["valor", "value", "custo", "cost", "taxa", "rate", "todas", "all", "/"]),
        (["resultados"], ["custo", "indicador", "tipo", "valor"]), (["results"], ["cost", "indicator", "type", "value"]),
        (["leads"], ["custo", "cost", "por", "per"]), (["cadastros"], ["custo", "por"]),
    ],
    "receita": [
        (["valor de conversao da compra"], ["custo", "/"]), (["purchase conversion value"], ["cost", "/"]),
        (["purchases value"], ["cost"]), (["valor da compra"], ["custo"]),
        (["valor conv"], ["custo", "/", "todas", "por"]), (["conv. value"], ["cost", "/", "all", "per"]),
        (["conversion value"], ["cost", "/", "all", "per"]), (["valor de conversao"], ["custo", "/", "todas", "por"]),
        (["receita"], []), (["revenue"], []), (["faturamento"], []),
    ],
}


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.strip().lower())


def mapear_colunas(cabecalho, overrides):
    cab_norm = [norm(c) for c in cabecalho]
    mapa = {}
    for campo, regras in CAMPOS.items():
        if campo in overrides:
            alvo = norm(overrides[campo])
            if alvo in cab_norm:
                mapa[campo] = cab_norm.index(alvo)
            continue
        for incluir, excluir in regras:
            for i, c in enumerate(cab_norm):
                if i in mapa.values():
                    continue
                if all(p in c for p in incluir) and not any(p in c for p in excluir):
                    mapa[campo] = i
                    break
            if campo in mapa:
                break
    return mapa


# ---------------------------------------------------------------- leitura
def ler_linhas(caminho):
    if caminho.lower().endswith((".xlsx", ".xlsm")):
        try:
            import openpyxl
        except ImportError:
            sys.exit("Para ler XLSX instale openpyxl (pip install openpyxl) ou exporte em CSV.")
        wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
        ws = wb.active
        return [["" if v is None else v for v in row] for row in ws.iter_rows(values_only=True)]

    with open(caminho, "rb") as f:
        bruto = f.read()
    if bruto.startswith((b"\xff\xfe", b"\xfe\xff")):
        texto = bruto.decode("utf-16")
    else:
        for enc in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                texto = bruto.decode(enc)
                break
            except UnicodeDecodeError:
                continue
    amostra = "\n".join(texto.splitlines()[:30])
    contagens = {d: amostra.count(d) for d in (",", ";", "\t")}
    delim = max(contagens, key=contagens.get)
    return list(csv.reader(io.StringIO(texto), delimiter=delim))


def achar_cabecalho(linhas, overrides):
    for idx, linha in enumerate(linhas[:30]):
        mapa = mapear_colunas(linha, overrides)
        if "gasto" in mapa and len(mapa) >= 3:
            return idx, mapa
    return None, None


# ---------------------------------------------------------------- números
RE_PT = re.compile(r"\d,\d{1,2}$|\d\.\d{3},")
RE_EN = re.compile(r"\d\.\d{1,2}$|\d\.\d{4,}$|\d,\d{3}\.")


def limpar(v):
    return re.sub(r"[R$US€\s %]", "", str(v)).strip()


def detectar_decimal(linhas, colunas):
    pt = en = 0
    for linha in linhas:
        for i in colunas:
            if i < len(linha) and not isinstance(linha[i], (int, float)):
                v = limpar(linha[i])
                pt += bool(RE_PT.search(v))
                en += bool(RE_EN.search(v))
    return "," if pt > en else "."


def num(v, decimal):
    if isinstance(v, (int, float)):
        return float(v)
    s = limpar(v)
    if s in ("", "-", "--", "—"):
        return None
    if decimal == ",":
        s = s.replace(".", "").replace(",", ".")
    else:
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


# ---------------------------------------------------------------- análise
def div(a, b):
    return a / b if a is not None and b else None


def analisar(linhas, idx_cab, mapa, args):
    dados = linhas[idx_cab + 1:]
    numericos = [i for c, i in mapa.items() if c != "nome"]
    decimal = detectar_decimal(dados, numericos)
    agregado = {}
    repetidos = set()
    for linha in dados:
        if not any(str(c).strip() for c in linha):
            continue
        nome = str(linha[mapa["nome"]]).strip() if "nome" in mapa and mapa["nome"] < len(linha) else "(sem nome)"
        if not nome or norm(nome).startswith("total") or norm(nome) in ("--", "-"):
            continue
        reg = agregado.get(nome)
        if reg is None:
            reg = agregado[nome] = {"nome": nome, "linhas": 0}
        else:
            repetidos.add(nome)
        reg["linhas"] += 1
        for campo in ("gasto", "impressoes", "alcance", "cliques", "conversoes", "receita", "frequencia"):
            if campo in mapa and mapa[campo] < len(linha):
                v = num(linha[mapa[campo]], decimal)
                if v is not None:
                    reg[campo] = reg.get(campo, 0) + v

    regs = [r for r in agregado.values() if r.get("gasto")]
    total = {k: sum(r.get(k, 0) for r in regs) for k in ("gasto", "impressoes", "cliques", "conversoes", "receita")}

    # metas
    cpa_alvo, roas_alvo, roas_eq = args.cpa_alvo, args.roas_alvo, None
    origem_meta = "informada"
    if args.margem:
        roas_eq = 1 / args.margem
        if args.ticket and not cpa_alvo:
            cpa_alvo = args.ticket * args.margem
            origem_meta = "CPA máximo = ticket × margem"
    if not cpa_alvo and not roas_alvo and not roas_eq:
        cpa_alvo = div(total["gasto"], total["conversoes"])
        origem_meta = "média da conta, pois nenhuma meta foi informada"
    tem_receita = "receita" in mapa and total["receita"] > 0

    for r in regs:
        g, imp, cl, cv, rec = (r.get(k) for k in ("gasto", "impressoes", "cliques", "conversoes", "receita"))
        cv = cv or 0
        r["cpm"] = div(g * 1000, imp) if imp else None
        r["ctr"] = div((cl or 0) * 100, imp) if imp and cl is not None else None
        r["cpc"] = div(g, cl)
        r["cvr"] = div(cv * 100, cl) if cl else None
        r["cpa"] = div(g, cv)
        r["roas"] = div(rec, g) if tem_receita else None
        r["share"] = div(g * 100, total["gasto"])
        if r["linhas"] > 1 or "frequencia" not in r:
            freq = div(imp, r.get("alcance")) if r["linhas"] == 1 else None
            r["frequencia"] = freq
        r["alertas"] = alertas(r, cv, cpa_alvo, roas_alvo, roas_eq, args)

    regs.sort(key=lambda r: r["gasto"], reverse=True)
    resumo = {
        **total,
        "cpm": div(total["gasto"] * 1000, total["impressoes"]),
        "ctr": div(total["cliques"] * 100, total["impressoes"]),
        "cpc": div(total["gasto"], total["cliques"]),
        "cvr": div(total["conversoes"] * 100, total["cliques"]),
        "cpa": div(total["gasto"], total["conversoes"]),
        "roas": div(total["receita"], total["gasto"]) if tem_receita else None,
        "cpa_alvo": cpa_alvo, "roas_alvo": roas_alvo, "roas_equilibrio": roas_eq,
        "origem_meta": origem_meta, "decimal": decimal, "itens": len(regs),
        "agregados": len(repetidos),
    }
    return resumo, regs


def alertas(r, cv, cpa_alvo, roas_alvo, roas_eq, a):
    out = []
    g = r["gasto"]
    if cpa_alvo:
        if cv == 0 and g >= 2 * cpa_alvo:
            out.append(("PAUSAR", f"gastou {n(g / cpa_alvo, 1)}x o CPA alvo sem conversão"))
        elif cv >= a.min_conv_pausa and r["cpa"] > 1.5 * cpa_alvo:
            out.append(("PAUSAR", f"CPA {r['cpa'] / cpa_alvo - 1:+.0%} vs alvo com {n(cv, 0 if cv == int(cv) else 1)} conversões"))
        elif cv >= a.min_conv and r["cpa"] <= 0.8 * cpa_alvo:
            out.append(("ESCALAR", f"CPA {r['cpa'] / cpa_alvo - 1:+.0%} vs alvo com {n(cv, 0 if cv == int(cv) else 1)} conversões"))
        elif cv == 0 and g < cpa_alvo:
            out.append(("AGUARDAR", "gasto ainda abaixo de 1x o CPA alvo"))
    if r["roas"] is not None and cv >= a.min_conv_pausa:
        if roas_eq and r["roas"] < roas_eq:
            out.append(("ABAIXO DO EQUILÍBRIO", f"ROAS {n(r['roas'], 2)} < equilíbrio {n(roas_eq, 2)}"))
        elif roas_alvo and r["roas"] >= 1.2 * roas_alvo and cv >= a.min_conv:
            out.append(("ESCALAR", f"ROAS {n(r['roas'], 2)} ≥ 120% da meta"))
        elif roas_alvo and r["roas"] < 0.7 * roas_alvo:
            out.append(("REVISAR", f"ROAS {n(r['roas'], 2)} < 70% da meta {n(roas_alvo, 2)}"))
    if r.get("frequencia") and r["frequencia"] > a.freq_max:
        out.append(("FADIGA", f"frequência {n(r['frequencia'], 1)} > {n(a.freq_max, 1)}"))
    if r.get("ctr") is not None and (r.get("impressoes") or 0) >= 1000 and r["ctr"] < a.ctr_min:
        out.append(("CTR BAIXO", f"CTR {n(r['ctr'], 2, '%')} < {n(a.ctr_min, 2, '%')}"))
    nome = norm(r["nome"])
    if out and any(k in nome for k in ("marca", "brand", "institucional")):
        out.append(("CONTEXTO", "campanha de marca: CPA/ROAS naturalmente bons; escala limitada pela demanda de busca"))
    elif out and any(k in nome for k in ("remarketing", "retarget", "rmkt", "rtg")):
        out.append(("CONTEXTO", "remarketing: resultado inflado por quem compraria de qualquer jeito; frequência alta é esperada"))
    return out


# ---------------------------------------------------------------- saída
def brl(v):
    if v is None:
        return "—"
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def n(v, casas=0, suf=""):
    if v is None:
        return "—"
    return f"{v:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".") + suf


def imprimir(resumo, regs, mapa, cabecalho, args):
    p = print
    p("# Análise de campanhas\n")
    p("**Colunas reconhecidas:** " + ", ".join(f"{c} → \"{cabecalho[i]}\"" for c, i in mapa.items()))
    faltando = [c for c in ("conversoes", "cliques", "impressoes", "receita") if c not in mapa]
    if faltando:
        p(f"**Não encontradas:** {', '.join(faltando)} (use --col campo=\"Nome da coluna\" se existirem com outro nome)")
    if resumo["agregados"]:
        p(f"**Obs.:** {resumo['agregados']} itens apareciam em várias linhas (ex.: quebra por dia) e foram somados; frequência recalculada indisponível nesses casos.")
    p("")
    p("## Resumo")
    p(f"- Itens com gasto: {resumo['itens']}")
    p(f"- Investimento: {brl(resumo['gasto'])} · Conversões: {n(resumo['conversoes'])}" + (f" · Receita: {brl(resumo['receita'])}" if resumo["roas"] is not None else ""))
    p(f"- CPM {brl(resumo['cpm'])} · CTR {n(resumo['ctr'], 2, '%')} · CPC {brl(resumo['cpc'])} · CVR {n(resumo['cvr'], 2, '%')}")
    p(f"- **CPA {brl(resumo['cpa'])}**" + (f" · **ROAS {n(resumo['roas'], 2)}**" if resumo["roas"] is not None else ""))
    metas = []
    if resumo["cpa_alvo"]:
        metas.append(f"CPA alvo {brl(resumo['cpa_alvo'])} ({resumo['origem_meta']})")
    if resumo["roas_alvo"]:
        metas.append(f"ROAS alvo {n(resumo['roas_alvo'], 2)}")
    if resumo["roas_equilibrio"]:
        metas.append(f"ROAS de equilíbrio {n(resumo['roas_equilibrio'], 2)}")
    if metas:
        p("- Referências: " + " · ".join(metas))

    pausar = [r for r in regs if any(t in ("PAUSAR", "ABAIXO DO EQUILÍBRIO") for t, _ in r["alertas"])]
    escalar = [r for r in regs if any(t == "ESCALAR" for t, _ in r["alertas"])]
    if pausar:
        g = sum(r["gasto"] for r in pausar)
        p(f"- Verba em candidatos a pausar/revisar: **{brl(g)} ({g / resumo['gasto']:.0%} do total)**")
    if escalar:
        g = sum(r["gasto"] for r in escalar)
        p(f"- Itens candidatos a escalar: {len(escalar)} (hoje com {g / resumo['gasto']:.0%} da verba)")
    top3 = sum(r["gasto"] for r in regs[:3])
    if len(regs) > 3:
        p(f"- Concentração: os 3 maiores itens têm {top3 / resumo['gasto']:.0%} da verba")

    p("\n## Tabela (ordenada por gasto)\n")
    cols = ["Nome", "Gasto", "%", "Impr.", "CPM", "CTR", "CPC", "Conv.", "CVR", "CPA"]
    tem_roas = resumo["roas"] is not None
    if tem_roas:
        cols.append("ROAS")
    cols.append("Freq.")
    p("| " + " | ".join(cols) + " |")
    p("|" + "---|" * len(cols))
    for r in regs[: args.top]:
        linha = [r["nome"][:50], brl(r["gasto"]), n(r["share"], 1, "%"), n(r.get("impressoes")),
                 brl(r["cpm"]), n(r["ctr"], 2, "%"), brl(r["cpc"]), n(r.get("conversoes") or 0, 0 if (r.get("conversoes") or 0) == int(r.get("conversoes") or 0) else 1),
                 n(r["cvr"], 2, "%"), brl(r["cpa"])]
        if tem_roas:
            linha.append(n(r["roas"], 2))
        linha.append(n(r.get("frequencia"), 2))
        p("| " + " | ".join(linha) + " |")
    if len(regs) > args.top:
        p(f"\n_(+{len(regs) - args.top} itens omitidos; use --top para ver mais)_")

    p("\n## Alertas\n")
    ordem = ["PAUSAR", "ABAIXO DO EQUILÍBRIO", "REVISAR", "FADIGA", "CTR BAIXO", "ESCALAR", "AGUARDAR", "CONTEXTO"]
    algum = False
    for tipo in ordem:
        itens = [(r, msg) for r in regs for t, msg in r["alertas"] if t == tipo]
        if not itens:
            continue
        algum = True
        p(f"**{tipo}**")
        for r, msg in itens:
            p(f"- {r['nome'][:60]} ({brl(r['gasto'])}): {msg}")
        p("")
    if not algum:
        p("Nenhum alerta com os critérios atuais.")
    p("_Alertas são triagem automática: confira fase de aprendizado, papel no funil e mudanças recentes antes de agir._")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("arquivo")
    ap.add_argument("--cpa-alvo", type=float)
    ap.add_argument("--roas-alvo", type=float)
    ap.add_argument("--ticket", type=float, help="ticket médio (com --margem deriva o CPA máximo)")
    ap.add_argument("--margem", type=float, help="margem de contribuição em fração (0.4 = 40%%)")
    ap.add_argument("--freq-max", type=float, default=3.0)
    ap.add_argument("--ctr-min", type=float, default=0.8, help="CTR mínimo em %% (padrão 0.8)")
    ap.add_argument("--min-conv", type=float, default=5, help="conversões mínimas para sugerir escala")
    ap.add_argument("--min-conv-pausa", type=float, default=3, help="conversões mínimas para julgar CPA/ROAS")
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--col", action="append", default=[], metavar='CAMPO="Coluna"',
                    help="força o mapeamento: nome, gasto, impressoes, alcance, frequencia, cliques, conversoes, receita")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.margem and args.margem > 1:
        args.margem /= 100

    overrides = {}
    for item in args.col:
        if "=" in item:
            k, v = item.split("=", 1)
            overrides[norm(k)] = v.strip().strip('"')

    linhas = ler_linhas(args.arquivo)
    idx, mapa = achar_cabecalho(linhas, overrides)
    if idx is None:
        print("Não reconheci as colunas do arquivo. Primeiras linhas encontradas:")
        for l in linhas[:5]:
            print("  ", l)
        sys.exit(1)
    resumo, regs = analisar(linhas, idx, mapa, args)
    if args.json:
        for r in regs:
            r["alertas"] = [{"tipo": t, "motivo": m} for t, m in r["alertas"]]
        json.dump({"resumo": resumo, "itens": regs,
                   "colunas": {c: linhas[idx][i] for c, i in mapa.items()}},
                  sys.stdout, ensure_ascii=False, indent=2, default=str)
        print()
    else:
        imprimir(resumo, regs, mapa, linhas[idx], args)


if __name__ == "__main__":
    main()
