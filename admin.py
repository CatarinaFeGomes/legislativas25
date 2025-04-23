import streamlit as st
from storage import carregar_afirmacoes, guardar_afirmacoes
from storage import carregar_partidos, guardar_partidos
from utils import ver_afirmacoes

def menu_admin():
    st.subheader("Menu ADMIN")
    opcao = st.selectbox("Escolhe uma opção:", ["Afirmações", "Partidos"])

    if opcao == "Afirmações":
        menu_admin_afirmacoes()
    elif opcao == "Partidos":
        menu_admin_partidos()

def menu_admin_afirmacoes():
    st.markdown("### ADMIN >> Afirmações")
    escolha = st.radio("Escolhe uma opção:", [
        "Ver afirmações",
        "Adicionar várias afirmações para um partido",
        "Editar afirmação",
        "Remover afirmação"
    ])

    if escolha == "Ver afirmações":
        ver_afirmacoes_opcao()
    elif escolha == "Adicionar várias afirmações para um partido":
        adicionar_varias_afirmacoes_opcao()
    elif escolha == "Editar afirmação":
        editar_afirmacao_opcao()
    elif escolha == "Remover afirmação":
        remover_afirmacao_opcao()

def menu_admin_partidos():
    st.markdown("### ADMIN >> Partidos")
    escolha = st.radio("Escolhe uma opção:", [
        "Adicionar partidos",
        "Editar partidos",
        "Remover partidos"
    ])

    if escolha == "Adicionar partidos":
        adicionar_partido()
    elif escolha == "Editar partidos":
        editar_partido()
    elif escolha == "Remover partidos":
        remover_partido()

def ver_afirmacoes_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)

def adicionar_varias_afirmacoes_opcao():
    partido = st.text_input("Nome do partido:")
    novas_afirmacoes = st.text_area("Escreve as afirmações (uma por linha):")
    if st.button("Adicionar Afirmações"):
        lista_afirmacoes = [{"texto": a.strip(), "partido": partido} for a in novas_afirmacoes.strip().split("\n") if a.strip()]
        if lista_afirmacoes:
            afirmacoes = carregar_afirmacoes()
            afirmacoes.extend(lista_afirmacoes)
            guardar_afirmacoes(afirmacoes)
            st.success(f"{len(lista_afirmacoes)} afirmações adicionadas com sucesso.")

def editar_afirmacao_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)
    opcoes = [f"{i+1}. {a['texto']} ({a['partido']})" for i, a in enumerate(afirmacoes)]
    escolha = st.selectbox("Seleciona uma afirmação para editar:", ["Cancelar"] + opcoes)

    if escolha != "Cancelar":
        indice = int(escolha.split(".")[0]) - 1
        nova_texto = st.text_input("Novo texto da afirmação:", value=afirmacoes[indice]["texto"])
        novo_partido = st.text_input("Novo nome do partido:", value=afirmacoes[indice]["partido"])
        if st.button("Guardar alterações"):
            afirmacoes[indice]["texto"] = nova_texto
            afirmacoes[indice]["partido"] = novo_partido
            guardar_afirmacoes(afirmacoes)
            st.success("Afirmação atualizada com sucesso.")

def remover_afirmacao_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)
    opcoes = [f"{i+1}. {a['texto']} ({a['partido']})" for i, a in enumerate(afirmacoes)]
    escolha = st.selectbox("Seleciona uma afirmação para remover:", ["Cancelar"] + opcoes)

    if escolha != "Cancelar":
        indice = int(escolha.split(".")[0]) - 1
        if st.button("Confirmar remoção"):
            afirmacoes.pop(indice)
            guardar_afirmacoes(afirmacoes)
            st.success("Afirmação removida com sucesso.")

def adicionar_partido():
    sigla = st.text_input("Sigla do novo partido (ex: BE):")
    nome = st.text_input("Nome completo do partido (ex: Bloco de Esquerda):")
    if st.button("Adicionar partido"):
        partidos = carregar_partidos()
        if not sigla or not nome:
            st.error("Sigla ou nome inválido.")
            return
        if any(p["sigla"].lower() == sigla.lower() for p in partidos):
            st.error("Já existe um partido com essa sigla.")
            return
        partidos.append({"sigla": sigla, "nome": nome})
        guardar_partidos(partidos)
        st.success("Partido adicionado com sucesso.")

def editar_partido():
    partidos = carregar_partidos()
    if not partidos:
        st.info("Não existem partidos registados.")
        return
    nomes = [f"{i+1}. {p['sigla']} - {p['nome']}" for i, p in enumerate(partidos)]
    escolha = st.selectbox("Seleciona um partido para editar:", ["Cancelar"] + nomes)

    if escolha != "Cancelar":
        indice = int(escolha.split(".")[0]) - 1
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
        st.info("Não existem partidos registados.")
        return
    nomes = [f"{i+1}. {p['sigla']} - {p['nome']}" for i, p in enumerate(partidos)]
    escolha = st.selectbox("Seleciona um partido para remover:", ["Cancelar"] + nomes)

    if escolha != "Cancelar":
        indice = int(escolha.split(".")[0]) - 1
        p = partidos[indice]
        if st.button(f"Confirmar remoção de '{p['sigla']} - {p['nome']}'"):
            partidos.pop(indice)
            guardar_partidos(partidos)
            st.success("Partido removido com sucesso.")