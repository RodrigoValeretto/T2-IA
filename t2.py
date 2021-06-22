import random
import numpy as np
from scipy.spatial import distance_matrix


class vertice:
    def __init__(self, x, y, arestas=[]):
        # x é a posição do ponto no plano horizontal
        # y é a posição do ponto no plano vertical
        # arestas são as arestas que esse vertice conecta a outros vertices
        self._x = x
        self._y = y
        self._arestas = arestas

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def arestas(self):
        return self._arestas

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @arestas.setter
    def arestas(self, arestas):
        self._arestas = arestas

    def __str__(self):
        return '(' + str(self._x) + ', ' + str(self._y) + ')'


class aresta:
    def __init__(self, v1, v2, d):
        # v1 é o primeiro vertice da aresta
        # v2 é o segundo vertice da aresta
        # d é a distância da aresta
        self._v1 = v1
        self._v2 = v2
        self._d = d

    @property
    def v1(self):
        return self._v1

    @property
    def v2(self):
        return self._v2

    @property
    def d(self):
        return self._d

    @v1.setter
    def v1(self, v1):
        self._v1 = v1

    @v2.setter
    def v2(self, v2):
        self._v2 = v2

    @d.setter
    def d(self, d):
        self._d = d

    def __str__(self):
        return str(self._v1) + ', ' + str(self._v2) + ', ' + str(self._d)


def getDist(aresta):
    return aresta.d


def generateKNN(v, k, seed=None):
    # v é o número de vértices à serem gerados, k é o número de vizinhos que cada vértice terá
    # e seed é a semente utilizada para a geração aleatória
    random.seed(seed)
    verticesArray = []
    xyArray = []

    for _ in range(0, v):
        x = random.randint(0, v)
        y = random.randint(0, v)
        verticesArray.append(vertice(x, y,))
        xyArray.append([x, y])

    distMatrix = distance_matrix(
        xyArray, xyArray)  # linhas x colunas

    for i in range(0, len(verticesArray)):
        kmenores = []
        for j in range(0, len(verticesArray)):
            if(i == j):
                continue
            elif(len(kmenores) < k):
                kmenores.append(
                    aresta(verticesArray[i], verticesArray[j], distMatrix[i, j]))
                kmenores.sort(key=getDist)
            else:
                if(distMatrix[i, j] < kmenores[k-1].d):
                    kmenores[k-1] = aresta(verticesArray[i],
                                           verticesArray[j], distMatrix[i, j])
        verticesArray[i].arestas = kmenores

    for i in verticesArray:
        for j in i.arestas:
            print(j)


'''
    for i in verticesArray:
        auxArray = []
        for j in verticesArray:
            if(i == j):
                continue
            else:
                distance = np.sqrt((i.x - j.x)**2 + (i.y - j.y)**2)
                auxArray.append(aresta(i, j, distance))
        # print(auxArray)
'''


generateKNN(10, 3, 1)
