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


def encontraCaminho(arestas, s, f):
    v1 = f
    caminho = []

    while(v1 != s):
        for i in arestas:
            if(i.v2 == v1):
                caminho.append(i)
                v1 = i.v1
    return caminho


def generateKNN(v, k, seed=None):
    # v é o número de vértices à serem gerados, k é o número de vizinhos que cada vértice terá
    # e seed é a semente utilizada para a geração aleatória
    random.seed(seed)
    grafo = []  # Corresponde ao nosso grafo, sendo ele uma lista de vertices
    AdjList = []
    xyArray = []

    for i in range(0, v):
        x = random.randint(0, v)
        y = random.randint(0, v)
        grafo.append(vertice(i, x, y))
        AdjList.append(set())
        xyArray.append([x, y])

    distMatrix = distance_matrix(
        xyArray, xyArray)  # linhas x colunas

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

        AdjList[i] = AdjList[i].union(kmenores)
        for j in kmenores:
            AdjList[j.v.index].add(adj(grafo[i], distMatrix[j.v.index, i]))
    return grafo, AdjList, distMatrix


def buscaLargura(G, s, f):
    # Função de busca em largura
    # Recebe o vertice inicial s e o vertice final f
    vf = G[f]
    marked = [s]
    fila = [s]
    arestasLidas = []

    while(len(fila) != 0):
        vi = fila.pop(0)
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                arestasLidas.append(w)
                marked.append(w.v.index)
                fila.append(w.v.index)
                if(w.v == vf):
                    print("Achou")
                    printList(arestasLidas)
                    #caminho = encontraCaminho(arestasLidas, vs, vf)
                    return  # caminho

    # printArray(marked)
    printList(arestasLidas)
    print('não achou')


def BP(G, s, f):
    vf = G[f]
    marked = [s]
    pilha = [s]
    arestasLidas = []

    while(len(pilha) != 0):
        vi = pilha.pop()
        for w in AdjList[vi]:
            if(w.v.index not in marked):
                arestasLidas.append(w)
                marked.append(w.v.index)
                pilha.append(w.v.index)
                if(w.v == vf):
                    print("Achou")
                    printList(arestasLidas)
                    #caminho = encontraCaminho(arestasLidas, vs, vf)
                    return  # caminho
        # printList(pilha)

    # printArray(marked)
    printList(arestasLidas)
    print('não achou')


# Rotina principal
# Gera o grafo knn e uma matriz de distância entre os vértices
grafo, AdjList, distMatrix = generateKNN(20, 3, 1)

# Faz o plot do grafo
xScatter = []
yScatter = []

fig, ax = plt.subplots()

for i in grafo:
    xScatter.append(i.x)
    yScatter.append(i.y)
    print('iteração ', i)
    for j in AdjList[i.index]:
        print(j)
        xData = [i.x, j.v.x]
        yData = [i.y, j.v.y]
        ax.plot(xData, yData, color='red')

ax.scatter(xScatter, yScatter, color='red')
# ax.set_xlim(-0.5)
# ax.set_ylim(-0.5)
ax.grid(True)


# Inicia algoritmos de busca
print("inicia busca")
caminho = buscaLargura(grafo, 11, 17)
#caminho = BP(grafo, 11, 17)

# Plot do caminho da busca em largura
""" if(caminho):
    for i in caminho:
        xData = [i.v1.x, i.v2.x]
        yData = [i.v1.y, i.v2.y]
        ax.plot(xData, yData, color='black') """

# Funções para visualização do grafo
# printList(grafo)
plt.show()
