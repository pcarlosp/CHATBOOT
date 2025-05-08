import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from datetime import datetime
import os
import json

# -------- CONFIGURAR USUÁRIOS --------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status is False:
    st.error("Usuário ou senha incorretos")
elif authentication_status is None:
    st.warning("Digite seu usuário e senha")
elif authentication_status:
    authenticator.logout("Sair", "sidebar")
    st.sidebar.success(f"Bem-vindo, {name}")

    # -------- SISTEMA DE CHAT --------
    st.title("Magnolia Group 🌸")
    if "sala" not in st.session_state:
        st.session_state.sala = "Geral"

    sala = st.selectbox("Escolha a sala", ["Geral", "Financeiro", "Projetos", "Social"], key="sala")
    mensagem = st.text_input("Digite sua mensagem")
    if st.button("Enviar"):
        if mensagem:
            nova = {
                "hora": datetime.now().strftime("%H:%M:%S"),
                "usuario": name,
                "sala": sala,
                "mensagem": mensagem
            }
            if not os.path.exists("mensagens.json"):
                with open("mensagens.json", "w") as f:
                    json.dump([], f)
            with open("mensagens.json", "r") as f:
                historico = json.load(f)
            historico.append(nova)
            with open("mensagens.json", "w") as f:
                json.dump(historico, f, indent=4)
            st.experimental_rerun()

    st.subheader(f"📜 Conversas em {sala}")
    if os.path.exists("mensagens.json"):
        with open("mensagens.json", "r") as f:
            mensagens = json.load(f)
        for msg in reversed(mensagens[-50:]):
            if msg["sala"] == sala:
                st.markdown(f"**{msg['hora']} - {msg['usuario']}**: {msg['mensagem']}")