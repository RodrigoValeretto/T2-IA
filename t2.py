import random
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


class vertice:
    def __init__(self, index, x, y):
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
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))


class adj:
    def __init__(self, v, d):
        # v1 é o primeiro vertice da aresta
        # v2 é o segundo vertice da aresta
        # d é a distância da aresta
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

    def __eq__(self, other):
        return self._v.x == other.v.x and self._v.y == other.v.y and self._d == other.d

    def __hash__(self):
        return hash(str(self))


def getDist(adj):
    # Função usada para ordenação de arestas
    return adj.d


def printList(list):
    for i in list:
        print(i)


def encontraCaminho(G, antecessores, s, f):
    v = f
    caminho = [G[f]]

    while(v != s):
        v = antecessores[v]
        caminho.insert(0, G[v])
    return caminho


def generateKNN(v, k, seed=None):
    # v é o número de vértices à serem gerados, k é o número de vizinhos que cada vértice terá
    # e seed é a semente utilizada para a geração aleatória
    random.seed(seed)
    grafo = []  # Corresponde ao nosso grafo, sendo ele uma lista de vertices
    xyArray = []
    AdjList = []

    cont = 0
    while len(xyArray) != v:
        x = random.randint(0, v)
        y = random.randint(0, v)
        if([x, y] not in xyArray):
            xyArray.append([x, y])
            grafo.append(vertice(cont, x, y))
            AdjList.append([])
            cont += 1

    distMatrix = distance_matrix(xyArray, xyArray)  # linhas x colunas

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


def buscaLargura(G, AdjList, s, f):
    # Função de busca em largura
    # Recebe o vertice inicial s e o vertice final f
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    fila = [s]
    antecessores = []

    for _ in range(0, len(G)):
        antecessores.append(None)

    vi = None
    while(len(fila) != 0):
        vi = fila.pop(0)
        if(vi == f):
            print("Busca concluída: caminho encontrado!")
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                marked.append(w.v.index)
                fila.append(w.v.index)
                antecessores[w.v.index] = vi
    print('Busca concluída: não foi possível encontrar um caminho!')


def buscaProfundidade(G, AdjList, s, f):
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    pilha = [s]
    antecessores = []

    for _ in range(0, len(G)):
        antecessores.append(None)

    vi = None
    while(len(pilha) != 0):
        vi = pilha.pop()
        if(vi == f):
            print("Busca concluída: caminho encontrado!")
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                marked.append(w.v.index)
                pilha.append(w.v.index)
                antecessores[w.v.index] = vi
    print('Busca concluída: não foi possível encontrar um caminho!')


def buscaAstar(G, AdjList, distMatrix, s, f):
    # Função de busca em largura
    # Recebe o vertice inicial s e o vertice final f
    print('Buscando', G[f], 'a partir de', str(G[s]) + '...')
    marked = [s]
    fila = [s]
    antecessores = []

    for _ in range(0, len(G)):
        antecessores.append(None)

    vi = None
    while(len(fila) != 0):
        vi = fila.pop(0)
        if(vi == f):
            print("Busca concluída: caminho encontrado!")
            printList(antecessores)
            caminho = encontraCaminho(G, antecessores, s, f)
            return caminho
        for w in AdjList[vi]:
            woptions = []
            if(w.v.index not in marked):
                woptions.append(w.v.index)
                marked.append(w.v.index)
                fila.append(w.v.index)
                antecessores[w.v.index] = vi
    print('Busca concluída: não foi possível encontrar um caminho!')


# Rotina principal
# Gera o grafo knn e uma matriz de distância entre os vértices
grafo, AdjList, distMatrix = generateKNN(10, 3, 1)

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
        ax.plot(xData, yData, color='red')

ax.scatter(xScatter, yScatter, color='red')
# ax.set_xlim(-0.5)
# ax.set_ylim(-0.5)
ax.grid(True)


# Inicia algoritmos de busca
print("inicia busca")
inicio = 0
fim = 4

caminho = buscaLargura(grafo, AdjList, inicio, fim)
#caminho = buscaProfundidade(grafo, AdjList, inicio, fim)

ax.scatter(grafo[inicio].x, grafo[inicio].y, color='blue')
ax.scatter(grafo[fim].x, grafo[fim].y, color='green')

# Plot do caminho da busca em largura
if(caminho):
    for i in range(0, len(caminho)-1):
        xData = [caminho[i].x, caminho[i+1].x]
        yData = [caminho[i].y, caminho[i+1].y]
        ax.plot(xData, yData, color='black')

# Funções para visualização do grafo
# print('grafo')
# printList(grafo)
plt.show()


# Existe um erro ao plotar, que as vezes exibe uma aresta que não existe
# deve estar relacionado com a marcação dos antecessores de um vertice
