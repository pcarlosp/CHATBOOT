
import streamlit as st
from datetime import datetime
import os
import json

st.set_page_config(page_title="Magnolia Group 🌸", layout="centered")

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

st.title("Magnolia Group 🌸")

if not st.session_state.usuario:
    nome = st.text_input("Digite seu nome para entrar no chat:")
    if nome:
        st.session_state.usuario = nome
    st.stop()

st.success(f"Bem-vindo, {st.session_state.usuario}!")

salas = ["Geral", "Financeiro", "Projetos", "Social"]
sala = st.selectbox("Escolha a sala", salas)

# Carregar mensagens
if os.path.exists("mensagens.json"):
    with open("mensagens.json", "r") as f:
        mensagens = json.load(f)
else:
    mensagens = []

# Exibir mensagens corrigidas
st.subheader(f"📜 Conversas em {sala}")
for msg in reversed(mensagens[-50:]):
    if msg["sala"] == sala:
        alinhamento = "flex-end" if msg["usuario"] == st.session_state.usuario else "flex-start"
        cor = "#DCF8C6" if alinhamento == "flex-end" else "#FFFFFF"
        conteudo = msg['mensagem'].replace("<", "&lt;").replace(">", "&gt;")
        html = f'''
        <div style="display: flex; justify-content: {alinhamento}; margin-bottom: 10px;">
            <div style="
                background-color: {cor};
                border-radius: 10px;
                padding: 10px;
                max-width: 70%;
                box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
            ">
                <small><strong>{msg['usuario']} ({msg['hora']})</strong></small><br>
                {conteudo}
            </div>
        </div>
        '''
        st.markdown(html, unsafe_allow_html=True)

# Formulário para envio
with st.form("enviar", clear_on_submit=True):
    nova = st.text_input("Digite sua mensagem e pressione ENTER")
    enviar = st.form_submit_button("Enviar")
    if enviar and nova:
        nova_msg = {
            "usuario": st.session_state.usuario,
            "mensagem": nova,
            "sala": sala,
            "hora": datetime.now().strftime("%H:%M:%S")
        }
        mensagens.append(nova_msg)
        with open("mensagens.json", "w") as f:
            json.dump(mensagens, f, indent=4)
        st.experimental_rerun()

if st.button("🧹 Limpar mensagens desta sala"):
    mensagens = [m for m in mensagens if m["sala"] != sala]
    with open("mensagens.json", "w") as f:
        json.dump(mensagens, f, indent=4)
    st.experimental_rerun()
