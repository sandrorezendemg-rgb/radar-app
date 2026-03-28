import streamlit as st
import pandas as pd
from radar_engine import run_radar
from ai_agent import run_agent

# =========================
# CONFIG
# =========================
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
# EXECUÇÃO
# =========================
if st.button("🔍 Rodar Radar"):

    df = run_radar(narratives, risk, mode)

    if df.empty:
        st.warning("Nenhuma oportunidade encontrada.")
        st.stop()

    # =========================
    # FILTRO QUALIDADE
    # =========================
    df = df[df["Score"] >= 4]

    if df.empty:
        st.warning("Nenhuma oportunidade com score relevante.")
        st.stop()

    # =========================
    # RANKING
    # =========================
    df = df.sort_values(by="Score", ascending=False)

    top = df.iloc[0]

    st.divider()

    # =========================
    # AÇÃO IMEDIATA
    # =========================
    st.markdown("## ⚡ Ação Imediata")

    st.success(f"""
🎯 **Ativo:** {top['Ativo']}  
📈 **Sinal:** {top['Sinal']}  
📊 **Score:** {top['Score']}  

💰 **Entrada:** {top['Entrada']}  
🛑 **Stop:** {top['SL']}  
🎯 **Alvo:** {top['TP2']}
""")

    st.divider()

    # =========================
    # RANKING VISUAL
    # =========================
    st.subheader("🏆 Ranking de Oportunidades")

    for i in range(len(df)):
        row = df.iloc[i]

        color = "#00C853" if row["Sinal"] == "COMPRA" else "#D50000"

        qualidade = "🔥 ALTA" if row["Score"] >= 6 else "⚠️ MÉDIA"

        st.markdown(f"""
<div style="
padding:15px;
margin-bottom:12px;
border-radius:10px;
background-color:#111;
border-left:5px solid {color};
">

<h3>{row['Ativo']} | {row['Sinal']}</h3>

<b>Score:</b> {row['Score']}  
<b>Qualidade:</b> {qualidade}  

<br>

<b>Entrada:</b> {row['Entrada']}  
<b>SL:</b> {row['SL']}  
<b>TP:</b> {row['TP2']}  

<hr>

<b>1D:</b> {row.get('1D','-')}<br>
<b>4H:</b> {row.get('4H','-')}<br>
<b>15M:</b> {row.get('15M','-')}<br>
<b>1M:</b> {row.get('1M','-')}

</div>
""", unsafe_allow_html=True)

    st.divider()

    # =========================
    # ANÁLISE IA
    # =========================
    st.subheader("🧠 Racional Institucional")

    analysis = run_agent(df.head(3).to_dict(orient="records"))

    st.info(analysis)