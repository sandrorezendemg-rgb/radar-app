import pandas as pd
import requests

# =========================
# NARRATIVAS
# =========================
NARRATIVAS = {
    "AI": ["RNDRUSDT", "FETUSDT", "AGIXUSDT"],
    "DeFi": ["UNIUSDT", "AAVEUSDT", "COMPUSDT"],
    "RWA": ["ONDOUSDT", "POLYXUSDT"],
    "Gaming": ["IMXUSDT", "GALAUSDT"]
}

# =========================
# BINANCE DATA
# =========================
def get_data(symbol, interval, limit=200):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}

    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        df = pd.DataFrame(data, columns=[
            "time","open","high","low","close","volume",
            "ct","qav","trades","tb","tq","ignore"
        ])

        df["close"] = df["close"].astype(float)
        df["high"] = df["high"].astype(float)
        df["low"] = df["low"].astype(float)

        return df
    except:
        return pd.DataFrame()

# =========================
# SMC CORE
# =========================

def detect_trend(df):
    return "Alta" if df["close"].iloc[-1] > df["close"].mean() else "Baixa"

def detect_bos(df):
    return df["high"].iloc[-1] > df["high"].rolling(20).max().iloc[-2]

def detect_sweep(df):
    return df["low"].iloc[-1] < df["low"].rolling(20).min().iloc[-2]

def detect_momentum(df):
    return df["close"].iloc[-1] > df["close"].iloc[-5]

# =========================
# RADAR
# =========================
def run_radar(narratives, risk, mode):

    ativos = []
    for n in narratives:
        ativos.extend(NARRATIVAS.get(n, []))

    ativos = list(set(ativos))

    results = []

    for ativo in ativos:

        df_1d = get_data(ativo, "1d")
        df_4h = get_data(ativo, "4h")
        df_15m = get_data(ativo, "15m")
        df_1m = get_data(ativo, "1m")

        if df_1d.empty or df_4h.empty or df_15m.empty or df_1m.empty:
            continue

        # =========================
        # 1D → BIAS
        # =========================
        trend = detect_trend(df_1d)
        bos = detect_bos(df_1d)

        # =========================
        # 4H → CONTEXTO
        # =========================
        momentum_4h = detect_momentum(df_4h)

        # =========================
        # 15M → GATILHO
        # =========================
        sweep = detect_sweep(df_15m)

        # =========================
        # 1M → CONFIRMAÇÃO
        # =========================
        confirm = detect_momentum(df_1m)

        # =========================
        # SCORE SMC
        # =========================
        score = 0

        if trend == "Alta":
            score += 2
        if bos:
            score += 1
        if momentum_4h:
            score += 1
        if sweep:
            score += 1
        if confirm:
            score += 1

        sinal = "COMPRA" if score >= 4 else "VENDA"

        price = df_1m["close"].iloc[-1]

        results.append({
            "Ativo": ativo,
            "Entrada": round(price, 4),
            "SL": round(price * 0.98, 4),
            "TP1": round(price * 1.02, 4),
            "TP2": round(price * 1.04, 4),
            "Score": score,
            "Sinal": sinal,
            "1D": f"{trend} {'BOS' if bos else ''}",
            "4H": "Momentum" if momentum_4h else "Fraco",
            "15M": "Sweep" if sweep else "Sem sweep",
            "1M": "Confirmação" if confirm else "Sem confirmação"
        })

    return pd.DataFrame(results)