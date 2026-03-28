import pandas as pd
import requests

# =========================
# Função principal do radar
# =========================
def run_radar(narratives, risk, mode):
    # 1️⃣ Pega top symbols
    top_symbols = get_top_symbols(limit=300)  # garante liquidez e universo maior
    ativos = filter_by_narrative(top_symbols, narratives)
    if not ativos:
        ativos = top_symbols[:20]

    results = []
    watchlist = []

    for ativo in ativos:
        try:
            df_1d = get_data(ativo, "1d")
            df_4h = get_data(ativo, "4h")
            df_15m = get_data(ativo, "15m")
            df_1m = get_data(ativo, "1m")
        except Exception as e:
            print(f"Erro API {ativo}: {e}")
            continue

        if df_1d.empty or df_4h.empty or df_15m.empty or df_1m.empty:
            watchlist.append({"Ativo": ativo, "Motivo": "Dados incompletos"})
            continue

        # =========================
        # SMC + OB + FVG + Sweep + Confirmação
        # =========================
        trend = detect_trend(df_1d)
        bos = detect_bos(df_1d)
        ob = detect_order_block(df_4h)
        fvg = detect_fvg(df_4h)
        sweep = detect_sweep(df_15m)
        confirm = detect_momentum(df_1m)

        score = 0
        if trend == "Alta": score += 2
        if bos: score += 1
        if ob: score += 2
        if fvg: score += 1
        if sweep: score += 1
        if confirm: score += 1

        direction = "COMPRA" if score >= 5 else "VENDA"
        entry, sl, tp, rr = sniper_entry(df_1m, direction)

        # =========================
        # Ativos que não passam ainda nos critérios
        # =========================
        if score < 4 or rr < 1.2:
            watchlist.append({
                "Ativo": ativo,
                "Score": score,
                "RR": rr,
                "Motivo": "Score ou R:R abaixo do esperado"
            })
            continue

        results.append({
            "Ativo": ativo,
            "Entrada": entry,
            "SL": sl,
            "TP1": round(entry + (tp-entry)*0.5,4),
            "TP2": tp,
            "RR": rr,
            "Score": score,
            "Sinal": direction,
            "1D": f"{trend} {'BOS' if bos else ''}",
            "4H": f"{ob if ob else 'Sem OB'} | {'FVG' if fvg else 'Sem FVG'}",
            "15M": "Sweep" if sweep else "Sem sweep",
            "1M": "Confirmação" if confirm else "Sem confirmação"
        })

    # =========================
    # Mensagem explicativa
    # =========================
    if len(results) < 5:
        msg = f"⚠️ Apenas {len(results)} ativos passaram nos critérios do Radar.\n"
        msg += "Possíveis motivos:\n"
        msg += "- Score baixo (SMC incompleto ou momentum fraco)\n"
        msg += "- R:R insuficiente\n"
        msg += "- Falta de dados na API Binance\n"
        msg += "- Volume/LIquidez baixo\n"
        print(msg)

    # =========================
    # Retorna resultados + watchlist
    # =========================
    return pd.DataFrame(results), pd.DataFrame(watchlist)