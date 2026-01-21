import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração Visual Estilo "Modo Pro"
st.set_page_config(page_title="IA PRO MONITOR", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #06090f; color: #ffffff; }
    .signal-card { 
        padding: 40px; border-radius: 20px; text-align: center;
        border: 2px solid #00ffcc; background: rgba(0, 255, 204, 0.1);
        box-shadow: 0 0 20px #00ffcc;
    }
    .call { color: #00ffcc; font-size: 60px; }
    .put { color: #ff4b4b; font-size: 60px; }
    </style>
    """, unsafe_allow_html=True)

# URL da sua Planilha Google (Publicada como CSV)
# Você substituirá este link pelo seu após publicar a planilha
SHEET_URL = "SUA_URL_DO_GOOGLE_SHEETS_AQUI/export?format=csv"

st.title("⚡ IA PREDICTOR - ESPELHAMENTO REAL-TIME")

try:
    df = pd.read_csv(SHEET_URL)
    ultimo_sinal = df.iloc[-1] # Pega a última linha escrita pela IA
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        cor_classe = "call" if "CALL" in ultimo_sinal['Sinal'] else "put"
        st.markdown(f'''
            <div class="signal-card">
                <p style="font-size: 20px;">SINAL ATUAL</p>
                <h1 class="{cor_classe}">{ultimo_sinal['Sinal']}</h1>
                <p>Ativo: {ultimo_sinal['Ativo']}</p>
            </div>
        ''', unsafe_allow_html=True)
        
    with col2:
        st.metric("ASSERTIVIDADE", f"{ultimo_sinal['Confiança']}%")
        st.write(f"Última atualização: {ultimo_sinal['Hora']}")

except:
    st.warning("Aguardando o primeiro sinal ser enviado do navegador...")

st.empty()
import time
time.sleep(2)
st.rerun()
