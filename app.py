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
    # =========================
# RANKING AUTOMÁTICO
# =========================
df = df.sort_values(by="Score", ascending=False)

st.subheader("🏆 Ranking de Oportunidades")

# =========================
# CARDS COM CORES
# =========================
for i in range(len(df)):

    row = df.iloc[i]

    color = "#00C853" if row["Sinal"] == "COMPRA" else "#D50000"

    st.markdown(f"""
<div style="
padding:15px;
margin-bottom:10px;
border-radius:10px;
background-color:#111;
border-left:5px solid {color};
">

<h3>{row['Ativo']} | {row['Sinal']}</h3>

<b>Score:</b> {row['Score']} <br>
<b>Entrada:</b> {row['Entrada']} | 
<b>SL:</b> {row['SL']} | 
<b>TP:</b> {row['TP2']} <br><br>

<b>1D:</b> {row['1D']}<br>
<b>4H:</b> {row['4H']}<br>
<b>15M:</b> {row['15M']}<br>
<b>1M:</b> {row['1M']}

</div>
""", unsafe_allow_html=True)

# destaque TOP 1
top = df.iloc[0]

st.success(f"🔥 MELHOR OPORTUNIDADE: {top['Ativo']} | Score {top['Score']}")
    # =========================
    # ANÁLISE
    # =========================
    st.subheader("🧠 Análise Institucional")

    st.text(analysis)