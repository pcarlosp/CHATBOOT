import streamlit as st
from datetime import datetime

# Usuários cadastrados (pode ser adaptado)
USUARIOS = {
    "pablo": "1234",
    "admin": "admin",
    "equipe": "senha"
}

# Inicialização de sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "conversas" not in st.session_state:
    st.session_state.conversas = []

def login():
    st.title("🔐 Login do Chat Interno")
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if usuario in USUARIOS and USUARIOS[usuario] == senha:
            st.session_state.logado = True
            st.session_state.usuario = usuario
            st.success("Login realizado com sucesso!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha inválidos.")

def chat():
    st.title("💬 Chat Privado Interno")
    st.markdown(f"Bem-vindo, **{st.session_state.usuario}**!")

    destinatario = st.selectbox("Enviar para:", [u for u in USUARIOS if u != st.session_state.usuario])
    mensagem = st.text_input("Mensagem:", key="mensagem_input")

    if st.button("Enviar"):
        if mensagem:
            st.session_state.conversas.append({
                "hora": datetime.now().strftime("%H:%M"),
                "remetente": st.session_state.usuario,
                "destinatario": destinatario,
                "mensagem": mensagem
            })
            st.success("Mensagem enviada.")

    st.subheader("📨 Conversa com " + destinatario)
    for msg in st.session_state.conversas:
        if (msg["remetente"] == st.session_state.usuario and msg["destinatario"] == destinatario) or            (msg["remetente"] == destinatario and msg["destinatario"] == st.session_state.usuario):
            st.markdown(f"**{msg['hora']} - {msg['remetente']}**: {msg['mensagem']}")

    if st.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.experimental_rerun()

if st.session_state.logado:
    chat()
else:
    login()