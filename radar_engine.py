# radar_engine.py
import pandas as pd
import requests
from datetime import datetime

# =========================
# CONFIGURAÇÕES
# =========================
TIMEFRAMES = ["1d", "4h", "1h", "15m", "5m", "1m"]
MIN_VOLUME = 10000  # volume mínimo para considerar ativo

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

def simulate_smc(price, idx=1):
    """Gera Entry, SL, TP1 e TP2 diferentes por ativo"""
    factor = 0.98 + (idx % 5) * 0.005  # pequeno ajuste por ativo
    sl = round(price * factor, 4)
    tp1 = round(price * (1 + (idx % 5) * 0.01), 4)
    tp2 = round(price * (1 + ((idx % 5)+1) * 0.01), 4)
    entry = round(price, 4)
    score = max(3, min(10, 5 + (idx % 4)))  # Score entre 3 e 9
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
def run_radar(selected_narratives=None, risk="Médio", mode="Sniper"):
    """
    Executa Radar para teste de múltiplos ativos reais.
    selected_narratives é ignorado por enquanto.
    """
    symbols = get_binance_symbols()
    results = []

    for idx, sym in enumerate(symbols):
        price, volume = get_ticker(sym)
        if price is None or volume < MIN_VOLUME:
            continue

        entry, sl, tp1, tp2, score = simulate_smc(price, idx)
        multi_tf = generate_multi_tf()

        results.append({
            "Ativo": sym,
            "Entrada": entry,
            "SL": sl,
            "TP1": tp1,
            "TP2": tp2,
            "Score": score,
            "Sinal": "COMPRA" if idx % 2 == 0 else "VENDA",
            "1D": multi_tf["1D"],
            "4H": multi_tf["4H"],
            "15M": multi_tf["15M"],
            "1M": multi_tf["1M"]
        })

    df = pd.DataFrame(results)

    if df.empty:
        print("Nenhum ativo encontrado com volume suficiente.")

    # Ranking por Score
    df = df.sort_values(by="Score", ascending=False)
    return df