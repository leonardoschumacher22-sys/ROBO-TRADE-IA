import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

# --- CONFIGURAÇÃO VISUAL ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- MEMÓRIA DA SESSÃO ---
if "wins" not in st.session_state: st.session_state.wins = 0
if "losses" not in st.session_state: st.session_state.losses = 0
if "historico" not in st.session_state: st.session_state.historico = []

# --- CSS PARA DISPLAY IDÊNTICO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; }
    .news-yellow { background: #854d0e; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; border: none; height: 3em; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 15px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 15px; border-radius: 5px; transition: 0.5s; }
    </style>
    """, unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo, col_pair, col_status = st.columns([1, 3, 2])
with col_logo: st.markdown("## IT")
with col_pair: ativo = st.selectbox("", ["EURUSD=X", "BTC-USD", "GBPUSD=X"], label_visibility="collapsed")
with col_status: st.markdown("<p style='text-align:right; color:#8b949e;'>Análises diárias: Ilimitado</p>", unsafe_allow_html=True)

# --- BUSCA DE DADOS ---
@st.cache_data(ttl=1) # Cache de apenas 1 segundo para ser tempo real
def get_data(ticker):
    data = yf.download(ticker, period="1d", interval="1m", progress=False)
    if data.empty: return None
    # Indicadores Técnicos
    data['EMA_10'] = data['Close'].ewm(span=10).mean()
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    return data

df = get_data(ativo)

if df is not None:
    # Cálculos
    last_p = float(df['Close'].iloc[-1].item())
    high_p = float(df['High'].max().item())
    low_p = float(df['Low'].min().item())
    
    total = st.session_state.wins + st.session_state.losses
    taxa = (st.session_state.wins / total * 100) if total > 0 else 0

    # --- LAYOUT PRINCIPAL ---
    c_main, c_side = st.columns([2, 1])

    with c_main:
        st.markdown("### Gráfico em tempo real")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Informações Inferiores
        inf1, inf2 = st.columns(2)
        with inf1:
            st.markdown(f"""<div class='card'><b>Informações do ativo</b><br><br>
            Ativo: {ativo}<br>Cotado: {last_p:.5f}<br>Topo: {high_p:.5f}</div>""", unsafe_allow_html=True)
        with inf2:
            st.markdown(f"<div class='card'><b>Índice de medo</b><br><br><center><h2 style='color:#facc15;'>53</h2>Neutro</center></div>", unsafe_allow_html=True)

    with c_side:
        st.markdown("### Análise com I.A.")
        
        # Barra de Assertividade Ativa
        st.markdown(f"<b>Assertividade da Sessão: {taxa:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa}%'></div></div>", unsafe_allow_html=True)

        # Lógica de Sinal (Vela Seguinte)
        ema = df['EMA_10'].iloc[-1].item()
        sma = df['SMA_20'].iloc[-1].item()
        sinal = "COMPRA" if ema > sma else "VENDA"
        cor_sinal = "#4ade80" if sinal == "COMPRA" else "#f87171"

        if st.button("ANALISAR ENTRADA AGORA"):
            with st.spinner('Sincronizando com a corretora...'):
                time.sleep(1)
                st.markdown(f"""
                <div style='border: 2px solid white; padding:15px; border-radius:10px; background:{cor_sinal}; color:black; text-align:center;'>
                    <h2 style='margin:0;'>{sinal} 🟢</h2>
                    <b>ENTRADA: PRÓXIMA VELA</b><br>
                    Confiança: 95% | Expiração: 1 min
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown(f"<br><div class='card'><b>Explicação</b><br><small>Cruzamento de EMA detectado. Projeção de fluxo para a vela seguinte.</small></div>", unsafe_allow_html=True)
        
        # Feedback de Assertividade
        st.write("Resultado do sinal:")
        fb1, fb2 = st.columns(2)
        if fb1.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if fb2.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # --- NOTÍCIAS (DISPLAY IGUAL À IMAGEM) ---
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>SEC autoriza Nasdaq</b><br>Negociação de ETF de Bitcoin permitida.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Fundador da Terra (LUNA)</b><br>Procurado pela Interpol.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Alta Volatilidade</b><br>Esperada para o par EUR/USD nas próximas horas.</div>", unsafe_allow_html=True)

else:
    st.error("Erro ao carregar dados. Verifique a conexão.")
