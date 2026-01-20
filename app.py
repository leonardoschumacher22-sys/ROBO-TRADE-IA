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

# --- ESTILIZAÇÃO CSS (VISUAL PREMIUM) ---
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

# --- INICIALIZAÇÃO DO ESTADO ---
if "p_cima" not in st.session_state:
    st.session_state.p_cima = 0
    st.session_state.p_baixo = 0
    st.session_state.sinal_card = ""
    st.session_state.explicacao = "Aguardando análise para a próxima vela..."

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
            st.error("E-mail não encontrado.")
    st.stop()

# --- CABEÇALHO ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo:
    st.markdown("## IT")
with col_pair:
    ativo_selecionado = st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"], label_visibility="collapsed")
with col_mode:
    st.markdown("<div class='header-info'>Análises diárias restantes: <b>Ilimitado</b></div>", unsafe_allow_html=True)

# --- CONTEÚDO DINÂMICO ---
@st.fragment(run_every=2)
def render_dashboard():
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### Monitoramento de Fluxo")
        # Gráfico fixo para evitar o KeyError 'BBU_20_2.0'
        chart_data = pd.DataFrame(np.random.randn(50, 1), columns=['Fluxo'])
        st.line_chart(chart_data, height=300)
        
        col_info, col_medo, col_mvp = st.columns(3)
        with col_info:
            preco_random = 1.187000 + random.uniform(-0.0005, 0.0005)
            st.markdown(f"""
                <div class='card'>
                    <b>Informações do ativo</b><br>
                    <small>Ativo: {ativo_selecionado}<br>Cotação: {preco_random:.6f}</small>
                </div>
            """, unsafe_allow_html=True)
            
        with col_medo:
            st.markdown("<div class='card'><center><b>Índice de medo</b></center>", unsafe_allow_html=True)
            v_medo = random.randint(45, 55)
            fig = go.Figure(go.Indicator(mode="gauge+number", value=v_medo, gauge={'axis':{'range':[0,100]}, 'bar':{'color':"yellow"}}))
            fig.update_layout(height=140, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_mvp:
            st.markdown("<div class='card
