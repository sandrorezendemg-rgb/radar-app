import streamlit as st
import pandas as pd
from radar_engine import run_radar
from ai_agent import run_agent

st.set_page_config(layout="wide")

# =========================
# HEADER
# =========================
st.title("🚀 Radar Confluência PRO")
st.caption("SMC + Multi-Timeframe + Execução Inteligente")

# =========================
# FILTROS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    narratives = st.multiselect(
        "Narrativas",
        ["AI", "RWA", "DeFi", "Gaming"],
        default=["AI"]
    )

with col2:
    risk = st.selectbox("Risco", ["Baixo", "Médio", "Alto"])

with col3:
    mode = st.selectbox("Modo", ["Sniper", "Intraday", "Swing"])

# =========================
# BOTÃO
# =========================
if st.button("🔍 Rodar Radar"):

    df = run_radar(narratives, risk, mode)
    analysis = run_agent(df.head(3).to_dict(orient="records"))

    st.divider()

    # =========================
    # SINAIS EM CARDS
    # =========================
    st.subheader("📊 Oportunidades")

    cols = st.columns(len(df))

    for i, col in enumerate(cols):
        row = df.iloc[i]

        with col:
            st.markdown(f"""
### {row['Ativo']}

**Sinal:** {row['Sinal']}  
**Score:** {row['Score']}

Entrada: `{row['Entrada']}`  
SL: `{row['SL']}`  
TP1: `{row['TP1']}`  
TP2: `{row['TP2']}`

---
**1D:** {row['1D']}  
**4H:** {row['4H']}  
**15M:** {row['15M']}  
**1M:** {row['1M']}
""")

    st.divider()

    # =========================
    # ANÁLISE
    # =========================
    st.subheader("🧠 Análise Institucional")

    st.text(analysis)