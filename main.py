import streamlit as st
from admin import menu_admin
from user import menu_utilizador  # Importa apenas uma vez
def main():
    st.title("🗳️ VotoMatch: Assistente de Decisão de Voto")

    if "menu" not in st.session_state:
        st.session_state.menu = "main"
    if "nome_utilizador" not in st.session_state:
        st.session_state.nome_utilizador = ""

    if st.session_state.menu == "main":
        opcao = st.segmented_control("Escolhe o modo:", ["Admin", "Utilizador"])

        if opcao == "Admin":
            st.session_state.menu = "admin"

        elif opcao == "Utilizador":
            st.session_state.nome_utilizador = st.text_input("Nome do utilizador:").strip()
            if st.button("Entrar"):
                if st.session_state.nome_utilizador:
                    st.session_state.menu = "utilizador"
                else:
                    st.warning("Nome inválido.")

    elif st.session_state.menu == "admin":
        menu_admin()

    elif st.session_state.menu == "utilizador":
        menu_utilizador(st.session_state.nome_utilizador)


if __name__ == "__main__":
    main()
