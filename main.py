import streamlit as st
from admin import menu_admin
from user import menu_utilizador

st.set_page_config(page_title="VotoMatch", page_icon="🗳️")

st.title("🗳️ VotoMatch: Assistente de Decisão de Voto")

# Estado da página
if "modo" not in st.session_state:
    st.session_state.modo = None

modo = st.radio(
    "Escolhe o modo:",
    ("Admin (gerir afirmações)", "Utilizador (responder)", "Sair")
)

if modo == "Admin (gerir afirmações)":
    menu_admin()

elif modo == "Utilizador (responder)":
    menu_utilizador()

elif modo == "Sair":
    st.info("A aplicação foi terminada. Obrigado por usar o VotoMatch!")
