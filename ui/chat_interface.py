import streamlit as st
from io import StringIO
import requests

st.title("💬 Chatbot com Rasa")

#Streamlit perde os dados do dialogo anterior.
# Por isso, estamos criando uma lista vazia dentro de session_state caso nao tenha ainda com o histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# Para cada mensagem dentro de histórico, mostre
#de quem veio e o conteúdo
for mensagem in st.session_state.historico:
    st.chat_message(mensagem["emissor"]).write(mensagem["conteudo"])

if msg_atual := st.chat_input("Digite sua mensagem..."):
    st.chat_message("usuario").write(msg_atual)
    st.session_state.historico.append({"emissor": "usuario", "conteudo": msg_atual})

response = requests.post(
    "http://localhost:5005/webhooks/rest/webhook",
    json={"sender": "usuario", "message": msg_atual}
)
bot_msg = ""
for r in response.json():
    bot_msg = r.get("text", "")

if bot_msg:
    st.chat_message("assistant").write(bot_msg)
    st.session_state.historico.append({"emissor": "assistant", "conteudo": bot_msg})

#upload de imagens
#uploaded_files = st.file_uploader("Envie uma imagem do seu exame", accept_multiple_files=True, type=["jpg", "jpeg", "png"])