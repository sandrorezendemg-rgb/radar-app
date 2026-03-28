import streamlit as st
import pandas as pd
from radar_engine import run_radar
from ai_agent import run_agent

# =========================
# CONFIGURAÇÃO PÁGINA
# =========================
st.set_page_config(
    page_title="🚀 Radar Confluência PRO",
    layout="wide"
)

# =========================
# HEADER
# =========================
st.title("🚀 Radar Confluência PRO")
st.caption("SMC + Multi-Timeframe + Execução Inteligente + Sniper R:R")

st.markdown("---")

# =========================
# FILTROS VISUAIS
# =========================
st.subheader("🔧 Seleção de Narrativas e Perfil")

cols = st.columns([1,1,1,1])

narratives = []
if cols[0].button("AI"): narratives.append("AI")
if cols[1].button("RWA"): narratives.append("RWA")
if cols[2].button("DeFi"): narratives.append("DeFi")
if cols[3].button("L1"): narratives.append("L1")

cols2 = st.columns([1,1,1,1])
if cols2[0].button("L2"): narratives.append("L2")
if cols2[1].button("Blue Chips"): narratives.append("Blue Chips")
if cols2[2].button("Oráculo"): narratives.append("Oraculo")
if cols2[3].button("Todas"): narratives = ["AI","RWA","DeFi","L1","L2","Blue Chips","Oraculo"]

risk = st.radio("⚡ Nível de Risco", ["Baixo", "Médio", "Alto"], horizontal=True)
mode = st.radio("🏹 Modo Radar", ["Sniper", "Intraday", "Swing"], horizontal=True)

st.markdown("---")

# =========================
# EXECUÇÃO RADAR
# =========================
if st.button("🔍 Rodar Radar"):

    with st.spinner("Rodando Radar e analisando ativos..."):
        df, watchlist = run_radar(narratives, risk, mode)

    # =========================
    # RESULTADOS
    # =========================
    if df.empty:
        st.warning("Nenhuma oportunidade passou nos critérios do Radar.")
        if not watchlist.empty:
            st.subheader("📌 Watchlist de ativos próximos")
            st.table(watchlist)
    else:
        st.success(f"{len(df)} ativos selecionados para ação imediata.")
        st.subheader("⚡ Ação Imediata")
        for idx, row in df.iterrows():
            color = "#00C853" if row["Sinal"]=="COMPRA" else "#D50000"
            qualidade = "🔥 ALTA" if row["Score"]>=6 else "⚠️ MÉDIA"
            st.markdown(f"""
<div style="padding:15px;margin-bottom:12px;border-radius:10px;
             background-color:#111;border-left:5px solid {color};">
<h3>{row['Ativo']} | {row['Sinal']}</h3>
<b>Score:</b> {row['Score']}  | <b>Qualidade:</b> {qualidade}<br>
<b>Entrada:</b> {row['Entrada']}  | <b>SL:</b> {row['SL']}  | <b>TP:</b> {row['TP2']}<br>
<hr>
<b>1D:</b> {row.get('1D','-')}<br>
<b>4H:</b> {row.get('4H','-')}<br>
<b>15M:</b> {row.get('15M','-')}<br>
<b>1M:</b> {row.get('1M','-')}
</div>
""", unsafe_allow_html=True)

        # =========================
        # WATCHLIST
        # =========================
        if not watchlist.empty:
            st.subheader("📌 Watchlist de ativos próximos")
            st.table(watchlist)

        # =========================
        # RACIONAL INSTITUCIONAL
        # =========================
        st.subheader("🧠 Racional Institucional")
        analysis = run_agent(df.head(5).to_dict(orient="records"))
        st.info(analysis)

    st.markdown("---")
    st.caption("Radar Confluência PRO | SMC + Multi-Timeframe + Sniper R:R")