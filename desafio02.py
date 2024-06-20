def menu():
    print("""
[d]   Depositar
[s]   Sacar
[e]   Extrato
[nc]  Nova Conta
[nu]  Novo Usuario
[q]   Sair
->""",end="")
    return input() 

def depositar(saldo,valor,extrato,/):
    if valor > 0:
        saldo += valor
        extrato += f"\nDeposito de R${valor:.2f}"
        print(f"\nDeposito de R${valor:.2f} realizado com sucesso")
    else:
        print (f"\nO valor inserido para deposito é invalido")
    return saldo,extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saque = numero_saques >= LIMITE_SAQUES 
    excedeu_limite = valor > limite
    excedeu_saldo = valor > saldo

    if excedeu_saque:
        print("\nNão foi possivel sacar,pois o limite diario de saques foi atingido")

    elif excedeu_limite:
        print("\nNão foi possivel sacar pois o valor de saque é maior que o limite permitido")

    elif excedeu_saldo:
        print("\nNão foi possivel sacar pois o valor de saque é maior que o saldo da conta")

    elif valor > 0:
        saldo -= valor
        extrato += f"\nSaque de R${valor:.2f}"
        print(f"\nSaque de R${valor:.2f} realizado com sucesso")
        numero_saques +=1

    else:
        print("Não foi possivel sacar pois o valor de saque é invalido")

    return saldo,extrato,numero_saques

def mostrar_extrato(saldo, /, *,extrato):
    print("extrato".center(30,"-"))
    print("Não houve nenhuma movimentação na conta" if extrato=="" else extrato)
    print()
    print(f"SALDO DA CONTA: R${saldo:.2f}")
    print("-"*30)

def criar_usuario(usuarios):
    cpf = input("Qual o seu cpf? (somente numeros)")
    usuario  = verificar_usuarios(cpf,usuarios)

    if usuario:
        print("Não foi possivel criar novo usuario,pois ja existe um com esse cpf")
    else:
        nome = input("Qual o seu nome completo? ")
        nascimento = input("Qual a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Qual o seu endereço?(logradouro,numero,bairro,cidade/sigla do estado): ")

        usuarios.append({"nome": nome, "data_nascimento": nascimento,"cpf": cpf, "endereco":endereco})
        print("\nUsuario criado com sucesso!!!!!")

def verificar_usuarios(cpf,usuarios):
    usuario_existe = False
    for usuario in usuarios:
        if usuario["cpf"]== cpf:
            usuario_existe= True
    return usuario_existe

def criar_conta(AGENCIA,numero_conta,usuarios):
    cpf = input("Qual o seu cpf? (somente numeros): ")
    existe = verificar_usuarios(cpf,usuarios)
    
    if existe:
        for individuo in usuarios:
            if individuo["cpf"]== cpf:
                nome_titular_conta = individuo["nome"]
                print("\nConta criada com sucesso!")
                return {"agencia": AGENCIA,"numero_conta": numero_conta,"usuario":nome_titular_conta}
    else:
        print("Não foi possivel criar uma conta,pois nao existe um usuario com esse cpf")
        return ""
    
def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    contas = []
    usuarios = []
    AGENCIA = "0001"
    numero_conta = 1

    while True:
        opção = menu()

        if opção == "q":
            break

        elif opção == "d":
            valor = float(input("Qual o valor que voce deseja depositar? R$"))
            saldo,extrato = depositar(saldo,valor,extrato)

        elif opção == "s":
            valor = float(input("Qual o valor que voce deseja sacar? R$"))
            saldo,extrato,numero_saques = sacar(saldo=saldo,valor=valor,extrato=extrato,limite=limite,numero_saques=numero_saques,LIMITE_SAQUES=LIMITE_SAQUES)

        elif opção == "e":
            mostrar_extrato(saldo,extrato=extrato)

        elif opção == "nc":
            conta = criar_conta(AGENCIA,numero_conta,usuarios)    

            if conta != "":
                contas.append(conta)
                numero_conta += 1

        elif opção == "nu":
            criar_usuario(usuarios)

        else:
            print("Opção invalida,tente novamente")
            print()

main()

