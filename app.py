import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if "wins" not in st.session_state: st.session_state.wins = 0
if "losses" not in st.session_state: st.session_state.losses = 0

# --- CSS PARA DISPLAY IGUAL À IMAGEM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; margin-bottom: 5px; }
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; margin-bottom: 5px; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.2em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 12px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- ATIVOS ---
ativos_dict = {
    "FOREX/OTC": {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X"},
    "CRYPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"},
    "STOCKS": {"APPLE": "AAPL", "TESLA": "TSLA"}
}

# --- FUNÇÃO DE DADOS SEM TRAVAMENTO ---
def get_safe_data(ticker):
    try:
        # Busca dados recentes (1 dia, intervalo 1m)
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 25:
            return None
        
        # Cálculos de Indicadores
        df['MA10'] = df['Close'].ewm(span=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['MA20'] + (df['STD'] * 2)
        df['Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        return df
    except:
        return None

# --- UI SUPERIOR ---
c1, c2, c3 = st.columns([1, 2, 2])
with c1: st.markdown("## IT")
with c2: cat = st.selectbox("Cat", list(ativos_dict.keys()), label_visibility="collapsed")
with c3: 
    at_nome = st.selectbox("Ativo", list(ativos_dict[cat].keys()), label_visibility="collapsed")
    ticker_id = ativos_dict[cat][at_nome]

# Carregamento
df_live = get_safe_data(ticker_id)

if df_live is not None:
    # Captura segura de valores
    val_atual = float(df_live['Close'].iloc[-1])
    rsi_now = float(df_live['RSI'].iloc[-1])
    b_up = float(df_live['Upper'].iloc[-1])
    b_low = float(df_live['Lower'].iloc[-1])
    
    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    # Layout
    col_g, col_a = st.columns([2, 1])

    with col_g:
        st.markdown(f"### {at_nome} (M1)")
        fig = go.Figure(data=[go.Candlestick(x=df_live.index, open=df_live['Open'], high=df_live['High'], low=df_live['Low'], close=df_live['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        inf1, inf2 = st.columns(2)
        with inf1: st.markdown(f"<div class='card'><b>Informações</b><br>Preço: {val_atual:.5f}<br>RSI: {rsi_now:.2f}</div>", unsafe_allow_html=True)
        with inf2: st.markdown(f"<div class='card'><b>Status</b><br><center><h3 style='color:#4ade80;'>ATIVO</h3></center></div>", unsafe_allow_html=True)

    with col_a:
        st.markdown(f"<b>Assertividade: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de sinal para a próxima vela
        sinal_final = "AGUARDAR"
        cor_fundo = "#30363d"
        
        if val_atual <= b_low or rsi_now < 30:
            sinal_final = "COMPRA"; cor_fundo = "#4ade80"
        elif val_atual >= b_up or rsi_now > 70:
            sinal_final = "VENDA"; cor_fundo = "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Lendo mercado...'):
                time.sleep(0.8)
                st.markdown(f"""
                <div style='background:{cor_fundo}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{sinal_final}</h2>
                    <b>PRÓXIMA VELA (M1)</b>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        b1, b2 = st.columns(2)
        if b1.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if b2.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # NOTÍCIAS
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>Nasdaq 100</b><br>Volume recorde em contratos futuros.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Zona do Euro</b><br>Inflação impacta pares de moedas.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Bitcoin (BTC)</b><br>Suporte institucional em 64k.</div>", unsafe_allow_html=True)

else:
    st.error("Conexão interrompida. O Yahoo Finance está demorando para responder.")
    if st.button("Tentar Reconectar Agora"): st.rerun()
