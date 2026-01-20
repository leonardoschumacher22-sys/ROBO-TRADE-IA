import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# --- FUNÇÃO AUXILIAR (DEFINIDA NO TOPO PARA EVITAR ERROS) ---
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# --- CONFIGURAÇÃO DA INTERFACE ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# Inicialização de Memória
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 160px; }
    .news-card { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; border: none; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 10px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DADOS REAIS ---
def get_live_data(ticker):
    try:
        # Busca dados reais de 1 minuto
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty or len(data) < 20: return None
        
        df = data.copy()
        # Indicadores Blindados (evitam ValueError)
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['SMA20'] + (df['STD'] * 2)
        df['Lower'] = df['SMA20'] - (df['STD'] * 2)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        return df
    except:
        return None

# --- HEADER ---
c1, c2, c3 = st.columns([1, 2, 2])
with c1: st.markdown("## IT")
with c2: cat = st.selectbox("Categoria", ["MOEDAS", "CRIPTOS", "AÇÕES"], label_visibility="collapsed")
with c3:
    ativos = {"MOEDAS": "EURUSD=X", "CRIPTOS": "BTC-USD", "AÇÕES": "AAPL"}
    ticker = ativos[cat]
    st.info(f"Conectado: {ticker}")

# --- EXECUÇÃO E LÓGICA ---
df = get_live_data(ticker)

if df is not None:
    # Captura Segura de Valores Únicos
    p_atual = float(df['Close'].iloc[-1].item())
    rsi_val = float(df['RSI'].iloc[-1].item())
    b_up = float(df['Upper'].iloc[-1].item())
    b_low = float(df['Lower'].iloc[-1].item())
    
    # Índice de Medo Real baseado na Volatilidade
    volat = (df['High'].iloc[-1] - df['Low'].iloc[-1]) / p_atual * 1000
    medo_idx = int(clamp(50 + volat, 10, 90))

    col_g, col_a = st.columns([2, 1])

    with col_g:
        st.markdown(f"### Gráfico Real: {ticker}")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        m1, m2 = st.columns(2)
        with m1: st.markdown(f"<div class='card'><b>Métricas de Mercado</b><br><br>Preço: {p_atual:.5f}<br>RSI: {rsi_val:.2f}</div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='card'><b>Índice de Medo</b><br><br><center><h2 style='color:#facc15;'>{medo_idx}</h2>Neutro</center></div>", unsafe_allow_html=True)

    with col_a:
        total = st.session_state.wins + st.session_state.losses
        taxa = (st.session_state.wins / total * 100) if total > 0 else 0
        st.write(f"**Assertividade:** {taxa:.1f}%")
        st.markdown(f"<div style='background:#333; height:12px; border-radius:5px;'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de Análise (Sai do AGUARDAR se tocar as bandas)
        sinal = "AGUARDAR"
        cor = "#30363d"
        if p_atual >= b_up or rsi_val > 70: sinal = "VENDA 🔴"; cor = "#f87171"
        elif p_atual <= b_low or rsi_val < 30: sinal = "COMPRA 🟢"; cor = "#4ade80"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Lendo algoritmos...'):
                time.sleep(0.5)
                st.markdown(f"<div style='background:{cor}; padding:20px; border-radius:10px; text-align:center;'><h2>{sinal}</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        res_w, res_l = st.columns(2)
        if res_w.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if res_l.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()
else:
    st.error("Aguardando sinal da Bolsa... Verifique sua conexão.")
    if st.button("Tentar Reconectar"): st.rerun()
