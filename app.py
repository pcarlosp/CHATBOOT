import streamlit as st
from chat_engine import responder
from storage import carregar_conversas, salvar_mensagem

st.set_page_config(page_title="Chat Interno", layout="centered")

st.title("💬 Chat Interno da Equipe")

usuario = st.text_input("Seu nome:", key="usuario")
mensagem = st.text_input("Mensagem:", key="mensagem_input")

if st.button("Enviar"):
    if usuario and mensagem:
        resposta = responder(mensagem)
        salvar_mensagem(usuario, mensagem, resposta)
        st.success(f"Resposta: {resposta}")
    else:
        st.warning("Preencha seu nome e a mensagem.")

st.subheader("📜 Histórico de Conversas")
historico = carregar_conversas()
for msg in reversed(historico[-10:]):
    st.markdown(f"**{msg['hora']} - {msg['usuario']}:** {msg['mensagem']}")
    st.markdown(f"🧠 _Resposta:_ {msg['resposta']}")
    st.markdown("---")