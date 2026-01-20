import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# 1. FUNÇÃO DE CONTROLE (Definida primeiro para evitar NameError)
def fix_range(n, min_n, max_n):
    return max(min(max_n, n), min_n)

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# Memória de ganhos
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# 3. ESTILO CSS PARA FICAR IGUAL À SUA IMAGEM
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; min-height: 150px; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; border: none; }
    .assert-bar { background: #333; height: 12px; border-radius: 5px; width: 100%; }
    .assert-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1s ease; }
    </style>
    """, unsafe_allow_html=True)

# 4. CAPTURA DE DADOS REAIS DA BOLSA
@st.fragment # Otimiza a atualização do gráfico
def render_app():
    # Seleção de Ativo
    col_l, col_c, col_a = st.columns([1, 2, 2])
    with col_l: st.markdown("## IT")
    with col_c: cat = st.selectbox("Cat", ["FOREX", "CRYPTO"], label_visibility="collapsed")
    with col_a:
        ticker = "EURUSD=X" if cat == "FOREX" else "BTC-USD"
        st.info(f"Ativo: {ticker}")

    # Busca Dados
    try:
        data = yf.download(ticker, period="1d", interval="1m", progress=False)
        if data.empty:
            st.warning("Aguardando conexão com a bolsa...")
            return

        # Cálculos Técnicos (Blindados contra ValueError)
        df = data.copy()
        df['SMA'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['SMA'] + (df['STD'] * 2)
        df['Lower'] = df['SMA'] - (df['STD'] * 2)

        # Extração de valores ÚNICOS (Uso de .item() para matar o erro das fotos)
        preco_atual = float(df['Close'].iloc[-1].iloc[0] if isinstance(df['Close'].iloc[-1], pd.Series) else df['Close'].iloc[-1])
        b_up = float(df['Upper'].iloc[-1])
        b_low = float(df['Lower'].iloc[-1])
        
        # Índice de Medo (Dinâmico)
        volat = (df['High'].iloc[-1] - df['Low'].iloc[-1]) * 1000
        medo_val = int(fix_range(50 + volat, 10, 95))

        # --- LAYOUT DASHBOARD ---
        c_g, c_s = st.columns([2, 1])

        with c_g:
            st.markdown("### Gráfico em Tempo Real")
            fig = go.Figure(data=[go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                increasing_line_color='#4ade80', decreasing_line_color='#f87171'
            )])
            fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # Cards de Informação
            m1, m2 = st.columns(2)
            with m1: st.markdown(f"<div class='card'><b>Métricas</b><br><br>Preço: {preco_atual:.5f}<br>Topo: {df['High'].max():.5f}</div>", unsafe_allow_html=True)
            with m2: st.markdown(f"<div class='card'><b>Índice de Medo</b><br><br><center><h2 style='color:#facc15;'>{medo_val}</h2>Neutro</center></div>", unsafe_allow_html=True)

        with c_s:
            total = st.session_state.wins + st.session_state.losses
            taxa = (st.session_state.wins / total * 100) if total > 0 else 0
            st.write(f"Assertividade: {taxa:.1f}%")
            st.markdown(f"<div class='assert-bar'><div class='assert-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

            # LÓGICA DE IA (Sinal Analítico)
            sinal = "AGUARDAR"
            cor = "#30363d"
            if preco_atual >= b_up: sinal = "VENDA 🔴"; cor = "#f87171"
            elif preco_atual <= b_low: sinal = "COMPRA 🟢"; cor = "#4ade80"

            if st.button("ANALISAR PRÓXIMA VELA"):
                with st.spinner('Lendo padrões...'):
                    time.sleep(0.6)
                    st.markdown(f"<div style='background:{cor}; padding:20px; border-radius:10px; text-align:center;'><h2>{sinal}</h2></div>", unsafe_allow_html=True)
            
            st.write("---")
            bw, bl = st.columns(2)
            if bw.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
            if bl.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    except Exception as e:
        st.error(f"Erro de conexão: {e}")
        if st.button("Reiniciar Sistema"): st.rerun()

render_app()
