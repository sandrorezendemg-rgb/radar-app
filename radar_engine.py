# radar_engine.py
import pandas as pd
import requests

def run_radar(selected_narratives=None, risk="Médio", mode="Sniper"):
    """
    selected_narratives: lista de narrativas escolhidas pelo usuário
    risk: Baixo, Médio, Alto
    mode: Sniper, Intraday, Swing
    """

    # Se nenhuma narrativa for selecionada, varrer todas
    all_narratives = ["AI", "RWA", "DEFI", "L1", "L2", "BLUE CHIPS", "ORACULO"]
    if not selected_narratives:
        selected_narratives = all_narratives

    df_list = []

    # API pública Binance
    url = "https://api.binance.com/api/v3/ticker/24hr"
    resp = requests.get(url)
    tickers = resp.json()  # Lista de dicionários

    # Filtra apenas pares USDT
    usdt_tickers = [t for t in tickers if t['symbol'].endswith('USDT')]

    # Para cada narrativa, pegar até 10 ativos aleatórios para teste
    for narrative in selected_narratives:
        narrative_tickers = usdt_tickers[:10]  # Aqui pode ser refinado por mapeamento de narrativa
        for t in narrative_tickers:
            last_price = float(t['lastPrice'])
            df_list.append({
                "Ativo": t['symbol'],
                "Entrada": last_price,
                "SL": last_price * 0.98,
                "TP1": last_price * 1.02,
                "TP2": last_price * 1.05,
                "Score": 5,  # Simulado
                "Sinal": "COMPRA",
                "1D": "-",
                "4H": "-",
                "15M": "-",
                "1M": "-"
            })

    df = pd.DataFrame(df_list)

    return df