LIMITE_SAQUE = 3
saque_total = 0
limite = 500
extrato = ""
saldo = 0

while True:
    print("""
[1] Saque
[2] Depósito
[3] Extrato
[4] Finalizar
""")
    opcao = int(input())

    if opcao == 1:
        if saque_total < LIMITE_SAQUE and saldo > 0:
            valor = float(input("Digite o valor do saque R$ "))
            if (valor <= limite) and (valor <= saldo) and (valor > 0):
                saldo -= valor
                saque_total += 1
                extrato += f"Saque: R$ {valor:.2f}\n"
                print("Saque realizado com sucesso.")
            else:
                print("Saldo insuficiente ou valor de saque inválido")
        else:
            print("Você atingiu o limite de saque diário ou não possui saldo positivo para sacar.")
    elif opcao == 2:
        valor = float(input("Digite o valor que deseja depositar R$ "))
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
            print("Depósito realizado com sucesso.")
        else:
            print("Não é possível depositar esse valor.")
    elif opcao == 3:
        print(f"{extrato}\nSeu saldo atual é R$ {saldo:.2f}.")
    elif opcao == 4:
        print("Finalizando operação...")
        break
    else:
        print("Opção inválida, a operação será cancelada.")
        break
