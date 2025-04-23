import csv
import os

FICHEIRO_AFIRMACOES = "afirmacoes.csv"

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



#TODO eliminar este .json e usar o csv
import json
import os

FICHEIRO_PARTIDOS = "partidos.json"

def carregar_partidos():
    if not os.path.exists(FICHEIRO_PARTIDOS):
        return []
    try:
        with open(FICHEIRO_PARTIDOS, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return []  # ficheiro vazio
            return json.loads(conteudo)
    except json.JSONDecodeError:
        print("Erro: ficheiro de partidos corrompido ou com formato inválido.")
        return []


def guardar_partidos(partidos):
    with open("partidos.json", "w", encoding="utf-8") as f:
        json.dump(partidos, f, ensure_ascii=False, indent=2)


import csv

def carregar_partidos_csv():
    try:
        with open("partidos.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print("Ficheiro 'partidos.csv' não encontrado.")
        return []



import csv
import os

FICHEIRO_DEBATES = "debates.csv"
import csv

def carregar_debates():
    try:
        with open("debates.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)
    except FileNotFoundError:
        print("Ficheiro 'debates.csv' não encontrado.")
        return []

