import pandas as pd
import requests
import time

# =========================
# CONFIGURAÇÃO
# =========================
BASE_URL = "https://api.binance.com/api/v3/klines"
TICKER_URL = "https://api.binance.com/api/v3/ticker/price"

# =========================
# FUNÇÃO RADAR
# =========================
def run_radar(narratives, risk, mode):
    """
    narratives: lista de narrativas (ex: AI, RWA, DeFi, L1, L2, Blue Chips, Oraculo)
    risk: "Baixo", "Médio", "Alto"
    mode: "Sniper", "Intraday", "Swing"
    """

    # =========================
    # PEGAR TODOS OS PARES USDT
    # =========================
    response = requests.get(TICKER_URL)
    all_tickers = response.json()
    usdt_pairs = [t['symbol'] for t in all_tickers if t['symbol'].endswith("USDT")]

    df_list = []

    # =========================
    # FILTRAGEM POR NARRATIVA
    # =========================
    for symbol in usdt_pairs:
        # Checa se ativo pertence a alguma narrativa
        if not any(n.upper() in symbol for n in narratives):
            continue

        # =========================
        # BUSCA DADOS DE 1H
        # =========================
        params = {
            "symbol": symbol,
            "interval": "1h",
            "limit": 50
        }

        try:
            klines = requests.get(BASE_URL, params=params).json()
            if len(klines) == 0:
                continue
        except:
            continue

        close = float(klines[-1][4])

        # =========================
        # CÁLCULO DE ENTRADA, SL E TP
        # =========================
        rr_map = {"Baixo": 1.5, "Médio": 2, "Alto": 3}
        rr = rr_map.get(risk, 2)

        entry = close
        sl = round(entry * 0.98, 4)
        tp1 = round(entry + (entry - sl) * rr * 0.5, 4)
        tp2 = round(entry + (entry - sl) * rr, 4)

        score = 5  # score inicial

        df_list.append({
            "Ativo": symbol,
            "Entrada": entry,
            "SL": sl,
            "TP1": tp1,
            "TP2": tp2,
            "Score": score,
            "Sinal": "COMPRA" if close > sl else "VENDA",
            "1D": "-",
            "4H": "-",
            "15M": "-",
            "1M": "-"
        })

        # Delay pequeno para não sobrecarregar
        time.sleep(0.05)

    df = pd.DataFrame(df_list)

    # Ranking por score
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)

    return df