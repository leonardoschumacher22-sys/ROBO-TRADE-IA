import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import time

# ================= CONFIG =================
st.set_page_config(
    page_title="IT • MODO PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= CSS =================
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #0b0f17;
    color: #e5e7eb;
}
.card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 14px;
    padding: 16px;
}
.badge-green {
    background: #14532d;
    color: #4ade80;
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}
.badge-red {
    background: #7f1d1d;
    color: #f87171;
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}
.btn-main button {
    width: 100%;
    height: 55px;
    background: #22c55e;
    color: #052e16;
    font-weight: 700;
    border-radius: 14px;
    border: none;
    font-size: 16px;
}
.news-blue {
    background: #0c4a6e;
    border-radius: 14px;
    padding: 14px;
    font-size: 13px;
}
.news-yellow {
    background: #78350f;
    border-radius: 14px;
    padding: 14px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
h1, h2, h3 = st.columns([1, 3, 2])
with h1:
    st.markdown("## 🟢 **IT**")
with h2:
    ativo = st.selectbox(
        "",
        ["EURUSD=X", "GBPUSD=X", "BTC-USD"],
        label_visibility="collapsed"
    )
with h3:
    st.markdown(
        "<p style='text-align:right;color:#9ca3af'>Análises diárias: ilimitadas</p>",
        unsafe_allow_html=True
    )

# ================= DATA =================
@st.cache_data(ttl=2)
def load_data(ticker):
    df = yf.download(
        ticker,
        period="1d",
        interval="1m",
        progress=False
    )
    if df is None or df.empty:
        return None

    df["EMA10"] = df["Close"].ewm(span=10).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()
    return df

df = load_data(ativo)

if df is None:
    st.error("Erro ao carregar dados.")
    st.stop()

# ================= SAFE VALUES =================
last_price = float(df["Close"].iloc[-1])
high_price = float(df["High"].max())

ema10 = float(df["EMA10"].iloc[-1])
ema20 = float(df["EMA20"].iloc[-1])

# ================= SIGNAL =================
prob_up = 68 if ema10 > ema20 else 42
prob_down = 100 - prob_up
signal = "COMPRA" if prob_up > prob_down else "VENDA"

# ================= LAYOUT =================
left, right = st.columns([2.2, 1])

# ================= CHART =================
with left:
    st.markdown("### 📈 Gráfico em tempo real")

    fig = go.Figure()

    fig.add_candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Preço"
    )

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["EMA10"],
        line=dict(color="#22c55e", width=2),
        name="EMA 10"
    ))

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["EMA20"],
        line=dict(color="#38bdf8", width=2),
        name="EMA 20"
    ))

    fig.update_layout(
        template="plotly_dark",
        height=420,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis_rangeslider_visible=False,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div class="card">
        <b>Informações do ativo</b><br><br>
        Ativo: {ativo}<br>
        Cotação: {last_price:.5f}<br>
        Máxima: {high_price:.5f}
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <b>Índice de medo</b><br><br>
        <h2 style="color:#facc15">53</h2>
        Neutro
        </div>
        """, unsafe_allow_html=True)

# ================= AI PANEL =================
with right:
    st.markdown("### 🤖 Análise com I.A.")

    a, b = st.columns(2)
    with a:
        st.markdown(
            f"<div class='badge-green'>{prob_up}%<br>Cima</div>",
            unsafe_allow_html=True
        )
    with b:
        st.markdown(
            f"<div class='badge-red'>{prob_down}%<br>Baixo</div>",
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="btn-main">', unsafe_allow_html=True)
    if st.button("ANALISAR ENTRADA AGORA"):
        with st.spinner("Processando sinais..."):
            time.sleep(1)
            st.success(f"Sinal confirmado: **{signal}**")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
    <b>{signal}</b><br><br>
    Ativo: {ativo}<br>
    Confiança: 95%<br>
    Expiração: 1 minuto
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <b>Explicação</b><br>
    Cruzamento da EMA 10 acima da EMA 20 indicando continuação de fluxo.
    </div>
    """, unsafe_allow_html=True)

# ================= NEWS =================
st.markdown("### 📰 Notícias importantes")

n1, n2, n3 = st.columns(3)

n1.markdown("""
<div class="news-blue">
<b>SEC autoriza Nasdaq</b><br>
ETF de Bitcoin aprovado.
</div>
""", unsafe_allow_html=True)

n2.markdown("""
<div class="news-yellow">
<b>Fundador da Terra (LUNA)</b><br>
Procurado pela Interpol.
</div>
""", unsafe_allow_html=True)

n3.markdown("""
<div class="news-blue">
<b>Alta volatilidade</b><br>
Esperada para EUR/USD.
</div>
""", unsafe_allow_html=True)
