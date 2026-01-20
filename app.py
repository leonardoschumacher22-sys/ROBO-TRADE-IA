import streamlit as st

# --- TESTE MANUAL (SEM PLANILHA) ---
def verificar_acesso(email_digitado):
    # Coloque o seu e-mail exatamente aqui dentro da lista
    lista_teste = ["leonardo.schumacher22@gmail.com"]
    
    email_limpo = email_digitado.strip().lower()
    return email_limpo in lista_teste

# --- INTERFACE ---
st.sidebar.title("🔐 Teste de Acesso")
usuario = st.sidebar.text_input("Digite seu e-mail para testar:")

if usuario:
    if verificar_acesso(usuario):
        st.sidebar.success("✅ ACESSO LIBERADO!")
        st.title("🤖 Robô de Sinais IA - EM FUNCIONAMENTO")
        
        # Aqui você coloca o resto do seu código (Gráficos e Sinais)
        st.info("📊 SINAL ATUAL: EUR/USD OTC | COMPRA 🟢")
    else:
        st.sidebar.error("E-mail não autorizado no teste.")
