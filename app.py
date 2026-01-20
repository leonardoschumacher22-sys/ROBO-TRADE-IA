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
st.set_page_config(page_title="IT - IA PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS ---
st.markdown("""
    <style>
    .main { background-color: #1a1c22; color: #ffffff; }
    .stButton>button {
        width: 100%; background-color: #00c853; color: white;
        font-weight: bold; border-radius: 5px; height: 3.5em; border: none;
    }
    .card {
        background-color: #23272f; padding: 20px; border-radius: 10px;
        border: 1px solid #30363d; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN ---
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
            st.error("E-mail não autorizado.")
    st.stop()

# --- MAPEAMENTO DE ATIVOS ---
ativos_map = {"EUR/USD": "EURUSD=X", "GBP/USD": "GBPUSD=X", "BTC/USD": "BTC-USD"}

# --- HEADER ---
c_logo, c_ativo, c_status = st.columns([1, 3, 2])
with c_logo: st.markdown("## IT")
with c_ativo: 
    escolha = st.selectbox("", list(ativos_map.keys()), label_visibility="collapsed")
    ticker = ativos_map[escolha]
with c_status:
    st.markdown("<div style='text-align:right; color:#00ff00;'>● IA Conectada</div>", unsafe_allow_html=True)

# --- ENGINE DE PROCESSAMENTO ---
@st.cache_data(ttl=60)
def carregar_dados(symbol):
    data = yf.download(symbol, period="1d", interval="1m")
    # Limpeza de colunas MultiIndex se necessário
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    # Cálculo de indicadores
    data['RSI'] = ta.rsi(data['Close'], length=14)
    bb = ta.bbands(data['Close'], length=20, std=2)
    # Concatena garantindo que as colunas das bandas existam
    data = pd.concat([data, bb], axis=1)
    data['SMA_20'] = ta.sma(data['Close'], length=20)
    return data.dropna()

try:
    df = carregar_dados(ticker)
    
    # Identificar nomes das colunas das Bandas de Bollinger (evita KeyError)
    col_upper = [c for c in df.columns if 'BBU' in c][0]
    col_lower = [c for c in df.columns if 'BBL' in c][0]

    # --- DASHBOARD ---
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Monitoramento de Fluxo (Real-Time)")
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name="Preço"
        )])
        # Adiciona Bandas
        fig.add_trace(go.Scatter(x=df.index, y=df[col_upper], line=dict(color='gray', width=1), name="Banda Sup", opacity=0.3))
        fig.add_trace(go.Scatter(x=df.index, y=df[col_lower], line=dict(color='gray', width=1), name="Banda Inf", opacity=0.3))
        
        fig.update_layout(height=400, template="plotly_dark", margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### Julgamento da IA")
        if st.button("ANALISAR AGORA"):
            with st.spinner('Aguardando confluência...'):
                time.sleep(1.5)
                
                ultimo_preco = df['Close'].iloc[-1]
                ultimo_rsi = df['RSI'].iloc[-1]
                sup_band = df[col_upper].iloc[-1]
                inf_band = df[col_lower].iloc[-1]
                
                sinal = "AGUARDAR"
                if ultimo_rsi < 35 and ultimo_preco <= inf_band:
                    sinal = "COMPRA"
                elif ultimo_rsi > 65 and ultimo_preco >= sup_band:
                    sinal = "VENDA"
                
                fuso = pytz.timezone('America/Sao_Paulo')
                agora = datetime.now(fuso)
                
                if sinal != "AGUARDAR":
                    cor = "#00c853" if sinal == "COMPRA" else "#d50000"
                    st.markdown(f"""
                        <div style='background:{cor}; padding:20px; text-align:center; border-radius:10px; border: 2px solid white;'>
                            <h2 style='margin:0; color:white;'>{sinal} 🟢</h2>
                            <p style='color:white;'><b>Ativo:</b> {escolha} | <b>Horário:</b> {agora.strftime("%H:%M")}</p>
                            <hr style='border:0.5px solid rgba(255,255,255,0.3);'>
                            <p style='font-size:13px; color:white; text-align:left;'>
                                <b>Se der loss, siga as proteções:</b><br>
                                • +1 entrada às {(agora + timedelta(minutes=1)).strftime("%H:%M")}<br>
                                • +1 entrada às {(agora + timedelta(minutes=2)).strftime("%H:%M")}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Mercado sem confluência clara. IA sugere aguardar a próxima vela.")

except Exception as e:
    st.error(f"Erro na leitura de dados: {e}. Verifique se o ativo está aberto no mercado.")

# --- FOOTER ---
st.markdown("---")
st.markdown("<small>Estratégia baseada em Exaustão de Preço (RSI + Bollinger Bands)</small>", unsafe_allow_html=True)
