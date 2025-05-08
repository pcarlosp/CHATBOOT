import streamlit as st
from datetime import datetime
import os
import json

# -------- SISTEMA DE CHAT MAGNOLIA --------
st.set_page_config(page_title="Magnolia Group 🌸", layout="centered")
st.title("Magnolia Group 🌸")

if "usuario" not in st.session_state:
    st.session_state.usuario = st.text_input("Digite seu nome para entrar no chat:")
    st.stop()

st.success(f"Bem-vindo, {st.session_state.usuario}!")

if "sala" not in st.session_state:
    st.session_state.sala = "Geral"

sala = st.selectbox("Escolha a sala", ["Geral", "Financeiro", "Projetos", "Social"], key="sala")
mensagem = st.text_input("Digite sua mensagem")
if st.button("Enviar"):
    if mensagem:
        nova = {
            "hora": datetime.now().strftime("%H:%M:%S"),
            "usuario": st.session_state.usuario,
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