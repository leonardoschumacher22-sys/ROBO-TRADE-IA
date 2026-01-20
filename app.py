import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="IA PRECISION - GOMERE SYNC", layout="wide")

# --- CSS PARA FOCO EM SINAIS ---
st.markdown("""
    <style>
    .main { background-color: #060d14; color: #e1e1e1; }
    .stButton>button { background: linear-gradient(90deg, #00c853, #b2ff59); color: black; font-weight: bold; border: none; }
    .card-sinal { background: #121921; border: 2px solid #00d2ff; padding: 20px; border-radius: 15px; text-align: center; }
    .taxa-box { font-size: 24px; color: #00d2ff; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA ---
if "win" not in st.session_state: st.session_state.win = 0
if "loss" not in st.session_state: st.session_state.loss = 0

# --- FUNÇÃO DE BUSCA DE ALTA VELOCIDADE ---
def get_live_data(ticker_name):
    mapa = {"EUR/USD": "EURUSD=X", "BTC/USD": "BTC-USD", "GBP/USD": "GBPUSD=X"}
    # Forçamos o download sem cache para tentar reduzir o delay
    data = yf.download(mapa[ticker_name], period="1d", interval="1m", progress=False)
    if data.empty: return None
    
    # INDICADORES DE PRECISÃO (Para bater com corretora)
    # RSI: Detecta se o preço "esticou" demais
    delta = data['Close'].diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=13, adjust=False).mean()
    ema_down = down.ewm(com=13, adjust=False).mean()
    rs = ema_up / ema_down
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Médias Rápidas
    data['EMA_5'] = data['Close'].ewm(span=5, adjust=False).mean()
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
    
    return data

# --- INTERFACE ---
st.title("🎯 IA Precision - Trader Room Sync")
par = st.selectbox("Paridade", ["EUR/USD", "GBP/USD", "BTC/USD"])

df = get_live_data(par)

if df is not None:
    # Captura de valores atuais
    c_price = float(df['Close'].iloc[-1].item())
    c_rsi = float(df['RSI'].iloc[-1].item())
    ema5 = float(df['EMA_5'].iloc[-1].item())
    ema20 = float(df['EMA_20'].iloc[-1].item())

    # --- LÓGICA DE ANÁLISE PARA PRÓXIMA VELA ---
    # Só dá sinal se houver confluência (Médias + RSI)
    decisao = "AGUARDAR"
    if ema5 > ema20 and c_rsi < 70: 
        decisao = "COMPRA 🟢"
    elif ema5 < ema20 and c_rsi > 30: 
        decisao = "VENDA 🔴"
    
    # Ajuste de filtro para evitar erros em lateralização
    if 45 < c_rsi < 55:
        decisao = "AGUARDAR (Mercado Lateral)"

    c1, c2 = st.columns([2, 1])

    with c1:
        # Gráfico de Velas
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Dashboard de Assertividade
        total = st.session_state.win + st.session_state.loss
        taxa = (st.session_state.win / total * 100) if total > 0 else 0
        st.markdown(f"<div class='taxa-box'>Assertividade Real: {taxa:.1f}%</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("### Sinal para Vela Seguinte")
        if st.button("GERAR ANÁLISE"):
            with st.spinner('Sincronizando...'):
                time.sleep(1)
                st.markdown(f"""
                <div class='card-sinal'>
                    <h1 style='color: white;'>{decisao}</h1>
                    <hr>
                    <p>Entrada na abertura da próxima vela</p>
                    <small>Preço Base: {c_price:.5f}</small>
                </div>
                """, unsafe_allow_html=True)
        
        # Botões de correção manual de aprendizado
        st.write("Resultado do último sinal:")
        cb1, cb2 = st.columns(2)
        if cb1.button("✅ WIN"): st.session_state.win += 1; st.rerun()
        if cb2.button("❌ LOSS"): st.session_state.loss += 1; st.rerun()

st.info("Nota: O mercado OTC das corretoras pode divergir do mercado real. Use esta ferramenta como confluência técnica.")
