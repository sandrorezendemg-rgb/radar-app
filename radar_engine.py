import pandas as pd
import requests
import time

# =========================
# CONFIGURAÇÃO API BINANCE
# =========================
BASE_URL = "https://api.binance.com/api/v3/klines"
TICKER_URL = "https://api.binance.com/api/v3/ticker/price"

# =========================
# MAPA DE NARRATIVAS
# =========================
NARRATIVE_MAP = {
    "AI": ["RNDRUSDT","MORPHOUSDT","TAOUSDT"],
    "RWA": ["PAXGUSDT","TUSDUSDT"],
    "DeFi": ["UNIUSDT","AAVEUSDT","CAKEUSDT"],
    "L1": ["ETHUSDT","SOLUSDT","ADAUSDT"],
    "L2": ["MATICUSDT","OPUSDT","ARBUSDT"],
    "BLUE CHIPS": ["BTCUSDT","ETHUSDT","XRPUSDT"],
    "ORACULO": ["LINKUSDT","HBARUSDT"]
}

# =========================
# FUNÇÃO RADAR
# =========================
def run_radar(narratives, risk, mode):
    """
    narratives: lista de narrativas escolhidas pelo usuário
    risk: "Baixo", "Médio", "Alto"
    mode: "Sniper", "Intraday", "Swing"
    """
    df_list = []

    # =========================
    # Seleciona ativos da narrativa
    # =========================
    selected_symbols = []
    for n in narratives:
        selected_symbols += NARRATIVE_MAP.get(n.upper(), [])
    selected_symbols = list(set(selected_symbols))  # Remove duplicados

    # =========================
    # BUSCA DADOS DE MERCADO
    # =========================
    for symbol in selected_symbols:
        params = {
            "symbol": symbol,
            "interval": "1h",
            "limit": 50
        }

        try:
            klines = requests.get(BASE_URL, params=params, timeout=5).json()
            if len(klines) == 0:
                continue
        except:
            continue

        close = float(klines[-1][4])

        # =========================
        # CÁLCULO ENTRADA / SL / TP
        # =========================
        rr_map = {"Baixo": 1.5, "Médio": 2, "Alto": 3}
        rr = rr_map.get(risk, 2)

        entry = close
        sl = round(entry * 0.98, 4)
        tp1 = round(entry + (entry - sl) * rr * 0.5, 4)
        tp2 = round(entry + (entry - sl) * rr, 4)

        # Score inicial simplificado
        score = 5

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

        time.sleep(0.05)  # Delay pequeno para API

    df = pd.DataFrame(df_list)

    # =========================
    # Ranking por Score
    # =========================
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)

    # =========================
    # Mensagem caso não encontre ativos
    # =========================
    if df.empty:
        print("Nenhum ativo encontrado para as narrativas selecionadas.")

    return df