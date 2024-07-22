def menu():
    print("""\033[34m\n
=-=-=-=-=-MENU-=-=-=-=-=
[d]    Depositar
[s]    Sacar
[e]    Extrato
[nc]   Nova conta
[lc]   Listar contas
[nu]   Novo usuário
[q]    Sair""")

    while True:
        a = str(input("\033[34mDigite a sua opção:\033[m ")).strip().lower()
        if a.isalpha():
            break
        else:
            print("\033[031mOpção inválida!\033[m")
    return a


def fazer_deposito(valor, saldo, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("\033[32mDepósito realizado com sucesso.\033[m")
    else:
        print("\033[31mNão é possível depositar esse valor.\033[m")

    return saldo, extrato


def fazer_saque(*, saque_total, saldo, limite, extrato, valor):
    if (valor <= limite) and (valor <= saldo) and (valor > 0):
        saldo -= valor
        saque_total += 1
        extrato += f"Saque: R$ {valor:.2f}\n"
        print("\033[32mSaque realizado com sucesso.")
    else:
        print("\033[31mSaldo insuficiente ou valor de saque inválido")

    return extrato, saldo, saque_total


def exibir_extrato(saldo, /, *, extrato):
    print(f"\033[34m\n=-=-=-=-EXTRATO-=-=-=-={extrato}\nSeu saldo atual é R$ {saldo:.2f}.")


def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario


def nova_conta(agencia, usuarios, n_conta):
    cpf = input("\033[34mDigite o seu cpf (somente o número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\033[32mConta criada com sucesso! ")

        return {'agencia': agencia, 'n_conta': n_conta, 'usuario': usuario}
    print("\033[31mNão foi encontrado nenhum usuario para criar uma conta.")


def listar_contas(contas):
    for conta in contas:
        print("\033[34m\n=-=-=-=-=-=-= CONTA =-=-=-=-=-=-=")
        print(f"Agência: {conta['agencia']}")
        print(f"c/c: {conta['n_conta']}")
        print(f"Agência: {conta['usuario']['nome']}")


def novo_usuario(usuarios):
    cpf = input("\033[34mDigite o seu cpf (somente o número): ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\033[31mUsuario já existente. ")
        return

    nome = str(input("\033[34mDigite o nome completo: "))
    data_nascimento = input("Digite a sua data de nascimneto (dd-mm-aa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    return {'nome': nome, 'data_nascimento': data_nascimento, 'cpf': cpf, 'endereco': endereco}


def iniciando_operacao():
    LIMITE_SAQUE = 3
    AGENCIA = '0001'
    saque_total = 0
    limite = 500
    extrato = "\n"
    saldo = 0
    contas = []
    n_conta = 1
    usuarios = []

    while True:
        opcao = menu()

        if opcao == 'd':
            valor = float(input("\033[34mDigite o valor que deseja depositar R$ "))

            saldo, extrato = fazer_deposito(valor, saldo, extrato)
        elif opcao == 's':
            if saque_total < LIMITE_SAQUE and saldo > 0:
                valor = float(input("\033[34mDigite o valor do saque R$ "))

                extrato, saldo, saque_total = fazer_saque(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    saque_total=saque_total)
            else:
                print("\033[31mVocê atingiu o limite de saque diário ou não possui saldo positivo para sacar. ")
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == 'nc':
            conta = nova_conta(AGENCIA, usuarios, n_conta)
            if conta is not None:
                contas.append(conta)
                n_conta += 1
        elif opcao == 'lc':
            listar_contas(contas)
        elif opcao == 'nu':
            usuario = novo_usuario(usuarios)
            if usuario is not None:
                usuarios.append(usuario)
        elif opcao == 'q':
            print("\033[32mFinalizando operação...")
            break
        else:
            print("\033[31mOpção inválida, a operação será cancelada.")
            break


iniciando_operacao()
