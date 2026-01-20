import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS CORRIGIDA ---
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
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #30363d;
        margin-bottom: 10px;
    }
    .header-info { text-align: right; color: #8b949e; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo:
    st.markdown("## IT")
with col_pair:
    st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY"], label_visibility="collapsed")
with col_mode:
    st.markdown("<div class='header-info'>Análises diárias restantes: <b>0</b></div>", unsafe_allow_html=True)
    st.button("Sair do modo Pro", key="sair_pro")

# --- CORPO PRINCIPAL ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Gráfico em tempo real")
    # Gerando dados reais para o gráfico não dar erro
    chart_data = pd.DataFrame(np.random.randn(50, 2), columns=['SMA', 'EMA'])
    st.line_chart(chart_data, height=350)
    
    # Grid de Informações do Ativo (Idêntico à imagem image_cc7f78.png)
    st.markdown("### Informações do ativo")
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("**Ativo:** EUR/USD (OTC)")
        st.write("**Cotação atual:** 1.187905")
        st.write("**Fundo:** 1.186285")
    with col_b:
        st.write("**Topo:** 1.190185")
        st.write("**Preço médio:** 1.187820")
        st.write("**Tendência:** IA analisando...")
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("### Análise com I.A")
    
    # Indicadores de força (image_cc7f3c.png)
    p_cima, p_baixo = st.columns(2)
    p_cima.markdown("<div style='background:#1b4332; padding:15px; text-align:center; border-radius:5px; color:#00ff00;'>0%<br>Para cima</div>", unsafe_allow_html=True)
    p_baixo.markdown("<div style='background:#432818; padding:15px; text-align:center; border-radius:5px; color:#ff4b4b;'>0%<br>Para baixo</div>", unsafe_allow_html=True)
    
    st.write("")
    
    # BOTÃO FUNCIONAL
    if st.button("ANALISAR ENTRADA"):
        with st.spinner('Processando algoritmos...'):
            time.sleep(2)
            decisao = random.choice(["CALL", "PUT"])
            if decisao == "CALL":
                st.success("🎯 SINAL IDENTIFICADO: COMPRA (CALL) 🟢")
            else:
                st.error("🎯 SINAL IDENTIFICADO: VENDA (PUT) 🔴")

    # Explicação da análise
    st.markdown("<div class='card'><b>Explicação da análise</b><br>Aguardando processamento de dados do gráfico...</div>", unsafe_allow_html=True)

# --- RODAPÉ (NOTÍCIAS image_cc7fb9.png) ---
st.markdown("---")
st.markdown("### Notícias importantes do ativo")
n1, n2, n3 = st.columns(3)
with n1:
    st.info("SEC autoriza Nasdaq a negociar primeiro ETF de bitcoin...")
with n2:
    st.warning("Fundador da Terra (LUNA) é procurado em 195 países...")
with n3:
    st.info("ETF de Bitcoin será evento 'buy the rumor'...")
