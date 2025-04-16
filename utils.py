import json
import os
from datetime import datetime

def ver_afirmacoes(afirmacoes):
    if not afirmacoes:
        print("\nNenhuma afirmação registada.")
        return
    print("\n--- Lista de Afirmações ---")
    for i, af in enumerate(afirmacoes):
        print(f"{i+1}. \"{af['texto']}\"  ({af['partido']})")

def guardar_resultado_utilizador(nome_utilizador, pontuacoes, respostas_por_valor, data_hora):
    ficheiro = os.path.join("historico", f"{nome_utilizador}.json")
    os.makedirs("historico", exist_ok=True)

    novo_registo = {
        "data": data_hora,
        "pontuacoes": pontuacoes,
        "respostas": respostas_por_valor
    }

    if os.path.exists(ficheiro):
        with open(ficheiro, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.append(novo_registo)

    with open(ficheiro, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=4, ensure_ascii=False)
