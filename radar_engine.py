import pandas as pd
import requests

def get_binance_data(symbol="BTCUSDT", interval="15m", limit=100):
    url = f"https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }

    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "time","open","high","low","close","volume",
        "close_time","qav","trades","tbbav","tbqav","ignore"
    ])

    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)

    return df


def run_radar(narratives, risk, mode):

    ativos = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]

    results = []

    for ativo in ativos:

        df = get_binance_data(ativo)

        if df.empty:
            continue

        price = df["close"].iloc[-1]

        # lógica simples (placeholder SMC)
        score = 5 if price > df["close"].mean() else 3
        sinal = "COMPRA" if score >= 5 else "VENDA"

        results.append({
            "Ativo": ativo,
            "Entrada": round(price, 2),
            "SL": round(price * 0.98, 2),
            "TP1": round(price * 1.02, 2),
            "TP2": round(price * 1.04, 2),
            "Score": score,
            "Sinal": sinal,
            "1D": "Tendência baseada em média",
            "4H": "Zona simulada",
            "15M": "Fluxo ativo",
            "1M": "Confirmação leve"
        })

    return pd.DataFrame(results)