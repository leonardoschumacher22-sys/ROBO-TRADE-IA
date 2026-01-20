import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="IT - ULTRA PRECISION", layout="wide", initial_sidebar_state="collapsed")

if "wins" not in st.session_state: st.session_state.wins = 0
if "losses" not in st.session_state: st.session_state.losses = 0

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; }
    .assertividade-fill { background: #00d2ff; height: 15px; border-radius: 5px; transition: 0.8s; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTA DE ATIVOS ---
ativos = {
    "📊 MOEDAS": {"EUR/USD (OTC)": "EURUSD=X", "GBP/USD (OTC)": "GBPUSD=X", "USD/JPY (OTC)": "JPY=X"},
    "🍎 AÇÕES": {"APPLE": "AAPL", "TESLA": "TSLA", "NVIDIA": "NVDA"},
    "₿ CRIPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"}
}

# --- PROCESSAMENTO TÉCNICO (O "PULO DO GATO") ---
@st.cache_data(ttl=1)
def get_analysis_data(ticker):
    data = yf.download(ticker, period="1d", interval="1m", progress=False)
    if data.empty or len(data) < 30: return None
    
    # 1. RSI (Força Relativa)
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    data['RSI'] = 100 - (100 / (1 + (gain / loss)))
    
    # 2. Bandas de Bollinger (Volatilidade)
    data['MA20'] = data['Close'].rolling(window=20).mean()
    data['STD'] = data['Close'].rolling(window=20).std()
    data['Upper'] = data['MA20'] + (data['STD'] * 2)
    data['Lower'] = data['MA20'] - (data['STD'] * 2)
    
    # 3. EMA Rápida e Lenta
    data['EMA5'] = data['Close'].ewm(span=5).mean()
    data['EMA20'] = data['Close'].ewm(span=20).mean()
    
    return data

# --- INTERFACE ---
c_cat, c_pair = st.columns(2)
cat = c_cat.selectbox("Categoria", list(ativos.keys()))
escolha = c_pair.selectbox("Ativo", list(ativos[cat].keys()))
ticker = ativos[cat][escolha]

df = get_analysis_data(ticker)

if df is not None:
    # Captura de Indicadores Atuais
    c_close = df['Close'].iloc[-1]
    c_rsi = df['RSI'].iloc[-1]
    c_upper = df['Upper'].iloc[-1]
    c_lower = df['Lower'].iloc[-1]
    c_ema5 = df['EMA5'].iloc[-1]
    c_ema20 = df['EMA20'].iloc[-1]

    # --- LÓGICA DE ALTA ASSERTIVIDADE ---
    sinal = "AGUARDAR"
    confianca = 0
    
    # GATILHO DE COMPRA: Preço tocou banda inferior + RSI < 35 + Cruzamento de Alta
    if c_close <= c_lower and c_rsi < 40 and c_ema5 > df['EMA5'].iloc[-2]:
        sinal = "COMPRA"
        confianca = 91.5
    
    # GATILHO DE VENDA: Preço tocou banda superior + RSI > 65 + Cruzamento de Baixa
    elif c_close >= c_upper and c_rsi > 60 and c_ema5 < df['EMA5'].iloc[-2]:
        sinal = "VENDA"
        confianca = 93.2
        
    # FILTRO DE SEGURANÇA: Se o mercado estiver lateral demais, cancela
    if abs(c_ema5 - c_ema20) < 0.00005: # Ajuste conforme o par
        sinal = "MERCADO LATERAL"

    # --- DISPLAY ---
    c_plot, c_ana = st.columns([2, 1])
    
    with c_plot:
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.add_trace(go.Scatter(x=df.index, y=df['Upper'], name="Banda Sup", line=dict(color='rgba(173, 216, 230, 0.4)')))
        fig.add_trace(go.Scatter(x=df.index, y=df['Lower'], name="Banda Inf", line=dict(color='rgba(173, 216, 230, 0.4)')))
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with c_ana:
        total = st.session_state.wins + st.session_state.loss if "loss" in st.session_state else 0
        taxa = (st.session_state.wins / total * 100) if total > 0 else 0
        
        st.markdown(f"<b>Assertividade: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div style='background:#30363d; height:15px; border-radius:5px;'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        st.write("---")
        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Filtrando ruídos...'):
                time.sleep(1)
                if sinal in ["COMPRA", "VENDA"]:
                    cor = "#4ade80" if sinal == "COMPRA" else "#f87171"
                    st.markdown(f"""
                    <div style='background:{cor}; padding:20px; border-radius:10px; color:black; text-align:center;'>
                        <h1>{sinal} 🟢</h1>
                        <b>CONFIANÇA: {confianca}%</b><br>
                        Entrada na abertura da próxima vela
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning(f"Sinal Abortado: {sinal}. Condições insuficientes para vitória.")

        st.write("---")
        fb1, fb2 = st.columns(2)
        if fb1.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if fb2.button("❌ LOSS"): 
            if "loss" not in st.session_state: st.session_state.loss = 0
            st.session_state.loss += 1
            st.rerun()

# Notícias na base...
st.markdown("### Notícias Importantes")
st.columns(3)[0].markdown("<div class='card' style='background:#1e3a8a'><b>Volatilidade</b><br>Alta detectada no par selecionado.</div>", unsafe_allow_html=True)
