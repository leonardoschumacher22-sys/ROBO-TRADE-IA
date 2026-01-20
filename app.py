import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS (CLONE DO VISUAL DAS IMAGENS) ---
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
    h3 { font-size: 18px !important; margin-bottom: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
# Coloque seu e-mail aqui para liberar o acesso
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
    st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"], label_visibility="collapsed")
with col_mode:
    st.markdown("<div class='header-info'>Análises diárias restantes: <b>Ilimitado</b></div>", unsafe_allow_html=True)
    if st.button("Sair do modo Pro"):
        st.session_state.logado = False
        st.rerun()

# --- CONTEÚDO PRINCIPAL ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Gráfico em tempo real")
    # Simulação de Gráfico de Tendência (image_cc7f97.png)
    chart_data = pd.DataFrame(np.random.randn(50, 2), columns=['SMA', 'EMA'])
    st.line_chart(chart_data, height=300)
    
    # Grid de Informações Inferiores (image_cc8a3d.png)
    col_info, col_medo, col_mvp = st.columns(3)
    
    with col_info:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<b>Informações do ativo</b>", unsafe_allow_html=True)
        st.write("---")
        st.write(f"Ativo: **EUR/USD (OTC)**")
        st.write(f"Cotação: **1.187075**")
        st.write(f"Fundo: **1.186285**")
        st.write(f"Topo: **1.190185**")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_medo:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<center><b>Índice de medo</b></center>", unsafe_allow_html=True)
        # Velocímetro usando Plotly
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = 53,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "yellow"},
                'steps': [
                    {'range': [0, 40], 'color': "red"},
                    {'range': [40, 60], 'color': "orange"},
                    {'range': [60, 100], 'color': "green"}]
            }
        ))
        fig.update_layout(height=180, margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mvp:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<b>Índice de MVP</b>", unsafe_allow_html=True)
        st.line_chart(np.random.randn(20, 1), height=150)
        st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("### Análise com I.A")
    # Força de Compra/Venda
    p_cima, p_baixo = st.columns(2)
    p_cima.markdown("<div style='background:#1b4332; padding:15px; text-align:center; border-radius:5px; color:#00ff00;'>68%<br>Para cima</div>", unsafe_allow_html=True)
    p_baixo.markdown("<div style='background:#432818; padding:15px; text-align:center; border-radius:5px; color:#ff4b4b;'>32%<br>Para baixo</div>", unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("ANALISAR ENTRADA"):
        with st.spinner('IA Verificando Fluxo...'):
            time.sleep(2)
            decisao = random.choice(["CALL", "PUT"])
            confianca = random.randint(89, 98)
            
            if decisao == "CALL":
                st.markdown(f"<div style='background:#00c853; padding:20px; text-align:center; border-radius:10px;'><h2>COMPRA 🟢</h2>Confiança: {confianca}%</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#d50000; padding:20px; text-align:center; border-radius:10px;'><h2>VENDA 🔴</h2>Confiança: {confianca}%</div>", unsafe_allow_html=True)

    st.markdown("<div class='card' style='margin-top:15px;'><b>Explicação da análise</b><br><small>O algoritmo identificou uma forte rejeição no suporte histórico com aumento de volume comprador.</small></div>", unsafe_allow_html=True)

# --- NOTÍCIAS (image_cc7fb9.png) ---
st.markdown("---")
st.markdown("### Notícias importantes do ativo")
n1, n2, n3 = st.columns(3)
n1.info("SEC autoriza Nasdaq a negociar primeiro ETF de Bitcoin.")
n2.warning("Fundador da Terra (LUNA) é procurado pela Interpol.")
n3.info("Volume de negociação em OTC sobe 15% esta semana.")
