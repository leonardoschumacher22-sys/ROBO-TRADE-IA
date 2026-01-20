import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - LIVE MARKET PRO", layout="wide", initial_sidebar_state="collapsed")

# Memória de Sessão para os ganhos e métricas
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 150px; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; margin-bottom: 8px;}
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; border: none; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE BUSCA DE DADOS REAIS ---
def get_live_data(ticker):
    try:
        # Puxa os dados reais (intervalo de 1 minuto)
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty: return None
        
        # Cálculos Técnicos Reais
        df = data.copy()
        df['SMA'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['SMA'] + (df['STD'] * 2)
        df['Lower'] = df['SMA'] - (df['STD'] * 2)
        return df
    except:
        return None

# --- HEADER E SELEÇÃO ---
c1, c2, c3 = st.columns([1, 2, 2])
with c1: st.markdown("## IT")
with c2: cat = st.selectbox("Categoria", ["FOREX", "CRIPTOMOEDAS", "AÇÕES"], label_visibility="collapsed")
with c3:
    ativos_dict = {
        "FOREX": "EURUSD=X",
        "CRIPTOMOEDAS": "BTC-USD",
        "AÇÕES": "AAPL"
    }
    ticker = ativos_dict[cat]
    st.markdown(f"**Ativo Selecionado:** {ticker}")

# --- EXECUÇÃO ---
df = get_live_data(ticker)

if df is not None:
    # Dados para os Cards
    preco_atual = float(df['Close'].iloc[-1])
    b_up = float(df['Upper'].iloc[-1])
    b_low = float(df['Lower'].iloc[-1])
    # Índice de Medo Simulado com base na volatilidade real
    volatilidade = (df['High'].iloc[-1] - df['Low'].iloc[-1]) / preco_atual * 10000
    medo_idx = int(clamp(50 + volatilidade, 0, 100))

    col_graf, col_ana = st.columns([2, 1])

    with col_graf:
        st.markdown(f"### Gráfico Real em Tempo Aberto")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']
        )])
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        m1, m2 = st.columns(2)
        with m1: st.markdown(f"<div class='card'><b>Métricas Bolsa</b><br><br>Preço: {preco_atual:.5f}<br>Máxima: {df['High'].max():.5f}</div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='card'><b>Índice de Medo</b><br><br><center><h2 style='color:#facc15;'>{medo_idx}</h2>Ganância</center></div>", unsafe_allow_html=True)

    with col_ana:
        total = st.session_state.wins + st.session_state.losses
        taxa = (st.session_state.wins / total * 100) if total > 0 else 0
        st.write(f"**Assertividade:** {taxa:.1f}%")
        st.markdown(f"<div style='background:#333; height:12px; border-radius:5px;'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de Sinal Analítica
        sinal = "AGUARDAR"
        cor = "#333"
        if preco_atual >= b_up: sinal = "VENDA 🔴"; cor = "#f87171"
        elif preco_atual <= b_low: sinal = "COMPRA 🟢"; cor = "#4ade80"
        else: sinal = "AGUARDAR ⚠️"; cor = "#30363d"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Lendo dados da Bolsa...'):
                time.sleep(1)
                st.markdown(f"<div style='background:{cor}; padding:20px; border-radius:10px; text-align:center;'><h2>{sinal}</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        b_w, b_l = st.columns(2)
        if b_w.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if b_l.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

else:
    st.error("Servidor da Bolsa ocupado. Tentando reconectar...")
    time.sleep(2)
    st.rerun()

def clamp(n, minn, maxn): return max(min(maxn, n), minn)
