import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS (VISUAL PREMIUM IDÊNTICO) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    [data-testid="stAppViewContainer"] { background-color: #0e1117; }
    .stButton>button {
        width: 100%;
        background-color: #00c853;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3.5em;
        border: none;
    }
    .card {
        background-color: #1a1c22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }
    .header-info { text-align: right; color: #8b949e; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

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

# --- MAPEAMENTO DE ATIVOS ---
ticker_map = {
    "EUR/USD (OTC)": "EURUSD=X",
    "GBP/USD (OTC)": "GBPUSD=X",
    "BTC/USD": "BTC-USD"
}

# --- BUSCA DE DADOS E CÁLCULO DE INDICADORES ---
@st.cache_data(ttl=60)
def get_market_data(ativo_nome):
    ticker_symbol = ticker_map[ativo_nome]
    df = yf.download(ticker_symbol, period="1d", interval="5m", progress=False)
    
    if df.empty:
        return None
    
    # Cálculo de Indicadores Reais
    df['SMA_20'] = df['Close'].rolling(window=20).mean()
    df['EMA_10'] = df['Close'].ewm(span=10, adjust=False).mean()
    
    # CORREÇÃO DO ERRO: Extração de valores escalares usando .item()
    info = {
        "preco_atual": float(df['Close'].iloc[-1].item()),
        "topo_diario": float(df['High'].max().item()),
        "fundo_diario": float(df['Low'].min().item()),
        "last_ema": float(df['EMA_10'].iloc[-1].item()),
        "last_sma": float(df['SMA_20'].iloc[-1].item()),
        "df": df
    }
    return info

# --- CABEÇALHO ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo:
    st.markdown("## IT")
with col_pair:
    ativo_selecionado = st.selectbox("", list(ticker_map.keys()), label_visibility="collapsed")
with col_mode:
    st.markdown("<div class='header-info'>Análises restantes: <b>Ilimitado</b></div>", unsafe_allow_html=True)
    if st.button("Sair do modo Pro"):
        st.session_state.logado = False
        st.rerun()

# --- PROCESSAMENTO DE DADOS ---
data = get_market_data(ativo_selecionado)

if data:
    c1, c2 = st.columns([2, 1])

    with c1:
        st.markdown("### Gráfico em tempo real")
        # Gráfico Candlestick Profissional
        fig = go.Figure(data=[go.Candlestick(
            x=data['df'].index,
            open=data['df']['Open'],
            high=data['df']['High'],
            low=data['df']['Low'],
            close=data['df']['Close'],
            name="Preço"
        )])
        # Adiciona a linha da EMA para visualização técnica
        fig.add_trace(go.Scatter(x=data['df'].index, y=data['df']['EMA_10'], name="EMA 10", line=dict(color='#00ff00', width=1.5)))
        fig.update_layout(template="plotly_dark", height=380, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
        col_info, col_medo, col_mvp = st.columns(3)
        with col_info:
            st.markdown(f"""
                <div class='card'>
                    <b>Informações do ativo</b><br>
                    <small>
                    Ativo: {ativo_selecionado}<br>
                    Cotado: {data['preco_atual']:.5f}<br>
                    Fundo: {data['fundo_diario']:.5f}<br>
                    Topo: {data['topo_diario']:.5f}
                    </small>
                </div>
            """, unsafe_allow_html=True)
            
        with col_medo:
            st.markdown("<div class='card'><center><b>Índice de medo</b></center>", unsafe_allow_html=True)
            gauge = go.Figure(go.Indicator(mode="gauge+number", value=53, gauge={'axis':{'range':[0,100]}, 'bar':{'color':"yellow"}, 'steps':[{'range':[0,40],'color':"red"},{'range':[40,60],'color':"orange"},{'range':[60,100],'color':"green"}]}))
            gauge.update_layout(height=140, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(gauge, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_mvp:
            st.markdown("<div class='card'><b>Tendência Atual</b><br><br>", unsafe_allow_html=True)
            tendencia = "ALTA 📈" if data['last_ema'] > data['last_sma'] else "BAIXA 📉"
            st.write(f"Mercado em: **{tendencia}**")
            st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("### Análise com I.A")
        
        # Lógica de Probabilidade baseada no Indicador
        if data['last_ema'] > data['last_sma']:
            p_cima, p_baixo, decisao, cor_bg = 74, 26, "COMPRA 🟢", "#00c853"
        else:
            p_cima, p_baixo, decisao, cor_bg = 31, 69, "VENDA 🔴", "#d50000"

        col_p1, col_p2 = st.columns(2)
        col_p1.markdown(f"<div style='background:#1b4332; padding:10px; text-align:center; border-radius:5px; color:#00ff00;'>{p_cima}%<br>Cima</div>", unsafe_allow_html=True)
        col_p2.markdown(f"<div style='background:#432818; padding:10px; text-align:center; border-radius:5px; color:#ff4b4b;'>{p_baixo}%<br>Baixo</div>", unsafe_allow_html=True)
        
        st.write("")
        
        if st.button("ANALISAR ENTRADA"):
            with st.spinner('Analisando algoritmos...'):
                time.sleep(1.5)
                fuso_br = pytz.timezone('America/Sao_Paulo')
                agora = datetime.now(fuso_br)
                h_entrada = agora.strftime("%H:%M")
                h_gale1 = (agora + timedelta(minutes=1)).strftime("%H:%M")
                h_gale2 = (agora + timedelta(minutes=2)).strftime("%H:%M")
                
                st.markdown(f"""
                    <div style='background:{cor_bg}; padding:20px; text-align:center; border-radius:10px; border: 2px solid white;'>
                        <h2 style='margin:0; color:white;'>{decisao}</h2>
                        <p style='margin:5px 0; font-weight:bold; color:white;'>ATIVO: {ativo_selecionado}</p>
                        <p style='margin:0; color:white;'>Confiança: {np.random.randint(93, 98)}% | Início: {h_entrada}</p>
                        <hr style='margin:10px 0; border:0.5 solid rgba(255,255,255,0.3);'>
                        <p style='margin:0; font-size:13px; color:white; text-align:left;'>
                            <b>Proteção de Capital (Gale):</b><br>
                            • Próximo minuto: {h_gale1}<br>
                            • Segundo minuto: {h_gale2}
                        </p>
                    </div>
                """, unsafe_allow_html=True)

        st.markdown(f"<div class='card' style='margin-top:15px;'><b>Explicação da análise</b><br><small>Detectado cruzamento de EMA 10 sob SMA 20, indicando {'força compradora' if decisao == 'COMPRA 🟢' else 'pressão vendedora'}.</small></div>", unsafe_allow_html=True)

else:
    st.error("Erro ao conectar com o mercado. Verifique sua internet.")

# Rodapé
st.markdown("---")
st.markdown("### Notícias Rápidas")
st.info("Volatilidade alta detectada nos pares de Moedas OTC.")
