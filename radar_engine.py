
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

        for col in ["open","high","low","close"]:
            df[col] = df[col].astype(float)

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

def detect_fvg(df):
    for i in range(len(df)-3, len(df)-1):
        if df["low"].iloc[i] > df["high"].iloc[i-2]:
            return True
    return False

def detect_order_block(df):
    prev = df.iloc[-5:-1]

    bearish = prev[prev["close"] < prev["open"]]
    bullish = prev[prev["close"] > prev["open"]]

    last = df.iloc[-1]

    if last["close"] > last["open"] and not bearish.empty:
        return "Bullish OB"
    elif last["close"] < last["open"] and not bullish.empty:
        return "Bearish OB"

    return None

# =========================
# SNIPER + R:R
# =========================

def get_swing_low(df):
    return df["low"].rolling(10).min().iloc[-1]

def get_swing_high(df):
    return df["high"].rolling(10).max().iloc[-1]

def calculate_rr(entry, sl, tp):
    risk = abs(entry - sl)
    reward = abs(tp - entry)
    if risk == 0:
        return 0
    return round(reward / risk, 2)

def sniper_entry(df_1m, direction):
    price = df_1m["close"].iloc[-1]

    if direction == "COMPRA":
        sl = get_swing_low(df_1m)
        tp = price + (price - sl) * 2
    else:
        sl = get_swing_high(df_1m)
        tp = price - (sl - price) * 2

    rr = calculate_rr(price, sl, tp)

    return round(price, 4), round(sl, 4), round(tp, 4), rr

# =========================
# RADAR PRINCIPAL
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
        # 4H → ZONAS
        # =========================
        ob = detect_order_block(df_4h)
        fvg = detect_fvg(df_4h)

        # =========================
        # 15M → GATILHO
        # =========================
        sweep = detect_sweep(df_15m)

        # =========================
        # 1M → CONFIRMAÇÃO
        # =========================
        confirm = detect_momentum(df_1m)

        # =========================
        # SCORE
        # =========================
        score = 0

        if trend == "Alta":
            score += 2
        if bos:
            score += 1
        if ob:
            score += 2
        if fvg:
            score += 1
        if sweep:
            score += 1
        if confirm:
            score += 1

        direction = "COMPRA" if score >= 5 else "VENDA"

        # =========================
        # SNIPER ENTRY
        # =========================
        entry, sl, tp, rr = sniper_entry(df_1m, direction)

        # filtro institucional
        if rr < 1.5:
            continue

        results.append({
            "Ativo": ativo,
            "Entrada": entry,
            "SL": sl,
            "TP1": round(entry + (tp - entry) * 0.5, 4),
            "TP2": tp,
            "RR": rr,
            "Score": score,
            "Sinal": direction,
            "1D": f"{trend} {'BOS' if bos else ''}",
            "4H": f"{ob if ob else 'Sem OB'} | {'FVG' if fvg else 'Sem FVG'}",
            "15M": "Sweep" if sweep else "Sem sweep",
            "1M": "Confirmação" if confirm else "Sem confirmação"
        })

    return pd.DataFrame(results)