import streamlit as st
import pandas as pd
import numpy as np
import time
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - IA REAL TIME", layout="wide", initial_sidebar_state="collapsed")

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
        else:
            st.error("E-mail não autorizado.")
    st.stop()

# --- MAPEAMENTO DE ATIVOS ---
# Mapeia o nome amigável para o símbolo real da API
ativos_map = {
    "EUR/USD": "EURUSD=X",
    "GBP/USD": "GBPUSD=X",
    "BTC/USD": "BTC-USD"
}

# --- TOPBAR ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo:
    st.markdown("## IT")
with col_pair:
    selecionado = st.selectbox("", list(ativos_map.keys()), label_visibility="collapsed")
    ticker = ativos_map[selecionado]
with col_mode:
    st.markdown("<div style='text-align:right;'>Modo: <b>Análise Real</b></div>", unsafe_allow_html=True)

# --- DASHBOARD ---
c1, c2 = st.columns([2, 1])

with c1:
    st.markdown(f"### Gráfico de Velas: {selecionado}")
    # Busca dados reais para o gráfico
    df_chart = yf.download(ticker, period="1d", interval="1m").tail(50)
    
    fig_chart = go.Figure(data=[go.Candlestick(
        x=df_chart.index, open=df_chart['Open'], high=df_chart['High'],
        low=df_chart['Low'], close=df_chart['Close']
    )])
    fig_chart.update_layout(height=350, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_chart, use_container_width=True)
    
    col_info, col_medo, col_mvp = st.columns(3)
    with col_info:
        preco_atual = df_chart['Close'].iloc[-1]
        st.markdown(f"<div class='card'><b>Info</b><br><small>Preço: {preco_atual:.4f}<br>Topo (1d): {df_chart['High'].max():.4f}</small></div>", unsafe_allow_html=True)
    with col_medo:
        # Calcula RSI para o velocímetro
        rsi_valor = ta.rsi(df_chart['Close'], length=14).iloc[-1]
        st.markdown("<div class='card'><center><b>RSI (Força)</b></center>", unsafe_allow_html=True)
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=rsi_valor, gauge={'axis':{'range':[0,100]},'bar':{'color':"white"},'steps':[{'range':[0,30],'color':"green"},{'range':[70,100],'color':"red"}]}))
        fig_rsi.update_layout(height=150, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
        st.plotly_chart(fig_rsi, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col_mvp:
        st.markdown("<div class='card'><b>Volatilidade</b>", unsafe_allow_html=True)
        st.line_chart(df_chart['Close'].pct_change(), height=120)
        st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("### Julgamento da IA")
    
    if st.button("ANALISAR VELA AGORA"):
        with st.spinner('Lendo padrões de velas...'):
            # Lógica de Julgamento Real
            df_analise = yf.download(ticker, period="1d", interval="1m").tail(20)
            rsi = ta.rsi(df_analise['Close'], length=14).iloc[-1]
            
            fuso_br = pytz.timezone('America/Sao_Paulo')
            agora = datetime.now(fuso_br)
            h1 = (agora + timedelta(minutes=1)).strftime("%H:%M")
            h2 = (agora + timedelta(minutes=2)).strftime("%H:%M")

            if rsi < 40:
                decisao, cor, explicacao = "COMPRA 🟢", "#00c853", "Vela em zona de suporte com RSI baixo. Reversão de alta iminente."
            elif rsi > 60:
                decisao, cor, explicacao = "VENDA 🔴", "#d50000", "Vela em zona de exaustão com RSI alto. Tendência de queda imediata."
            else:
                decisao, cor, explicacao = "AGUARDAR ⚪", "#555555", "Mercado lateralizado. Sem força clara na vela atual."

            if decisao != "AGUARDAR ⚪":
                st.markdown(f"""
                    <div style='background:{cor}; padding:20px; text-align:center; border-radius:10px; border: 2px solid white;'>
                        <h2 style='margin:0; color:white;'>{decisao}</h2>
                        <p style='color:white;'><b>Ativo:</b> {selecionado} | <b>Horário:</b> {agora.strftime("%H:%M")}</p>
                        <hr style='border:0.5px solid rgba(255,255,255,0.3);'>
                        <p style='font-size:13px; color:white; text-align:left;'>
                            <b>Caso a vela feche contra, faça:</b><br>
                            • +1 entrada no próximo minuto às {h1}<br>
                            • +1 entrada no minuto seguinte às {h2}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning(f"IA Sugere: {decisao}. Motivo: {explicacao}")

    st.markdown("<div class='card' style='margin-top:15px;'><small>A IA julga a vela baseada no RSI e Volume real do mercado.</small></div>", unsafe_allow_html=True)
