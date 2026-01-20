import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz # Necessário para o horário de Brasília

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS (CLONE PREMIUM) ---
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

# --- SISTEMA DE ACESSO ---
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

# --- CABEÇALHO ---
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

# --- CONTEÚDO ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown("### Gráfico em tempo real")
    chart_data = pd.DataFrame(np.random.randn(50, 2), columns=['SMA', 'EMA'])
    st.line_chart(chart_data, height=300)
    
    col_info, col_medo, col_mvp = st.columns(3)
    with col_info:
        st.markdown("<div class='card'><b>Informações do ativo</b><br><small>Ativo: "+ativo_selecionado+"<br>Cotação: 1.187075<br>Fundo: 1.186285<br>Topo: 1.190185</small></div>", unsafe_allow_html=True)
        
    with col_medo:
        st.markdown("<div class='card'><center><b>Índice de medo</b></center>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(mode="gauge+number", value=53, gauge={'axis':{'range':[0,100]}, 'bar':{'color':"yellow"}, 'steps':[{'range':[0,40],'color':"red"},{'range':[40,60],'color':"orange"},{'range':[60,100],'color':"green"}]}))
        fig.update_layout(height=150, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mvp:
        st.markdown("<div class='card'><b>Índice de MVP</b>", unsafe_allow_html=True)
        st.line_chart(np.random.randn(20, 1), height=120)
        st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("### Análise com I.A")
    p_cima, p_baixo = st.columns(2)
    p_cima.markdown("<div style='background:#1b4332; padding:10px; text-align:center; border-radius:5px; color:#00ff00;'>68%<br>Cima</div>", unsafe_allow_html=True)
    p_baixo.markdown("<div style='background:#432818; padding:10px; text-align:center; border-radius:5px; color:#ff4b4b;'>32%<br>Baixo</div>", unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("ANALISAR ENTRADA"):
        with st.spinner('Analisando...'):
            time.sleep(2)
            decisao = random.choice(["COMPRA 🟢", "VENDA 🔴"])
            cor_bg = "#00c853" if "COMPRA" in decisao else "#d50000"
            confianca = random.randint(91, 98)
            
            # CONFIGURAÇÃO DO HORÁRIO DE BRASÍLIA
            fuso_br = pytz.timezone('America/Sao_Paulo')
            agora = datetime.now(fuso_br)
            h_entrada = agora.strftime("%H:%M")
            h_gale1 = (agora + timedelta(minutes=1)).strftime("%H:%M")
            h_gale2 = (agora + timedelta(minutes=2)).strftime("%H:%M")
            
            # SINAL COM LINGUAGEM PARA LEIGOS
            st.markdown(f"""
                <div style='background:{cor_bg}; padding:20px; text-align:center; border-radius:10px; border: 2px solid white;'>
                    <h2 style='margin:0; color:white;'>{decisao}</h2>
                    <p style='margin:5px 0; font-weight:bold; color:white;'>ATIVO: {ativo_selecionado}</p>
                    <p style='margin:0; color:white;'>Confiança: {confianca}% | Início: {h_entrada}</p>
                    <hr style='margin:10px 0; border:0.5px solid rgba(255,255,255,0.3);'>
                    <p style='margin:0; font-size:13px; color:white; text-align:left;'>
                        <b>Caso não ganhe de primeira:</b><br>
                        • +1 entrada no próximo minuto ({h_gale1})<br>
                        • +1 entrada no minuto seguinte ({h_gale2})
                    </p
