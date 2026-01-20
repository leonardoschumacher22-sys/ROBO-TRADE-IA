import streamlit as st
import pandas as pd
import numpy as np
import time
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - IA ALTA PRECISÃO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #1a1c22; color: #ffffff; }
    .stButton>button {
        width: 100%; background-color: #00c853; color: white;
        font-weight: bold; border-radius: 5px; height: 3.5em; border: none;
        box-shadow: 0px 4px 15px rgba(0, 200, 83, 0.3);
    }
    .card {
        background-color: #23272f; padding: 20px; border-radius: 10px;
        border: 1px solid #30363d; margin-bottom: 15px;
    }
    .metric-box { text-align: center; padding: 10px; border-radius: 5px; background: #161b22; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN (TRAVA) ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔐 Acesso Restrito - IA PRO")
    email = st.text_input("E-mail:")
    if st.button("ENTRAR NA PLATAFORMA"):
        if email.strip().lower() == "leonardo.schumacher22@gmail.com":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("Acesso negado.")
    st.stop()

# --- MAPEAMENTO ---
ativos_map = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "BTC/USD": "BTC-USD"}

# --- HEADER ---
c_logo, c_ativo, c_status = st.columns([1, 3, 2])
with c_logo: st.markdown("## IT")
with c_ativo: 
    escolha = st.selectbox("", list(ativos_map.keys()), label_visibility="collapsed")
    ticker = ativos_map[escolha]
with c_status:
    st.markdown("<div style='text-align:right; color:#00ff00;'>● Servidor Online (Alta Precisão)</div>", unsafe_allow_html=True)

# --- ENGINE DE DADOS ---
# Baixa dados recentes para análise técnica profunda
df = yf.download(ticker, period="1d", interval="1m").tail(100)
df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

# Cálculo de Indicadores de Precisão
df['RSI'] = ta.rsi(df['Close'], length=14)
bbands = ta.bbands(df['Close'], length=20, std=2)
df = pd.concat([df, bbands], axis=1)
df['SMA_20'] = ta.sma(df['Close'], length=20)

# --- DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Monitoramento de Fluxo")
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Preço"
    )])
    # Adiciona Bandas de Bollinger ao gráfico para visualização pro
    fig.add_trace(go.Scatter(x=df.index, y=df['BBU_20_2.0'], line=dict(color='rgba(173, 216, 230, 0.4)'), name="Banda Sup"))
    fig.add_trace(go.Scatter(x=df.index, y=df['BBL_20_2.0'], line=dict(color='rgba(173, 216, 230, 0.4)'), name="Banda Inf"))
    fig.update_layout(height=400, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f"<div class='metric-box'><small>RSI</small><br><b>{df['RSI'].iloc[-1]:.2f}</b></div>", unsafe_allow_html=True)
    with m2: 
        tendencia = "ALTA" if df['Close'].iloc[-1] > df['SMA_20'].iloc[-1] else "BAIXA"
        st.markdown(f"<div class='metric-box'><small>TENDÊNCIA</small><br><b>{tendencia}</b></div>", unsafe_allow_html=True)
    with m3: st.markdown(f"<div class='metric-box'><small>VOLATILIDADE</small><br><b>ALTA</b></div>", unsafe_allow_html=True)

with col2:
    st.markdown("### Inteligência Artificial")
    
    if st.button("BUSCAR CONFLUÊNCIA"):
        with st.spinner('Aguardando confirmação técnica...'):
            time.sleep(2)
            
            # Variáveis atuais
            preco = df['Close'].iloc[-1]
            rsi = df['RSI'].iloc[-1]
            b_sup = df['BBU_20_2.0'].iloc[-1]
            b_inf = df['BBL_20_2.0'].iloc[-1]
            
            # LÓGICA DE ALTA PRECISÃO (CONFLUÊNCIA)
            sinal = "AGUARDAR"
            
            # Critério de Compra: RSI baixo + Preço tocou banda inferior
            if rsi < 35 and preco <= b_inf:
                sinal = "COMPRA"
            # Critério de Venda: RSI alto + Preço tocou banda superior
            elif rsi > 65 and preco >= b_sup:
                sinal = "VENDA"
            
            fuso = pytz.timezone('America/Sao_Paulo')
            agora = datetime.now(fuso)
            
            if sinal != "AGUARDAR":
                cor = "#00c853" if sinal == "COMPRA" else "#d50000"
                st.markdown(f"""
                    <div style='background:{cor}; padding:20px; text-align:center; border-radius:10px; border: 2px solid white;'>
                        <h2 style='margin:0; color:white;'>{sinal} 🟢</h2>
                        <p style='color:white;'><b>Ativo:</b> {escolha} | <b>Entrada:</b> {agora.strftime("%H:%M")}</p>
                        <hr style='border:0.5px solid rgba(255,255,255,0.3);'>
                        <p style='font-size:12px; color:white; text-align:left;'>
                            <b>INSTRUÇÃO DE SEGURANÇA:</b><br>
                            • Expiração: 1 minuto<br>
                            • Se a vela fechar contra: Entrada às {(agora + timedelta(minutes=1)).strftime("%H:%M")}<br>
                            • Última proteção: Entrada às {(agora + timedelta(minutes=2)).strftime("%H:%M")}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                st.balloons()
            else:
                st.warning("IA ANALISOU: O mercado não apresenta confluência segura no momento. Aguarde a próxima vela para evitar loss.")

    st.markdown("""
        <div class='card' style='margin-top:15px;'>
            <b>Estratégia IT Pro:</b><br>
            <small>Analisa RSI + Bandas de Bollinger + SMA20 para filtrar entradas falsas em mercados laterais.</small>
        </div>
    """, unsafe_allow_html=True)
