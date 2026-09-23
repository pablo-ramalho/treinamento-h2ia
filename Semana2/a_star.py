# PSEUDOCÓDIGO
# FRONTEIRA = ESTADO_INICIAL                    (a estrutura de dados é uma FILA)
# VISITADOS = VAZIO                             (a estrutura de dados é um CONJUNTO)
#
# FAÇA                                          (laço de repetição)
#
#   SE FRONTEIRA ESTÁ VAZIA
#       RETORNE SOLUÇÃO_VAZIA
#
#   NO_ATUAL = REMOVA NÓ DO INÍCIO DA FILA
#
#   SE NO_ATUAL FOR O OBJETIVO (GOAL)
#       RETORNE NO_ATUAL
#
#   ADICIONE NO_ATUAL AO CONJUNTO VISITADOS
#   EXPANDA NO_ATUAL E ARMAZENE SEUS VIZINHOS NA FRONTEIRA
#
##########################################################################################

#   STATE REPRESENTA A SITUAÇÃO ATUAL DO AGENTE NO AMBIENTE (EXEMPLO: COORDENADAS DO AGENTE NUMA DETERMINADA CONFIGURAÇÃO)
#   STATE É UMA TUPLA DE 9 ELEMENTOS. CADA ELEMENTO DA TUPLA É UM NÚMERO QUE REPRESENTA A PEÇA LOCALIZADA NA CÉLULA ESPECÍFICA (OU UMA CÉLULA VAZIA SE FOR None)
#
#   PARENT É O NÓ PAI DO NÓ A PARTIR DO QUAL CHEGOU NO NÓ ATUAL
#
#   ACTION É UMA AÇÃO A SER REALIZADA A PARTIR DO ESTADO ATUAL
#   ACTION É UMA TUPLA DA FORMA (direction, (celula1, celula2, celula3, celula4, celula5, celula6, celula7, celula8, celula9))
#   ONDE:
#   direction => A DIREÇÃO DA PEÇA QUE PODERÁ SE DESLOCAR PARA PREENCHER A CÉLULA VAZIA (TORNANDO A PEÇA DESLOCADA A NOVA CÉLULA VAZIA)
#                A DIREÇÃO TEM RELAÇÃO COM A AÇÃO (action), OU SEJA, SÓ SÃO VÁLIDOS: 'DOWN', 'UP', 'LEFT' ou 'RIGHT'
#   row       => A LINHA DA PEÇA ADJACENTE À CÉLULA VAZIA
#   column    => A COLUNA DA PEÇA ADJACENTE À CÉLULA VAZIA
#   OU SEJA, A TUPLA (celula1, celula2, celula3, celula4, celula5, celula6, celula7, celula8, celula9) CORRESPONDE AO ESTADO (state)
#
#   DIREÇÕES VÁLIDAS:
#   'down' => DESLOCA A PEÇA PARA BAIXO
#   'up'   => DESLOCA A PEÇA PARA CIMA
#   'left' => DESLOCA A PEÇA PARA A ESQUERDA
#   'right'=> DESLOCA A PEÇA PARA A DIREITA
import time

class Node:

    def __init__(self, state, parent, action, goal, offset=None, swapped=None):
        """
        STATE   => TUPLA DA FORMA (celula1, celula2, celula3, celula4, celula5, celula6, celula7, celula8, celula9)
        PARENT  => NÓ QUE GEROU O NÓ ATUAL
        ACTION  => STRING CONTENDO AS SEGUINTES DIREÇÕES VÁLIDAS:
                    'down' (PARA BAIXO)\n
                    'up' (PARA CIMA)\n
                    'left' (PARA A ESQUERDA)\n
                    'right' (PARA A DIREITA)
        GOAL    => ESTADO OBJETIVO
        OFFSET  => ÍNDICE DE DESLOCAMENTO RELATIVO AO MOVIMENTO DA CÉLULA VAZIA NO ESTADO ATUAL
        SWAPPED => ÍNDICE ANTIGO DA CÉLULA VAZIA NO ESTADO ATUAL
        """
        self.state = state
        self.parent = parent
        self.action = action

        if parent is None:
            self.g = 0

        else:
            self.g = self.parent.g + 1

        self.calculateEstimatedCost(goal, offset, swapped)

    def calculateEstimatedCost(self, goal, offset=None, swapped=None):
        xi = lambda i : i // 3
        xGOAL = lambda i : goal.index(self.state[i]) // 3
        yi = lambda i : i % 3
        yGOAL = lambda i : goal.index(self.state[i]) % 3
        MANHATTAN = lambda x, xGOAL, y, yGOAL: abs(x - xGOAL) + abs(y - yGOAL)

        self.h = 0

        """CALCULA A DISTÂNCIA DE MANHATTAN PARA CADA PEÇA E ARMAZENA O RESULTADO EM h DO NÓ ATUAL (node.h)"""
        for i in range(len(self.state)):

            if self.state[i] is not None:
                x = xi(i)
                xG = xGOAL(i)
                y = yi(i)
                yG = yGOAL(i)
                dMANHATTAN = MANHATTAN(x, xG, y, yG)

                self.h += dMANHATTAN

        """CALCULA A DISTÂNCIA ANTIGA (dOLD) E A DISTÂNCIA NOVA (dNEW) PARA CALCULAR A NOVA HEURÍSTICA PARA O NÓ ATUAL"""
        if offset is not None and self.parent is not None:
            dOLD = MANHATTAN(xi(swapped), xGOAL(offset),
                             yi(swapped), yGOAL(offset))
            dNEW = MANHATTAN(xi(offset), xGOAL(offset),
                             yi(offset), yGOAL(offset))

            self.h = self.h - dOLD + dNEW

        self.f = self.g + self.h

class Frontier:

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def containsState(self, state):

        for node in self.frontier:

            if node.state == state:
                return True

        return False

    def remove(self):

        if self.empty():
            raise Exception("NÃO HÁ ELEMENTOS NA FRONTEIRA PARA REMOVER")

        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

    def empty(self):
        return len(self.frontier) == 0

class Board:

    def __init__(self, cell=(1, 6, 5, 7, 3, 8, None, 4, 2)):
        self.solution = None

        digit = {1, 2, 3, 4, 5, 6, 7, 8}

        #   VERIFICA SE AS CÉLULAS DO TABULEIRO CONTÉM VALORES VÁLIDOS (ENUMERAÇÕES DE 1 A 8 E NONE, QUE CORRESPONDE A UMA CÉLULA VAZIA)
        if None not in cell and not any(digit for position in cell):
            raise Exception("TABULEIRO INVÁLIDO")

        #   CASO CONTENHA VALORES VÁLIDOS ATRIBUI A CÉLULA PASSADA COMO PARÂMETRO PARA O ATRIBUTO cell DESTA CLASSE
        self.cell = cell

        #   DEFINE O ESTADO ATUAL DO TABULEIRO (LEMBRANDO, É UMA TUPLA DE 9 ELEMENTOS)
        self.start = self.cell[:9]

        #   DEFINE O ESTADO OBJETIVO (GOAL) COM A CÉLULA VAZIA NA ÚLTIMA POSIÇÃO
        self.goal = (1, 2, 3, 4, 5, 6, 7, 8, None)

        print('ESTADO INICIAL:')
        self.imprimirEstado(self.start)
        print()

        print('ESTADO OBJETIVO:')
        self.imprimirEstado(self.goal)

    def imprimirEstado(self, state):
        isFirstColumnIndex = lambda index: (index + 1) % 3 == 0

        digit = {1, 2, 3, 4, 5, 6, 7, 8}

        for index in range(len(state)):

            if state[index] in digit:
                print(state[index], end='\t')

            if state[index] is None:
                print(' ', end='\t')

            if isFirstColumnIndex(index):
                print()

    def imprimirDirecoes(self, actions):
        stepsNumber = 0

        for index in range(len(actions)):

            if actions[index] == 'down':
                print(f'BAIXO {'-> ' if index < len(actions) - 1 else ''}', end='')

            elif actions[index] == 'up':
                print(f'CIMA {'-> ' if index < len(actions) - 1 else ''}', end='')

            elif actions[index] == 'left':
                print(f'ESQUERDA {'-> ' if index < len(actions) - 1 else ''}', end='')

            else:
                print(f'DIREITA {'-> ' if index < len(actions) - 1 else ''}', end='')

            stepsNumber += 1

        print('\n')
        print(f'NÚMERO DE MOVIMENTOS: {stepsNumber}')

    def immprimirFronteira(self, frontier):

        print(f'FRONTEIRA:')

        for node in frontier:
            print(f'Estado: {node.state}\tMovimento: {node.action if node.action is not None else 'nenhum'}\tCusto f: {node.f}\tCusto g: {node.g}\tCusto h: {node.h}')

        print()

    def movements(self, currentNode):
        """CRIA O MODELO DE TRANSIÇÃO (result/RESULTADO)"""

        # ESTADO DO NÓ ATUAL
        state = currentNode.state[:9]

        # INDICE ONDE ESTÁ LOCALIZADA A CÉLULA VAZIA
        noneIndex = state.index(None)

        LINE = lambda : noneIndex // 3
        COLUMN = lambda : noneIndex % 3
        BAIXO = lambda line, column: ((LINE() + 1) * 3) + COLUMN()
        CIMA = lambda line, column: ((LINE() - 1) * 3) + COLUMN()
        ESQUERDA = lambda line, column: (LINE() * 3) + (COLUMN() - 1)
        DIREITA = lambda line, column: (LINE() * 3) + (COLUMN() + 1)

        # AÇÕES VÁLIDAS: 'down', 'up', 'left' e 'right'

        result = []

        #   MOVER A CÉLULA VAZIA PARA BAIXO
        if LINE() + 1 < 3:
            offset = BAIXO(LINE(), COLUMN())
            step = ('down', ((state[:noneIndex]) + (state[offset],) + (state[noneIndex + 1:offset]) + (None,) + (state[offset+1:])))
            swapped = step[1].index(None)
            Node(step[1], currentNode, step[0], self.goal, offset, swapped)
            result.append(step)

        #   MOVER A CÉLULA VAZIA PARA CIMA
        if LINE() - 1 >= 0:
            offset = CIMA(LINE(), COLUMN())
            step = ('up', ((state[:offset]) + (None,) + (state[offset + 1:noneIndex]) + (state[offset],) + (state[noneIndex + 1:])))
            swapped = step[1].index(None)
            Node(step[1], currentNode, step[0], self.goal, offset, swapped)
            result.append(step)

        #   MOVER A CÉLULA VAZIA PARA A ESQUERDA
        if COLUMN() - 1 >= 0:
            offset = ESQUERDA(LINE(), COLUMN())
            step = ('left', ((state[:offset]) + (None,) + (state[offset],) + (state[noneIndex + 1:])))
            swapped = step[1].index(None)
            Node(step[1], currentNode, step[0], self.goal, offset, swapped)
            result.append(step)

        #   MOVER A CÉLULA VAZIA PARA A DIREITA
        if COLUMN() + 1 < 3:
            offset = DIREITA(LINE(), COLUMN())
            step = ('right', ((state[:noneIndex]) + (state[offset],) + (None,) + (state[offset + 1:])))
            swapped = step[1].index(None)
            Node(step[1], currentNode, step[0], self.goal, offset, swapped)
            result.append(step)

        return result

    def a_star(self):
        """ENCONTRA A SOLUÇÃO (SE EXISTIR)"""

        #   CONTA A QUANTIDADE DE NÓS EXPLORADOS
        self.exploredCount = 0
        totalNodesCount = 0
        pathCost = 0

        start = Node(state=self.start, parent=None, action=None, goal=self.goal)
        frontier = Frontier()
        frontier.add(start)

        self.explored = set()

        while True:

            if frontier.empty():
                raise Exception("A FRONTEIRA DE BUSCA ESTÁ VAZIA. NÃO EXISTE SOLUÇÃO!")

            #   REMOVE O NÓ DO INÍCIO DA FRONTEIRA (É UMA FILA)
            node = frontier.remove()
            self.exploredCount += 1

            #   CHECA SE É UM ESTADO OBJETIVO (GOAL)
            if node.state == self.goal:
                actions = []
                cells = []

                #   PERCORRE A BUSCA DO NÓ ATUAL ATÉ O NÓ QUE REFERENCIA O ESTADO INICIAL
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent

                #   INVERTE AS LISTAS DOS COMPONENTES DA SOLUÇÃO PARA QUE A LISTA CONTENHA AS AÇÕES E ESTADOS NA ORDEM CORRETA (DO INÍCIO AO FIM)
                actions.reverse()
                cells.reverse()

                #   SOLUÇÃO CONSTRUÍDA
                self.solution = (actions, cells)

                totalNodesCount = self.exploredCount + len(frontier.frontier)

                print(f'CAMINHO: ', end='')
                self.imprimirDirecoes(actions)
                print(f'ESTADOS EXPANDIDOS: {self.exploredCount}')
                print(f'CRITÉRIO DE DESEMPATE: FIFO por Ordem de inserção\n')
                print(f'INFORMAÇÕES COMPLEMENTARES')
                print(f'ESTADOS NA FRONTEIRA: {len(frontier.frontier)}')
                print(f'TOTAL DE ESTADOS: {totalNodesCount}\n')

                return

            #   ADICIONA O NÓ ATUAL À LISTA DE NÓS VISITADOS
            self.explored.add(node.state)

            #   EXPANDE OS NÓS VIZINHOS (MÉTODO movements)
            for action, state in self.movements(node):
                """
                    AGORA O MÉTODO MOVEMENTS RECEBE UM NODE
                """

                if not frontier.containsState(state) and state not in self.explored:
                    childNode = Node(state=state, parent=node, action=action, goal=self.goal)
                    frontier.add(childNode)

            #   ORDENA OS NÓS DA FRONTEIRA PELO CUSTO ESTIMADO DE f = g + h (FILA DE PRIORIDADE)
            frontier.frontier.sort(key=lambda node : node.f)

        totalNodesCount = self.exploredCount + len(frontier)

        print(f'SOLUÇÃO INEXISTENTE')
        print(f'ESTADOS EXPANDIDOS: {self.exploredCount}')
        print(f'CRITÉRIO DE DESEMPATE: FIFO por Ordem de inserção\n')
        print(f'INFORMAÇÕES COMPLEMENTARES')
        print(f'ESTADOS NA FRONTEIRA: {len(frontier)}')
        print(f'TOTAL DE ESTADOS: {totalNodesCount}')

def formatTime(t):

    #   HORAS
    if t >= 3600:
        return f'{t / 3600.0:.0f}h'

    #   MINUTOS
    if t >= 60:
        return f'{t / 60.0:.0f}min'

    #   SEGUNDOS
    if t >= 1.0:
        return f'{t:.0f}s'

    #   MILISSEGUNDOS
    elif t >= 1e-3:
        return f'{t * 1e3:.0f}ms'

    #   MICROSSEGUNDOS
    elif t >= 1e-6:
        return f'{t * 1e6:.0f}µs'

    #   NANOSSEGUNDOS
    else:
        return f'{t * 1e9:.0f}ns'

print('============================================PRIMEIRA INSTÂNCIA============================================')
tabuleiro = Board((1, 2, None, 4, 5, 3, 7, 8, 6))
tempoInicio = time.perf_counter()
tabuleiro.a_star()
tempoFim = time.perf_counter()
t = tempoFim - tempoInicio
print(f'TEMPO DE EXECUÇÃO: {formatTime(t)}')

print('============================================SEGUNDA INSTÂNCIA============================================')
tabuleiro = Board((1, 5, 2, 4, 8, 3, None, 7, 6))
tempoInicio = time.perf_counter()
tabuleiro.a_star()
tempoFim = time.perf_counter()
t = tempoFim - tempoInicio
print(f'TEMPO DE EXECUÇÃO: {formatTime(t)}')

print('============================================TERCEIRA INSTÂNCIA============================================')
tabuleiro = Board((None, 8, 2, 5, 7, 3, 1, 4, 6))
tempoInicio = time.perf_counter()
tabuleiro.a_star()
tempoFim = time.perf_counter()
t = tempoFim - tempoInicio
print(f'TEMPO DE EXECUÇÃO: {formatTime(t)}')

print('============================================QUARTA INSTÂNCIA============================================')
tabuleiro = Board((8, 7, None, 5, 4, 2, 1, 6, 3))
tempoInicio = time.perf_counter()
tabuleiro.a_star()
tempoFim = time.perf_counter()
t = tempoFim - tempoInicio
print(f'TEMPO DE EXECUÇÃO: {formatTime(t)}')

print('============================================QUINTA INSTÂNCIA============================================')
tabuleiro = Board((8, 6, 7, 2, 5, 4, 3, None, 1))
tempoInicio = time.perf_counter()
tabuleiro.a_star()
tempoFim = time.perf_counter()
t = tempoFim - tempoInicio
print(f'TEMPO DE EXECUÇÃO: {formatTime(t)}')