import pandas as pd
from binance.client import Client

# =========================
# CONFIGURAÇÃO BINANCE
# =========================
API_KEY = "SUA_API_KEY"
API_SECRET = "SEU_API_SECRET"

client = Client(API_KEY, API_SECRET)

# =========================
# FUNÇÃO RADAR
# =========================
def run_radar(narratives, risk, mode):
    """
    narratives: lista de narrativas escolhidas pelo usuário
    risk: "Baixo", "Médio", "Alto"
    mode: "Sniper", "Intraday", "Swing"
    """

    # =========================
    # BUSCA DE ATIVOS
    # =========================
    tickers = client.get_ticker()  # Todos os pares disponíveis
    df_list = []

    # =========================
    # FILTRAGEM POR NARRATIVAS
    # =========================
    for t in tickers:
        symbol = t['symbol']

        # Apenas USDT (simplificação)
        if not symbol.endswith("USDT"):
            continue

        # Checa se ativo pertence a narrativa
        if not any(n.upper() in symbol for n in narratives):
            continue

        # =========================
        # DADOS HISTÓRICOS
        # =========================
        try:
            klines = client.get_klines(
                symbol=symbol,
                interval=Client.KLINE_INTERVAL_1HOUR,
                limit=50
            )
        except:
            continue

        # Preço de fechamento atual
        close = float(klines[-1][4])

        # =========================
        # CÁLCULO INICIAL DE ENTRADA E ALVOS
        # =========================
        # Ajusta R:R baseado em risco
        rr_map = {"Baixo": 1.5, "Médio": 2, "Alto": 3}
        rr = rr_map.get(risk, 2)

        # Entrada = último fechamento
        entry = close

        # Stop Loss = 2% abaixo do fechamento (exemplo)
        sl = round(entry * 0.98, 4)

        # TP1 e TP2 baseados no R:R
        tp1 = round(entry + (entry - sl) * rr * 0.5, 4)
        tp2 = round(entry + (entry - sl) * rr, 4)

        # Score fictício inicial
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

    df = pd.DataFrame(df_list)

    # =========================
    # RANKING POR SCORE
    # =========================
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)

    return df