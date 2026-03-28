import streamlit as st
import pandas as pd
from radar_engine import run_radar
from ai_agent import run_agent

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide", page_title="🚀 Radar Confluência PRO")

# =========================
# HEADER
# =========================
st.title("🚀 Radar Confluência PRO")
st.caption("SMC + Multi-Timeframe + Execução Inteligente")

st.divider()

# =========================
# NARRATIVAS (Checkbox estilo futurista)
# =========================
st.subheader("Selecione Narrativas")

options = ["AI", "RWA", "DEFI", "L1", "L2", "BLUE CHIPS", "ORACULO"]
cols = st.columns(len(options))
selected_narratives = []

for idx, n in enumerate(options):
    if cols[idx].checkbox(n):
        selected_narratives.append(n)

if not selected_narratives:
    st.info("Selecione ao menos uma narrativa para rodar o Radar.")

st.divider()

# =========================
# RISCO e MODO
# =========================
col1, col2 = st.columns(2)

with col1:
    risk = st.radio("Risco", ["Baixo", "Médio", "Alto"], horizontal=True)

with col2:
    mode = st.radio("Modo", ["Sniper", "Intraday", "Swing"], horizontal=True)

st.divider()

# =========================
# EXECUÇÃO RADAR
# =========================
if st.button("🔍 Rodar Radar"):
    if not selected_narratives:
        st.warning("Selecione ao menos uma narrativa.")
        st.stop()

    df = run_radar(selected_narratives, risk, mode)

    if df.empty:
        st.warning("Nenhum ativo encontrado para as narrativas selecionadas.")
        st.stop()

    # Filtrar por Score mínimo
    df = df[df["Score"] >= 4]
    if df.empty:
        st.warning("Nenhuma oportunidade com score relevante.")
        st.stop()

    # Ranking
    df = df.sort_values(by="Score", ascending=False)
    top = df.iloc[0]

    st.divider()

    # =========================
    # AÇÃO IMEDIATA (Top Ativo)
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
    # RANKING VISUAL DE TODOS OS ATIVOS
    # =========================
    st.subheader("🏆 Ranking de Oportunidades")

    for _, row in df.iterrows():
        color = "#00C853" if row["Sinal"] == "COMPRA" else "#D50000"
        qualidade = "🔥 ALTA" if row["Score"] >= 6 else "⚠️ MÉDIA"

        st.markdown(f"""
<div style="
padding:15px;
margin-bottom:12px;
border-radius:10px;
background-color:#111;
border-left:5px solid {color};
color:#fff;
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
    # RACIONAL INSTITUCIONAL
    # =========================
    st.subheader("🧠 Racional Institucional")
    analysis = run_agent(df.head(3).to_dict(orient="records"))
    st.info(analysis)