from admin import menu_admin
from user import menu_utilizador

def main():
    print("=== VotoMatch: Assistente de Decisão de Voto ===")
    while True:
        modo = input("\nEscolhe o modo:\n1. Admin (gerir afirmações)\n2. Utilizador (responder)\n0. Sair\nEscolha: ")
        if modo == "1":
            menu_admin()
        elif modo == "2":
            menu_utilizador()
        elif modo == "0":
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
