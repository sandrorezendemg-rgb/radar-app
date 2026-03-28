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

    try:
        df = run_radar(narratives, risk, mode)

        # =========================
        # VALIDAÇÃO INICIAL
        # =========================
        if df is None or df.empty:
            st.warning("Nenhuma oportunidade encontrada.")
            st.stop()

        # Verifica colunas essenciais
        required_cols = ["Ativo", "Score", "Sinal"]
        for col in required_cols:
            if col not in df.columns:
                st.error(f"Erro: coluna obrigatória '{col}' não encontrada.")
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
🎯 **Ativo:** {top.get('Ativo','-')}  
📈 **Sinal:** {top.get('Sinal','-')}  
📊 **Score:** {top.get('Score','-')}  

💰 **Entrada:** {top.get('Entrada','-')}  
🛑 **Stop:** {top.get('SL','-')}  
🎯 **Alvo:** {top.get('TP2','-')}
""")

        st.divider()

        # =========================
        # RANKING VISUAL
        # =========================
        st.subheader("🏆 Ranking de Oportunidades")

        for i in range(len(df)):
            row = df.iloc[i]

            sinal = row.get("Sinal", "")
            color = "#00C853" if sinal == "COMPRA" else "#D50000"

            score = row.get("Score", 0)
            qualidade = "🔥 ALTA" if score >= 6 else "⚠️ MÉDIA"

            st.markdown(f"""
<div style="
padding:15px;
margin-bottom:12px;
border-radius:10px;
background-color:#111;
border-left:5px solid {color};
">

<h3>{row.get('Ativo','-')} | {sinal}</h3>

<b>Score:</b> {score}  
<b>Qualidade:</b> {qualidade}  

<br>

<b>Entrada:</b> {row.get('Entrada','-')}  
<b>SL:</b> {row.get('SL','-')}  
<b>TP:</b> {row.get('TP2','-')}  

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

        try:
            analysis = run_agent(df.head(3).to_dict(orient="records"))
            st.info(analysis)
        except Exception as e:
            st.warning(f"Erro na análise IA: {e}")

    except Exception as e:
        st.error(f"Erro geral na execução: {e}")
        st.stop()