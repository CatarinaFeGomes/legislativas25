import os
import streamlit as st
import random
import json
from datetime import datetime
import matplotlib.pyplot as plt
from utils import guardar_resultado_utilizador
from storage import carregar_afirmacoes, carregar_partidos, carregar_debates


# Função para mostrar o menu do utilizador
def menu_utilizador():
    st.title("Modo Utilizador")

    nome_utilizador = st.text_input("Nome do utilizador:").strip()
    if not nome_utilizador:
        st.warning("Nome inválido.")
        return

    opcao = st.segmented_control("Escolha uma das opções",
                                 ["Responder ao questionário", "Histórico", "Partidos", "Sair"])

    if opcao == "Responder ao questionário":
        responder_questionario(nome_utilizador)
    elif opcao == "Histórico":
        menu_utilizador_historico(nome_utilizador)
    elif opcao == "Partidos":
        menu_utilizador_partidos()
    elif opcao == "Sair":
        st.info("Saindo...")


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
        st.info("Saindo...")


# Função para o menu de partidos no modo utilizador
def menu_utilizador_partidos():
    st.subheader("Partidos")

    opcao = st.radio("Escolha uma das opções", [
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
        st.info("Saindo...")


def responder_questionario(nome_utilizador):
    """Função para o utilizador responder ao questionário e ver resultados."""
    print("\n--- RESPOSTA AO QUESTIONÁRIO ---")
    todas_afirmacoes = carregar_afirmacoes()
    if not todas_afirmacoes:
        print("Nenhuma afirmação encontrada. Adiciona algumas no modo admin.")
        return

    partidos = list(set(af["partido"] for af in todas_afirmacoes))
    num_partidos = len(partidos)

    if num_partidos < 2:
        print("É necessário pelo menos 2 partidos diferentes.")
        return

    afirmacoes_por_partido = {partido: [] for partido in partidos}
    for af in todas_afirmacoes:
        afirmacoes_por_partido[af["partido"]].append(af)

    min_afirmacoes = min(len(afirmacoes_por_partido[partido]) for partido in partidos)
    max_total = min_afirmacoes * num_partidos
    min_total = 2 * num_partidos

    print(f"\nNúmero de partidos: {num_partidos}")
    print(f"Escolhe o número de afirmações (mínimo: {min_total}, máximo: {max_total}, múltiplo de {num_partidos})")

    while True:
        try:
            total_afirmacoes = int(input("Número de afirmações: "))
            if min_total <= total_afirmacoes <= max_total and total_afirmacoes % num_partidos == 0:
                break
            else:
                print("Número inválido. Deve ser múltiplo do número de partidos e dentro dos limites.")
        except ValueError:
            print("Por favor, introduz um número válido.")

    num_por_partido = total_afirmacoes // num_partidos
    afirmacoes_selecionadas = []

    for partido in partidos:
        random.shuffle(afirmacoes_por_partido[partido])
        afirmacoes_selecionadas.extend(afirmacoes_por_partido[partido][:num_por_partido])

    random.shuffle(afirmacoes_selecionadas)

    pontuacoes = {partido: 0 for partido in partidos}
    opcoes = {"1": 2, "2": 1, "3": 0, "4": -1, "5": -2}
    respostas_por_valor = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}

    for i, af in enumerate(afirmacoes_selecionadas):
        print(f"\n{i + 1}/{len(afirmacoes_selecionadas)} - {af['texto']}")
        print("1. Concordo totalmente\n2. Concordo\n3. Neutro\n4. Discordo\n5. Discordo totalmente")
        resposta = input("Escolha (1-5): ")
        while resposta not in opcoes:
            resposta = input("Escolha inválida. Introduz um número entre 1 e 5: ")
        pontuacoes[af["partido"]] += opcoes[resposta]
        respostas_por_valor[resposta] += 1

    print("\n=== RESULTADOS ===")
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    for posicao, (partido, score) in enumerate(ranking, start=1):
        print(f"{posicao}º - {partido}: {score} pontos")

    # Guardar histórico do utilizador com data e hora
    guardar_resultado_utilizador(nome_utilizador, pontuacoes, respostas_por_valor,
                                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mostrar_grafico_resultado_partidos(pontuacoes)

    # Menu extra para ver histórico
    ver = input("\nQueres ver o histórico deste utilizador? (s/n): ").lower()
    if ver == "s":
        ver_historico_utilizador(nome_utilizador)


def mostrar_grafico_resultado_partidos(pontuacoes):
    """Função para mostrar gráfico das pontuações por partido."""
    partidos = list(pontuacoes.keys())
    valores = list(pontuacoes.values())

    plt.figure(figsize=(8, 5))
    plt.bar(partidos, valores, color='lightgreen')
    plt.title("Pontuação final por partido")
    plt.ylabel("Pontuação")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.show()


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