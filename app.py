import streamlit as st
import pandas as pd

# Link do CSV da sua planilha (Publicar na Web)
URL_PLANILHA = "COLE_AQUI_SEU_LINK_TERMINADO_EM_CSV"

def verificar_acesso(email_digitado):
    try:
        # Lê a planilha e remove espaços em branco
        df = pd.read_csv(URL_PLANILHA)
        # Transforma tudo em minúsculo para comparar sem erros
        emails_vips = df['E-mail'].str.strip().str.lower().tolist()
        return email_digitado.strip().lower() in emails_vips
    except Exception as e:
        # Se der erro na leitura, mostra o motivo para facilitar o conserto
        st.sidebar.error(f"Erro de conexão com o banco: {e}")
        return False

# Interface
st.sidebar.title("🔐 Login do Assinante")
usuario = st.sidebar.text_input("Digite seu e-mail:")

if usuario:
    if verificar_acesso(usuario):
        st.success("✅ ACESSO LIBERADO!")
        st.title("🤖 Painel de Sinais IA - OTC")
        # Coloque o resto do código do seu robô aqui...
    else:
        st.error("❌ E-mail não encontrado na base de assinantes.")
