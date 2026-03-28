import pandas as pd

def run_radar(narratives, risk, mode):

    data = [
        {
            "Ativo": "RNDRUSDT",
            "Entrada": 7.42,
            "SL": 7.27,
            "TP1": 7.57,
            "TP2": 7.71,
            "Score": 6,
            "Sinal": "COMPRA",
            "1D": "Alta (BOS)",
            "4H": "OB + FVG",
            "15M": "Sweep + HL",
            "1M": "Confirmação"
        }
    ]

    return pd.DataFrame(data)