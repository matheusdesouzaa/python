from abc import ABC,abstractproperty,abstractclassmethod

class Cliente:
    def __init__(self,endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self,conta,transacao):
        transacao.registrar(conta)

    def adicionar_conta(self,conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self,nome,data_nascimento,cpf,endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento =  data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self,numero,cliente):
        self._saldo = 0
        self._numero = numero
        self._cliente = cliente
        self._agencia = "0001"
        self._historico = Historico()

    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)

    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def historico(self):
        return self._historico
    
    def depositar(self,valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nDeposito de R${valor:.2f} realizado com sucesso")
        else:
            print (f"\nO valor inserido para deposito é invalido")
            return False
        return True
    
    def sacar(self,valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("\nNão foi possivel sacar,pois você não tem saldo suficiente")

        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso")
            return True

        else:
            print("\nNão foi possivel sacar pois o valor informado é invalido")
            
        return False
    
class ContaCorrente(Conta):
    def __init__(self,numero,cliente,limite=500,limite_saques=3):
        super().__init__(numero,cliente)
        self.limite = limite
        self.limite_saques=limite_saques

    def sacar(self,valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]==Saque.__name__])
        excedeu_limite = valor >self.limite
        excedeu_saque = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nNão foi possivel sacar pois o valor de saque é maior que o limite permitido")

        elif excedeu_saque:
            print("\nNão foi possivel sacar,pois o limite diario de saques foi atingido")
        
        else:
            return super().sacar(valor)

        return False
    
    def __str__(self):
        return f"""\n
Agencia:\t{self.agencia}
C/C:\t\t{self.numero}
Titular\t{self.cliente.nome}
"""
    
class Historico():
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append({"tipo":transacao.__class__.__name__,"valor":transacao.valor})

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self,conta):
        pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        transacao_aceita = conta.sacar(self.valor)  
        if transacao_aceita:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self,conta):
        transacao_aceita = conta.depositar(self.valor)
        if transacao_aceita:
            conta.historico.adicionar_transacao(self)

def menu():
    print("""
[d]   Depositar
[s]   Sacar
[e]   Extrato
[nc]  Nova Conta
[nu]  Novo Usuario
[lc]  Listar contas
[q]   Sair
->""",end="")
    return input() 

def filtrar_cliente(cpf,clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

def sacar(clientes):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

def exibir_extrato(clientes):
    cpf = input("informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)
    if not cliente:
        print("\nCliente não encontrado")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n============EXTRATO=================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato += "Não foram realizadas movimentações"
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao["tipo"]}:\n\tR${transacao["valor"]:.2f}"
        
    print(extrato)
    print(f"\nSaldo:\t\t\tR${conta.saldo:.2f}")
    print("============================================")

def listar_contas(contas):
    for conta in contas:
        print("="*100)
        print(str(conta))

def criar_cliente(clientes):
    cpf = input("Informe o cpf: ")
    cliente = filtrar_cliente(cpf,clientes)
    if cliente:
        print("\nJa existe cliente com esse cpf")
        return
    
    nome = input("informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro,numero,bairro,cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome,data_nascimento=data_nascimento,cpf=cpf,endereco=endereco)
    clientes.append(cliente)
    print("\nCliente criado com sucesso")

def criar_conta(numero_conta,clientes,contas):
    cpf = input("Informe o cpf do cliente: ")
    cliente = filtrar_cliente(cpf,clientes)

    if not cliente:
        print("Cliente não encontrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!")

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "q":
            break

        elif opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta,clientes,contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "nu":
            criar_cliente(clientes)

        else:
            print("Operação invalida")

main()