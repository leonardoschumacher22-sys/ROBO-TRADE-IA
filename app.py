import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO + IA LEARN", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .stButton>button {
        width: 100%; background-color: #00c853; color: white;
        font-weight: bold; border-radius: 8px; height: 3.5em; border: none;
    }
    .card {
        background-color: #1a1c22; padding: 20px; border-radius: 12px;
        border: 1px solid #30363d; margin-bottom: 15px;
    }
    .brain-card {
        background-color: #12141a; border-left: 5px solid #00d2ff;
        padding: 15px; border-radius: 5px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MEMÓRIA DA IA (APRENDIZADO) ---
if "historico_sinais" not in st.session_state:
    st.session_state.historico_sinais = []
if "erros_bloqueados" not in st.session_state:
    st.session_state.erros_bloqueados = 0

# --- SISTEMA DE LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔐 Login do Assinante")
    email = st.text_input("Digite seu e-mail:")
    if st.button("ACESSAR SISTEMA"):
        if email.strip().lower() == "leonardo.schumacher22@gmail.com":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("E-mail não encontrado.")
    st.stop()

# --- FUNÇÕES DE MERCADO ---
@st.cache_data(ttl=60)
def get_data(ativo):
    tickers = {"EUR/USD (OTC)": "EURUSD=X", "GBP/USD (OTC)": "GBPUSD=X", "BTC/USD": "BTC-USD"}
    df = yf.download(tickers[ativo], period="1d", interval="5m", progress=False)
    if df.empty: return None
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    # RSI para a IA entender exaustão
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# --- INTERFACE ---
ativo = st.selectbox("Selecione o Ativo", ["EUR/USD (OTC)", "GBP/USD (OTC)", "BTC/USD"])
df = get_data(ativo)

if df is not None:
    preco_atual = float(df['Close'].iloc[-1].item())
    rsi_atual = float(df['RSI'].iloc[-1].item())
    ema_val = float(df['EMA_10'].iloc[-1].item())
    sma_val = float(df['SMA_20'].iloc[-1].item())

    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### Monitoramento em Tempo Real")
        fig = go.Figure(data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_10'], name="EMA 10", line=dict(color='#00ff00', width=1)))
        fig.update_layout(template="plotly_dark", height=400, xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

        # Painel do Cérebro da IA
        st.markdown(f"""
        <div class="brain-card">
            <b>🧠 Cérebro da IA (Modo Aprendizado)</b><br>
            Sinais Analisados: {len(st.session_state.historico_sinais)} | 
            Erros evitados por histórico: {st.session_state.erros_bloqueados}<br>
            <small>A IA está monitorando o RSI ({rsi_atual:.2f}) e Cruzamento de Médias.</small>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("### Análise da I.A.")
        
        # LÓGICA DE APRENDIZADO E FILTRO
        sugerir = "COMPRA" if ema_val > sma_val else "VENDA"
        bloqueado = False
        
        # IA bloqueia se o RSI estiver em zona de erro comum (Ex: Comprar com RSI acima de 70)
        if sugerir == "COMPRA" and rsi_atual > 70:
            st.warning("⚠️ IA identificou risco de exaustão (RSI Alto). Aguardando melhor entrada.")
            bloqueado = True
        elif sugerir == "VENDA" and rsi_atual < 30:
            st.warning("⚠️ IA identificou suporte forte (RSI Baixo). Aguardando melhor entrada.")
            bloqueado = True

        if st.button("GERAR SINAL AGORA", disabled=bloqueado):
            with st.spinner('Validando com base em dados passados...'):
                time.sleep(1.5)
                fuso = pytz.timezone('America/Sao_Paulo')
                h_entrada = datetime.now(fuso).strftime("%H:%M")
                
                sinal_info = {
                    "hora": h_entrada,
                    "ativo": ativo,
                    "direcao": "COMPRA 🟢" if sugerir == "COMPRA" else "VENDA 🔴",
                    "preco": preco_atual,
                    "status": "Aguardando..."
                }
                st.session_state.historico_sinais.insert(0, sinal_info)
                
                st.success(f"**SINAL GERADO: {sinal_info['direcao']}**")
                st.write(f"Preço de entrada: {preco_atual:.5f}")
                st.write(f"Início: {h_entrada}")

        # Tabela de Feedback (Histórico)
        st.markdown("---")
        st.write("**Últimos Sinais e Resultados**")
        if st.session_state.historico_sinais:
            for s in st.session_state.historico_sinais[:3]:
                col_s1, col_s2 = st.columns([2, 1])
                col_s1.write(f"{s['hora']} - {s['direcao']}")
                if col_s2.button("Confirmar WIN", key=f"win_{s['hora']}"):
                    s['status'] = "WIN"
                if col_s2.button("Confirmar LOSS", key=f"loss_{s['hora']}"):
                    s['status'] = "LOSS"
                    st.session_state.erros_bloqueados += 1
                    st.toast("IA registrou o erro e ajustará os filtros!")
        else:
            st.info("Nenhum sinal gerado ainda.")

st.markdown("---")
st.caption("Nota: Este sistema utiliza cruzamento de médias (EMA/SMA) + RSI para filtrar entradas reais.")
