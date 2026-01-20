import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# 1. FUNÇÃO AUXILIAR (Corrigindo o NameError)
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# Estilo visual para bater com a imagem original
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 160px; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; height: 3.5em; border-radius: 8px; }
    .assert-fill { background: #00d2ff; height: 12px; border-radius: 10px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE DADOS REAL-TIME (Blindado)
def get_live_data(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 20: return None
        
        # --- LINHA CRÍTICA: CORRIGE O ERRO DAS IMAGENS ---
        # Isso remove o Multi-Index que causa o ValueError
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Indicadores
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
    except Exception as e:
        st.error(f"Erro na API: {e}")
        return None

# 4. INTERFACE E LÓGICA
col_id, col_cat, col_ativo = st.columns([1, 2, 2])
with col_id: st.markdown("## IT")
with col_cat: categoria = st.selectbox("Cat", ["FOREX", "CRIPTOS"], label_visibility="collapsed")
with col_ativo:
    ticker = "EURUSD=X" if categoria == "FOREX" else "BTC-USD"
    st.info(f"Ativo: {ticker}")

df = get_live_data(ticker)

if df is not None:
    # Captura de valores (Blindagem com .item() para evitar Series ambígua)
    p_atual = float(df['Close'].iloc[-1])
    rsi_val = float(df['RSI'].iloc[-1])
    b_up = float(df['Upper'].iloc[-1])
    b_low = float(df['Lower'].iloc[-1])
    
    # Índice de Medo Real (Baseado na Volatilidade Atual)
    volat = (df['High'].iloc[-1] - df['Low'].iloc[-1]) / p_atual * 1000
    medo_idx = int(clamp(50 + (volat * 10), 10, 90))

    c_graph, c_side = st.columns([2, 1])

    with c_graph:
        st.markdown(f"### Gráfico em Tempo Real: {ticker}")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#4ade80', decreasing_line_color='#f87171'
        )])
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        m1, m2 = st.columns(2)
        with m1: st.markdown(f"<div class='card'><b>Métricas Bolsa</b><br><br>Preço: {p_atual:.5f}<br>RSI: {rsi_val:.2f}</div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='card'><b>Índice de Medo</b><br><br><center><h2 style='color:#facc15;'>{medo_idx}</h2>Dinâmico</center></div>", unsafe_allow_html=True)

    with c_side:
        total = st.session_state.wins + st.session_state.losses
        taxa = (st.session_state.wins / total * 100) if total > 0 else 0
        st.write(f"Assertividade: {taxa:.1f}%")
        st.markdown(f"<div style='background:#333; height:12px; border-radius:5px;'><div class='assert-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de Sinal (Sai do AGUARDAR se tocar as bandas)
        sinal = "AGUARDAR"
        cor_sinal = "#30363d"
        
        if p_atual >= b_up or rsi_val > 68: sinal = "VENDA 🔴"; cor_sinal = "#f87171"
        elif p_atual <= b_low or rsi_val < 32: sinal = "COMPRA 🟢"; cor_sinal = "#4ade80"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Escaneando Bolsa...'):
                time.sleep(0.5)
                st.markdown(f"<div style='background:{cor_sinal}; padding:20px; border-radius:10px; text-align:center;'><h2>{sinal}</h2></div>", unsafe_allow_html=True)
        
        st.write("---")
        bw, bl = st.columns(2)
        if bw.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if bl.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()
else:
    st.warning("⚠️ Conectando aos servidores da Bolsa... Clique no botão abaixo se demorar.")
    if st.button("🔄 Forçar Reconexão"): st.rerun()
