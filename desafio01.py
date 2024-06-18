#criação do menu
menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=>"""

#variaveis
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

#looping infinito que só acaba se a pessoa escolher [q]
while True:
    opcao = input(menu)

    if opcao == "d":                                                #codigo caso a pessoa escolha realizar o depósito
        while True:                                                 #looping ate a pessoa colocar um valor positivo para depósito 
            deposito = float(input("deposito de R$"))
            if deposito >0:
                saldo += deposito
                extrato += f"Deposito de R${deposito:.2f} \n"
                break

    elif opcao == "s":                                                                                  #codigo caso a pessoa escolha fazer o saque
        saque = float(input("Valor a sacar R$"))
        if saque > saldo:
            print("Não foi possivel sacar pois o saque é maior que o saldo disponivel")
        elif saque >500:
            print("Não foi possivel sacar pois o valor de saque excedeu o limite de R$500.00")
        elif numero_saques >= LIMITE_SAQUES:
            print("Não foi possivel sacar pois o limite diário de saque ja foi atingido (3)")
        elif saque <0:
            print("Não foi possivel sacar pois não é possivel sacar valores negativos")
        else:
            saldo -= saque
            numero_saques += 1
            extrato += f"Saque de R${saque:.2f} \n"
    
    elif opcao == "e":                                                                                  #codigo caso a pessoa escolha ver o extrato
        print("extrato".center(30,"-"))
        print("Não houve nenhuma movimentação na conta" if extrato=="" else extrato)
        print()
        print(f"SALDO DA CONTA: R${saldo:.2f}")
        print("-"*37)

    elif opcao == "q":                                                                                 #encerramento do programa
        break

    else:                                                                                               #caso a pessoa erre as opções do menu
        print("Operação inválida, por favor selecione novamente a operação desejada")