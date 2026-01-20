import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="IT - MODO PRO NEXT CANDLE", layout="wide", initial_sidebar_state="collapsed")

# --- MEMÓRIA TÉCNICA (IA) ---
if "memoria_ia" not in st.session_state:
    st.session_state.memoria_ia = []
if "historico_sinais" not in st.session_state:
    st.session_state.historico_sinais = []
if "sinal_pendente" not in st.session_state:
    st.session_state.sinal_pendente = None

# --- CSS PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background: #00c853; color: white; border-radius: 8px; font-weight: bold; height: 3.5em; }
    .card { background: #1a1c22; padding: 20px; border-radius: 12px; border: 1px solid #30363d; margin-bottom: 10px; }
    .brain-card { background-color: #12141a; border-left: 5px solid #00d2ff; padding: 15px; border-radius: 5px; margin-top: 10px; }
    .win { color: #00ff00; font-weight: bold; }
    .loss { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNÇÃO DE MERCADO ---
def fetch_data(ativo):
    tickers = {"EUR/USD (OTC)": "EURUSD=X", "BTC/USD": "BTC-USD", "GBP/USD (OTC)": "GBPUSD=X"}
    df = yf.download(tickers[ativo], period="1d", interval="1m", progress=False)
    if df.empty: return None
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    df['RSI'] = 100 - (100 / (1 + (gain / loss)))
    return df

# --- INTERFACE ---
st.markdown("## 🤖 IT - Analisador de Vela Seguinte")
ativo_escolhido = st.selectbox("", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"], label_visibility="collapsed")
df = fetch_data(ativo_escolhido)

if df is not None:
    # --- CÁLCULO DE ASSERTIVIDADE ---
    total_sinais = len(st.session_state.historico_sinais)
    vitorias = len([s for s in st.session_state.historico_sinais if s.get('status') == 'WIN'])
    taxa_acerto = (vitorias / total_sinais * 100) if total_sinais > 0 else 0

    # --- PROCESSAMENTO AUTOMÁTICO DE RESULTADOS ---
    if st.session_state.sinal_pendente:
        s = st.session_state.sinal_pendente
        # Verifica se a vela seguinte já fechou (2 minutos após a análise: 1m da análise + 1m da vela seguinte)
        if datetime.now() >= s['timestamp_expiracao']:
            preco_fechamento = float(df['Close'].iloc[-1].item())
            venceu = (preco_fechamento > s['preco_entrada']) if s['direcao'] == "COMPRA" else (preco_fechamento < s['preco_entrada'])
            
            status = "WIN" if venceu else "LOSS"
            s['status'] = status
            st.session_state.historico_sinais.append(s)
            
            if status == "LOSS":
                st.session_state.memoria_ia.append({"rsi": s['rsi'], "direcao": s['direcao']})
            
            st.session_state.sinal_pendente = None
            st.rerun()

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### Fluxo de Vela (1 Minuto)")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_10'], name="EMA 10", line=dict(color='#00ff00', width=1)))
        fig.update_layout(template="plotly_dark", height=380, xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""
        <div class="brain-card">
            <div style="display: flex; justify-content: space-between;">
                <b>🧠 Assertividade da Sessão</b>
                <b style="color: #00d2ff;">{taxa_acerto:.1f}%</b>
            </div>
            <div style="background: #30363d; border-radius: 10px; height: 8px; margin: 10px 0;">
                <div style="background: #00d2ff; width: {taxa_acerto}%; height: 8px; border-radius: 10px;"></div>
            </div>
            <small>Sinais: {total_sinais} | Vitórias: {vitorias} | Filtros Ativos: {len(st.session_state.memoria_ia)}</small>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### Próxima Vela")
        rsi_atual = float(df['RSI'].iloc[-1].item())
        ema = float(df['EMA_10'].iloc[-1].item())
        sma = float(df['SMA_20'].iloc[-1].item())
        
        direcao_prevista = "COMPRA" if ema > sma else "VENDA"
        cor_sinal = "#00c853" if direcao_prevista == "COMPRA" else "#ff4b4b"

        # Verificação de Memória (Aprendizado)
        bloqueado = any(abs(e['rsi'] - rsi_atual) < 1.5 and e['direcao'] == direcao_prevista for e in st.session_state.memoria_ia)

        if bloqueado:
            st.error("⚠️ IA: Entrada para próxima vela bloqueada por risco de perda (Histórico).")
        else:
            if st.button("ANALISAR PRÓXIMA VELA"):
                with st.spinner('Projetando vela seguinte...'):
                    time.sleep(1)
                    agora = datetime.now()
                    st.session_state.sinal_pendente = {
                        "preco_entrada": float(df['Close'].iloc[-1].item()),
                        "direcao": direcao_prevista,
                        "rsi": rsi_atual,
                        "timestamp_analise": agora,
                        "timestamp_expiracao": agora + timedelta(minutes=2), # 1m para fechar atual + 1m da próxima
                        "status": "Aguardando"
                    }
                    st.rerun()

        if st.session_state.sinal_pendente:
            s = st.session_state.sinal_pendente
            st.markdown(f"""
            <div style="background: {cor_sinal}; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid white;">
                <h2 style="margin: 0;">{s['direcao']}</h2>
                <p>ENTRADA NA PRÓXIMA VELA</p>
                <small>Preço Ref: {s['preco_entrada']:.5f}<br>Aguarde o fechamento para validar...</small>
            </div>
            """, unsafe_allow_html=True)

# Histórico Rápido
st.markdown("---")
if st.session_state.historico_sinais:
    cols = st.columns(len(st.session_state.historico_sinais[-5:]))
    for i, s in enumerate(st.session_state.historico_sinais[-5:]):
        cor_status = "#00ff00" if s['status'] == "WIN" else "#ff4b4b"
        cols[i].markdown(f"<div style='text-align:center; border: 1px solid #30363d; border-radius: 5px;'>{s['direcao']}<br><b style='color:{cor_status}'>{s['status']}</b></div>", unsafe_allow_html=True)
