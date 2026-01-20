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
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DE ESTADO (Para travar a análise) ---
if "analise_realizada" not in st.session_state:
    st.session_state.p_cima = 0
    st.session_state.p_baixo = 0
    st.session_state.sinal_html = ""
    st.session_state.texto_analise = "A explicação da análise aparecerá aqui após solicitar."

# --- LOGIN ---
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
    ativo_selecionado = st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"], label_visibility="collapsed")
with col_mode:
    st.markdown("<div style='text-align:right; color:#8b949e;'>Análises: <b>Ilimitado</b></div>", unsafe_allow_html=True)

# --- FRAGMENTO PARA DADOS EM TEMPO REAL (Gráficos e Índices) ---
@st.fragment(run_every=2)
def live_market_data():
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### Gráfico em tempo real")
        st.line_chart(pd.DataFrame(np.random.randn(50, 2), columns=['SMA', 'EMA']), height=300)
        
        m1, m2, m3 = st.columns(3)
        with m1:
            preco = 1.187000 + random.uniform(-0.0002, 0.0002)
            st.markdown(f"<div class='card'><b>Ativo</b><br><small>{ativo_selecionado}<br>Preço: {preco:.6f}</small></div>", unsafe_allow_html=True)
        with m2:
            val = random.randint(45, 55)
            fig = go.Figure(go.Indicator(mode="gauge+number", value=val, gauge={'axis':{'range':[0,100]},'bar':{'color':"yellow"}}))
            fig.update_layout(height=140, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig, use_container_width=True)
        with m3:
            st.markdown("<div class='card'><b>MVP</b>", unsafe_allow_html=True)
            st.line_chart(np.random.randn(15, 1), height=80)
            st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("### Análise com I.A")
        # EXIBE OS VALORES TRAVADOS DO SESSION_STATE
        pc, pb = st.columns(2)
        pc.markdown(f"<div style='background:#1b4332; padding:10px; text-align:center; border-radius:5px; color:#00ff00;'>{st.session_state.p_cima}%<br>Cima</div>", unsafe_allow_html=True)
        pb.markdown(f"<div style='background:#432818; padding:10px; text-align:center; border-radius:5px; color:#ff4b4b;'>{st.session_state.p_baixo}%<br>Baixo</div>", unsafe_allow_html=True)
        
        if st.button("ANALISAR ENTRADA"):
            with st.spinner('Analisando próxima vela...'):
                time.sleep(2)
                # ATUALIZA OS DADOS APENAS AQUI
                st.session_state.p_cima = random.randint(30, 70)
                st.session_state.p_baixo = 100 - st.session_state.p_cima
