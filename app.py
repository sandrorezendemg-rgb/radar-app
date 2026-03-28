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

narratives_options = ["AI","RWA","DeFi","L1","L2","Blue Chips","Oraculo"]

# Checkboxes múltiplos em colunas
narratives = []
cols = st.columns(4)
for i, option in enumerate(narratives_options):
    if cols[i % 4].checkbox(option):
        narratives.append(option)

# Confere se ao menos uma narrativa foi selecionada
if not narratives:
    st.warning("Selecione ao menos uma narrativa para rodar o radar.")
    st.stop()

risk = st.radio("⚡ Nível de Risco", ["Baixo", "Médio", "Alto"], horizontal=True)
mode = st.radio("🏹 Modo Radar", ["Sniper", "Intraday", "Swing"], horizontal=True)

st.markdown("---")

# =========================
# EXECUÇÃO RADAR
# =========================
if st.button("🔍 Rodar Radar"):

    with st.spinner("Rodando Radar e analisando ativos..."):
        # run_radar retorna apenas df principal
        df = run_radar(narratives, risk, mode)

    # =========================
    # RESULTADOS
    # =========================
    if df.empty:
        st.warning("Nenhuma oportunidade passou nos critérios do Radar.")
    else:
        st.success(f"{len(df)} ativos selecionados para ação imediata.")

        # =========================
        # AÇÃO IMEDIATA E RANKING
        # =========================
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
        # RACIONAL INSTITUCIONAL
        # =========================
        st.subheader("🧠 Racional Institucional")
        analysis = run_agent(df.head(5).to_dict(orient="records"))
        st.info(analysis)

    st.markdown("---")
    st.caption("Radar Confluência PRO | SMC + Multi-Timeframe + Sniper R:R")