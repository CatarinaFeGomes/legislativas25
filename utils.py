import streamlit as st
import json
import os
from datetime import datetime

# Função para mostrar as afirmações
def ver_afirmacoes(afirmacoes):
    if not afirmacoes:
        st.warning("Nenhuma afirmação registada.")
        return
    st.subheader("📃 Lista de Afirmações")
    for i, af in enumerate(afirmacoes):
        st.markdown(f"**{i+1}.** \"{af['texto']}\"  (_{af['partido']}_)")

# Função para guardar os resultados do utilizador
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
