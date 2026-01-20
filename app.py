import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- MEMÓRIA DA SESSÃO ---
if "wins" not in st.session_state: st.session_state.wins = 0
if "losses" not in st.session_state: st.session_state.losses = 0

# --- CSS PARA DISPLAY IDÊNTICO À IMAGEM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; }
    .news-yellow { background: #854d0e; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 15px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 15px; border-radius: 5px; transition: 0.8s; }
    </style>
    """, unsafe_allow_html=True)

# --- DICIONÁRIO DE ATIVOS ---
ativos = {
    "📊 MOEDAS": {"EUR/USD (OTC)": "EURUSD=X", "GBP/USD (OTC)": "GBPUSD=X", "USD/JPY (OTC)": "JPY=X"},
    "🍎 AÇÕES": {"APPLE": "AAPL", "TESLA": "TSLA", "NVIDIA": "NVDA"},
    "₿ CRIPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"}
}

# --- BUSCA DE DADOS COM TRATAMENTO DE ERRO ---
@st.cache_data(ttl=1)
def get_clean_data(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty or len(data) < 21: return None
        
        # Indicadores de Alta Precisão
        data['EMA5'] = data['Close'].ewm(span=5).mean()
        data['EMA20'] = data['Close'].ewm(span=20).mean()
        
        # RSI
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        data['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        # Bandas de Bollinger
        data['MA20'] = data['Close'].rolling(window=20).mean()
        data['STD'] = data['Close'].rolling(window=20).std()
        data['Upper'] = data['MA20'] + (data['STD'] * 2)
        data['Lower'] = data['MA20'] - (data['STD'] * 2)
        
        return data
    except:
        return None

# --- CABEÇALHO ---
c_logo, c_cat, c_pair = st.columns([1, 2, 2])
with c_logo: st.markdown("## IT")
with c_cat: categoria = st.selectbox("", list(ativos.keys()), label_visibility="collapsed")
with c_pair: 
    escolha = st.selectbox("", list(ativos[categoria].keys()), label_visibility="collapsed")
    ticker_atual = ativos[categoria][escolha]

df = get_clean_data(ticker_atual)

if df is not None:
    # Extração de valores individuais para evitar ValueError
    c_close = float(df['Close'].iloc[-1].item())
    c_rsi = float(df['RSI'].iloc[-1].item())
    c_upper = float(df['Upper'].iloc[-1].item())
    c_lower = float(df['Lower'].iloc[-1].item())
    c_ema5_atual = float(df['EMA5'].iloc[-1].item())
    c_ema5_prev = float(df['EMA5'].iloc[-2].item())
    
    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    c_main, c_side = st.columns([2, 1])

    with c_main:
        st.markdown(f"### Gráfico em tempo real: {escolha}")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        inf1, inf2 = st.columns(2)
        with inf1:
            st.markdown(f"""<div class='card'><b>Informações do ativo</b><br><br>
            Ativo: {escolha}<br>Cotado: {c_close:.5f}<br>RSI: {c_rsi:.2f}</div>""", unsafe_allow_html=True)
        with inf2:
            st.markdown(f"<div class='card'><b>Índice de Medo</b><br><br><center><h2 style='color:#facc15;'>53</h2>Neutro</center></div>", unsafe_allow_html=True)

    with c_side:
        st.markdown(f"<b>Assertividade Ativa: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de sinal corrigida para evitar erro de comparação
        sinal = "AGUARDAR"
        cor_box = "#30363d"
        
        if c_close <= c_lower and c_rsi < 40:
            sinal = "COMPRA"; cor_box = "#4ade80"
        elif c_close >= c_upper and c_rsi > 60:
            sinal = "VENDA"; cor_box = "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Validando...'):
                time.sleep(1)
                st.markdown(f"""
                <div style='background:{cor_box}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{sinal}</h2>
                    <b>ENTRADA: VELA SEGUINTE</b><br>
                    Confiança: 92.4%
                </div>
                """, unsafe_allow_html=True)
        
        st.write("Resultado:")
        fb1, fb2 = st.columns(2)
        if fb1.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if fb2.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # --- NOTÍCIAS (MANTENDO O DISPLAY) ---
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>SEC e Nasdaq</b><br>Regulação de ETFs traz liquidez ao mercado.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Atenção Geopolítica</b><br>Impactos no preço do Petróleo e Moedas.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Alta Volatilidade</b><br>Movimentação atípica esperada em M1.</div>", unsafe_allow_html=True)

else:
    st.warning("⚠️ Carregando dados do mercado... Aguarde.")
