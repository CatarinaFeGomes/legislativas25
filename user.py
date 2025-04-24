import os
import streamlit as st
import random
import json
from datetime import datetime
import matplotlib.pyplot as plt
from utils import guardar_resultado_utilizador
from storage import carregar_afirmacoes, carregar_partidos, carregar_debates


# Função para mostrar o menu do utilizador
def menu_utilizador(nome_utilizador):
    st.title("Modo Utilizador")
    st.write(f"Bem-vindo, **{nome_utilizador}**!")

    opcao = st.segmented_control("Escolha uma das opções",
                                 ["Responder ao questionário", "Histórico", "Partidos", "Sair"])

    if opcao == "Responder ao questionário":
        responder_questionario(nome_utilizador)
    elif opcao == "Histórico":
        menu_utilizador_historico(nome_utilizador)
    elif opcao == "Partidos":
        menu_utilizador_partidos()
    elif opcao == "Sair":
        st.session_state.menu = "main"


# Função para mostrar o menu do histórico
def menu_utilizador_historico(nome_utilizador):
    st.subheader(f"Histórico de {nome_utilizador}")

    opcao = st.segmented_control("Escolha uma das opções",
                                 ["Ver evolução dos vencedores ao longo do tempo", "Ver pódio total", "Sair"])

    if opcao == "Ver evolução dos vencedores ao longo do tempo":
        ver_historico_utilizador(nome_utilizador)
    elif opcao == "Ver pódio total":
        st.warning("Em desenvolvimento...")
    elif opcao == "Sair":
        st.session_state.menu = "utilizador"
        st.rerun()


# Função para o menu de partidos no modo utilizador
def menu_utilizador_partidos():
    st.subheader("Partidos")

    opcao = st.segmented_control("Escolha uma das opções", [
        "Ver siglas e nomes dos partidos",
        "Ver dados do partido",
        "Ver debates",
        "Procurar debate por partido",
        "Sair"
    ])

    if opcao == "Ver siglas e nomes dos partidos":
        mostrar_partidos_e_letras()
    elif opcao == "Ver dados do partido":
        dados_do_partido()
    elif opcao == "Ver debates":
        ver_debates()
    elif opcao == "Procurar debate por partido":
        sigla = st.text_input("Insere a sigla do partido a procurar nos debates (ex: PS)").strip().upper()
        if sigla:
            pesquisar_debates_por_partido(sigla)
    elif opcao == "Sair":
        st.session_state.menu = "utilizador"
        st.rerun()


import streamlit as st
import random
from datetime import datetime


def responder_questionario(nome_utilizador):
    """Questionário com navegação passo a passo em Streamlit."""

    st.subheader("Respostas ao Questionário")
    todas_afirmacoes = carregar_afirmacoes()

    if not todas_afirmacoes:
        st.warning("Nenhuma afirmação encontrada. Adiciona algumas no modo admin.")
        return

    # Obter partidos únicos
    partidos = list(set(af["partido"] for af in todas_afirmacoes))
    num_partidos = len(partidos)

    if num_partidos < 2:
        st.warning("É necessário pelo menos 2 partidos diferentes.")
        return

    # Agrupar afirmações por partido
    afirmacoes_por_partido = {partido: [] for partido in partidos}
    for af in todas_afirmacoes:
        afirmacoes_por_partido[af["partido"]].append(af)

    min_afirmacoes = min(len(afirmacoes_por_partido[p]) for p in partidos)
    max_total = min_afirmacoes * num_partidos
    min_total = 2 * num_partidos

    # Inicializar sessão
    if "iniciado" not in st.session_state:
        st.session_state.iniciado = False
        st.session_state.afirmacoes = []
        st.session_state.respostas = []
        st.session_state.pagina = 0
        st.session_state.total_afirmacoes = 0
        st.session_state.mostrar_resultados = False

    # Escolha de número de afirmações
    if not st.session_state.iniciado:
        total_afirmacoes = st.number_input(
            "Número de afirmações:",
            min_value=min_total,
            max_value=max_total,
            step=num_partidos
        )

        if total_afirmacoes:
            st.session_state.total_afirmacoes = total_afirmacoes
            if st.button("Iniciar Questionário"):
                num_por_partido = total_afirmacoes // num_partidos
                afirmacoes_selecionadas = []

                for partido in partidos:
                    random.shuffle(afirmacoes_por_partido[partido])
                    afirmacoes_selecionadas.extend(afirmacoes_por_partido[partido][:num_por_partido])

                random.shuffle(afirmacoes_selecionadas)

                st.session_state.afirmacoes = afirmacoes_selecionadas
                st.session_state.respostas = [None] * len(afirmacoes_selecionadas)
                st.session_state.iniciado = True
                st.session_state.pagina = 0

    if st.session_state.iniciado and not st.session_state.mostrar_resultados:
        af = st.session_state.afirmacoes[st.session_state.pagina]
        opcoes = [
            "1. Concordo totalmente",
            "2. Concordo",
            "3. Neutro",
            "4. Discordo",
            "5. Discordo totalmente"
        ]

        st.markdown(f"**{st.session_state.pagina + 1}/{len(st.session_state.afirmacoes)}** - {af['texto']}")
        resposta = st.radio(
            "Seleciona a tua resposta:",
            opcoes,
            index=opcoes.index(st.session_state.respostas[st.session_state.pagina]) if st.session_state.respostas[
                st.session_state.pagina] else 2,
            key=f"radio_{st.session_state.pagina}"
        )
        st.session_state.respostas[st.session_state.pagina] = resposta

        col1, col2, col3 = st.columns(3)

        if col1.button("⬅️ Anterior") and st.session_state.pagina > 0:
            st.session_state.pagina -= 1

        if col2.button("➡️ Seguinte") and st.session_state.pagina < len(st.session_state.afirmacoes) - 1:
            st.session_state.pagina += 1

        if st.session_state.pagina == len(st.session_state.afirmacoes) - 1:
            if col3.button("📊 Ver Resultados"):
                st.session_state.mostrar_resultados = True

    if st.session_state.mostrar_resultados:
        pontuacoes = {partido: 0 for partido in partidos}
        respostas_por_valor = {str(i): 0 for i in range(1, 6)}
        valores = {
            "1. Concordo totalmente": 2,
            "2. Concordo": 1,
            "3. Neutro": 0,
            "4. Discordo": -1,
            "5. Discordo totalmente": -2
        }

        for i, af in enumerate(st.session_state.afirmacoes):
            resposta = st.session_state.respostas[i]
            valor = valores[resposta]
            pontuacoes[af["partido"]] += valor
            respostas_por_valor[resposta[0]] += 1

        st.markdown("---")
        st.markdown("### 📊 RESULTADOS")
        ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
        for posicao, (partido, score) in enumerate(ranking, start=1):
            st.write(f"{posicao}º - {partido}: {score} pontos")

        guardar_resultado_utilizador(
            nome_utilizador,
            pontuacoes,
            respostas_por_valor,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        mostrar_grafico_resultado_partidos(pontuacoes)

        if st.radio("Queres ver o histórico deste utilizador?", ["Não", "Sim"], key="ver_historico_resultado") == "Sim":
            from historico import ver_historico_utilizador
            ver_historico_utilizador(nome_utilizador)


def mostrar_grafico_resultado_partidos(pontuacoes):
    """Mostra gráfico das pontuações por partido com Streamlit."""
    partidos = list(pontuacoes.keys())
    valores = list(pontuacoes.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(partidos, valores, color='lightgreen')
    ax.set_title("Pontuação final por partido")
    ax.set_ylabel("Pontuação")
    plt.xticks(rotation=15)
    plt.tight_layout()

    st.pyplot(fig)


def ver_historico_utilizador(nome):
    """Função para mostrar o histórico do utilizador."""
    ficheiro = os.path.join("historico", f"{nome}.json")
    if not os.path.exists(ficheiro):
        print("Não há histórico para este utilizador.")
        return

    with open(ficheiro, "r", encoding="utf-8") as f:
        historico = json.load(f)

    if not historico:
        print("Histórico vazio.")
        return

    partidos = list(historico[0]["pontuacoes"].keys())
    datas = [reg["data"] for reg in historico]  # data com hora
    for partido in partidos:
        valores = [reg["pontuacoes"].get(partido, 0) for reg in historico]
        plt.plot(datas, valores, marker="o", label=partido)

    plt.title(f"Evolução das pontuações - {nome}")
    plt.xlabel("Data e hora")
    plt.ylabel("Pontuação")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def mostrar_partidos_e_letras():
    """Função para mostrar as letras (siglas) e os partidos associados (nome completo)."""
    todas_afirmacoes = carregar_afirmacoes()
    if not todas_afirmacoes:
        print("Nenhuma afirmação encontrada. Adiciona algumas no modo admin.")
        return

    siglas_usadas = set(af["partido"] for af in todas_afirmacoes)
    partidos_registados = carregar_partidos()

    # Criar um dicionário sigla → nome
    mapa_sigla_para_nome = {p["sigla"]: p["nome"] for p in partidos_registados}

    print("\n--- Partidos e Letras Associadas ---")
    for sigla in sorted(siglas_usadas):
        nome = mapa_sigla_para_nome.get(sigla, "(nome desconhecido)")
        print(f"{sigla} - {nome}")


def dados_do_partido():
    partidos = carregar_partidos()
    if not partidos:
        print("Não existem partidos registados.")
        return

    print("\n--- Lista de Partidos ---")
    for i, partido in enumerate(partidos, start=1):
        print(f"{i}. {partido['sigla']} - {partido['nome']}")

    try:
        escolha = int(input("\nEscolhe o número do partido (0 para cancelar): "))
        if escolha == 0:
            return
        if 1 <= escolha <= len(partidos):
            p = partidos[escolha - 1]
            print("\n--- Dados do Partido ---")
            print(f"Sigla: {p['sigla']}")
            print(f"Nome: {p['nome']}")
            print(f"Ideologia Política: {p['ideologia']}")
            print(f"Económicamente: {p['economia']}")
            print(f"Socialmente: {p['sociedade']}")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")


def ver_debates():
    debates = carregar_debates()
    if not debates:
        print("Não existem debates registados.")
        return

    print("\n--- Lista de Debates ---")
    for debate in debates:
        numero = debate.get("Número", "?")
        partido1 = debate.get("Partido1", "?")
        partido2 = debate.get("Partido2", "?")
        print(f"{numero}. {partido1} vs {partido2}")


def pesquisar_debates_por_partido(sigla):
    """Mostra todos os debates onde a sigla do partido aparece como Partido1 ou Partido2."""
    sigla = sigla.strip().upper()
    debates = carregar_debates()
    if not debates:
        print("Não existem debates registados.")
        return

    resultados = [
        debate for debate in debates
        if debate.get("Partido1", "").upper() == sigla or debate.get("Partido2", "").upper() == sigla
    ]

    if not resultados:
        print(f"Nenhum debate encontrado para o partido '{sigla}'.")
        return

    print(f"\n--- Debates com o partido '{sigla}' ---")
    for debate in resultados:
        numero = debate.get("Número", "?")
        p1 = debate.get("Partido1", "?")
        p2 = debate.get("Partido2", "?")
        print(f"{numero}. {p1} vs {p2}")


if __name__ == "__main__":
    menu_utilizador()