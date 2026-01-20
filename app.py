import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS (CLONE DAS IMAGENS) ---
st.markdown("""
    <style>
    .main { background-color: #1a1c22; color: #ffffff; }
    .stButton>button {
        width: 100%;
        background-color: #00c853;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        height: 3.5em;
        border: none;
    }
    .card {
        background-color: #23272f;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    .header-info { text-align: right; color: #8b949e; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔐 Login do Assinante")
    email = st.text_input("Digite seu e-mail:")
    if st.button("ACESSAR SISTEMA"):
        if email.strip().lower() == "leonardo.schumacher22@gmail.com":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("E-mail não autorizado.")
    st.stop()

# --- CABEÇALHO (image_cc8a1d.png) ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo:
    st.markdown("## IT")
with col_pair:
    ativo_selecionado = st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"], label_visibility="collapsed")
with col_mode:
    st.markdown("<div class='header-info'>Análises diárias restantes: <b>Ilimitado</b></div>", unsafe_allow_html=True)
    if st.button("Sair do modo Pro"):
        st.session_state.logado = False
        st.rerun()

# --- CONTEÚDO PRINCIPAL ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Gráfico em tempo real")
    # Gráfico de linha conforme image_cc7f97.png
    chart_data = pd.DataFrame(np.random.randn(50, 2), columns=['SMA', 'EMA'])
    st.line_chart(chart_data, height=300)
    
    # Grid de Informações (image_cc8a3d.png)
    col_info, col_medo, col_mvp = st.columns(3)
    
    with col_info:
        st.markdown(f"""
            <div class='card'>
                <b>Informações do ativo</b><br>
                <small>
                Ativo: {ativo_selecionado}<br>
                Cotação: 1.187075<br>
                Fundo: 1.186285<br>
                Topo: 1.190185
                </small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_medo:
        st.markdown("<div class='card'><center><b>Índice de medo</b></center>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 53,
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "yellow"},
                'steps': [
                    {'range': [0, 40], 'color': "red
