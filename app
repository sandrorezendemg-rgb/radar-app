import streamlit as st
import pandas as pd
from radar_engine import run_radar
from ai_agent import run_agent

st.title("🚀 Radar Confluência PRO")

if st.button("Rodar Radar"):

    df = run_radar([], "", "")

    st.dataframe(df)

    analysis = run_agent(df.head(2).to_dict(orient="records"))

    st.text(analysis)