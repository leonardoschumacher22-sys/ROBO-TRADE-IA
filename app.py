import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="IA TRADE PRO - SINAIS", page_icon="📈", layout="wide")

# Estilização Profissional (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .signal-card { 
        padding: 20px; border-radius: 10px; 
        background-color: #1e2130; border: 2px solid #00ff00;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (LOGIN) ---
st.sidebar.title("💎 ÁREA VIP")
email_usuario = st.sidebar.text_input("E-mail do Assinante")
# Adicione seu e-mail na lista abaixo para testar
ASSINANTES = ["seuemail@gmail.com", "leonardo@email.com"]

if email_usuario in ASSINANTES:
    st.sidebar.success("Assinatura Ativa!")
    
    # --- CONTEÚDO DO DASHBOARD ---
    st.title("🤖 Algoritmo de IA - Sinais OTC")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Gráfico de Tendência IA")
        # Gráfico corrigido usando numpy (np)
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Força', 'Volume', 'IA'])
        st.line_chart(chart_data)

    with col2:
        st.subheader("🚨 Sinal em Tempo Real")
        placeholder = st.empty()
        
        # Simulação de Sinais
        while True:
            with placeholder.container():
                st.markdown(f"""
                <div class="signal-card">
                    <h3 style='color: #00ff00;'>PAR: EUR/USD OTC</h3>
                    <h1 style='color: #00ff00;'>COMPRA (CALL) 🟢</h1>
                    <p>Confiança da IA: {random.randint(90, 98)}%</p>
                    <p>Expiração: 1 Minuto</p>
                </div>
                """, unsafe_allow_html=True)
                st.warning("⚠️ Aguarde o fechamento da vela para entrar.")
            time.sleep(60)

else:
    st.title("🔒 Acesso Restrito")
    st.error("Por favor, faça login com um e-mail autorizado para ver os sinais.")
    st.info("Ainda não é assinante? Adquira seu acesso mensal abaixo.")
    st.link_button("ASSINAR AGORA", "https://sua-pagina-de-vendas.com")
