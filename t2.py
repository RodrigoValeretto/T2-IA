import random
import time
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


class vertice:
    def __init__(self, index, x, y):
        # index é o indice do vertice no grafo
        # x é a posição do ponto no plano horizontal
        # y é a posição do ponto no plano vertical
        self._index = index
        self._x = x
        self._y = y

    # getters da classe
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def index(self):
        return self._index

    # setters da classe
    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @index.setter
    def index(self, index):
        self._index = index

    # definição da string gerada pela classe
    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ')'

    # sobrecarga do operador ==
    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    # Definindo hash para a classe
    def __hash__(self):
        return hash(str(self))


class adj:
    def __init__(self, v, d):
        # v é o vertice adjacente
        # d é a distância desse vértice
        self._v = v
        self._d = d

    # getters da classe
    @property
    def v(self):
        return self._v

    @property
    def d(self):
        return self._d

    # setters da classe
    @v.setter
    def v(self, v):
        self._v = v

    @d.setter
    def d(self, d):
        self._d = d

    # definição da string gerada pela classe
    def __str__(self):
        return str(self._v) + ' - ' + str(self._d)

    # sobrecarga do operador ==
    def __eq__(self, other):
        return self._v == other.v and self._d == other.d

    # Definindo hash para a classe
    def __hash__(self):
        return hash(str(self))


def getDist(adj):
    # Função usada para ordenação de adjacentes
    return adj.d


def printList(list):
    # Função de auxílio, utilizada apenas para debug do código
    for i in list:
        print(i)


def encontraCaminho(G, antecessores, s, f):
    # Função responsável por encontrar o caminho
    # encontrado pela busca entre os vertices de índice s e f
    v = f
    caminho = [G[f]]
    distPerc = 0

    while(v != s):
        distPerc += distMatrix[v, antecessores[v]]
        v = antecessores[v]
        caminho.insert(0, G[v])
    return caminho


def ordA(distPercVet, distMatrix, w, f):
    # Ordenação utilizada para busca A, nesse caso, para a heuristica
    # multiplicamos o valor da distância euclidiana do vertice em questão até o
    # vertice buscado pela distancia percorrida desde o vertice inicial até o atual
    # somado a 1 (para evitar que g seja zero e o valor tenda a zero)
    g = distPercVet[w]
    return g + distMatrix[w, f]*(g + 1)


def generateKNN(v, k, seed=None):
    # Função responsável pela geração do grafo KNN
    # v é o número de vértices à serem gerados
    # k é o número mínimo de vizinhos que cada vértice terá
    # seed é a semente (número inteiro ou vazio) utilizada para a geração aleatória

    # Verifica se v é maior que k
    if(v < k):
        print('ERRO: Valor de v menor que o valor de k!')
        exit()

    random.seed(seed)
    grafo = []  # Corresponde ao nosso grafo, sendo ele uma lista de vertices
    xyArray = []
    AdjList = []  # lista de adjacências do nosso grafo

    cont = 0
    while len(xyArray) != v:
        x = random.randint(0, v)
        y = random.randint(0, v)
        if([x, y] not in xyArray):
            xyArray.append([x, y])
            grafo.append(vertice(cont, x, y))
            AdjList.append([])
            cont += 1

    distMatrix = distance_matrix(xyArray, xyArray)

    for i in range(0, v):
        kmenores = []
        for j in range(0, v):
            if(i == j):
                continue
            elif(len(kmenores) < k):
                kmenores.append(
                    adj(grafo[j], distMatrix[i, j]))
                kmenores.sort(key=getDist)
            else:
                if(distMatrix[i, j] < kmenores[k-1].d):
                    kmenores[k-1] = adj(grafo[j], distMatrix[i, j])
                    kmenores.sort(key=getDist)
        for j in kmenores:
            if(j not in AdjList[i]):
                AdjList[i].append(j)
                AdjList[j.v.index].append(
                    adj(grafo[i], distMatrix[j.v.index, i]))
    return grafo, AdjList, distMatrix


def buscaLargura(G, AdjList, distMatrix, s, f):
    # Função de busca em largura
    # Recebe o indice do vértice inicial s e o indice do vertice final f
    # Também recebe o grafo G e a lista de adjacência dos vértices
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    fila = [s]
    antecessores = []
    distPercVet = []

    for _ in range(0, len(G)):
        antecessores.append(None)
        distPercVet.append(0)

    vi = None
    it = 0
    while(len(fila) != 0):
        vi = fila.pop(0)
        if(vi == f):
            print("Busca concluída: caminho encontrado em", it, "iterações!")
            print("Tamanho total do caminho:", distPercVet[f])
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                marked.append(w.v.index)
                fila.append(w.v.index)
                antecessores[w.v.index] = vi
                distPercVet[w.v.index] = distPercVet[vi] + \
                    distMatrix[vi, w.v.index]
        it += 1
    print('Busca concluída: não foi possível encontrar um caminho em', it, 'iterações!')


def buscaProfundidade(G, AdjList, distMatrix, s, f):
    # Função de busca em profundidade
    # Recebe o indice do vértice inicial s e o indice do vertice final f
    # Também recebe o grafo G e a lista de adjacência dos vértices
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    pilha = [s]
    antecessores = []
    distPercVet = []

    for _ in range(0, len(G)):
        antecessores.append(None)
        distPercVet.append(0)

    vi = None
    it = 0
    while(len(pilha) != 0):
        vi = pilha.pop()
        if(vi == f):
            print("Busca concluída: caminho encontrado em", it, "iterações!")
            print("Tamanho total do caminho:", distPercVet[f])
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                marked.append(w.v.index)
                pilha.append(w.v.index)
                antecessores[w.v.index] = vi
                distPercVet[w.v.index] = distPercVet[vi] + \
                    distMatrix[vi, w.v.index]
        it += 1
    print('Busca concluída: não foi possível encontrar um caminho em', it, 'iterações!')


def buscaDjikstra(G, AdjList, distMatrix, s, f):
    # Função de busca utilizando algoritmo djikstra (best first)
    # Recebe o indice do vértice inicial s e o indice do vertice final f
    # Também recebe o grafo G, a lista de adjacência dos vértices e
    # a matriz com as distâncias euclidianas entre os vértices
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    fila = [s]
    antecessores = []
    distPercVet = []

    for _ in range(0, len(G)):
        antecessores.append(None)
        distPercVet.append(0)

    vi = None
    it = 0
    while(len(fila) != 0):
        vi = fila.pop(0)
        if(vi == f):
            print("Busca concluída: caminho encontrado em", it, "iterações!")
            print("Tamanho total do caminho:", distPercVet[f])
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                fila.append(w.v.index)
                marked.append(w.v.index)
                antecessores[w.v.index] = vi
                distPercVet[w.v.index] = distPercVet[vi] + \
                    distMatrix[vi, w.v.index]
            else:
                newDist = distPercVet[vi] + distMatrix[vi, w.v.index]
                oldDist = distPercVet[w.v.index]
                if(newDist < oldDist):
                    antecessores[w.v.index] = vi
                    distPercVet[w.v.index] = newDist
        fila.sort(key=lambda w: distPercVet[w])
        it += 1
    print('Busca concluída: não foi possível encontrar um caminho em', it, 'iterações!')


def buscaA(G, AdjList, distMatrix, s, f):
    # Função de busca A
    # Recebe o indice do vértice inicial s e o indice do vertice final f
    # Também recebe o grafo G, a lista de adjacência dos vértices e
    # a matriz com as distâncias euclidianas entre os vértices
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    fila = [s]
    antecessores = []
    distPercVet = []

    for _ in range(0, len(G)):
        antecessores.append(None)
        distPercVet.append(0)

    vi = None
    it = 0
    while(len(fila) != 0):
        vi = fila.pop(0)
        if(vi == f):
            print("Busca concluída: caminho encontrado em", it, "iterações!")
            print("Tamanho total do caminho:", distPercVet[f])
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                fila.append(w.v.index)
                marked.append(w.v.index)
                antecessores[w.v.index] = vi
                distPercVet[w.v.index] = distPercVet[vi] + \
                    distMatrix[vi, w.v.index]
        fila.sort(key=lambda w: ordA(distPercVet, distMatrix, w, f))
        it += 1
    print('Busca concluída: não foi possível encontrar um caminho em', it, 'iterações!')


def buscaAstar(G, AdjList, distMatrix, s, f):
    # Função de busca A estrela
    # Recebe o indice do vértice inicial s e o indice do vertice final f
    # Também recebe o grafo G, a lista de adjacência dos vértices e
    # a matriz com as distâncias euclidianas entre os vértices
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    fila = [s]
    antecessores = []
    distPercVet = []

    for _ in range(0, len(G)):
        antecessores.append(None)
        distPercVet.append(0)

    vi = None
    it = 0
    while(len(fila) != 0):
        vi = fila.pop(0)
        if(vi == f):
            print("Busca concluída: caminho encontrado em", it, "iterações!")
            print("Tamanho total do caminho:", distPercVet[f])
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                fila.append(w.v.index)
                marked.append(w.v.index)
                antecessores[w.v.index] = vi
                distPercVet[w.v.index] = distPercVet[vi] + \
                    distMatrix[vi, w.v.index]
            else:
                newDist = distPercVet[vi] + distMatrix[vi, w.v.index]
                oldDist = distPercVet[w.v.index]
                if(newDist < oldDist):
                    antecessores[w.v.index] = vi
                    distPercVet[w.v.index] = newDist
        fila.sort(key=lambda w: distPercVet[w] + distMatrix[w, f])
        it += 1
    print('Busca concluída: não foi possível encontrar um caminho em', it, 'iterações!')


# Rotina principal
# Gera o grafo knn, a lista de adjacências e uma matriz de distância entre os vértices
# Não é possível gerar um grafo com um v < k, o programa vai finalizar caso aconteça
print("Gerando grafo KNN...")
grafo, AdjList, distMatrix = generateKNN(300, 5, 74)
print("Grafo gerado!")

# Indices dos vertices para os algoritmos de busca
inicio = 0
fim = 12

# Inicia cálculo do tempo
startTime = time.time()

# Algoritmos de busca (testar um algoritmo por execução)
#caminho = buscaLargura(grafo, AdjList, distMatrix, inicio, fim)
#caminho = buscaProfundidade(grafo, AdjList, distMatrix, inicio, fim)
#caminho = buscaDjikstra(grafo, AdjList, distMatrix, inicio, fim)
#caminho = buscaA(grafo, AdjList, distMatrix, inicio, fim)
caminho = buscaAstar(grafo, AdjList, distMatrix, inicio, fim)

# Finaliza contagem de tempo e a exibe
endTime = time.time()
print("Tempo de busca:", endTime - startTime)

print("Plotando grafo...")
# Faz o plot do grafo
xScatter = []
yScatter = []

fig, ax = plt.subplots()

for i in grafo:
    xScatter.append(i.x)
    yScatter.append(i.y)
    for j in AdjList[i.index]:
        xData = [i.x, j.v.x]
        yData = [i.y, j.v.y]
        ax.plot(xData, yData, color='pink')

ax.scatter(xScatter, yScatter, color='palevioletred', zorder=90)
# ax.set_xlim(-0.5)
# ax.set_ylim(-0.5)
ax.grid(True)

# Plot dos vértices de inicio e fim
ax.scatter(grafo[inicio].x, grafo[inicio].y, color='royalblue', zorder=100)
ax.scatter(grafo[fim].x, grafo[fim].y, color='lime', zorder=100)

# Plot do caminho encontrado na busca (caso seja bem sucedido)
xScatter.clear()
yScatter.clear()
if(caminho):
    for i in range(0, len(caminho)-1):
        xData = [caminho[i].x, caminho[i+1].x]
        yData = [caminho[i].y, caminho[i+1].y]
        ax.plot(xData, yData, color='black', zorder=97)
    for i in caminho:
        xScatter.append(i.x)
        yScatter.append(i.y)
    ax.scatter(xScatter, yScatter, color='yellow', zorder=96)

# Funções para visualização do grafo
# print('grafo')
# printList(grafo)
plt.show()
