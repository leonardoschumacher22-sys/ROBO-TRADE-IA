import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
import yfinance as yf

# --- CONFIGURAÇÃO DE AMBIENTE ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# Memória para manter os ganhos salvos durante a sessão
if 'wins' not in st.session_state: st.session_state.wins = 0
if 'losses' not in st.session_state: st.session_state.losses = 0

# --- ESTILO VISUAL (DARK MODE GOMERE) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #00d2ff; }
    .news-yellow { background: #854d0e; padding: 12px; border-radius: 8px; font-size: 12px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 12px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 12px; border-radius: 5px; transition: 1.5s ease; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE CAPTURA DE DADOS ---
def get_live_market_data(ticker):
    try:
        # Puxa os dados mais recentes (1 minuto de intervalo)
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 20: return None
        
        # INDICADORES TÉCNICOS (O CORAÇÃO DA ANÁLISE)
        df['MA20'] = df['Close'].rolling(window=20).mean()
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['MA20'] + (df['STD'] * 2)
        df['Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # RSI - Índice de Força Relativa
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        return df
    except:
        return None

# --- UI SUPERIOR ---
col_logo, col_cat, col_ativo = st.columns([1, 2, 2])
with col_logo: st.markdown("## IT")
with col_cat: 
    categoria = st.selectbox("Categoria", ["FOREX", "CRYPTO", "STOCKS"], label_visibility="collapsed")
with col_ativo:
    lista_ativos = {
        "FOREX": {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "USD/JPY": "JPY=X"},
        "CRYPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD"},
        "STOCKS": {"APPLE": "AAPL", "TESLA": "TSLA"}
    }
    nome_exibicao = st.selectbox("Ativo", list(lista_ativos[categoria].keys()), label_visibility="collapsed")
    ticker_final = lista_ativos[categoria][nome_exibicao]

# --- PROCESSAMENTO PRINCIPAL ---
df_dados = get_live_market_data(ticker_final)

if df_dados is not None:
    # Extração de valores (Blindagem contra erro ValueError)
    preco_agora = float(df_dados['Close'].iloc[-1])
    rsi_agora = float(df_dados['RSI'].iloc[-1])
    b_sup = float(df_dados['Upper'].iloc[-1])
    b_inf = float(df_dados['Lower'].iloc[-1])
    
    # Cálculo de Assertividade
    total = st.session_state.wins + st.session_state.losses
    taxa_win = (st.session_state.wins / total * 100) if total > 0 else 0

    c_left, c_right = st.columns([2, 1])

    with c_left:
        st.markdown(f"### Gráfico Online: {nome_exibicao}")
        # Gráfico de Candlestick Real
        fig = go.Figure(data=[go.Candlestick(
            x=df_dados.index, open=df_dados['Open'], high=df_dados['High'], low=df_dados['Low'], close=df_dados['Close'],
            increasing_line_color= '#4ade80', decreasing_line_color= '#f87171'
        )])
        fig.update_layout(template="plotly_dark", height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Cards Inferiores
        m1, m2 = st.columns(2)
        with m1: st.markdown(f"<div class='card'><b>Métricas de Preço</b><br>Valor: {preco_agora:.5f}<br>RSI: {rsi_agora:.2f}</div>", unsafe_allow_html=True)
        with m2: st.markdown(f"<div class='card'><b>Fator de Risco</b><br><center><h2 style='color:#facc15; margin:0;'>53</h2>Moderado</center></div>", unsafe_allow_html=True)

    with c_right:
        st.markdown(f"<b>Assertividade Ativa: {taxa_win:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa_win}%'></div></div>", unsafe_allow_html=True)

        # LÓGICA DE ANÁLISE (Otimizada para Reversão em M1)
        # Se o preço toca a banda e o RSI confirma a exaustão, gera o sinal.
        sinal_txt = "AGUARDAR"
        cor_card = "#30363d"
        
        if preco_agora <= (b_inf * 1.0002) or rsi_agora < 35:
            sinal_txt = "COMPRA"; cor_card = "#4ade80"
        elif preco_agora >= (b_sup * 0.9998) or rsi_agora > 65:
            sinal_txt = "VENDA"; cor_card = "#f87171"

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Analisando padrões...'):
                time.sleep(0.5)
                st.markdown(f"""
                <div style='background:{cor_card}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{sinal_txt}</h2>
                    <b>ENTRADA NA ABERTURA DA PRÓXIMA VELA</b>
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("Resultado do Sinal:")
        bw, bl = st.columns(2)
        if bw.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if bl.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # NOTÍCIAS (MANTENDO O DISPLAY SOLICITADO)
    st.markdown("### Notícias Importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>Nasdaq 100</b><br>Alta volatilidade detectada no setor tech.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Zona do Euro</b><br>Decisões de taxas impactam pares de moedas.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Bitcoin (BTC)</b><br>Suporte de 60k mantido por grandes players.</div>", unsafe_allow_html=True)

else:
    st.error("Conexão com o mercado interrompida. Tentando reconectar...")
    time.sleep(2)
    st.rerun()
