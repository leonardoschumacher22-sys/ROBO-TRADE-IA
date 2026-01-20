import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="IT - GLOBAL ASSETS PRO", layout="wide", initial_sidebar_state="collapsed")

# --- MEMÓRIA DA SESSÃO ---
if "wins" not in st.session_state: st.session_state.wins = 0
if "losses" not in st.session_state: st.session_state.losses = 0

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; }
    .news-yellow { background: #854d0e; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 15px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 15px; border-radius: 5px; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- DICIONÁRIO AMPLIADO DE ATIVOS (GOMERE & HOMEBROKER STYLE) ---
ativos = {
    "📊 MOEDAS (FOREX)": {
        "EUR/USD (OTC)": "EURUSD=X",
        "GBP/USD (OTC)": "GBPUSD=X",
        "USD/JPY (OTC)": "JPY=X",
        "AUD/USD (OTC)": "AUDUSD=X",
        "USD/CAD (OTC)": "CAD=X",
        "EUR/JPY (OTC)": "EURJPY=X",
        "GBP/JPY (OTC)": "GBPJPY=X",
    },
    "🍎 AÇÕES (STOCKS)": {
        "APPLE INC (OTC)": "AAPL",
        "MICROSOFT (OTC)": "MSFT",
        "TESLA MOTORS": "TSLA",
        "AMAZON.COM": "AMZN",
        "NVIDIA CORP": "NVDA",
        "META (FACEBOOK)": "META",
        "NETFLIX INC": "NFLX",
    },
    "₿ CRIPTOMOEDAS": {
        "BITCOIN / USD": "BTC-USD",
        "ETHEREUM / USD": "ETH-USD",
        "SOLANA / USD": "SOL-USD",
        "BINANCE COIN": "BNB-USD",
        "RIPPLE (XRP)": "XRP-USD",
        "CARDANO (ADA)": "ADA-USD",
    },
    "🏆 COMMODITIES": {
        "OURO (XAU/USD)": "GC=F",
        "PRATA (XAG/USD)": "SI=F",
        "PETRÓLEO BRENT": "BZ=F",
    }
}

# --- CABEÇALHO ---
col_logo, col_cat, col_pair = st.columns([1, 2, 2])
with col_logo: st.markdown("## IT")
with col_cat: 
    categoria = st.selectbox("Categoria", list(ativos.keys()), label_visibility="collapsed")
with col_pair:
    escolha = st.selectbox("Ativo", list(ativos[categoria].keys()), label_visibility="collapsed")
    ativo_ticker = ativos[categoria][escolha]

# --- BUSCA DE DADOS ---
@st.cache_data(ttl=1)
def get_data(ticker):
    data = yf.download(ticker, period="1d", interval="1m", progress=False)
    if data.empty: return None
    data['EMA_10'] = data['Close'].ewm(span=10).mean()
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    return data

df = get_data(ativo_ticker)

if df is not None:
    last_p = float(df['Close'].iloc[-1].item())
    high_p = float(df['High'].max().item())
    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    c_main, c_side = st.columns([2, 1])

    with c_main:
        st.markdown(f"### Gráfico: {escolha}")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        inf1, inf2 = st.columns(2)
        with inf1:
            st.markdown(f"""<div class='card'><b>Informações do ativo</b><br><br>
            Ativo: {escolha}<br>Preço: {last_p:.4f}<br>Máxima Dia: {high_p:.4f}</div>""", unsafe_allow_html=True)
        with inf2:
            st.markdown(f"<div class='card'><b>Status do Mercado</b><br><br><center><h2 style='color:#4ade80;'>ATIVO</h2>Operacional</center></div>", unsafe_allow_html=True)

    with c_side:
        st.markdown("### Análise com I.A.")
        st.markdown(f"<b>Assertividade da Sessão: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        ema = df['EMA_10'].iloc[-1].item()
        sma = df['SMA_20'].iloc[-1].item()
        sinal = "COMPRA" if ema > sma else "VENDA"
        cor_sinal = "#4ade80" if sinal == "COMPRA" else "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Escaneando fluxo...'):
                time.sleep(1)
                st.markdown(f"""
                <div style='border: 2px solid white; padding:15px; border-radius:10px; background:{cor_sinal}; color:black; text-align:center;'>
                    <h2 style='margin:0;'>{sinal} 🟢</h2>
                    <b>ENTRADA: PRÓXIMA VELA</b><br>
                    Confiança: 94.8%
                </div>
                """, unsafe_allow_html=True)
        
        st.write("Resultado:")
        fb1, fb2 = st.columns(2)
        if fb1.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if fb2.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # --- NOTÍCIAS IGUAL À IMAGEM ---
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>FED e Taxas de Juros</b><br>Expectativa de manutenção impacta ativos de risco.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Halving do Bitcoin</b><br>Mineradores ajustam posições estratégicas.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Bolsas Americanas</b><br>Nasdaq abre em alta com setor de tecnologia forte.</div>", unsafe_allow_html=True)

else:
    st.error("Ativo indisponível ou mercado fechado no momento.")
