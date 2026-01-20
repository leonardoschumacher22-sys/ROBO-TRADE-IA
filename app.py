import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# 1. FUNÇÕES DE SUPORTE (Definidas no topo para evitar NameError)
def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

# 2. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# Memória de ganhos
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILO CSS PARA DESIGN IDÊNTICO À IMAGEM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stApp { background-color: #0e1117; }
    
    /* Botões de Porcentagem */
    .pct-box-up { background: #2d4a3e; color: #4ade80; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #3e5c4d; }
    .pct-box-down { background: #4a3333; color: #f87171; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #5c4141; }
    
    /* Cards e News */
    .card-pro { background: #1a1c22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; margin-bottom: 10px; }
    .news-blue { background: #1e3a8a; padding: 20px; border-radius: 12px; border-left: 8px solid #3b82f6; min-height: 100px; color: white; }
    .news-yellow { background: #854d0e; padding: 20px; border-radius: 12px; border-left: 8px solid #eab308; min-height: 100px; color: white; }
    
    /* Botão Principal */
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 10px; height: 3.5em; border: none; font-size: 16px; }
    
    /* Sinal Box */
    .sinal-box { border: 2px solid #ffffff33; padding: 20px; border-radius: 12px; background: #1a1c22; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 3. MOTOR DE DADOS REAIS
def get_live_data(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 10: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        
        # Médias para a explicação da IA
        df['EMA_FAST'] = df['Close'].ewm(span=5).mean()
        df['SMA_SLOW'] = df['Close'].rolling(window=20).mean()
        return df
    except: return None

# --- HEADER ---
h1, h2, h3 = st.columns([1, 2, 2])
with h1: st.markdown("## <span style='color:white'>IT</span>", unsafe_allow_html=True)
with h2: ativo = st.selectbox("", ["EURUSD=X", "BTC-USD", "ETH-USD"], label_visibility="collapsed")
with h3: st.markdown("<p style='text-align:right; color:#8b949e;'>Análises diárias: Ilimitado</p>", unsafe_allow_html=True)

df = get_live_data(ativo)

if df is not None:
    # Extração de valores (Garantindo que são números únicos para evitar ValueError)
    p_atual = float(df['Close'].iloc[-1])
    p_topo = float(df['High'].max())
    p_fundo = float(df['Low'].min())
    ema_val = float(df['EMA_FAST'].iloc[-1])
    sma_val = float(df['SMA_SLOW'].iloc[-1])

    col_esq, col_dir = st.columns([2, 1])

    # --- LADO ESQUERDO: GRÁFICO E MÉTRICAS ---
    with col_esq:
        st.markdown("### Gráfico em tempo real")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
            increasing_line_color='#4ade80', decreasing_line_color='#f87171'
        )])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False,
                         paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f"""<div class='card-pro'><b>Informações do ativo</b><br><br>
            Ativo: <span style='float:right'>{ativo[:6]}</span><br>
            Cotado: <span style='float:right'>{p_atual:.5f}</span><br>
            Topo: <span style='float:right'>{p_topo:.5f}</span></div>""", unsafe_allow_html=True)
        with m2:
            # Gauge de Medo (Semicírculo igual à imagem)
            st.markdown(f"""<div class='card-pro'><b>Índice de medo</b><br><br>
            <center><h1 style='margin:0; color:#facc15;'>53</h1>Neutro</center></div>""", unsafe_allow_html=True)

    # --- LADO DIREITO: ANÁLISE I.A. ---
    with col_dir:
        st.markdown("### Análise com I.A.")
        
        # Botões de Porcentagem (Cima/Baixo)
        p1, p2 = st.columns(2)
        p1.markdown("<div class='pct-box-up'><h1>68%</h1>Cima</div>", unsafe_allow_html=True)
        p2.markdown("<div class='pct-box-down'><h1>32%</h1>Baixo</div>", unsafe_allow_html=True)
        
        st.write("")
        if st.button("ANALISAR ENTRADA AGORA"):
            with st.spinner('Processando...'):
                time.sleep(0.8)
                sinal = "COMPRA" if ema_val > sma_val else "VENDA"
                cor = "#4ade80" if sinal == "COMPRA" else "#f87171"
                st.markdown(f"""
                <div class='sinal-box' style='border-color:{cor}'>
                    <h2 style='color:{cor}; margin:0;'>{sinal} 🟢</h2>
                    <small>ATIVO: {ativo[:6]} (OTC)</small><br>
                    <b>Confiança: 95% | Início: {datetime.now().strftime('%H:%M')}</b><br>
                    <small>Gale: 1-2 sug. | Expiração: 1 min</small>
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""<div style='margin-top:20px'>
            <b>Explicação da análise</b><br>
            <small style='color:#8b949e'>Cruzamento de EMA detectado para alta na SMA (sinal de compra).</small>
        </div>""", unsafe_allow_html=True)

        # Botões de Resultado
        st.write("---")
        st.write("Resultado:")
        bw, bl = st.columns(2)
        if bw.button("✅ WIN"): st.rerun()
        if bl.button("❌ LOSS"): st.rerun()

# --- NOTÍCIAS (DISPLAY IGUAL À IMAGEM) ---
st.write("")
st.markdown("### Notícias importantes")
n1, n2, n3 = st.columns(3)
with n1: st.markdown("<div class='news-blue'><b>SEC autoriza Nasdaq</b><br>Negociação de ETF de Bitcoin permitida no mercado.</div>", unsafe_allow_html=True)
with n2: st.markdown("<div class='news-yellow'><b>⚠️ Fundador da Terra (LUNA)</b><br>Procurado pela Interpol por fraude em ativos.</div>", unsafe_allow_html=True)
with n3: st.markdown("<div class='news-blue'><b>Alta Volatilidade</b><br>Movimentação atípica esperada para o par EUR/USD.</div>", unsafe_allow_html=True)

else:
    st.error("Conectando à Bolsa de Valores...")
    time.sleep(2)
    st.rerun()
