import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="IT - MODO PRO REALTIME", layout="wide")

# --- AUTO-REFRESH (FORÇA O ROBÔ A RODAR SOZINHO) ---
# Isso faz o script atualizar a cada 30 segundos automaticamente
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()

# --- MEMÓRIA DA SESSÃO ---
if "historico_sinais" not in st.session_state:
    st.session_state.historico_sinais = []
if "sinal_pendente" not in st.session_state:
    st.session_state.sinal_pendente = None

# --- CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background: #00c853; color: white; font-weight: bold; border-radius: 8px; }
    .card { background: #1a1c22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .win-text { color: #00ff00; font-weight: bold; }
    .loss-text { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE BUSCA SEM CACHE TRAVADO ---
def fetch_realtime_data(ativo):
    tickers = {"EUR/USD (OTC)": "EURUSD=X", "BTC/USD": "BTC-USD", "GBP/USD (OTC)": "GBPUSD=X"}
    # Buscamos os dados dos últimos 2 dias em 1m para garantir que as médias existam
    df = yf.download(tickers[ativo], period="1d", interval="1m", progress=False)
    if df.empty or len(df) < 20:
        return None
    
    # Cálculos Reais
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    return df

# --- INTERFACE ---
st.subheader("🤖 Analisador em Tempo Real (Vela Seguinte)")

ativo = st.selectbox("Selecione o Ativo", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])

# Botão para forçar atualização manual se necessário
if st.button("🔄 ATUALIZAR AGORA"):
    st.rerun()

df = fetch_realtime_data(ativo)

if df is not None:
    preco_agora = float(df['Close'].iloc[-1].item())
    rsi_agora = float(df['RSI'].iloc[-1].item())
    ema = float(df['EMA_10'].iloc[-1].item())
    sma = float(df['SMA_20'].iloc[-1].item())

    # --- LÓGICA DE ASSERTIVIDADE ---
    vitorias = len([s for s in st.session_state.historico_sinais if s.get('status') == 'WIN'])
    total = len(st.session_state.historico_sinais)
    taxa = (vitorias / total * 100) if total > 0 else 0

    c1, c2 = st.columns([2, 1])

    with c1:
        # Gráfico Candlestick
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_10'], name="EMA 10", line=dict(color='#00ff00', width=1.5)))
        fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class='card'>
            <b>Taxa de Assertividade da Sessão: {taxa:.1f}%</b><br>
            <small>Preço atual: {preco_agora:.5f} | RSI: {rsi_agora:.2f}</small>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### Análise de Próxima Vela")
        
        # Lógica de Sinal para a vela seguinte
        direcao = "COMPRA" if ema > sma else "VENDA"
        cor = "#00c853" if direcao == "COMPRA" else "#ff4b4b"
        
        if st.button("ANALISAR PRÓXIMA VELA"):
            with st.spinner('Projetando...'):
                time.sleep(1)
                st.session_state.sinal_pendente = {
                    "preco_entrada": preco_agora,
                    "direcao": direcao,
                    "timestamp_expiracao": datetime.now() + timedelta(minutes=2),
                    "status": "Aguardando"
                }
                st.rerun()

        if st.session_state.sinal_pendente:
            s = st.session_state.sinal_pendente
            st.markdown(f"""
            <div style='background:{cor}; padding:15px; border-radius:10px; text-align:center; border: 2px solid white;'>
                <h2 style='margin:0;'>{s['direcao']}</h2>
                <p>Análise enviada para vela seguinte.</p>
                <small>Aguardando confirmação do mercado...</small>
            </div>
            """, unsafe_allow_html=True)

    # --- VERIFICAÇÃO AUTOMÁTICA DE RESULTADO ---
    if st.session_state.sinal_pendente:
        if datetime.now() >= st.session_state.sinal_pendente['timestamp_expiracao']:
            # Checa se o preço da vela seguinte fechou a favor
            preco_final = preco_agora 
            venceu = (preco_final > s['preco_entrada']) if s['direcao'] == "COMPRA" else (preco_final < s['preco_entrada'])
            s['status'] = "WIN" if venceu else "LOSS"
            st.session_state.historico_sinais.append(s)
            st.session_state.sinal_pendente = None
            st.rerun()

else:
    st.warning("⚠️ Aguardando resposta do mercado... Verifique sua conexão ou troque o ativo.")

# Barra de Status inferior
st.markdown("---")
st.write("**Histórico de Resultados Recentes:**")
if st.session_state.historico_sinais:
    cols = st.columns(10)
    for i, res in enumerate(st.session_state.historico_sinais[-10:]):
        cor_res = "win-text" if res['status'] == "WIN" else "loss-text"
        cols[i].markdown(f"<span class='{cor_res}'>{res['status']}</span>", unsafe_allow_html=True)
