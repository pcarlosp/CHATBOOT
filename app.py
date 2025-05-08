
import streamlit as st
from datetime import datetime
import os
import json
import openai

st.set_page_config(page_title="Magnolia Group 🌸", layout="centered")

# Chave da OpenAI (adicione sua chave aqui para testar localmente)
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")

def resposta_ia(pergunta):
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é o assistente do grupo Magnolia."},
                {"role": "user", "content": pergunta}
            ]
        )
        return resposta["choices"][0]["message"]["content"]
    except Exception as e:
        return f"(Erro com IA: {e})"

# Interface
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

sala = st.selectbox("Escolha a sala", ["Geral", "Financeiro", "Projetos", "Social", "🤖 Assistente IA"], key="sala")

with st.form("mensagem_form", clear_on_submit=True):
    mensagem = st.text_input("Digite sua mensagem e pressione ENTER")
    imagem = st.file_uploader("📷 Enviar imagem", type=["jpg", "jpeg", "png"])
    submitted = st.form_submit_button("Enviar")

    if submitted and (mensagem or imagem):
        nova = {
            "hora": datetime.now().strftime("%H:%M:%S"),
            "usuario": st.session_state.usuario,
            "sala": sala,
            "mensagem": mensagem,
            "imagem": None
        }

        if imagem:
            nome_arquivo = f"uploads/{datetime.now().strftime('%Y%m%d%H%M%S')}_{imagem.name}"
            with open(nome_arquivo, "wb") as f:
                f.write(imagem.read())
            nova["imagem"] = nome_arquivo

        if not os.path.exists("mensagens.json"):
            with open("mensagens.json", "w") as f:
                json.dump([], f)

        with open("mensagens.json", "r") as f:
            historico = json.load(f)
        historico.append(nova)

        # Se for sala de IA
        if sala == "🤖 Assistente IA" and mensagem:
            resposta = {
                "hora": datetime.now().strftime("%H:%M:%S"),
                "usuario": "🤖 IA",
                "sala": sala,
                "mensagem": resposta_ia(mensagem),
                "imagem": None
            }
            historico.append(resposta)

        with open("mensagens.json", "w") as f:
            json.dump(historico, f, indent=4)

st.subheader(f"📜 Conversas em {sala}")
if st.button("🧹 Limpar mensagens desta sala"):
    if os.path.exists("mensagens.json"):
        with open("mensagens.json", "r") as f:
            mensagens = json.load(f)
        mensagens = [m for m in mensagens if m["sala"] != sala]
        with open("mensagens.json", "w") as f:
            json.dump(mensagens, f, indent=4)
    st.experimental_rerun()

if os.path.exists("mensagens.json"):
    with open("mensagens.json", "r") as f:
        mensagens = json.load(f)

    for msg in reversed(mensagens[-100:]):
        if msg["sala"] == sala:
            cor = "#DCF8C6" if msg["usuario"] == st.session_state.usuario else "#FFFFFF"
            alinhamento = "flex-end" if msg["usuario"] == st.session_state.usuario else "flex-start"
            st.markdown(f'''
            <div style="display: flex; justify-content: {alinhamento}; margin-bottom: 10px;">
                <div style="
                    background-color: {cor};
                    border-radius: 10px;
                    padding: 10px;
                    max-width: 70%;
                    box-shadow: 1px 1px 5px rgba(0,0,0,0.1);
                ">
                    <small><strong>{msg['usuario']} ({msg['hora']})</strong></small><br>
                    {msg['mensagem']}
                    {f'<br><img src="{msg["imagem"]}" width="200">' if msg.get("imagem") else ""}
                </div>
            </div>
            ''', unsafe_allow_html=True)
