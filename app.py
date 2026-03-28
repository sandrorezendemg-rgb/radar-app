# app.py
import streamlit as st
import pandas as pd
from radar_engine import run_radar

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(layout="wide")
st.title("🚀 Radar Confluência PRO")
st.caption("SMC + Multi-Timeframe + Execução Inteligente")

# =========================
# SELEÇÃO DE NARRATIVAS
# =========================
st.subheader("Escolha as Narrativas")

narratives_list = ["AI", "RWA", "DEFI", "L1", "L2", "BLUE CHIPS", "ORACULO"]
narratives_selected = st.multiselect(
    "Narrativas",
    narratives_list,
    default=[],
    help="Selecione uma ou mais narrativas. Se nenhuma, o radar varrerá todos os ativos USDT."
)

st.divider()

# =========================
# CONFIGURAÇÕES DE RISCO E MODO
# =========================
col1, col2 = st.columns(2)

with col1:
    risk = st.selectbox("Risco", ["Baixo", "Médio", "Alto"], index=1)

with col2:
    mode = st.selectbox("Modo", ["Sniper", "Intraday", "Swing"], index=0)

st.divider()

# =========================
# EXECUÇÃO DO RADAR
# =========================
if st.button("🔍 Rodar Radar"):

    with st.spinner("Executando Radar e coletando dados da Binance..."):
        df = run_radar(selected_narratives=narratives_selected, risk=risk, mode=mode)

    if df.empty:
        st.warning("Nenhum ativo encontrado com volume suficiente ou critérios aplicados.")
        st.stop()

    # =========================
    # FILTRAGEM DE SCORE
    # =========================
    df = df[df["Score"] >= 4]
    if df.empty:
        st.warning("Nenhum ativo com Score relevante encontrado.")
        st.stop()

    # =========================
    # RANKING
    # =========================
    df = df.sort_values(by="Score", ascending=False)

    # =========================
    # TABELA DE RANKING
    # =========================
    st.subheader("🏆 Ranking de Oportunidades")
    st.dataframe(df[["Ativo", "Sinal", "Score", "Entrada", "SL", "TP1", "TP2"]], use_container_width=True)

    st.divider()

    # =========================
    # CARDS DE AÇÃO IMEDIATA
    # =========================
    st.subheader("⚡ Ação Imediata - Top 5 Ativos")

    for idx, row in df.head(5).iterrows():
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
<b>TP1:</b> {row['TP1']}  
<b>TP2:</b> {row['TP2']}  

<hr>

<b>1D:</b> {row.get('1D','-')}<br>
<b>4H:</b> {row.get('4H','-')}<br>
<b>15M:</b> {row.get('15M','-')}<br>
<b>1M:</b> {row.get('1M','-')}

</div>
""", unsafe_allow_html=True)

    st.divider()

    # =========================
    # EXPLICAÇÃO DO RACIONAL
    # =========================
    st.subheader("🧠 Racional Institucional (Simulado)")

    st.info(
        "Para cada ativo, o Radar analisa multi-timeframe (1D → 1M) e aplica lógica SMC, OB + FVG e Sniper. "
        "Entradas e SL/TP são simuladas neste teste; valores reais virão com análise completa de fluxo e confluência."
    )