from typing import List

class Node:
    '''REPRESENTA UMA CANDIDATA À SOLUÇÃO'''

    #   PADRÃO:
    #   SOLUÇÃO VAZIA COM 15 POSIÇÕES PREENCHIDAS COM 0
    #   NÓ PAI: NÃO EXISTE
    def __init__(self, candidate: List = [0 for _ in range(15)], parent = None):
        self.candidate = self.validateCandidate(candidate)
        self.parent = parent

    def validateCandidate(self, candidate):
        '''VALIDA A SOLUÇÃO CANDIDATA'''

        for presentItem in candidate:

            #   SE O FORMATO DA SOLUÇÃO FOR INVÁLIDO RETORNA UMA CANDIDATA VAZIA COM 15 ITENS
            if not(presentItem != 0 or presentItem != 1):
                return [0 for _ in range(15)]

        return candidate

class Items:

    #   PADRÃO
    #   ITENS COM PESOS 63, 21, 2, 32, 13, 80, 19, 37, 56, 41, 14, 8, 32, 42 E 7
    #   ITENS COM VALORES 13, 2, 20, 10, 7, 14, 7, 2, 2, 4, 16, 17, 17, 3, 21
    def __init__(self, peso: List = [63, 21, 2, 32, 13, 80, 19, 37, 56, 41, 14, 8, 32, 42, 7],
                       valor: List = [13, 2, 20, 10, 7, 14, 7, 2, 2, 4, 16, 17, 17, 3, 21]):

        if len(peso) == len(valor):
            self.weight = peso
            self.value = valor

        else:
            self.weight = [63, 21, 2, 32, 13, 80, 19, 37, 56, 41, 14, 8, 32, 42, 7]
            self.value = [13, 2, 20, 10, 7, 14, 7, 2, 2, 4, 16, 17, 17, 3, 21]

class Knapsack:
    '''CLASSE QUE REPRESENTA UMA MOCHILA
        ATRIBUTOS:
        NODE (a configuração atual da mochila)
        ITEMS (as informações de peso e valor de cada item presente na mochila)
        CAPACITY (o peso máximo suportado pela mochila)
    '''

    def __init__(self, start: Node = Node(), items: Items = Items(), capacity: int = 275):
        '''UMA MOCHILA RECEBE COMO PARÂMETROS DE ENTRADA:
                UMA SOLUÇÃO CANDIDATA (EXEMPLO: [0, 1, 0, 1])
                UM OBJETO DE ITENS (EXEMPLO: peso=[63, 4, 10, 9], valor=[4, 3, 20, 90])
                A CAPACIDADE MÁXIMA DA MOCHILA
        '''
        self.start = start
        self.items = items

        self.capacity = capacity
        self.totalWeight = self.calculateTotalWeight()
        self.totalValue = self.calculateTotalValue()

    def calculateTotalWeight(self):
        '''CALCULA O PESO TOTAL DOS ITENS NA MOCHILA'''
        totalWeight = 0

        for index in range(len(self.items.weight)):

            #   SE O ITEM ATUAL ESTIVER NA MOCHILA
            if self.start.candidate[index] == 1:
                totalWeight += self.items.weight[index]

                #   SE A SOMA TOTAL ULTRAPASSAR A CAPACIDADE MÁXIMA INVALIDA O VALOR
                if not(self.isViable(totalWeight)):
                    return -1

        return totalWeight

    def calculateTotalValue(self):
        '''CALCULA O PESO TOTAL DOS ITENS NA MOCHILA'''
        totalValue = 0

        for index in range(len(self.items.value)):

            #   SE O ITEM ATUAL ESTIVER NA MOCHILA
            if self.start.candidate[index] == 1:
                totalValue += self.items.value[index]

                #   SE A SOMA TOTAL ULTRAPASSAR A CAPACIDADE MÁXIMA INVALIDA O VALOR
                if not(self.isViable(self.totalWeight)):
                    return -1

        return totalValue

    def isViable(self, totalWeight):
        '''DETERMINA SE A SOLUÇÃO É VIÁVEL, ISTO É, SE NÃO ULTRAPASSA A CAPACIDADE MÁXIMA DA MOCHILA'''

        if totalWeight != -1 and totalWeight <= self.capacity:
            return True

        return False

    def neighbours(self, node : Node):
        '''GERA A VIZINHANÇA DE SOLUÇÕES CANDIDATAS A PARTIR DA CANDIDATA ATUAL'''
        currentNode = node
        neighbourhood = []

        #   GERA OS VIZINHOS UM POR UM E DESCARTA OS VIZINHOS QUE ULTRAPASSAM A CAPACIDADE MÁXIMA
        for i in range(len(currentNode.candidate)):
            neighbour = []

            j = 0

            for j in range(0, i):
                neighbour.append(currentNode.candidate[j])

            j = i

            #   MOVIMENTO QUE ADICIONA UM ITEM
            if currentNode.candidate[i] == 0:
                neighbour.append(1)

            #   MOVIMENTO QUE REMOVE UM ITEM
            if currentNode.candidate[i] == 1:
                neighbour.append(0)

            for j in range(i + 1, len(currentNode.candidate)):
                neighbour.append(currentNode.candidate[j])

            childNode = Node(neighbour, currentNode)
            items = self.items
            capacity = self.capacity
            newKnapsack = Knapsack(childNode, items, capacity)

            #   SE A VIZINHA FOR VIÁVEL ADICIONA ELA À VIZINHANÇA
            if newKnapsack.isViable(newKnapsack.totalWeight):
                neighbourhood.append(newKnapsack)

        return neighbourhood

def imprimirItens(items : Items, capacity: int):

    print('ITEM', end='\t')
    for index in range(len(items.weight)):
        print(f'{index + 1}', end='\t')
    print()

    print('PESO', end='\t')
    for weight in items.weight:
        print(f'{weight}', end='\t')
    print()

    print('VALOR', end='\t')
    for value in items.value:
        print(f'{value}', end='\t')

    print()

    print(f'CAPACIDADE MÁXIMA DA MOCHILA: {capacity}')
    print()

'''
class HillClimbing:

    def __init__(self):
'''
#   ETAPA 2 - REPRESENTAÇÃO E AVALIAÇÃO DE UMA SOLUÇÃO

#   TESTE 1 - MOCHILA VAZIA
candidataInicial = Node([0] * 15)
mochila = Knapsack(candidataInicial)
configuracao = mochila.start.candidate
pesoTotal = mochila.totalWeight
valorTotal = mochila.totalValue
capacidade = mochila.capacity

print(f'=================================TESTES DA ETAPA 2================================')

print(f'ITENS DISPONÍVEIS')
imprimirItens(mochila.items, capacidade)
print(f'=================================MOCHILA VAZIA====================================')

print(f'CONFIGURAÇÃO ATUAL DA MOCHILA: {configuracao}')
print(f'PESO TOTAL DOS ITENS NA MOCHILA: {pesoTotal}')
print(f'VALOR TOTAL DOS ITENS NA MOCHILA: {valorTotal}')

print()

#   TESTE 2 - CANDIDATA VIÁVEL
candidataInicial = Node([1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1])
mochila = Knapsack(candidataInicial)
configuracao = mochila.start.candidate
pesoTotal = mochila.totalWeight
valorTotal = mochila.totalValue

print(f'=================================CANDIDATA VIÁVEL=================================')
print(f'CONFIGURAÇÃO ATUAL DA MOCHILA: {configuracao}')
print(f'PESO TOTAL DOS ITENS NA MOCHILA: {pesoTotal}')
print(f'VALOR TOTAL DOS ITENS NA MOCHILA: {valorTotal}')

print()

#   TESTE 2 - CANDIDATA QUE ULTRAPASSA A CAPACIDADE MÁXIMA
candidataInicial = Node([0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1])
mochila = Knapsack(candidataInicial)
configuracao = mochila.start.candidate
pesoTotal = mochila.totalWeight
valorTotal = mochila.totalValue

print(f'=======CANDIDATA QUE ULTRAPASSA A CAPACIDADE MÁXIMA DA MOCHILA====================')
print(f'CONFIGURAÇÃO ATUAL DA MOCHILA: {configuracao}')
print(f'PESO TOTAL DOS ITENS NA MOCHILA: {pesoTotal if pesoTotal != -1 else 'inválido (peso excede a capacidade)'}')
print(f'VALOR TOTAL DOS ITENS NA MOCHILA: {valorTotal if pesoTotal != -1 else 'inválido (peso excede a capacidade)'}')

print('\n')

#   ETAPA 3 - DEFINIÇÃO DA VIZINHANÇA

print(f'=================================TESTES DA ETAPA 3================================')
candidataInicial = Node([0, 1, 1, 0])
items = Items([63, 21, 2, 32], [13, 2, 20, 10])
capacidade = 70
mochila = Knapsack(candidataInicial, items, capacidade)
configuracao = mochila.start.candidate
pesoTotal = mochila.totalWeight
valorTotal = mochila.totalValue

print(f'ITENS DISPONÍVEIS')
imprimirItens(mochila.items, capacidade)

print(f'=================================CANDIDATA VIÁVEL=================================')
print(f'CONFIGURAÇÃO ATUAL DA MOCHILA: {configuracao} ', end='')
print(f'PESO TOTAL DOS ITENS NA MOCHILA: {pesoTotal} ', end='')
print(f'VALOR TOTAL DOS ITENS NA MOCHILA: {valorTotal}\n')
print(f'VIZINHANÇA DA CANDIDATA ATUAL: ')
vizinhanca = mochila.neighbours(candidataInicial)
print(f'TOTAL DE VIZINHAS: {len(vizinhanca)}\n')

for neighbour in vizinhanca:
    print(f'VIZINHA {neighbour.start.candidate}:', end='  ')
    print(f'PESO TOTAL DOS ITENS: {neighbour.totalWeight}', end='  ')
    print(f'VALOR TOTAL DOS ITENS: {neighbour.totalValue}', end='  ')
    print(f'PAI DESTA VIZINHA: {neighbour.start.parent.candidate}')
print()

#   ETAPA 4 - IMPLEMENTAÇÃO DO HILL CLIMBING
print(f'=================================TESTES DA ETAPA 4================================')


def hillClimbing(knapsack : Knapsack):
    '''SOLUCIONA O PROBLEMA DA MOCHILA UTILIZANDO O ALGORITMO SUBIDA DE ENCOSTA'''

    #   VERIFICA SE A SOLUÇÃO É VIÁVEL
    if knapsack.isViable(knapsack.totalWeight):
        initialCandidate = knapsack.start.candidate
        initialWeight = knapsack.totalWeight
        initialValue = knapsack.totalValue

        currentNode = knapsack.start
        currentCandidate = initialCandidate

        goalFunctionEvaluations = 0

        items = knapsack.items
        capacity = knapsack.capacity

        print(f'CONFIGURAÇÃO INICIAL DA MOCHILA: {initialCandidate} ', end='')
        print(f'PESO TOTAL DOS ITENS NA MOCHILA: {initialWeight} ', end='')
        print(f'VALOR TOTAL DOS ITENS NA MOCHILA: {initialValue}\n')

        currentKnapsack = knapsack

        #   GERAÇÃO DAS VIZINHAS VIÁEVIS
        neighbourhood = currentKnapsack.neighbours(currentNode)

        totalHighestValue = currentKnapsack.totalValue
        existsHighestValue = True

        while existsHighestValue:
            remainingEvals = len(neighbourhood)

            print(f'VIZINHANÇA DA CANDIDATA ATUAL: ')

            #   ESCOLHA DA VIZINHA COM O MAIOR VALOR TOTAL
            for neighbour in neighbourhood:

                #   EXPANDE A VIZINHANÇA DA CANDIDATA COM O MAIOR VALOR TOTAL
                neighbourhood = currentKnapsack.neighbours(currentNode)
                currentNode = currentKnapsack.start
                print(f'VIZINHA {neighbour.start.candidate}: ', end='')
                print(f'PESO TOTAL DOS ITENS: {neighbour.totalWeight} ', end='')
                print(f'VALOR TOTAL DOS ITENS: {neighbour.totalValue}')

                goalFunctionEvaluations += 1

                #   SE A VIZINHA ATUAL TIVER UM VALOR TOTAL MAIOR DO QUE O MAIOR VALOR ENCONTRADO
                if neighbour.totalValue > totalHighestValue:
                    currentKnapsack = neighbour
                    totalHighestValue = currentKnapsack.totalValue

                #   SE A VIZINHA ATUAL TIVER UM VALOR TOTAL IGUAL AO MAIOR VALOR ENCONTRADO (EMPATE POR VALOR)
                elif neighbour.totalValue == totalHighestValue:

                    #   SE A VIZINHA ATUAL TIVER O MENOR PESO TOTAL OU O MESMO PESO DA OUTRA (EMPATE POR PESO)
                    if neighbour.totalWeight <= currentKnapsack.totalWeight:
                        currentKnapsack = neighbour
                        totalHighestValue = currentKnapsack.totalValue

                    #   SE A OUTRA VIZINHA TIVER O MENOR PESO TOTAL
                    else:
                        totalHighestValue = neighbour.totalValue

                #   SE A VIZINHA ATUAL NÃO MELHORAR O RESULTADO
                else:
                    remainingEvals -= 1

            print()

            #   SE NÃO EXISTIR UMA MELHORA NO VALOR TOTAL
            if remainingEvals == 0:
                print(f'NÃO HÁ MAIS MELHORAS PARA A FUNÇÃO OBJETIVO! ENCERRANDO O ALGORITMO\n')
                existsHighestValue = False

            #   SE EXISTIR UMA MELHORA NO VALOR TOTAL
            else:
                print(f'CANDIDATA COM O MAIOR VALOR TOTAL SELECIONADA: {currentKnapsack.start.candidate}')
                print(f'PESO TOTAL DOS ITENS DA CANDIDATA SELECIONADA: {currentKnapsack.totalWeight} ', end='')
                print(f'VALOR TOTAL DOS ITENS DA CANDIDATA SELECIONADA: {currentKnapsack.totalValue}\n')



        print(f'NÚMERO DE AVALIAÇÕES DA FUNÇÃO OBJETIVO: {goalFunctionEvaluations}\n')

        return currentKnapsack

    #   SE NÃO FOR UMA SOLUÇÃO VIÁVEL
    else:
        zerolist = [0] * len(knapsack.items.value)

        #   RETORNA UMA MOCHILA VAZIA SEM ITENS PARA SELEÇÃO
        return Knapsack(Node(zerolist), Items(zerolist, zerolist), 0)

candidataInicial = Node([0, 0, 0, 1, 0, 0])
items = Items([80, 19, 37, 56, 41, 42], [14, 7, 2, 2, 4, 3])
capacidade = 150                                                                            #   CAPACIDADE ARBITRÁRIA
mochila = Knapsack(candidataInicial, items, capacidade)

print(f'ITENS DISPONÍVEIS')
imprimirItens(mochila.items, capacidade)

print(f'==================EXECUTANDO O ALGORITMO HILL CLIMBING (SUBIDA DE ENCOSTA):===========')
mochilaComMaiorValorTotal = hillClimbing(mochila)

candidataComMaiorValor = mochilaComMaiorValorTotal.start.candidate
pesoTotal = mochilaComMaiorValorTotal.totalWeight
valorTotal = mochilaComMaiorValorTotal.totalValue

print(f'MOCHILA COM MAIOR VALOR ENCONTRADO: {candidataComMaiorValor} ', end='')
print(f'PESO TOTAL DOS ITENS NA MOCHILA: {pesoTotal} ', end='')
print(f'VALOR TOTAL DOS ITENS NA MOCHILA: {valorTotal}\n')