import pandas as pd
import requests
import time

# =========================
# CONFIG API BINANCE
# =========================
BASE_URL = "https://api.binance.com/api/v3/klines"

# =========================
# MAPA DE NARRATIVAS
# =========================
NARRATIVE_MAP = {
    "AI": ["RNDRUSDT","GALAUSDT","AGIXUSDT","FETUSDT","SANDUSDT"],
    "RWA": ["PAXGUSDT","TUSDUSDT","DGXUSDT"],
    "DEFI": ["UNIUSDT","AAVEUSDT","CAKEUSDT","MKRUSDT"],
    "L1": ["ETHUSDT","SOLUSDT","ADAUSDT"],
    "L2": ["MATICUSDT","OPUSDT","ARBUSDT"],
    "BLUE CHIPS": ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT"],
    "ORACULO": ["LINKUSDT","API3USDT","TRBUSDT"]
}

# =========================
# FUNÇÃO RADAR
# =========================
def run_radar(narratives, risk, mode):
    df_list = []

    # =========================
    # Seleciona ativos da narrativa
    # =========================
    selected_symbols = []
    for n in narratives:
        selected_symbols += NARRATIVE_MAP.get(n.upper(), [])
    selected_symbols = list(set(selected_symbols))  # Remove duplicados

    if not selected_symbols:
        print("Nenhum ativo disponível para as narrativas selecionadas.")
        return pd.DataFrame()

    # =========================
    # Parâmetros de risco e R:R
    # =========================
    rr_map = {"Baixo": 1.5, "Médio": 2, "Alto": 3}
    rr = rr_map.get(risk, 2)

    # =========================
    # Busca dados e calcula entradas
    # =========================
    for symbol in selected_symbols:
        try:
            # Candles 1H (para teste rápido)
            params = {"symbol": symbol, "interval": "1h", "limit": 50}
            klines = requests.get(BASE_URL, params=params, timeout=5).json()
            if not klines:
                continue

            close = float(klines[-1][4])
            high = float(klines[-1][2])
            low = float(klines[-1][3])

            # =========================
            # Entrada / SL / TP dinâmicos
            # =========================
            entry = round(close, 4)
            sl = round(low * 0.995, 4)
            tp1 = round(entry + (entry - sl) * 0.5 * rr, 4)
            tp2 = round(entry + (entry - sl) * rr, 4)

            # Score inicial simplificado
            score = 5

            # Sinal simplificado
            sinal = "COMPRA" if close > sl else "VENDA"

            df_list.append({
                "Ativo": symbol,
                "Entrada": entry,
                "SL": sl,
                "TP1": tp1,
                "TP2": tp2,
                "Score": score,
                "Sinal": sinal,
                "1D": "-",
                "4H": "-",
                "15M": "-",
                "1M": "-"
            })

            time.sleep(0.05)  # Pequeno delay para evitar bloqueio

        except Exception as e:
            print(f"Erro ao processar {symbol}: {e}")
            continue

    df = pd.DataFrame(df_list)

    # =========================
    # Ranking por Score
    # =========================
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)

    if df.empty:
        print("Nenhum ativo válido encontrado para as narrativas selecionadas.")

    return df