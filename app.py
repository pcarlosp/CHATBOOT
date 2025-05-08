
import streamlit as st
from datetime import datetime
import os
import json

st.set_page_config(page_title="Magnolia Group 🌸", layout="centered")

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

st.markdown("<h1 style='color:#3366cc;'>Magnolia Group 🌸</h1>", unsafe_allow_html=True)

if not st.session_state.usuario:
    nome = st.text_input("Digite seu nome para entrar no chat e pressione ENTER")
    if nome.strip():
        st.session_state.usuario = nome.strip().upper()
    st.stop()

st.success(f"Bem-vindo, {st.session_state.usuario}!")

sala = "Geral"
st.markdown("### 📜 Conversas em Geral")

if os.path.exists("mensagens.json"):
    with open("mensagens.json", "r") as f:
        mensagens = json.load(f)
else:
    mensagens = []

# Exibir mensagens
for msg in reversed(mensagens[-100:]):
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
        if msg.get("imagem"):
            try:
                st.image(msg["imagem"], width=200)
            except:
                st.warning("❌ Imagem não encontrada.")

# Envio de mensagem com preview de imagem
with st.form("mensagem_form", clear_on_submit=True):
    mensagem = st.text_input("Digite sua mensagem e pressione ENTER")
    imagem = st.file_uploader("📎 Enviar imagem", type=["jpg", "jpeg", "png"])
    submit = st.form_submit_button("Enviar")

    if submit and (mensagem.strip() or imagem):
        nova_msg = {
            "usuario": st.session_state.usuario,
            "mensagem": mensagem.strip(),
            "sala": sala,
            "hora": datetime.now().strftime("%H:%M:%S"),
            "imagem": None
        }
        if imagem:
            if not os.path.exists("uploads"):
                os.makedirs("uploads")
            nome_arquivo = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagem.name}"
            with open(nome_arquivo, "wb") as f:
                f.write(imagem.read())
            nova_msg["imagem"] = nome_arquivo

        mensagens.append(nova_msg)
        with open("mensagens.json", "w") as f:
            json.dump(mensagens, f, indent=4)

# Botão para limpar sala
if st.button("🧹 Limpar mensagens desta sala"):
    mensagens = [m for m in mensagens if m["sala"] != sala]
    with open("mensagens.json", "w") as f:
        json.dump(mensagens, f, indent=4)
