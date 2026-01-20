import streamlit as st
import pandas as pd

# COLE O LINK DO CSV DA PLANILHA AQUI
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/SUA_ID/pub?output=csv"

def verificar_acesso(email_digitado):
    try:
        # Lê a planilha sempre que alguém tenta logar
        df = pd.read_csv(URL_PLANILHA)
        # Verifica se o email digitado está na coluna 'E-mail'
        return email_digitado.strip().lower() in df['E-mail'].str.lower().values
    except Exception as e:
        return False

# --- INTERFACE ---
st.sidebar.title("🔐 Login do Assinante")
email_input = st.sidebar.text_input("Digite seu e-mail:")

if email_input:
    if verificar_acesso(email_input):
        st.sidebar.success("Acesso Liberado!")
        st.title("🤖 Robô de Sinais OTC")
        # Aqui entra o seu código de sinais que já criamos...
    else:
        st.sidebar.error("E-mail não encontrado.")
        st.error("Assinatura inativa ou e-mail incorreto.")
