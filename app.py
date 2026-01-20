import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import time

# ================= CONFIG =================
st.set_page_config(
    page_title="IT • MODO PRO AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================= SESSION MEMORY =================
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "weight_rsi" not in st.session_state:
    st.session_state.weight_rsi = 1.0
if "weight_macd" not in st.session_state:
    st.session_state.weight_macd = 1.0

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
</style>
""", unsafe_allow_html=True)

# ================= HEADER =================
h1, h2, h3 = st.columns([1, 3, 2])
with h1:
    st.markdown("## 🟢 **IT**")
with h2:
    ativo = st.selectbox("", ["EURUSD=X", "GBPUSD=X", "BTC-USD"], label_visibility="collapsed")
with h3:
    total = st.session_state.wins + st.session_state.losses
    acc = (st.session_state.wins / total * 100) if total > 0 else 0
    st.markdown(f"<p style='text-align:right;color:#9ca3af'>Assertividade: {acc:.1f}%</p>", unsafe_allow_html=True)

# ================= DATA =================
@st.cache_data(ttl=3)
def load_data(ticker):
    df = yf.download(ticker, period="1d", interval="1m", progress=False)
    if df is None or df.empty:
        return None

    df["EMA10"] = df["Close"].ewm(span=10).mean()
    df["EMA20"] = df["Close"].ewm(span=20).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = -delta.clip(upper=0).rolling(14).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12).mean()
    ema26 = df["Close"].ewm(span=26).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_SIGNAL"] = df["MACD"].ewm(span=9).mean()

    return df.dropna()

df = load_data(ativo)
if df is None:
    st.stop()

# ================= SAFE VALUES =================
last_price = float(df["Close"].iloc[-1])
ema10 = float(df["EMA10"].iloc[-1])
ema20 = float(df["EMA20"].iloc[-1])
rsi = float(df["RSI"].iloc[-1])
macd = float(df["MACD"].iloc[-1])
macd_signal = float(df["MACD_SIGNAL"].iloc[-1])

# ================= AI ENGINE =================
score = 0

if ema10 > ema20:
    score += 2
else:
    score -= 2

if rsi < 30:
    score += 1 * st.session_state.weight_rsi
elif rsi > 70:
    score -= 1 * st.session_state.weight_rsi

if macd > macd_signal:
    score += 1.5 * st.session_state.weight_macd
else:
    score -= 1.5 * st.session_state.weight_macd

confidence = min(max(int(50 + score * 10), 51), 95)

signal = "COMPRA" if score > 0 else "VENDA"
prob_up = confidence if signal == "COMPRA" else 100 - confidence
prob_down = 100 - prob_up

# ================= LAYOUT =================
left, right = st.columns([2.2, 1])

# ================= CHART =================
with left:
    fig = go.Figure()
    fig.add_candlestick(
        x=df.index, open=df["Open"], high=df["High"],
        low=df["Low"], close=df["Close"]
    )
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA10"], line=dict(color="#22c55e")))
    fig.add_trace(go.Scatter(x=df.index, y=df["EMA20"], line=dict(color="#38bdf8")))
    fig.update_layout(template="plotly_dark", height=420, xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

# ================= AI PANEL =================
with right:
    st.markdown("### 🤖 Análise com I.A.")

    a, b = st.columns(2)
    a.markdown(f"<div class='badge-green'>{prob_up}%<br>Cima</div>", unsafe_allow_html=True)
    b.markdown(f"<div class='badge-red'>{prob_down}%<br>Baixo</div>", unsafe_allow_html=True)

    if st.button("ANALISAR ENTRADA AGORA"):
        st.success(f"SINAL: **{signal}** | Confiança: {confidence}%")

    st.markdown(f"""
    <div class="card">
    EMA10/20 | RSI | MACD<br>
    RSI: {rsi:.1f}<br>
    Score: {score:.2f}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Resultado do sinal")
    c1, c2 = st.columns(2)
    if c1.button("✅ WIN"):
        st.session_state.wins += 1
        st.session_state.weight_rsi += 0.05
        st.session_state.weight_macd += 0.05
        st.rerun()
    if c2.button("❌ LOSS"):
        st.session_state.losses += 1
        st.session_state.weight_rsi = max(0.5, st.session_state.weight_rsi - 0.05)
        st.session_state.weight_macd = max(0.5, st.session_state.weight_macd - 0.05)
        st.rerun()
