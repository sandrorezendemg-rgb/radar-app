# radar_engine.py
import pandas as pd
import requests
from datetime import datetime, timedelta

# =========================
# CONFIGURAÇÕES
# =========================
TIMEFRAMES = ["1d", "4h", "1h", "15m", "5m", "1m"]
MIN_VOLUME = 10000  # volume mínimo para considerar ativo

# Narratives dinâmicas (exemplo: categorização inicial)
NARRATIVE_KEYWORDS = {
    "AI": ["RNDR", "AGIX", "AIDOGE"],
    "RWA": ["PAXG", "TUSD"],
    "DEFI": ["UNI", "AAVE", "SUSHI"],
    "L1": ["ETH", "SOL", "ADA"],
    "L2": ["MATIC", "OP"],
    "BLUE CHIPS": ["BTC", "BNB"],
    "ORACULO": ["LINK", "API3"]
}

# =========================
# FUNÇÕES AUXILIARES
# =========================
def get_binance_symbols():
    """Busca todos os pares USDT ativos na Binance"""
    url = "https://api.binance.com/api/v3/exchangeInfo"
    res = requests.get(url, timeout=5).json()
    symbols = [
        s['symbol'] for s in res['symbols']
        if s['quoteAsset'] == 'USDT' and s['status'] == 'TRADING'
    ]
    return symbols

def get_ticker(symbol):
    """Retorna preço atual e volume"""
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
    try:
        data = requests.get(url, timeout=5).json()
        price = float(data.get("lastPrice", 0))
        volume = float(data.get("quoteVolume", 0))
        return price, volume
    except:
        return None, None

def get_klines(symbol, interval="1d", limit=100):
    """Retorna candles do ativo"""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    try:
        data = requests.get(url, timeout=5).json()
        candles = []
        for c in data:
            candles.append({
                "open": float(c[1]),
                "high": float(c[2]),
                "low": float(c[3]),
                "close": float(c[4]),
                "volume": float(c[5]),
                "time": datetime.fromtimestamp(c[0]/1000)
            })
        return candles
    except:
        return []

def assign_narrative(symbol):
    """Classifica ativo por narrativa usando keywords"""
    for key, keywords in NARRATIVE_KEYWORDS.items():
        if any(k in symbol for k in keywords):
            return key
    return "OUTROS"

def simulate_smc(price):
    """Simula Entry, SL, TP e Score para teste"""
    sl = round(price * 0.98, 4)
    tp1 = round(price * 1.02, 4)
    tp2 = round(price * 1.05, 4)
    entry = round(price, 4)
    score = 5
    return entry, sl, tp1, tp2, score

def generate_multi_tf():
    """Simula sinais multi-timeframe"""
    return {
        "1D": "Alta (BOS)",
        "4H": "OB + FVG",
        "15M": "Sweep + HL",
        "1M": "Confirmação"
    }

# =========================
# FUNÇÃO PRINCIPAL
# =========================
def run_radar(selected_narratives, risk="Médio", mode="Sniper"):
    symbols = get_binance_symbols()
    results = []

    for sym in symbols:
        narrative = assign_narrative(sym)
        if narrative not in selected_narratives:
            continue

        price, volume = get_ticker(sym)
        if price is None or volume < MIN_VOLUME:
            continue

        entry, sl, tp1, tp2, score = simulate_smc(price)
        multi_tf = generate_multi_tf()

        results.append({
            "Ativo": sym,
            "Narrativa": narrative,
            "Entrada": entry,
            "SL": sl,
            "TP1": tp1,
            "TP2": tp2,
            "Score": score,
            "Sinal": "COMPRA",
            "1D": multi_tf["1D"],
            "4H": multi_tf["4H"],
            "15M": multi_tf["15M"],
            "1M": multi_tf["1M"]
        })

    df = pd.DataFrame(results)
    if df.empty:
        print("Nenhum ativo encontrado para as narrativas selecionadas ou volume insuficiente.")

    # Ranking por Score
    df = df.sort_values(by="Score", ascending=False)
    return df