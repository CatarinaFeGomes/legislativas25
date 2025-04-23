from storage import carregar_afirmacoes, guardar_afirmacoes
from storage import carregar_partidos, guardar_partidos
from storage import carregar_debates
from utils import ver_afirmacoes

def menu_admin():
    while True:
        print("\n--- Menu ADMIN ---")
        print("1. Afirmações")
        print("2. Partidos")
        print("0. Voltar")
        opcao = input("Escolha: ")
        if opcao == "1":
            menu_admin_afirmacoes()
        elif opcao == "2":
            menu_admin_partidos()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")




def menu_admin_afirmacoes():
    while True:
        print("\n--- ADMIN >> Afirmações ---")
        print("1. Ver afirmações")
        print("2. Adicionar várias afirmações para um partido")
        print("3. Editar afirmação")
        print("4. Remover afirmação")
        print("0. Voltar")
        opcao = input("Escolha: ")
        if opcao == "1":
            ver_afirmacoes_opcao()
        elif opcao == "2":
            adicionar_varias_afirmacoes_opcao()
        elif opcao == "3":
            editar_afirmacao_opcao()
        elif opcao == "4":
            remover_afirmacao_opcao()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def menu_admin_partidos():
    while True:
        print("\n--- ADMIN >> Partidos ---")
        print("1. Adicionar partidos")
        print("2. Editar partidos")
        print("3. Remover partidos")
        print("0. Voltar")
        opcao = input("Escolha: ")
        if opcao == "1":
            adicionar_partido()
        elif opcao == "2":
            editar_partido()
        elif opcao == "3":
            remover_partido()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")

def ver_afirmacoes_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)

def adicionar_varias_afirmacoes_opcao():
    partido = input("Nome do partido: ").strip()
    print("Escreve as afirmações (ENTER em branco para terminar):")
    novas_afirmacoes = []
    while True:
        texto = input("> ").strip()
        if not texto:
            break
        novas_afirmacoes.append({"texto": texto, "partido": partido})
    if novas_afirmacoes:
        afirmacoes = carregar_afirmacoes()
        afirmacoes.extend(novas_afirmacoes)
        guardar_afirmacoes(afirmacoes)
        print(f"{len(novas_afirmacoes)} afirmações adicionadas com sucesso.")

def editar_afirmacao_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)
    try:
        indice = int(input("\nNúmero da afirmação a editar (0 para cancelar): "))
        if indice == 0:
            return
        if 1 <= indice <= len(afirmacoes):
            nova_texto = input("Novo texto da afirmação (ENTER para manter): ").strip()
            novo_partido = input("Novo nome do partido (ENTER para manter): ").strip()
            if nova_texto:
                afirmacoes[indice - 1]["texto"] = nova_texto
            if novo_partido:
                afirmacoes[indice - 1]["partido"] = novo_partido
            guardar_afirmacoes(afirmacoes)
            print("Afirmação atualizada com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")

def remover_afirmacao_opcao():
    afirmacoes = carregar_afirmacoes()
    ver_afirmacoes(afirmacoes)
    try:
        indice = int(input("\nNúmero da afirmação a remover (0 para cancelar): "))
        if indice == 0:
            return
        if 1 <= indice <= len(afirmacoes):
            confirmacao = input("Tens a certeza que queres remover esta afirmação? (s/n): ")
            if confirmacao.lower() == "s":
                afirmacoes.pop(indice - 1)
                guardar_afirmacoes(afirmacoes)
                print("Afirmação removida com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")


def adicionar_partido():
    partidos = carregar_partidos()
    sigla = input("Sigla do novo partido (ex: BE): ").strip()
    nome = input("Nome completo do partido (ex: Bloco de Esquerda): ").strip()

    if not sigla or not nome:
        print("Sigla ou nome inválido.")
        return

    if any(p["sigla"].lower() == sigla.lower() for p in partidos):
        print("Já existe um partido com essa sigla.")
        return

    partidos.append({"sigla": sigla, "nome": nome})
    guardar_partidos(partidos)
    print("Partido adicionado com sucesso.")

def editar_partido():
    partidos = carregar_partidos()
    if not partidos:
        print("Não existem partidos registados.")
        return

    print("\n--- Partidos Existentes ---")
    for i, p in enumerate(partidos, start=1):
        print(f"{i}. {p['sigla']} - {p['nome']}")

    try:
        indice = int(input("\nNúmero do partido a editar (0 para cancelar): "))
        if indice == 0:
            return
        if 1 <= indice <= len(partidos):
            partido = partidos[indice - 1]
            nova_sigla = input(f"Nova sigla ({partido['sigla']}): ").strip()
            novo_nome = input(f"Novo nome ({partido['nome']}): ").strip()

            # Verifica se a nova sigla já existe noutro partido
            if nova_sigla and any(p["sigla"].lower() == nova_sigla.lower() and p != partido for p in partidos):
                print("Essa sigla já está a ser usada por outro partido.")
                return

            if nova_sigla:
                partido["sigla"] = nova_sigla
            if novo_nome:
                partido["nome"] = novo_nome

            guardar_partidos(partidos)
            print("Partido editado com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")

def remover_partido():
    partidos = carregar_partidos()
    if not partidos:
        print("Não existem partidos registados.")
        return

    print("\n--- Partidos Existentes ---")
    for i, p in enumerate(partidos, start=1):
        print(f"{i}. {p['sigla']} - {p['nome']}")

    try:
        indice = int(input("\nNúmero do partido a remover (0 para cancelar): "))
        if indice == 0:
            return
        if 1 <= indice <= len(partidos):
            p = partidos[indice - 1]
            confirmacao = input(f"Tens a certeza que queres remover '{p['sigla']} - {p['nome']}'? (s/n): ").lower()
            if confirmacao == "s":
                partidos.pop(indice - 1)
                guardar_partidos(partidos)
                print("Partido removido com sucesso.")
        else:
            print("Número inválido.")
    except ValueError:
        print("Entrada inválida.")


