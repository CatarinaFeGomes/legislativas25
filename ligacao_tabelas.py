import csv

# Função para carregar os dados de um CSV
def carregar_csv(ficheiro):
    with open(ficheiro, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

# Função para criar a ligação entre afirmações e partidos
def ligar_afirmacoes_partidos():
    # Carregar as tabelas de partidos e afirmações
    partidos = carregar_csv('partidos.csv')
    afirmacoes = carregar_csv('afirmacoes.csv')

    # Criar um dicionário de partidos com a letra como chave
    partidos_dict = {partido['letra']: partido['nome'] for partido in partidos}

    # Fazer a ligação das afirmações com os nomes dos partidos
    for afirmacao in afirmacoes:
        partido_letra = afirmacao['partido']
        partido_nome = partidos_dict.get(partido_letra, 'Partido Desconhecido')  # Caso a letra não exista
        afirmacao['partido_nome'] = partido_nome

    # Exibir as afirmações com o nome do partido associado
    for afirmacao in afirmacoes:
        print(f"A afirmação: {afirmacao['texto']} é do partido: {afirmacao['partido_nome']}")

# Chamar a função para ligar as afirmações aos partidos
if __name__ == "__main__":
    ligar_afirmacoes_partidos()
