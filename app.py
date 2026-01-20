import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="IT - PRECISÃO M1", layout="wide", initial_sidebar_state="collapsed")

# Inicialização de Variáveis de Memória (Persistentes na sessão)
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILIZAÇÃO CSS (IGUAL À SUA IMAGEM) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; }
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; height: 3.5em; border-radius: 8px; border: none; }
    .assert-bar-bg { background: #30363d; border-radius: 10px; height: 12px; width: 100%; margin: 10px 0; }
    .assert-bar-fill { background: #00d2ff; height: 12px; border-radius: 10px; transition: width 0.6s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTA DE ATIVOS ---
dict_ativos = {
    "FOREX": {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X"},
    "CRIPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"},
    "AÇÕES": {"APPLE": "AAPL", "TESLA": "TSLA"}
}

# --- FUNÇÃO DE BUSCA DE DADOS (SEM CACHE PARA EVITAR TRAVAMENTO) ---
def buscar_dados(ticker):
    try:
        # Tenta buscar os dados mais recentes
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 20:
            return None
        
        # Cálculo de Indicadores (Focados em Reversão de M1)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['B_Upper'] = df['MA20'] + (df['STD'] * 2)
        df['B_Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain / loss)))
        
        return df
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return None

# --- INTERFACE SUPERIOR ---
c_logo, c_cat, c_pair = st.columns([1, 2, 2])
with c_logo: st.markdown("## IT")
with c_cat: categoria = st.selectbox("", list(dict_ativos.keys()), label_visibility="collapsed")
with c_pair: 
    ativo_nome = st.selectbox("", list(dict_ativos[categoria].keys()), label_visibility="collapsed")
    ticker = dict_ativos[categoria][ativo_nome]

# --- PROCESSAMENTO ---
df = buscar_dados(ticker)

if df is not None:
    # Captura de valores de forma segura
    p_atual = float(df['Close'].iloc[-1])
    rsi_v = float(df['RSI'].iloc[-1])
    b_up = float(df['B_Upper'].iloc[-1])
    b_low = float(df['B_Lower'].iloc[-1])
    
    # Cálculo de Assertividade
    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    col_g, col_a = st.columns([2, 1])

    with col_g:
        st.markdown(f"### Gráfico {ativo_nome} (Tempo Real)")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Informações Inferiores (Igual à imagem)
        i1, i2 = st.columns(2)
        with i1: st.markdown(f"<div class='card'><b>Informações</b><br>Preço: {p_atual:.5f}<br>RSI: {rsi_v:.2f}</div>", unsafe_allow_html=True)
        with i2: st.markdown(f"<div class='card'><b>Índice de Medo</b><br><center><h2 style='color:#facc15; margin:0;'>53</h2>Neutro</center></div>", unsafe_allow_html=True)

    with col_a:
        st.markdown(f"<b>Assertividade Ativa: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assert-bar-bg'><div class='assert-bar-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de Sinal
        decisao = "AGUARDAR"
        cor_btn = "#30363d"
        if p_atual <= b_low or rsi_v < 35:
            decisao = "COMPRA"; cor_btn = "#4ade80"
        elif p_atual >= b_up or rsi_v > 65:
            decisao = "VENDA"; cor_btn = "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Lendo algoritmos...'):
                time.sleep(0.5)
                st.markdown(f"""
                <div style='background:{cor_btn}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{decisao}</h2>
                    <b>ENTRADA: VELA SEGUINTE</b>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("Resultado:")
        b_w, b_l = st.columns(2)
        if b_w.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if b_l.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # --- NOTÍCIAS (DADOS FIXOS IGUAIS À IMAGEM) ---
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>SEC aprova Nasdaq</b><br>Regras para ETFs trazem volatilidade.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Zona do Euro</b><br>Decisão sobre juros impacta pares OTC.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Fluxo M1</b><br>Detectada pressão de compra institucional.</div>", unsafe_allow_html=True)

else:
    st.warning("🔄 O sistema está tentando conectar aos dados do mercado. Se demorar, clique no botão abaixo.")
    if st.button("FORÇAR RECONEXÃO"): st.rerun()
