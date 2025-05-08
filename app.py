import streamlit as st
from datetime import datetime
import json
import os

ARQUIVO_USUARIOS = "usuarios.json"

# Função para carregar usuários
def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, "w") as f:
            json.dump({"admin": "admin"}, f)
    with open(ARQUIVO_USUARIOS, "r") as f:
        return json.load(f)

# Função para salvar novo usuário
def salvar_usuario(usuario, senha):
    usuarios = carregar_usuarios()
    if usuario in usuarios:
        return False
    usuarios[usuario] = senha
    with open(ARQUIVO_USUARIOS, "w") as f:
        json.dump(usuarios, f)
    return True

# Inicializar sessão
if "logado" not in st.session_state:
    st.session_state.logado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "conversas" not in st.session_state:
    st.session_state.conversas = []

def tela_login():
    st.title("🔐 Login")
    menu = st.radio("Opções", ["Entrar", "Registrar novo usuário"])
    if menu == "Entrar":
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
    st.title("💬 Chat Privado")
    usuarios = [u for u in carregar_usuarios() if u != st.session_state.usuario]
    destinatario = st.selectbox("Enviar para:", usuarios)
    mensagem = st.text_input("Mensagem:")
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

def tela_admin():
    st.title("🔧 Painel do Administrador")
    st.subheader("Usuários Registrados")
    usuarios = carregar_usuarios()
    for user in usuarios:
        st.markdown(f"👤 **{user}**")

    if st.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = ""
        st.experimental_rerun()

# Interface principal
if st.session_state.logado:
    if st.session_state.usuario == "admin":
        tela_admin()
    else:
        tela_chat()
else:
    tela_login()