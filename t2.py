import random
import matplotlib.pyplot as plt
from scipy.spatial import distance_matrix


class vertice:
    def __init__(self, x, y, arestas=[]):
        # x é a posição do ponto no plano horizontal
        # y é a posição do ponto no plano vertical
        # arestas são as arestas que esse vertice conecta a outros vertices
        self._x = x
        self._y = y
        self._arestas = arestas

    # getters da classe
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def arestas(self):
        return self._arestas

    # setters da classe
    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @arestas.setter
    def arestas(self, arestas):
        self._arestas = arestas

    # definição da string gerada pela classe
    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ')'

    # sobrecarga do operador ==
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class aresta:
    def __init__(self, v1, v2, d):
        # v1 é o primeiro vertice da aresta
        # v2 é o segundo vertice da aresta
        # d é a distância da aresta
        self._v1 = v1
        self._v2 = v2
        self._d = d

    # getters da classe
    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def d(self):
        return self._d

    # setters da classe
    @v1.setter
    def v1(self, v1):
        self._v1 = v1

    @v2.setter
    def v2(self, v2):
        self._v2 = v2

    @d.setter
    def d(self, d):
        self._d = d

    # definição da string gerada pela classe
    def __str__(self):
        return str(self._v1) + ', ' + str(self._v2) + ', ' + str(self._d)


def getDist(aresta):
    # Função usada para ordenação de arestas
    return aresta.d


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
    xyArray = []

    for _ in range(0, v):
        x = random.randint(0, v)
        y = random.randint(0, v)
        grafo.append(vertice(x, y,))
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
                    aresta(grafo[i], grafo[j], distMatrix[i, j]))
                kmenores.sort(key=getDist)
            else:
                if(distMatrix[i, j] < kmenores[k-1].d):
                    kmenores[k-1] = aresta(grafo[i],
                                           grafo[j], distMatrix[i, j])
                    kmenores.sort(key=getDist)

        grafo[i].arestas = kmenores
    return grafo, distMatrix


def buscaLargura(s, f):
    marked = [s]
    fila = [s]
    arestasLidas = []

    while(len(fila) != 0):
        v = fila.pop(0)
        for w in v.arestas:
            if(w.v2 not in marked):
                arestasLidas.append(w)
                marked.append(w.v2)
                fila.append(w.v2)
                if(w.v2 == f):
                    print("Achou")
                    caminho = encontraCaminho(arestasLidas, s, f)
                    return caminho

    # printArray(marked)
    print('não achou')


# Rotina principal

# Gera o grafo knn e uma matriz de distância entre os vértices
grafo, distMatrix = generateKNN(20, 3, 1)

# Faz o plot do grafo
xScatter = []
yScatter = []

fig, ax = plt.subplots()

for i in grafo:
    xScatter.append(i.x)
    yScatter.append(i.y)
    for j in i.arestas:
        # print(j)
        xData = [j.v1.x, j.v2.x]
        yData = [j.v1.y, j.v2.y]
        ax.plot(xData, yData, color='red')

ax.scatter(xScatter, yScatter, color='red')
ax.set_xlim(-0.5)
ax.set_ylim(-0.5)
ax.grid(True)


# Inicia algoritmos de busca
print("inicia busca")
caminho = buscaLargura(grafo[11], vertice(20, 12))

for i in caminho:
    xData = [i.v1.x, i.v2.x]
    yData = [i.v1.y, i.v2.y]
    ax.plot(xData, yData, color='black')

# Funções para visualização do grafo
# printList(grafo)
plt.show()
