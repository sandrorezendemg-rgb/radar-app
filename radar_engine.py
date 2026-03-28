import pandas as pd
import requests

# =========================
# MAPA DE NARRATIVAS
# =========================
NARRATIVAS = {
    "AI": ["RNDRUSDT", "FETUSDT", "AGIXUSDT"],
    "DeFi": ["UNIUSDT", "AAVEUSDT", "COMPUSDT"],
    "RWA": ["ONDOUSDT", "POLYXUSDT"],
    "Gaming": ["IMXUSDT", "GALAUSDT"]
}

def get_binance_data(symbol, interval="15m", limit=100):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()

        df = pd.DataFrame(data, columns=[
            "time","open","high","low","close","volume",
            "close_time","qav","trades","tbbav","tbqav","ignore"
        ])

        df["close"] = df["close"].astype(float)
        return df

    except:
        return pd.DataFrame()

# =========================
# RADAR PRINCIPAL
# =========================
def run_radar(narratives, risk, mode):

    ativos = []

    for n in narratives:
        ativos.extend(NARRATIVAS.get(n, []))

    ativos = list(set(ativos))  # remove duplicados

    results = []

    for ativo in ativos:

        df = get_binance_data(ativo)

        if df.empty:
            continue

        price = df["close"].iloc[-1]
        media = df["close"].mean()

        score = 6 if price > media else 3
        sinal = "COMPRA" if score >= 5 else "VENDA"

        results.append({
            "Ativo": ativo,
            "Entrada": round(price, 3),
            "SL": round(price * 0.98, 3),
            "TP1": round(price * 1.02, 3),
            "TP2": round(price * 1.04, 3),
            "Score": score,
            "Sinal": sinal,
            "1D": "Tendência dinâmica",
            "4H": "Zona ativa",
            "15M": "Fluxo",
            "1M": "Confirmação"
        })

    return pd.DataFrame(results)