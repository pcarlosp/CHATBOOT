import streamlit as st
from datetime import datetime
import json
import os

ARQUIVO_USUARIOS = "usuarios.json"
ARQUIVO_MENSAGENS = "mensagens.json"
REACTIONS = ["👍", "😂", "❤️", "🔥"]

# -------------------- Funções auxiliares --------------------

def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({"admin": "admin"}, f)
    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)

def salvar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return False
    usuarios[usuario] = senha
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)
    return True

def excluir_usuario(usuario):
    usuarios = carregar_usuarios()
    if usuario in usuarios and usuario != "admin":
        del usuarios[usuario]
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump(usuarios, f)

def carregar_mensagens():
    if not os.path.exists(ARQUIVO_MENSAGENS):
        with open(ARQUIVO_MENSAGENS, "w") as f:
            json.dump([], f)
    with open(ARQUIVO_MENSAGENS, "r") as f:
        return json.load(f)

def salvar_mensagem(remetente, destinatario, mensagem):
    mensagens = carregar_mensagens()
    mensagens.append({
        "hora": datetime.now().strftime("%H:%M:%S"),
        "remetente": remetente,
        "destinatario": destinatario,
        "mensagem": mensagem,
        "reacoes": []
    })
    with open(ARQUIVO_MENSAGENS, "w") as f:
        json.dump(mensagens, f, indent=4)

def adicionar_reacao(index, reacao):
    mensagens = carregar_mensagens()
    if index < len(mensagens):
        mensagens[index]["reacoes"].append(reacao)
        with open(ARQUIVO_MENSAGENS, "w") as f:
            json.dump(mensagens, f, indent=4)

# -------------------- Interface --------------------

if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

def tela_login():
    st.title("🔐 Login | Magnolia Group")
    aba = st.radio("Escolha:", ["Entrar", "Registrar novo usuário"])
    if aba == "Entrar":
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            usuarios = carregar_usuarios()
            if usuario in usuarios and usuarios[usuario] == senha:
                st.session_state.logado = True
                st.session_state.usuario = usuario
                st.success("Login realizado com sucesso!")
                st.experimental_rerun()
            else:
                st.error("Usuário ou senha inválidos.")
    else:
        novo_usuario = st.text_input("Novo usuário")
        nova_senha = st.text_input("Nova senha", type="password")
        if st.button("Registrar"):
            if salvar_usuario(novo_usuario, nova_senha):
                st.success("Usuário registrado com sucesso!")
            else:
                st.error("Usuário já existe.")

def tela_chat():
    st.title("Magnolia Group 💬 | Chat Interno")
    usuarios = [u for u in carregar_usuarios() if u != st.session_state.usuario]
    modo = st.radio("Modo de conversa:", ["Público (todos)", "Privado (1 pessoa)"])
    
    destinatario = "TODOS"
    if modo == "Privado (1 pessoa)":
        destinatario = st.selectbox("Escolha o usuário:", usuarios)

    col1, col2 = st.columns([4, 1])
    with col1:
        mensagem = st.text_input("Digite sua mensagem com emojis 😀🔥💬:")
    with col2:
        if st.button("Enviar"):
            if mensagem:
                salvar_mensagem(st.session_state.usuario, destinatario, mensagem)
                st.experimental_rerun()

    st.subheader(f"📨 Conversas {'Públicas' if destinatario == 'TODOS' else 'Privadas'}")
    mensagens = carregar_mensagens()
    for i, msg in enumerate(reversed(mensagens[-100:])):
        idx = len(mensagens) - 1 - i
        if msg["destinatario"] == "TODOS" or            (msg["remetente"] == st.session_state.usuario and msg["destinatario"] == destinatario) or            (msg["remetente"] == destinatario and msg["destinatario"] == st.session_state.usuario):

            with st.container():
                st.markdown(f"**🕒 {msg['hora']} - 👤 {msg['remetente']} ➜ {msg['destinatario']}**")
                st.markdown(f"> {msg['mensagem']}")
                if msg["reacoes"]:
                    st.markdown("Reações: " + " ".join(msg["reacoes"]))
                for r in REACTIONS:
                    if st.button(r, key=f"{r}_{idx}"):
                        adicionar_reacao(idx, r)
                        st.experimental_rerun()

    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.experimental_rerun()

def tela_admin():
    st.title("👑 Painel do Administrador | Magnolia Group")
    st.subheader("Usuários Registrados")
    usuarios = carregar_usuarios()
    for user in usuarios:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"👤 {user}")
        with col2:
            if user != "admin":
                if st.button("Excluir", key=f"del_{user}"):
                    excluir_usuario(user)
                    st.experimental_rerun()
    if st.button("🚪 Sair"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.experimental_rerun()

# -------------------- Main --------------------

if st.session_state.logado:
    if st.session_state.usuario == "admin":
        tela_admin()
    else:
        tela_chat()
else:
    tela_login()