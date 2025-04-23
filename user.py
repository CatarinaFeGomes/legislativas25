import random
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
import streamlit as st
from utils import guardar_resultado_utilizador
from storage import carregar_afirmacoes, carregar_partidos, carregar_partidos_csv, carregar_debates

def menu_utilizador():
    """Menu principal do utilizador."""
    st.title("VotoMatch - Modo Utilizador")
    nome_utilizador = st.text_input("Nome do utilizador", "").strip()
    if not nome_utilizador:
        st.error("Nome inválido.")
        return

    menu_opcao = st.selectbox("Escolha uma das opções:", ["Responder ao questionário", "Histórico", "Partidos", "Sair"])

    if menu_opcao == "Responder ao questionário":
        responder_questionario(nome_utilizador)
    elif menu_opcao == "Histórico":
        menu_utilizador_historico(nome_utilizador)
    elif menu_opcao == "Partidos":
        menu_utilizador_partidos()
    elif menu_opcao == "Sair":
        st.write("Saindo...")

def menu_utilizador_historico(nome_utilizador):
    st.title(f"Histórico - {nome_utilizador}")
    menu_opcao = st.selectbox("Escolha uma das opções:", ["Ver evolução dos vencedores ao longo do tempo", "Ver pódio total", "Sair"])

    if menu_opcao == "Ver evolução dos vencedores ao longo do tempo":
        ver_historico_utilizador(nome_utilizador)
    elif menu_opcao == "Ver pódio total":
        st.write("Em desenvolvimento...")
    elif menu_opcao == "Sair":
        st.write("Saindo...")

def menu_utilizador_partidos():
    st.title("Partidos")
    menu_opcao = st.selectbox("Escolha uma das opções:", ["Ver siglas e nomes dos partidos", "Ver dados do partido", "Ver debates", "Procurar debate por partido", "Sair"])

    if menu_opcao == "Ver siglas e nomes dos partidos":
        mostrar_partidos_e_letras()
    elif menu_opcao == "Ver dados do partido":
        dados_do_partido()
    elif menu_opcao == "Ver debates":
        ver_debates()
    elif menu_opcao == "Procurar debate por partido":
        sigla = st.text_input("Insere a sigla do partido a procurar nos debates (ex: PS)").strip().upper()
        if sigla:
            pesquisar_debates_por_partido(sigla)
    elif menu_opcao == "Sair":
        st.write("Saindo...")

def responder_questionario(nome_utilizador):
    """Função para o utilizador responder ao questionário e ver resultados."""
    st.title("Responder ao Questionário")
    todas_afirmacoes = carregar_afirmacoes()
    if not todas_afirmacoes:
        st.error("Nenhuma afirmação encontrada. Adiciona algumas no modo admin.")
        return

    partidos = list(set(af["partido"] for af in todas_afirmacoes))
    num_partidos = len(partidos)

    if num_partidos < 2:
        st.error("É necessário pelo menos 2 partidos diferentes.")
        return

    afirmacoes_por_partido = {partido: [] for partido in partidos}
    for af in todas_afirmacoes:
        afirmacoes_por_partido[af["partido"]].append(af)

    min_afirmacoes = min(len(afirmacoes_por_partido[partido]) for partido in partidos)
    max_total = min_afirmacoes * num_partidos
    min_total = 2 * num_partidos

    st.write(f"Número de partidos: {num_partidos}")
    st.write(f"Escolhe o número de afirmações (mínimo: {min_total}, máximo: {max_total}, múltiplo de {num_partidos})")

    total_afirmacoes = st.number_input("Número de afirmações", min_value=min_total, max_value=max_total, step=num_partidos)

    if total_afirmacoes % num_partidos != 0 or total_afirmacoes < min_total or total_afirmacoes > max_total:
        st.error(f"O número de afirmações deve ser múltiplo de {num_partidos} e dentro do intervalo de {min_total} a {max_total}.")
        return

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
        st.write(f"{i+1}/{len(afirmacoes_selecionadas)} - {af['texto']}")
        resposta = st.radio("Escolha a sua resposta:", ["1. Concordo totalmente", "2. Concordo", "3. Neutro", "4. Discordo", "5. Discordo totalmente"])
        while resposta not in opcoes:
            resposta = st.radio("Escolha inválida. Introduza um número entre 1 e 5:", ["1. Concordo totalmente", "2. Concordo", "3. Neutro", "4. Discordo", "5. Discordo totalmente"])

        pontuacoes[af["partido"]] += opcoes[resposta]
        respostas_por_valor[resposta] += 1

    st.write("=== RESULTADOS ===")
    ranking = sorted(pontuacoes.items(), key=lambda x: x[1], reverse=True)
    for posicao, (partido, score) in enumerate(ranking, start=1):
        st.write(f"{posicao}º - {partido}: {score} pontos")

    # Guardar histórico do utilizador com data e hora
    guardar_resultado_utilizador(nome_utilizador, pontuacoes, respostas_por_valor, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    mostrar_grafico_resultado_partidos(pontuacoes)

    # Menu extra para ver histórico
    ver = st.radio("Queres ver o histórico deste utilizador?", ["Sim", "Não"])
    if ver == "Sim":
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
    st.pyplot()

def ver_historico_utilizador(nome):
    """Função para mostrar o histórico do utilizador."""
    ficheiro = os.path.join("historico", f"{nome}.json")
    if not os.path.exists(ficheiro):
        st.error("Não há histórico para este utilizador.")
        return

    with open(ficheiro, "r", encoding="utf-8") as f:
        historico = json.load(f)

    if not historico:
        st.write("Histórico vazio.")
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
    st.pyplot()

def mostrar_partidos_e_letras():
    """Função para mostrar as letras (siglas) e os partidos associados (nome completo)."""
    todas_afirmacoes = carregar_afirmacoes()
    if not todas_afirmacoes:
        st.error("Nenhuma afirmação encontrada. Adiciona algumas no modo admin.")
        return

    siglas_usadas = set(af["partido"] for af in todas_afirmacoes)
    partidos_registados = carregar_partidos()

    # Criar um dicionário sigla → nome
    mapa_sigla_para_nome = {p["sigla"]: p["nome"] for p in partidos_registados}

    st.write("\n--- Partidos e Letras Associadas ---")
    for sigla in sorted(siglas_usadas):
        nome = mapa_sigla_para_nome.get(sigla, "(nome desconhecido)")
        st.write(f"{sigla} - {nome}")

def dados_do_partido():
    partidos = carregar_partidos_csv()
    if not partidos:
        st.error("Não existem partidos registados.")
        return

    st.write("\n--- Lista de Partidos ---")
    for i, partido in enumerate(partidos, start=1):
        st.write(f"{i}. {partido['sigla']} - {partido['nome']}")

    escolha = st.number_input("\nEscolhe o número do partido (0 para cancelar):", min_value=0, max_value=len(partidos))
    if escolha == 0:
        return
    if 1 <= escolha <= len(partidos):
        p = partidos[escolha - 1]
        st.write("\n--- Dados do Partido ---")
        st.write(f"Sigla: {p['sigla']}")
        st.write(f"Nome: {p['nome']}")
        st.write(f"Ideologia Política: {p['ideologia']}")
        st.write(f"Econômicamente: {p['economia']}")
        st.write(f"Socialmente: {p['sociedade']}")
    else:
        st.error("Número inválido.")

def ver_debates():
    debates = carregar_debates()
    if not debates:
        st.error("Não existem debates registados.")
        return

    st.write("\n--- Lista de Debates ---")
    for debate in debates:
        numero = debate.get("Número", "?")
        partido1 = debate.get("Partido 1", "?")
        partido2 = debate.get("Partido 2", "?")
        data = debate.get("Data", "?")
        st.write(f"Debate {numero}: {partido1} vs {partido2} em {data}")

def pesquisar_debates_por_partido(sigla):
    debates = carregar_debates()
    if not debates:
        st.error("Não existem debates registados.")
        return

    debates_partido = [debate for debate in debates if sigla in (debate.get("Partido 1", ""), debate.get("Partido 2", ""))]

    if not debates_partido:
        st.write(f"Não foram encontrados debates para o partido {sigla}.")
        return

    st.write(f"Debates encontrados para o partido {sigla}:")
    for debate in debates_partido:
        numero = debate.get("Número", "?")
        partido1 = debate.get("Partido 1", "?")
        partido2 = debate.get("Partido 2", "?")
        data = debate.get("Data", "?")
        st.write(f"Debate {numero}: {partido1} vs {partido2} em {data}")

if __name__ == "__main__":
    menu_utilizador()
