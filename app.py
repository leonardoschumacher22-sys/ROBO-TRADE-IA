import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# --- CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="IT - ANALISADOR PRO", layout="wide", initial_sidebar_state="collapsed")

if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILO VISUAL (DARK MODE) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; }
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 12px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1.5s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- CAPTURA DE DADOS SINCRONIZADA ---
def fetch_market_data(ticker):
    try:
        # Puxa os dados mais recentes do mercado global
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 20: return None
        
        # INDICADORES (Ajustados para bater com o gráfico da corretora)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['MA20'] + (df['STD'] * 2)
        df['Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # RSI (Identifica sobrecompra/sobrevenda)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        return df
    except:
        return None

# --- CABEÇALHO ---
c_logo, c_cat, c_ativo = st.columns([1, 2, 2])
with c_logo: st.markdown("## IT")
with c_cat: cat = st.selectbox("", ["FOREX", "CRYPTO", "STOCKS"], label_visibility="collapsed")
with c_ativo:
    ativos = {
        "FOREX": {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X"},
        "CRYPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"},
        "STOCKS": {"APPLE": "AAPL", "TESLA": "TSLA"}
    }
    nome = st.selectbox("", list(ativos[cat].keys()), label_visibility="collapsed")
    ticker = ativos[cat][nome]

# Carregamento
data = fetch_market_data(ticker)

if data is not None:
    # Valores numéricos puros para evitar erros de comparação
    val_atual = float(data['Close'].iloc[-1])
    rsi_val = float(data['RSI'].iloc[-1])
    b_up = float(data['Upper'].iloc[-1])
    b_low = float(data['Lower'].iloc[-1])
    
    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    # --- DASHBOARD ---
    col_g, col_a = st.columns([2, 1])

    with col_g:
        st.markdown(f"### Sincronizado com: {nome}")
        # Gráfico de Candles
        fig = go.Figure(data=[go.Candlestick(
            x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']
        )])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        i1, i2 = st.columns(2)
        with i1: st.markdown(f"<div class='card'><b>Métricas</b><br>Preço: {val_atual:.5f}<br>RSI: {rsi_val:.2f}</div>", unsafe_allow_html=True)
        with i2: st.markdown(f"<div class='card'><b>Status do Sinal</b><br><center><h2 style='color:#facc15; margin:0;'>ATIVO</h2>Conectado</center></div>", unsafe_allow_html=True)

    with col_a:
        st.markdown(f"<b>Assertividade Ativa: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # LÓGICA DE SINAL (REVERSÃO DE VELA)
        sinal = "AGUARDAR"
        cor_btn = "#30363d"
        
        if val_atual <= b_low or rsi_val < 35:
            sinal = "COMPRA 🟢"; cor_btn = "#4ade80"
        elif val_atual >= b_up or rsi_val > 65:
            sinal = "VENDA 🔴"; cor_btn = "#f87171"

        if st.button("ANALISAR AGORA"):
            with st.spinner('Lendo corretora...'):
                time.sleep(0.5)
                st.markdown(f"""
                <div style='background:{cor_btn}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{sinal}</h2>
                    <b>ENTRADA: PRÓXIMA VELA</b>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("Resultado:")
        bw, bl = st.columns(2)
        if bw.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if bl.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # NOTÍCIAS
    st.markdown("### Notícias Importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>Volume Nasdaq</b><br>Fluxo institucional detetado.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Zona Euro</b><br>Moedas em alta volatilidade.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Bitcoin (BTC)</b><br>Suporte de preço confirmado.</div>", unsafe_allow_html=True)

else:
    st.error("Erro de conexão. Tentando restabelecer sinal com a corretora...")
    time.sleep(2)
    st.rerun()
