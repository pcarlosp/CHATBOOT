
import streamlit as st
from datetime import datetime
import os
import json

# -------- SISTEMA DE CHAT MAGNOLIA --------
st.set_page_config(page_title="Magnolia Group 🌸", layout="centered")
st.title("Magnolia Group 🌸")

if "usuario" not in st.session_state or not st.session_state.usuario:
    nome = st.text_input("Digite seu nome para entrar no chat:")
    if nome:
        st.session_state.usuario = nome
        st.experimental_rerun()
    st.stop()

st.success(f"Bem-vindo, {st.session_state.usuario}!")

if "sala" not in st.session_state:
    st.session_state.sala = "Geral"

sala = st.selectbox("Escolha a sala", ["Geral", "Financeiro", "Projetos", "Social"], key="sala")

with st.form("mensagem_form", clear_on_submit=True):
    mensagem = st.text_input("Digite sua mensagem e pressione ENTER")
    submitted = st.form_submit_button("Enviar")
    if submitted and mensagem:
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
