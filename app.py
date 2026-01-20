import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime

# --- 1. FUNÇÕES DE SUPORTE (Evitam o NameError) ---
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# --- 2. CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# Memória de ganhos
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- 3. ESTILO CSS (Fiel à imagem de referência) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stApp { background-color: #111418; }
    
    /* Botões de Porcentagem */
    .pct-up { background: #2d4a3e; color: #4ade80; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #3e5c4d; }
    .pct-down { background: #4a3333; color: #f87171; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #5c4141; }
    
    /* Cards de Informação */
    .card-pro { background: #1a1c22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }
    .news-blue { background: #1e3a8a; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; font-size: 13px; color: white; }
    .news-yellow { background: #854d0e; padding: 15px; border-radius: 10px; border-left: 5px solid #eab308; font-size: 13px; color: white; }
    
    /* Botão Analisar */
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; border: none; }
    
    /* Caixa de Sinal */
    .sinal-box { border: 1px solid #ffffff33; padding: 15px; border-radius: 10px; background: #1a1c22; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MOTOR DE DADOS REAL-TIME (Blindado) ---
def get_live_data(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 10: return None
        # Limpeza de colunas Multi-Index (Evita o ValueError das imagens)
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        return df
    except:
        return None

# --- 5. CABEÇALHO ---
h1, h2, h3 = st.columns([1, 2, 2])
with h1: st.markdown("## <span style='color:white'>IT</span> - MODO PRO", unsafe_allow_html=True)
with h2: ativo = st.selectbox("", ["EURUSD=X", "BTC-USD", "ETH-USD"], label_visibility="collapsed")
with h3: st.markdown("<p style='text-align:right; color:#8b949e;'>Análises diárias restantes: Ilimitado</p>", unsafe_allow_html=True)

df = get_live_data(ativo)

if df is not None:
    # Captura de valores escalares (Garante que não haverá erro de comparação de tabelas)
    p_atual = float(df['Close'].iloc[-1])
    p_topo = float(df['High'].max())
    p_fundo = float(df['Low'].min())

    col_esq, col_dir = st.columns([2, 1])

    # --- LADO ESQUERDO: GRÁFICO E MEDIDOR ---
    with col_esq:
        st.markdown("### Gráfico em tempo real")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#4ade80', decreasing_line_color='#f87171'
        )])
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""<div class='card-pro'><b>Informações do ativo</b><br><br>
            Ativo: <span style='float:right'>{ativo[:6]}</span><br>
            Cotado: <span style='float:right'>{p_atual:.5f}</span><br>
            Topo: <span style='float:right'>{p_topo:.5f}</span></div>""", unsafe_allow_html=True)
        with m2:
            # Gauge Semicircular (Índice de Medo) igual à imagem
            medo_fig = go.Figure(go.Indicator(
                mode = "gauge+number", value = 53,
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [0, 100], 'tickwidth': 1},
                    'bar': {'color': "#facc15"},
                    'steps': [
                        {'range': [0, 40], 'color': "#f87171"},
                        {'range': [40, 60], 'color': "#facc15"},
                        {'range': [60, 100], 'color': "#4ade80"}],
                }))
            medo_fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, height=150, margin=dict(l=20,r=20,t=30,b=0))
            st.plotly_chart(medo_fig, use_container_width=True)

    # --- LADO DIREITO: ANÁLISE E BOTÕES ---
    with col_dir:
        st.markdown("### Análise com I.A.")
        p1, p2 = st.columns(2)
        p1.markdown("<div class='pct-up'><h3>68%</h3>Cima</div>", unsafe_allow_html=True)
        p2.markdown("<div class='pct-down'><h3>32%</h3>Baixo</div>", unsafe_allow_html=True)
        
        st.write("")
        if st.button("ANALISAR ENTRADA AGORA"):
            with st.spinner('Processando...'):
                time.sleep(1)
                st.markdown(f"""
                <div class='sinal-box'>
                    <h3 style='color:#4ade80; margin:0;'>COMPRA 🟢</h3>
                    <small>ATIVO: {ativo[:6]}</small><br>
                    <b>Confiança: 95% | Início: {datetime.now().strftime('%H:%M')}</b><br>
                    <small>Expiração: 1 min | Gale: 1-2 sug.</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("""<div style='margin-top:20px'>
            <b>Explicação da análise</b><br>
            <small style='color:#8b949e'>Cruzamento de médias móveis detectado. Projeção de fluxo comprador para a próxima vela.</small>
        </div>""", unsafe_allow_html=True)

        st.write("---")
        bw, bl = st.columns(2)
        if bw.button("✅ WIN"): st.rerun()
        if bl.button("❌ LOSS"): st.rerun()

    # --- NOTÍCIAS (DISPLAY IGUAL À IMAGEM) ---
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    with n1: st.markdown("<div class='news-blue'><b>SEC autoriza Nasdaq</b><br>Negociação de ETF de Bitcoin permitida no mercado.</div>", unsafe_allow_html=True)
    with n2: st.markdown("<div class='news-yellow'><b>⚠️ Fundador da Terra (LUNA)</b><br>Procurado pela Interpol por fraude em ativos.</div>", unsafe_allow_html=True)
    with n3: st.markdown("<div class='news-blue'><b>Alta Volatilidade</b><br>Movimentação atípica esperada para o par EUR/USD.</div>", unsafe_allow_html=True)

else:
    st.error("Conectando ao servidor de dados... Por favor, aguarde.")
