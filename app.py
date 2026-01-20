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

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #1a1c22; color: #ffffff; }
    .stButton>button {
        width: 100%; background-color: #00c853; color: white;
        font-weight: bold; border-radius: 5px; height: 3.5em; border: none;
    }
    .card {
        background-color: #23272f; padding: 20px; border-radius: 10px;
        border: 1px solid #30363d; margin-bottom: 15px;
    }
    .metric-box {
        padding: 10px; text-align: center; border-radius: 5px; font-weight: bold; font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO (Garante o 0% no início) ---
if "p_cima" not in st.session_state:
    st.session_state.update({
        "p_cima": 0,
        "p_baixo": 0,
        "sinal_html": "",
        "explicacao": "Aguardando solicitação de análise..."
    })

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
    st.stop()

# --- CABEÇALHO ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo: st.markdown("## IT")
with col_pair:
    ativo = st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"], label_visibility="collapsed")
with col_mode:
    st.markdown("<div style='text-align:right; color:#8b949e;'>Análises: <b>Ilimitado</b></div>", unsafe_allow_html=True)

# --- CONTEÚDO PRINCIPAL (Fragmento para evitar lag) ---
@st.fragment(run_every=2)
def live_dashboard():
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### Monitoramento de Fluxo")
        # Gráfico simples para evitar KeyError
        chart_df = pd.DataFrame(np.random.randn(30, 1), columns=["Preço"])
        st.line_chart(chart_df, height=250)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.markdown(f"<div class='card'><b>{ativo}</b><br><small>Cotação: {1.1870 + random.uniform(-0.001, 0.001):.5f}</small></div>", unsafe_allow_html=True)
        with m2:
            val = random.randint(45, 55)
            fig = go.Figure(go.Indicator(mode="gauge+number", value=val, gauge={'axis':{'range':[0,100]},'bar':{'color':"yellow"}}))
            fig.update_layout(height=140, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig, use_container_width=True)
        with m3:
            st.markdown("<div class='card'><b>MVP</b><br><small>Volume Estável</small></div>", unsafe_allow_html=True)

    with c2:
        st.markdown("### Análise com I.A")
        
        # Exibição das porcentagens
        pc_col, pb_col = st.columns(2)
        pc_col.markdown(f"<div class='metric-box' style='background:#1b4332; color:#00ff00;'>{st.session_state.p_cima}%<br><span style='font-size:12px;'>Cima</span></div>", unsafe_allow_html=True)
        pb_col.markdown(f"<div class='metric-box' style='background:#432818; color:#ff4b4b;'>{st.session_state.p_baixo}%
