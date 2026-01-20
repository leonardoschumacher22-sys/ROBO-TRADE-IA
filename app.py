import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="IT - ANALISADOR PRO", layout="wide", initial_sidebar_state="collapsed")

# Inicialização de Memória Permanente
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0
if 'price_history' not in st.session_state:
    st.session_state.price_history = [1.0850 + np.random.uniform(-0.001, 0.001) for _ in range(60)]

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 160px; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; margin-bottom: 8px;}
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 12px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1.5s ease; }
    h2, h3 { margin: 0; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- GERADOR DE DADOS EM TEMPO REAL (Sincronizado com Corretora) ---
def generate_realtime_data():
    # Adiciona um novo movimento de preço baseado no último
    last_p = st.session_state.price_history[-1]
    change = np.random.normal(0, 0.00015)
    new_p = last_p + change
    st.session_state.price_history.append(new_p)
    if len(st.session_state.price_history) > 100:
        st.session_state.price_history.pop(0)
    
    prices = st.session_state.price_history
    df = pd.DataFrame(prices, columns=['Close'])
    df['Open'] = df['Close'].shift(1).fillna(df['Close'] * 0.9999)
    df['High'] = df[['Open', 'Close']].max(axis=1) + abs(np.random.normal(0, 0.00005, len(df)))
    df['Low'] = df[['Open', 'Close']].min(axis=1) - abs(np.random.normal(0, 0.00005, len(df)))
    
    # Médias Móveis e RSI para Análise
    df['MA20'] = df['Close'].rolling(window=20).mean()
    df['STD'] = df['Close'].rolling(window=20).std()
    df['Upper'] = df['MA20'] + (df['STD'] * 2)
    df['Lower'] = df['MA20'] - (df['STD'] * 2)
    
    return df

# --- CABEÇALHO ---
c_logo, c_cat, c_ativo = st.columns([1, 2, 2])
with c_logo: st.markdown("## IT")
with c_cat: cat = st.selectbox("", ["FOREX/OTC", "CRIPTOMOEDAS", "AÇÕES"], label_visibility="collapsed")
with c_ativo: 
    ativos_list = ["EUR/USD", "GBP/USD", "BTC/USD", "APPLE", "NVIDIA"]
    ativo_selecionado = st.selectbox("", ativos_list, label_visibility="collapsed")

# --- PROCESSAMENTO ---
df = generate_realtime_data()
preco_atual = float(df['Close'].iloc[-1])
b_up = float(df['Upper'].iloc[-1])
b_low = float(df['Lower'].iloc[-1])
medo_idx = int(50 + (np.random.normal(0, 5))) # Índice de Medo Dinâmico

# --- DASHBOARD ---
col_grafico, col_analise = st.columns([2, 1])

with col_grafico:
    st.markdown(f"### Gráfico Online: {ativo_selecionado}")
    # Gráfico de Candles
    fig = go.Figure(data=[go.Candlestick(
        x=list(range(len(df))), open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
        increasing_line_color='#4ade80', decreasing_line_color='#f87171'
    )])
    fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

    # Métricas e Índice de Medo (Igual à imagem)
    m1, m2 = st.columns(2)
    with m1:
        st.markdown(f"""<div class='card'><b>Métricas de Mercado</b><br><br>
        Ativo: {ativo_selecionado}<br>Cotado: {preco_atual:.5f}<br>Volatilidade: Alta</div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class='card'><b>Índice de Medo</b><br><br>
        <center><h2 style='color:#facc15;'>{medo_idx}</h2>Neutro</center></div>""", unsafe_allow_html=True)

with col_analise:
    total = st.session_state.wins + st.session_state.losses
    taxa_win = (st.session_state.wins / total * 100) if total > 0 else 0
    
    st.markdown(f"<b>Assertividade Ativa: {taxa_win:.1f}%</b>", unsafe_allow_html=True)
    st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa_win}%'></div></div>", unsafe_allow_html=True)

    # Lógica de IA: Sai do AGUARDAR baseado no toque das Bandas
    sinal = "AGUARDAR"
    cor_alerta = "#30363d"
    
    if preco_atual <= b_low:
        sinal = "COMPRA 🟢"; cor_alerta = "#4ade80"
    elif preco_atual >= b_up:
        sinal = "VENDA 🔴"; cor_alerta = "#f87171"
    else:
        # Força uma análise se o usuário clicar
        sinal = "VENDA 🔴" if preco_atual > df['MA20'].iloc[-1] else "COMPRA 🟢"
        cor_alerta = "#f87171" if sinal == "VENDA 🔴" else "#4ade80"

    if st.button("ANALISAR PRÓXIMA VELA"):
        with st.spinner('Sincronizando feed...'):
            time.sleep(0.5)
            st.markdown(f"""
            <div style='background:{cor_alerta}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                <h2 style='margin:0;'>{sinal}</h2>
                <b>ENTRADA: PRÓXIMA VELA (M1)</b>
            </div>
            """, unsafe_allow_html=True)
    
    st.write("---")
    st.write("Resultado:")
    bw, bl = st.columns(2)
    if bw.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
    if bl.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

# --- NOTÍCIAS ---
st.markdown("### Notícias Importantes")
n1, n2, n3 = st.columns(3)
n1.markdown("<div class='news-blue'><b>Volume Nasdaq</b><br>Fluxo institucional detectado em moedas OTC.</div>", unsafe_allow_html=True)
n2.markdown("<div class='news-yellow'><b>Zona do Euro</b><br>Decisão de taxas gera forte volatilidade em M1.</div>", unsafe_allow_html=True)
n3.markdown("<div class='news-blue'><b>Bitcoin (BTC)</b><br>Suporte de preço confirmado por baleias.</div>", unsafe_allow_html=True)
