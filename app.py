  
import streamlit as st
from radar_engine import run_radar
from ai_agent import run_agent

st.set_page_config(layout="wide")

# =========================
# ESTILO FUTURISTA
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
button {
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("🚀 Radar Confluência PRO")
st.caption("Modo Institucional Ativo")

# =========================
# NARRATIVAS (TOGGLE STYLE)
# =========================
st.subheader("🧠 Narrativas")

col1, col2, col3, col4 = st.columns(4)

with col1:
    ai = st.toggle("AI")
with col2:
    defi = st.toggle("DeFi")
with col3:
    rwa = st.toggle("RWA")
with col4:
    gaming = st.toggle("Gaming")

narratives = []
if ai: narratives.append("AI")
if defi: narratives.append("DeFi")
if rwa: narratives.append("RWA")
if gaming: narratives.append("Gaming")

# =========================
# CONTROLE RÁPIDO
# =========================
col5, col6 = st.columns(2)

with col5:
    risk = st.radio("Risco", ["Baixo", "Médio", "Alto"], horizontal=True)

with col6:
    mode = st.radio("Modo", ["Sniper", "Intraday", "Swing"], horizontal=True)

# =========================
# EXECUÇÃO
# =========================
if st.button("⚡ Rodar Radar"):

    df = run_radar(narratives, risk, mode)

    if df.empty:
        st.warning("Nenhum ativo encontrado.")
        st.stop()

    df = df.sort_values(by="Score", ascending=False)

    top = df.iloc[0]

    # =========================
    # AÇÃO IMEDIATA
    # =========================
    st.markdown("## ⚡ Melhor Trade Agora")

    st.success(f"""
🎯 {top['Ativo']} | {top['Sinal']}  
Score: {top['Score']}

Entrada: {top['Entrada']}  
SL: {top['SL']}  
TP: {top['TP2']}
""")

    st.divider()

    # =========================
    # CARDS FUTURISTAS
    # =========================
    for _, row in df.iterrows():

        color = "#00FFAA" if row["Sinal"] == "COMPRA" else "#FF4B4B"

        st.markdown(f"""
<div style="
padding:15px;
margin-bottom:10px;
border-radius:12px;
background: linear-gradient(145deg,#111,#1c1f26);
border-left:4px solid {color};
">

<h3>{row['Ativo']} | {row['Sinal']}</h3>

Score: {row['Score']} <br>

Entrada: {row['Entrada']}  
SL: {row['SL']}  
TP: {row['TP2']}  

<hr>

1D: {row['1D']}  
4H: {row['4H']}  
15M: {row['15M']}  
1M: {row['1M']}

</div>
""", unsafe_allow_html=True)

    st.divider()

    # =========================
    # IA
    # =========================
    st.subheader("🧠 Racional IA")

    analysis = run_agent(df.head(3).to_dict(orient="records"))

    st.info(analysis)