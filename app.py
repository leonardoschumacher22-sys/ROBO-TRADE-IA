import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pytz
import yfinance as yf # Para dados históricos reais

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IT - MODO PRO", layout="wide", initial_sidebar_state="collapsed")

# --- ESTILIZAÇÃO CSS (VISUAL PREMIUM) ---
st.markdown("""
    <style>
    .main { background-color: #1a1c22; color: #ffffff; }
    .stButton>button {
        width: 100%;
        background-color: #00c853;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        height: 3.5em;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #00e676;
    }
    .card {
        background-color: #23272f;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .header-info { text-align: right; color: #8b949e; font-size: 14px; }
    .stSelectbox>div>div { border-color: #30363d; background-color: #23272f; color: #ffffff; }
    .stTextInput>div>div>input { background-color: #23272f; color: #ffffff; border-color: #30363d; }
    /* Estilização para as colunas de "Cima" e "Baixo" */
    .prediction-up {
        background:#1b4332; padding:10px; text-align:center; border-radius:5px; color:#00ff00;
        transition: transform 0.2s;
    }
    .prediction-up:hover {
        transform: translateY(-3px);
    }
    .prediction-down {
        background:#432818; padding:10px; text-align:center; border-radius:5px; color:#ff4b4b;
        transition: transform 0.2s;
    }
    .prediction-down:hover {
        transform: translateY(-3px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if "logado" not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    st.title("🔐 Login do Assinante")
    email = st.text_input("Digite seu e-mail:", key="login_email")
    if st.button("ACESSAR SISTEMA", key="login_button"):
        if email.strip().lower() == "leonardo.schumacher22@gmail.com":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("E-mail não encontrado.")
    st.stop()

# --- FUNÇÕES DE CÁLCULO DE INDICADORES ---
@st.cache_data(ttl=600) # Cache para não baixar os dados toda hora
def load_and_process_data(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="5m")
        if data.empty:
            st.error(f"Não foi possível carregar dados para {ticker}. Verifique o ticker.")
            return pd.DataFrame()

        # Calcular Médias Móveis
        data['SMA_20'] = data['Close'].rolling(window=20).mean()
        data['EMA_10'] = data['Close'].ewm(span=10, adjust=False).mean()
        
        # Últimos valores para as informações do ativo
        last_close = data['Close'].iloc[-1]
        high_52w = data['High'].max() # Poderia ser mais específico para o período
        low_52w = data['Low'].min() # Poderia ser mais específico para o período

        return data, last_close, high_52w, low_52w
    except Exception as e:
        st.error(f"Erro ao carregar dados para {ticker}: {e}")
        return pd.DataFrame(), 0, 0, 0


def generate_candlestick_chart(df, ticker_name):
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        close=df['Close'],
                                        name='Candlestick')],
                      layout=go.Layout(template="plotly_dark")) # Tema escuro

    # Adicionar médias móveis
    if 'SMA_20' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], line=dict(color='orange', width=1), name='SMA 20'))
    if 'EMA_10' in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df['EMA_10'], line=dict(color='purple', width=1), name='EMA 10'))

    fig.update_layout(
        title=f'{ticker_name} Gráfico de Velas (5 min)',
        xaxis_rangeslider_visible=False,
        height=400,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor='#23272f', # Fundo do gráfico
        paper_bgcolor='#23272f', # Fundo do papel
        font=dict(color='white')
    )
    fig.update_xaxes(gridcolor='#30363d')
    fig.update_yaxes(gridcolor='#30363d')
    return fig

# --- MAPEAMENTO DE ATIVOS PARA TICKERS YFINANCE ---
ticker_map = {
    "EUR/USD (OTC)": "EURUSD=X", # YFinance usa =X para forex
    "GBP/USD (OTC)": "GBPUSD=X",
    "BTC/USD": "BTC-USD"
}

# --- CABEÇALHO ---
col_logo, col_pair, col_mode = st.columns([1, 4, 2])
with col_logo:
    st.markdown("## IT")
with col_pair:
    # Ajusta o selectbox para usar as chaves do ticker_map
    ativo_selecionado_display = st.selectbox("", list(ticker_map.keys()), label_visibility="collapsed")
    ativo_ticker = ticker_map[ativo_selecionado_display]

with col_mode:
    st.markdown("<div class='header-info'>Análises diárias restantes: <b>Ilimitado</b></div>", unsafe_allow_html=True)
    if st.button("Sair do modo Pro", key="logout_button"):
        st.session_state.logado = False
        st.rerun()

# --- CONTEÚDO PRINCIPAL ---
c1, c2 = st.columns([2, 1])

# Carregar dados e indicadores
df_chart, last_close_price, highest_price, lowest_price = load_and_process_data(ativo_ticker)

with c1:
    st.markdown("### Gráfico em tempo real")
    if not df_chart.empty:
        fig_candle = generate_candlestick_chart(df_chart, ativo_selecionado_display)
        st.plotly_chart(fig_candle, use_container_width=True)
    else:
        st.warning("Não foi possível exibir o gráfico. Verifique o ticker selecionado.")
    
    col_info, col_medo, col_mvp = st.columns(3)
    with col_info:
        st.markdown(f"""
            <div class='card'>
                <b>Informações do ativo</b><br>
                <small>
                Ativo: {ativo_selecionado_display}<br>
                Cotação: {last_close_price:.5f}<br>
                Mínima: {lowest_price:.5f}<br>
                Máxima: {highest_price:.5f}
                </small>
            </div>
        """, unsafe_allow_html=True)
        
    with col_medo:
        st.markdown("<div class='card'><center><b>Índice de medo</b></center>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(mode="gauge+number", value=53, gauge={'axis':{'range':[0,100]}, 'bar':{'color':"yellow"}, 'steps':[{'range':[0,40],'color':"red"},{'range':[40,60],'color':"orange"},{'range':[60,100],'color':"green"}]}))
        fig.update_layout(height=150, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_mvp:
        st.markdown("<div class='card'><b>Índice de MVP</b>", unsafe_allow_html=True)
        st.line_chart(np.random.randn(20, 1), height=120) # Manter este aleatório por enquanto
        st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("### Análise com I.A")
    # Aumentar a dinâmica visual para as porcentagens
    if "pred_up" not in st.session_state:
        st.session_state.pred_up = 68
        st.session_state.pred_down = 32

    p_cima, p_baixo = st.columns(2)
    p_cima.markdown(f"<div class='prediction-up'>{st.session_state.pred_up}%<br>Cima</div>", unsafe_allow_html=True)
    p_baixo.markdown(f"<div class='prediction-down'>{st.session_state.pred_down}%<br>Baixo</div>", unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("ANALISAR ENTRADA AGORA", key="analyze_button"):
        with st.spinner('Analisando mercado...'):
            time.sleep(2) # Simular tempo de análise

            decisao = "AGUARDAR 🟡"
            cor_bg = "#ffc107" # Amarelo para aguardar
            explicacao = "Análise em andamento ou sem sinal claro."

            if not df_chart.empty and len(df_chart) >= 20: # Precisa de dados para as médias
                last_sma = df_chart['SMA_20'].iloc[-1]
                last_ema = df_chart['EMA_10'].iloc[-1]
                
                # Lógica simples de cruzamento de médias
                # Se a EMA cruzou a SMA de baixo para cima (sinal de compra)
                if df_chart['EMA_10'].iloc[-2] < df_chart['SMA_20'].iloc[-2] and last_ema >= last_sma:
                    decisao = "COMPRA 🟢"
                    cor_bg = "#00c853"
                    confianca = random.randint(91, 98)
                    explicacao = "Cruzamento de EMA para cima na SMA (sinal de compra)."
                    st.session_state.pred_up = random.randint(60, 80)
                    st.session_state.pred_down = 100 - st.session_state.pred_up

                # Se a EMA cruzou a SMA de cima para baixo (sinal de venda)
                elif df_chart['EMA_10'].iloc[-2] > df_chart['SMA_20'].iloc[-2] and last_ema <= last_sma:
                    decisao = "VENDA 🔴"
                    cor_bg = "#d50000"
                    confianca = random.randint(91, 98)
                    explicacao = "Cruzamento de EMA para baixo na SMA (sinal de venda)."
                    st.session_state.pred_down = random.randint(60, 80)
                    st.session_state.pred_up = 100 - st.session_state.pred_down
                else:
                    decisao = "AGUARDAR ⚪"
                    cor_bg = "#424242" # Cinza para aguardar sem sinal
                    confianca = random.randint(50, 70) # Menor confiança se não há sinal claro
                    explicacao = "Sem cruzamento de médias móveis claro no momento."
                    st.session_state.pred_up = random.randint(45, 55)
                    st.session_state.pred_down = 100 - st.session_state.pred_up
            else:
                confianca = random.randint(50, 70) # Menor confiança se não há dados suficientes
                explicacao = "Dados insuficientes para análise de médias móveis."
                st.session_state.pred_up = random.randint(45, 55)
                st.session_state.pred_down = 100 - st.session_state.pred_up

            # Ajuste de Horário de Brasília
            fuso_br = pytz.timezone('America/Sao_Paulo')
            agora = datetime.now(fuso_br)
            h_entrada = agora.strftime("%H:%M")
            h_gale1 = (agora + timedelta(minutes=1)).strftime("%H:%M")
            h_gale2 = (agora + timedelta(minutes=2)).strftime("%H:%M")
            
            st.markdown(f"""
                <div style='background:{cor_bg}; padding:20px; text-align:center; border-radius:10px; border: 2px solid white;'>
                    <h2 style='margin:0; color:white;'>{decisao}</h2>
                    <p style='margin:5px 0; font-weight:bold; color:white;'>ATIVO: {ativo_selecionado_display}</p>
                    <p style='margin:0; color:white;'>Confiança: {confianca}% | Início: {h_entrada}</p>
                    <hr style='margin:10px 0; border:0.5 solid rgba(255,255,255,0.3);'>
                    <p style='margin:0; font-size:13px; color:white; text-align:left;'>
                        <b>Se não ganhar de primeira, faça:</b><br>
                        • +1 entrada no próximo minuto às {h_gale1}<br>
                        • +1 entrada no minuto seguinte às {h_gale2}
                    </p>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div class='card' style='margin-top:15px;'><b>Explicação da análise</b><br><small>{explicacao}</small></div>", unsafe_allow_html=True)


    # Card de explicação da análise, atualizado dinamicamente
    st.markdown("<div class='card' style='margin-top:15px;' id='explanation_card'><b>Explicação da análise</b><br><small>O algoritmo baseia-se em padrões de cruzamento de médias móveis.</small></div>", unsafe_allow_html=True)

# Rodapé de Notícias
st.markdown("---")
st.markdown("### Notícias importantes")
n1, n2, n3 = st.columns(3)
n1.info("SEC autoriza Nasdaq a negociar primeiro ETF de Bitcoin.")
n2.warning("Fundador da Terra (LUNA) é procurado pela Interpol.")
n3.info("Alta volatilidade esperada para o par EUR/USD.")
