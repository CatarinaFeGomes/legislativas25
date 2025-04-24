import streamlit as st
from admin import menu_admin
from user import menu_utilizador


def main():
    st.title("🗳️ VotoMatch: Assistente de Decisão de Voto")

    if "menu" not in st.session_state:
        st.session_state.menu = "main"

    if st.session_state.menu == "main":
        opcao = st.segmented_control("Escolhe o modo:", ["Admin", "Utilizador"])
        if opcao == "Admin":
            st.session_state.menu = "admin"
            menu_admin()
        elif opcao == "Utilizador":
            st.session_state.menu = "utilizador"

    elif st.session_state.menu == "admin":
        menu_admin()
    elif st.session_state.menu == "utilizador":
        menu_utilizador()


if __name__ == "__main__":
    main()
