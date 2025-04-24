from storage import carregar_afirmacoes, guardar_afirmacoes
from storage import carregar_partidos, guardar_partidos
from utils import ver_afirmacoes
import streamlit as st


def menu_admin():
    st.subheader("🔧 Menu ADMIN")

    opcao = st.segmented_control(
        "Escolha uma opção:",
        ["Afirmações", "Partidos", "Sair"],
        key="menu_admin_radio"
    )

    if opcao == "Afirmações":
        menu_admin_afirmacoes()
    elif opcao == "Partidos":
        menu_admin_partidos()
    elif opcao == "Sair":
        st.session_state.menu = "main"
        st.rerun()  # Recarrega a página e volta ao menu principal


def menu_admin_afirmacoes():
    st.subheader("🔧 ADMIN >> Afirmações")

    opcao = st.segmented_control(
        "Escolha uma opção:",
        ["Ver afirmações", "Adicionar várias afirmações para um partido", "Editar afirmação", "Remover afirmação", "Sair"],
        key="admin_afirmacoes_radio"
    )

    if opcao == "Ver afirmações":
        ver_afirmacoes_opcao()
    elif opcao == "Adicionar várias afirmações para um partido":
        adicionar_varias_afirmacoes_opcao()
    elif opcao == "Editar afirmação":
        editar_afirmacao_opcao()
    elif opcao == "Remover afirmação":
        remover_afirmacao_opcao()
    elif opcao == "Sair":
        st.session_state.menu = "main"
        st.rerun()  # Recarrega a página e volta ao menu principal


def menu_admin_partidos():
    st.subheader("🔧 ADMIN >> Partidos")

    opcao = st.segmented_control(
        "Escolha uma opção:",
        ["Adicionar partidos", "Editar partidos", "Remover partidos", "Sair"],
        key="admin_partidos_radio"
    )

    if opcao == "Adicionar partidos":
        adicionar_partido()
    elif opcao == "Editar partidos":
        editar_partido()
    elif opcao == "Remover partidos":
        remover_partido()
    elif opcao == "Sair":
        st.session_state.menu = "main"
        st.rerun()  # Recarrega a página e volta ao menu principal


def ver_afirmacoes_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)


def adicionar_varias_afirmacoes_opcao():
    partido = st.text_input("Nome do partido:", key="novo_partido_afirmacoes")
    novas_afirmacoes_texto = st.text_area("Escreve as afirmações (1 por linha):", key="afirmacoes_textarea")

    if st.button("Adicionar afirmações"):
        linhas = [linha.strip() for linha in novas_afirmacoes_texto.split("\n") if linha.strip()]
        if partido and linhas:
            novas_afirmacoes = [{"texto": texto, "partido": partido} for texto in linhas]
            afirmacoes = carregar_afirmacoes()
            afirmacoes.extend(novas_afirmacoes)
            guardar_afirmacoes(afirmacoes)
            st.success(f"{len(novas_afirmacoes)} afirmações adicionadas com sucesso.")
        else:
            st.error("Preenche todos os campos corretamente.")


def editar_afirmacao_opcao():
    afirmacoes = carregar_afirmacoes()
    if not afirmacoes:
        st.info("Não existem afirmações.")
        return

    opcoes = [f"{i+1}. {a['texto']} ({a['partido']})" for i, a in enumerate(afirmacoes)]
    indice = st.selectbox("Seleciona a afirmação a editar:", options=list(range(len(opcoes))), format_func=lambda x: opcoes[x])

    nova_texto = st.text_input("Novo texto da afirmação:", value=afirmacoes[indice]["texto"])
    novo_partido = st.text_input("Novo nome do partido:", value=afirmacoes[indice]["partido"])

    if st.button("Guardar alterações"):
        afirmacoes[indice]["texto"] = nova_texto
        afirmacoes[indice]["partido"] = novo_partido
        guardar_afirmacoes(afirmacoes)
        st.success("Afirmação atualizada com sucesso.")


def remover_afirmacao_opcao():
    afirmacoes = carregar_afirmacoes()
    if not afirmacoes:
        st.info("Não existem afirmações.")
        return

    opcoes = [f"{i+1}. {a['texto']} ({a['partido']})" for i, a in enumerate(afirmacoes)]
    indice = st.selectbox("Seleciona a afirmação a remover:", options=list(range(len(opcoes))), format_func=lambda x: opcoes[x])

    if st.button("Remover afirmação"):
        afirmacoes.pop(indice)
        guardar_afirmacoes(afirmacoes)
        st.success("Afirmação removida com sucesso.")


def adicionar_partido():
    sigla = st.text_input("Sigla do novo partido (ex: BE):")
    nome = st.text_input("Nome completo do partido (ex: Bloco de Esquerda):")

    if st.button("Adicionar partido"):
        if not sigla or not nome:
            st.error("Sigla ou nome inválido.")
            return
        partidos = carregar_partidos()
        if any(p["sigla"].lower() == sigla.lower() for p in partidos):
            st.error("Já existe um partido com essa sigla.")
            return
        partidos.append({"sigla": sigla, "nome": nome})
        guardar_partidos(partidos)
        st.success("Partido adicionado com sucesso.")


def editar_partido():
    partidos = carregar_partidos()
    if not partidos:
        st.info("Não existem partidos.")
        return

    opcoes = [f"{p['sigla']} - {p['nome']}" for p in partidos]
    indice = st.selectbox("Seleciona o partido a editar:", options=list(range(len(partidos))), format_func=lambda x: opcoes[x])
    partido = partidos[indice]

    nova_sigla = st.text_input("Nova sigla:", value=partido["sigla"])
    novo_nome = st.text_input("Novo nome:", value=partido["nome"])

    if st.button("Guardar alterações"):
        if nova_sigla and any(p["sigla"].lower() == nova_sigla.lower() and p != partido for p in partidos):
            st.error("Essa sigla já está a ser usada por outro partido.")
            return

        partido["sigla"] = nova_sigla
        partido["nome"] = novo_nome
        guardar_partidos(partidos)
        st.success("Partido editado com sucesso.")


def remover_partido():
    partidos = carregar_partidos()
    if not partidos:
        st.info("Não existem partidos.")
        return

    opcoes = [f"{p['sigla']} - {p['nome']}" for p in partidos]
    indice = st.selectbox("Seleciona o partido a remover:", options=list(range(len(partidos))), format_func=lambda x: opcoes[x])
    partido = partidos[indice]

    if st.button(f"Remover '{partido['sigla']} - {partido['nome']}'"):
        partidos.pop(indice)
        guardar_partidos(partidos)
        st.success("Partido removido com sucesso.")
