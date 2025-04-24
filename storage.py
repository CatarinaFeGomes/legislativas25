import streamlit as st
import csv
import os
import json

# Ficheiros
FICHEIRO_AFIRMACOES = "afirmacoes.csv"
FICHEIRO_PARTIDOS_JSON = "partidos.json"
FICHEIRO_PARTIDOS_CSV = "partidos.csv"
FICHEIRO_DEBATES = "debates.csv"

# Funções CSV e JSON
def carregar_afirmacoes():
    afirmacoes = []
    if os.path.exists(FICHEIRO_AFIRMACOES):
        with open(FICHEIRO_AFIRMACOES, mode="r", encoding='utf-8') as ficheiro:
            reader = csv.reader(ficheiro)
            afirmacoes = [{"texto": linha[0], "partido": linha[1]} for linha in reader]
    return afirmacoes

def guardar_afirmacoes(afirmacoes):
    with open(FICHEIRO_AFIRMACOES, mode="w", newline='', encoding='utf-8') as ficheiro:
        writer = csv.writer(ficheiro)
        for af in afirmacoes:
            writer.writerow([af["texto"], af["partido"]])

def carregar_partidos_json():
    if not os.path.exists(FICHEIRO_PARTIDOS_JSON):
        return []
    try:
        with open(FICHEIRO_PARTIDOS_JSON, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return []
            return json.loads(conteudo)
    except json.JSONDecodeError:
        st.error("Erro: ficheiro de partidos corrompido ou com formato inválido.")
        return []

def guardar_partidos(partidos):
    with open(FICHEIRO_PARTIDOS_JSON, "w", encoding="utf-8") as f:
        json.dump(partidos, f, ensure_ascii=False, indent=2)

def carregar_partidos():
    try:
        with open(FICHEIRO_PARTIDOS_CSV, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        st.warning("Ficheiro 'partidos.csv' não encontrado.")
        return []

def carregar_debates():
    try:
        with open(FICHEIRO_DEBATES, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        st.warning("Ficheiro 'debates.csv' não encontrado.")
        return []

# Streamlit Interface
st.title("Gestão de Dados - VotoMatch")

tab1, tab2, tab3, tab4 = st.tabs(["Afirmações", "Partidos (CSV)", "Partidos (JSON)", "Debates"])

with tab1:
    st.header("Afirmações")
    afirmacoes = carregar_afirmacoes()
    for af in afirmacoes:
        st.write(f"🗨️ {af['texto']} — {af['partido']}")
    with st.form("nova_afirmacao"):
        texto = st.text_input("Texto da afirmação")
        partido = st.text_input("Partido associado")
        if st.form_submit_button("Adicionar"):
            afirmacoes.append({"texto": texto, "partido": partido})
            guardar_afirmacoes(afirmacoes)
            st.success("Afirmação adicionada!")

with tab2:
    st.header("Partidos (CSV)")
    partidos_csv = carregar_partidos()
    if partidos_csv:
        for p in partidos_csv:
            st.write(f"🏛️ {p.get('nome', 'Sem nome')} — {p}")

with tab3:
    st.header("Partidos (JSON)")
    partidos_json = carregar_partidos_json()
    if partidos_json:
        for p in partidos_json:
            st.json(p)

with tab4:
    st.header("Debates")
    debates = carregar_debates()
    if debates:
        for d in debates:
            st.write(f"🎤 {d}")

