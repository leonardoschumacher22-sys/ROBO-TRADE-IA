import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="IA TRADE PRO - SINAIS VIP",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILIZAÇÃO CSS (VISUAL MODO PRO) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #30363d; }
    .stButton>button {
        width: 100%;
        background-color: #00c853;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3.5em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { background-color: #00e676; border: none; color: white; }
    .card {
        background-color: #1c2128;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    .metric-label { color: #8b949e; font-size: 14px; }
    .metric-value { color: #ffffff; font-size: 18px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN (TRAVA DE SEGURANÇA) ---
# DICA: Para testar agora, use o e-mail abaixo. 
# Quando quiser liberar para clientes, adicione os e-mails deles nesta lista.
ASSINANTES_VIPS = [
    "leonardo.schumacher22@gmail.com",
    "teste@admin.com"
]

def verificar_acesso(email_digitado):
    return email_digitado.strip().lower() in ASSINANTES_VIPS

# Interface de Login na Lateral
st.sidebar.markdown("# 🔐 ÁREA VIP")
user_email = st.sidebar.text_input("E-mail do Assinante:")

if verificar_acesso(user_email):
    st.sidebar.success("Acesso Liberado!")
    if st.sidebar.button("Sair"):
        st.rerun()

    # --- DASHBOARD DE SINAIS (CONTEÚDO PROTEGIDO) ---
    
    # Cabeçalho
    col_header_1, col_header_2 = st.columns([4, 2])
    with col_header_1:
        st.markdown("# 🤖 Algoritmo IA Trade")
        st.write("Análise em tempo real dos pares de moedas mais voláteis.")
    with col_header_2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)"], label_visibility="collapsed")

    # Layout Principal
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("### 📊 Gráfico de Tendência IA")
        # Simulação de Gráfico de Indicadores
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['Força Compradora', 'Força Vendedora', 'Tendência IA']
        )
        st.line_chart(chart_data, height=300)

        # Informações do Ativo (Igual à imagem enviada)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("📋 **Informações do Ativo**")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<p class='metric-label'>Cotação atual</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>1.187905</p>", unsafe_allow_html=True)
        with c2:
            st.markdown("<p class='metric-label'>Topo</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>1.190185</p>", unsafe_allow_html=True)
        with c3:
            st.markdown("<p class='metric-label'>Fundo</p>", unsafe_allow_html=True)
            st.markdown("<p class='metric-value'>1.186285</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_side:
        st.markdown("### ⚡ Análise IA")
        
        # Por
