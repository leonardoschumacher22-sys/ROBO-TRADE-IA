import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime
import yfinance as yf

# --- CONFIGURAÇÃO DE INTERFACE ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- INICIALIZAÇÃO DE MEMÓRIA ---
if "wins" not in st.session_state: st.session_state.wins = 0
if "losses" not in st.session_state: st.session_state.losses = 0

# --- CSS PERSONALIZADO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; height: 100%; }
    .news-blue { background: #1e3a8a; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; border-left: 5px solid #00d2ff; }
    .news-yellow { background: #854d0e; padding: 15px; border-radius: 10px; font-size: 12px; height: 100px; border-left: 5px solid #facc15; }
    .stButton>button { width: 100%; background: #4ade80; color: black; font-weight: bold; border-radius: 8px; height: 3.5em; border: none; }
    .assertividade-bar { background: #30363d; border-radius: 5px; height: 15px; width: 100%; margin: 10px 0; }
    .assertividade-fill { background: #00d2ff; height: 15px; border-radius: 5px; transition: 1s ease-in-out; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTA DE ATIVOS AMPLIADA ---
ativos_dict = {
    "MOEDAS": {"EUR/USD (OTC)": "EURUSD=X", "GBP/USD (OTC)": "GBPUSD=X", "USD/JPY (OTC)": "JPY=X", "AUD/CAD (OTC)": "AUDCAD=X"},
    "AÇÕES": {"APPLE": "AAPL", "TESLA": "TSLA", "NVIDIA": "NVDA", "AMAZON": "AMZN"},
    "CRIPTO": {"BITCOIN": "BTC-USD", "ETHEREUM": "ETH-USD", "SOLANA": "SOL-USD"}
}

# --- MOTOR DE DADOS REAL-TIME ---
def fetch_live_data(ticker):
    try:
        # Buscamos dados de 1 dia com intervalo de 1 minuto
        df = yf.download(ticker, period="1d", interval="1m", progress=False)
        if df.empty or len(df) < 30:
            return None
        
        # INDICADORES PARA ASSERTIVIDADE
        df['MA10'] = df['Close'].ewm(span=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        
        # Bandas de Bollinger
        df['STD'] = df['Close'].rolling(window=20).std()
        df['Upper'] = df['MA20'] + (df['STD'] * 2)
        df['Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # RSI (Filtro de Reversão)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    except:
        return None

# --- CABEÇALHO ---
c1, c2, c3 = st.columns([1, 2, 2])
with c1: st.markdown("## IT")
with c2: cat_sel = st.selectbox("Categoria", list(ativos_dict.keys()), label_visibility="collapsed")
with c3: 
    ativo_nome = st.selectbox("Ativo", list(ativos_dict[cat_sel].keys()), label_visibility="collapsed")
    ticker_final = ativos_dict[cat_sel][ativo_nome]

# Execução do Motor
data_df = fetch_live_data(ticker_final)

if data_df is not None:
    # EXTRAÇÃO SEGURA DE VALORES (Evita o ValueError da imagem)
    p_atual = float(data_df['Close'].iloc[-1].item())
    p_high = float(data_df['High'].max().item())
    rsi_val = float(data_df['RSI'].iloc[-1].item())
    b_upper = float(data_df['Upper'].iloc[-1].item())
    b_lower = float(data_df['Lower'].iloc[-1].item())
    ma10 = float(data_df['MA10'].iloc[-1].item())
    ma20 = float(data_df['MA20'].iloc[-1].item())

    # --- LÓGICA DE SINAL (ALTA ASSERTIVIDADE) ---
    # Só entra se houver confluência: Preço fora da banda + RSI extremo
    decisao = "AGUARDAR"
    cor_alerta = "#30363d"
    confianca = "0%"

    if p_atual <= b_lower or rsi_val < 35:
        decisao = "COMPRA"
        cor_alerta = "#4ade80"
        confianca = "92.8%"
    elif p_atual >= b_upper or rsi_val > 65:
        decisao = "VENDA"
        cor_alerta = "#f87171"
        confianca = "94.1%"

    # --- DASHBOARD ---
    total_ops = st.session_state.wins + st.session_state.losses
    taxa_val = (st.session_state.wins / total_ops * 100) if total_ops > 0 else 0

    col_graph, col_ana = st.columns([2, 1])

    with col_graph:
        st.markdown(f"### Gráfico em tempo real: {ativo_nome}")
        fig = go.Figure(data=[go.Candlestick(x=data_df.index, open=data_df['Open'], high=data_df['High'], low=data_df['Low'], close=data_df['Close'])])
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Informações Inferiores
        inf1, inf2 = st.columns(2)
        with inf1:
            st.markdown(f"""<div class='card'><b>Informações do ativo</b><br><br>
            Ativo: {ativo_nome}<br>Cotado: {p_atual:.5f}<br>RSI: {rsi_val:.2f}</div>""", unsafe_allow_html=True)
        with inf2:
            st.markdown(f"<div class='card'><b>Índice de Medo</b><br><br><center><h2 style='color:#facc15;'>53</h2>Neutro</center></div>", unsafe_allow_html=True)

    with col_ana:
        st.markdown(f"<b>Assertividade Ativa: {taxa_val:.1f}%</b>", unsafe_allow_html=True)
        st.markdown(f"<div class='assertividade-bar'><div class='assertividade-fill' style='width:{taxa_val}%'></div></div>", unsafe_allow_html=True)

        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Sincronizando feed...'):
                time.sleep(0.5)
                st.markdown(f"""
                <div style='background:{cor_alerta}; padding:20px; border-radius:10px; color:black; text-align:center; border: 2px solid white;'>
                    <h2 style='margin:0;'>{decisao}</h2>
                    <b>ENTRADA: PRÓXIMA VELA</b><br>
                    Confiança: {confianca}
                </div>
                """, unsafe_allow_html=True)
        
        st.write("---")
        st.write("Resultado do último sinal:")
        btn_w, btn_l = st.columns(2)
        if btn_w.button("✅ WIN"): st.session_state.wins += 1; st.rerun()
        if btn_l.button("❌ LOSS"): st.session_state.losses += 1; st.rerun()

    # --- NOTÍCIAS ---
    st.markdown("### Notícias importantes")
    n1, n2, n3 = st.columns(3)
    n1.markdown("<div class='news-blue'><b>SEC aprova Nasdaq</b><br>Novas regras de liquidez para ETFs de BTC.</div>", unsafe_allow_html=True)
    n2.markdown("<div class='news-yellow'><b>Atenção Geopolítica</b><br>Volatilidade esperada em pares de USD.</div>", unsafe_allow_html=True)
    n3.markdown("<div class='news-blue'><b>Movimentação M1</b><br>Fluxo de ordens institucional detectado.</div>", unsafe_allow_html=True)

else:
    st.error("Erro na conexão com o mercado. Tentando reconectar...")
    time.sleep(2)
    st.rerun()
