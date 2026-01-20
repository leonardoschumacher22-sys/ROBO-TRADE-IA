import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="IT - MODO PROFISSIONAL", layout="wide", initial_sidebar_state="collapsed")

# Inicialização de Memória
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; }
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; height: 3.5em; border-radius: 8px; }
    .assertividade-bg { background: #30363d; border-radius: 10px; height: 12px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 10px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTA DE ATIVOS ---
ativos = {
    "FOREX/OTC": {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X"},
    "CRIPTOMOEDAS": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"},
    "AÇÕES": {"APPLE": "AAPL", "TESLA": "TSLA", "NVIDIA": "NVDA"}
}

# --- FUNÇÃO DE CAPTURA DE DADOS ---
def carregar_dados_vivos(ticker):
    try:
        # Forçamos a descarga de dados frescos
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 15:
            return None
        
        # Indicadores para o gráfico e análise
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['MA20'] + (df['STD'] * 2)
        df['Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        return df
    except:
        return None

# --- UI SUPERIOR ---
col_it, col_cat, col_ativo = st.columns([1, 2, 2])
with col_it: st.markdown("## IT")
with col_cat: categoria = st.selectbox("", list(ativos.keys()), label_visibility="collapsed")
with col_ativo: 
    nome_ativo = st.selectbox("", list(ativos[categoria].keys()), label_visibility="collapsed")
    ticker_final = ativos[categoria][nome_ativo]

# Execução do Carregamento
dados = carregar_dados_vivos(ticker_final)

if dados is not None:
    # Valores atuais para análise
    preco_agora = float(dados['Close'].iloc[-1])
    rsi_agora = float(dados['RSI'].iloc[-1])
    b_sup = float(dados['Upper'].iloc[-1])
    b_inf = float(dados['Lower'].iloc[-1])
    
    # Assertividade
    total_trades = st.session_state.wins + st.session_state.losses
    taxa_win = (st.session_state.wins / total_trades * 100) if total_trades > 0 else 0

    # --- CORPO DO DASHBOARD ---
    c_esquerdo, c_direito = st.columns([2, 1])

    with c_esquerdo:
        st.markdown(f"### Gráfico em Tempo Real: {nome_ativo}")
        fig = go.Figure(data=[go.Candlestick(x=dados.index, open=dados['Open'], high=dados['High'], low=dados['Low'], close=dados['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Informações Inferiores (Cards Azuis)
        i1, i2 = st.columns(2)
        with i1: st.markdown(f"<div class='card'><b>Métricas de Mercado</b><br>Preço: {preco_agora:.5f}<br>RSI: {rsi_agora:.2f}</div>", unsafe_allow_html=True)
        with i2: st.markdown(f"<div class='card'><b>Sentimento</b><br><center><h2 style='color:#facc15; margin:0;'>53</h2>Neutro</center></div>", unsafe_allow_html=True)

    with c_direito:
        st.markdown(f"<b>Assertividade Ativa: {taxa_win:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bg'><div class='assertividade-fill' style='width:{taxa_win}%'></div></div>", unsafe_allow_html=True)

        # Lógica de Entrada (Sinais)
        sinal = "AGUARDAR"
        cor_fundo = "#30363d"
        
        # Condição de Compra: Tocou na banda de baixo ou RSI baixo
        if preco_agora <= b_inf or rsi_agora < 38:
            sinal = "COMPRA"; cor_fundo = "#4ade80"
        # Condição de Venda: Tocou na banda de cima ou RSI alto
        elif preco_agora >= b_sup or rsi_agora > 62:
            sinal = "VENDA"; cor_fundo = "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Processando algoritmos...'):
                time.sleep(0.5)
                st.markdown(f"""
                <div style='background:{cor_fundo}; padding:25px; border-radius:12px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{sinal}</h2>
                    <p style='margin:0;'><b>PRÓXIMA VELA M1</b></p>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("Resultado:")
        w_col, l_col = st.columns(2)
        if w_col.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if l_col.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # --- NOTÍCIAS (DISPLAY FINAL) ---
    st.markdown("### Notícias Importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>Mercado Americano</b><br>Nasdaq apresenta forte volume comprador.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Zona do Euro</b><br>Inflação impacta pares de Forex.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Cripto Ativos</b><br>Suporte institucional detetado em BTC.</div>", unsafe_allow_html=True)

else:
    st.error("⚠️ Falha na conexão com os gráficos. A tentar reconectar...")
    time.sleep(3)
    st.rerun()
