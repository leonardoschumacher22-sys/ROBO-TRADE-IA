import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# Inicialização segura de memória
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILO CSS (DISPLAY IGUAL À IMAGEM) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; }
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 12px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE DADOS SEM BLOQUEIO ---
def get_market_data(ticker):
    try:
        # Busca dados do último dia em M1
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty or len(data) < 30: return None
        
        # Indicadores Calculados de forma Robusta
        df = data.copy()
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
c1, c2, c3 = st.columns([1, 2, 2])
with c1: st.markdown("## IT")
with c2: categoria = st.selectbox("Cat", ["MOEDAS", "CRIPTOS", "AÇÕES"], label_visibility="collapsed")
with c3:
    ativos = {"MOEDAS": "EURUSD=X", "CRIPTOS": "BTC-USD", "AÇÕES": "AAPL"}
    ticker = ativos[categoria]
    ativo_txt = st.selectbox("Ativo", [ticker], label_visibility="collapsed")

# Carregamento dos Dados
df = get_market_data(ticker)

if df is not None:
    # EXTRAÇÃO DE VALORES (Garante que são números e não listas)
    # Isso resolve o erro de ValueError das suas imagens
    try:
        preco_atual = float(df['Close'].iloc[-1])
        rsi_atual = float(df['RSI'].iloc[-1])
        b_superior = float(df['Upper'].iloc[-1])
        b_inferior = float(df['Lower'].iloc[-1])
    except:
        st.error("Erro ao processar indicadores. Tente novamente.")
        st.stop()

    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    # --- DASHBOARD ---
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown(f"### Gráfico em tempo real: {categoria}")
        # Criando Gráfico de Velas Real
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']
        )])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Cards de Informação
        inf1, inf2 = st.columns(2)
        with inf1: st.markdown(f"<div class='card'><b>Métricas</b><br>Preço: {preco_atual:.5f}<br>RSI: {rsi_atual:.2f}</div>", unsafe_allow_html=True)
        with inf2: st.markdown(f"<div class='card'><b>Índice de Medo</b><br><center><h2 style='color:#facc15; margin:0;'>53</h2>Neutro</center></div>", unsafe_allow_html=True)

    with col_side:
        st.markdown(f"<b>Assertividade Ativa: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # LÓGICA DE SINAL ATIVA
        # Afrouxamos um pouco para ele não ficar apenas em AGUARDAR
        sinal = "AGUARDAR"
        cor_box = "#30363d"
        
        if preco_atual <= (b_inferior * 1.0001) or rsi_atual < 40:
            sinal = "COMPRA"; cor_box = "#4ade80"
        elif preco_atual >= (b_superior * 0.9999) or rsi_atual > 60:
            sinal = "VENDA"; cor_box = "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Escaneando mercado...'):
                time.sleep(0.5)
                st.markdown(f"""
                <div style='background:{cor_box}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{sinal}</h2>
                    <b>SINAL PARA PRÓXIMA VELA (M1)</b>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("Resultado:")
        b_w, b_l = st.columns(2)
        if b_w.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if b_l.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # NOTÍCIAS
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>SEC aprova Nasdaq</b><br>Liquidez de ETFs deve aumentar volume.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Zona do Euro</b><br>Decisão sobre taxas gera volatilidade.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Suporte Cripto</b><br>Whales mantêm posições acima de 60k.</div>", unsafe_allow_html=True)

else:
    st.warning("🔄 Conectando aos servidores de dados... Por favor, aguarde ou clique em 'Rerun'.")
    if st.button("RECONECTAR AGORA"): st.rerun()
