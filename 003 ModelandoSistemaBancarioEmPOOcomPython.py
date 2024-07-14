from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if 0 < valor <= self._saldo:
            self._saldo -= valor
            print("\033[32mSaque realizado com sucesso.\033[m")
            return True
        else:
            print("\033[31mSaldo insuficiente ou valor de saque inválido.\033[m")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\033[32mDepósito realizado com sucesso.\033[m")
            return True
        else:
            print("\033[31mNão é possível depositar esse valor.\033[m")

        return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def saque(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico._transacoes if transacao["tipo"] == Saque.__name__]
                           )
        if numero_saque == self.limite_saques or valor > self.limite:
            print("\033[31mVocê atingiu o limite de saque diário ou valor de saque inválido.\033[m")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"Agência:  {self.agencia}\nC/C:  {self.numero}\nTitular:  {self.cliente.nome}"


class Historico:
    def __init__(self):
        self._transacoes = []

    def transacao(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    print("""\033[34m
=-=-=-=-=-MENU-=-=-=-=-=
[d]    Depositar
[s]    Sacar
[e]    Extrato
[nc]   Nova conta
[lc]   Listar contas
[nu]   Novo usuário
[q]    Sair\n""")

    while True:
        a = str(input("\033[34mDigite a sua opção:\033[m ")).strip().lower()
        if a.isalpha():
            break
        else:
            print("\033[31mOpção inválida!\033[m")
    return a


def fazer_deposito(usuarios):
    cpf = input("\033[34mInforme o cpf do Cliente:\033[m ")
    cliente = filtrar_usuario(cpf, usuarios)
    if not cliente:
        print("\033[31mCliente não encontrado.\033[m")
        return

    valor = float(input("\033[34mInforme o valor do depósito:\033[m "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def fazer_saque(usuarios):
    cpf = input("\033[34mInforme o CPF do cliente:\033[m ")
    cliente = filtrar_usuario(cpf, usuarios)

    if not cliente:
        print("\033[31mCliente não encontrado!\033[m")
        return

    valor = float(input("\033[34mInforme o valor do saque:\033[m "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(usuarios):
    cpf = input("\033[34mInforme o CPF do cliente:\033[m ")
    cliente = filtrar_usuario(cpf, usuarios)

    if not cliente:
        print("\033[31mCliente não encontrado!\033[m")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n\033[33m================ EXTRATO ================")
    transacoes = conta.historico.transacao

    extrato = ""
    if not transacoes or transacoes is None:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================\033[m")


def filtrar_usuario(cpf, usuarios):
    clientes_filtrados = [cliente for cliente in usuarios if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\033[31mCliente não possui conta!\033[m")
        return

    return cliente.contas[0]


def nova_conta(usuarios, contas, numero_conta):
    cpf = input("\033[34mInforme o CPF do cliente:\033[m ")
    cliente = filtrar_usuario(cpf, usuarios)

    if not cliente:
        print("\033[31mCliente não encontrado, fluxo de criação de conta encerrado!\033[m")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\033[32mConta criada com sucesso!\033[m")


def listar_contas(contas):
    for conta in contas:
        print("\033[33m=" * 100)
        print(str(conta))


def novo_usuario(usuarios):
    cpf = input("\033[34mInforme o CPF (somente número): ")
    cliente = filtrar_usuario(cpf, usuarios)

    if cliente:
        print("\033[31mJá existe cliente com esse CPF!\033[m")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado):\033[m ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    usuarios.append(cliente)

    print("\033[32mCliente criado com sucesso!\033[m")


def iniciando_operacao():
    contas = []
    usuarios = []

    while True:
        opcao = menu()

        if opcao == 'd':
            fazer_deposito(usuarios)
        elif opcao == 's':
            fazer_saque(usuarios)
        elif opcao == 'e':
            exibir_extrato(usuarios)
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            nova_conta(usuarios, contas, numero_conta)
        elif opcao == 'lc':
            listar_contas(contas)
        elif opcao == 'nu':
            novo_usuario(usuarios)
        elif opcao == 'q':
            print("\033[32mFinalizando operação...\033[m")
            break
        else:
            print("\033[31mOpção inválida, a operação será cancelada.\033[m")
            break


iniciando_operacao()
