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
    # Função para ordenação do vetor de arestas com base na distância de cada uma
    return aresta.d


def hasAresta(v1, v2):
    # Verifica se o vertice 1 contém uma aresta para o vertice 2
    for i in v1.arestas:
        if(i.v2 == v2):
            return True
    return False


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
        menores = []
        size = k - len(verticesArray[i].arestas)
        print(k, len(verticesArray[i].arestas))
        for j in range(0, len(verticesArray)):
            if(i == j):
                continue
            elif(len(menores) < size):
                menores.append(
                    aresta(verticesArray[i], verticesArray[j], distMatrix[i, j]))
                menores.sort(key=getDist)
            else:
                if(distMatrix[i, j] < menores[size-1].d):
                    menores[size-1] = aresta(verticesArray[i],
                                             verticesArray[j], distMatrix[i, j])
        for a in menores:
            verticesArray[i].arestas.append(a)

            if(len(a.v2.arestas) == k):
                continue
            elif(not hasAresta(a.v2, a.v1)):
                a.v2.arestas.append(aresta(a.v2, a.v1, a.d))
            print(a.v2.arestas)

    for i in verticesArray:
        for j in i.arestas:
            print(j)

    return verticesArray, distMatrix


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


verticesArray, distMatrix = generateKNN(10, 3, 1)

xScatter = []
yScatter = []


fig, ax = plt.subplots()

for i in verticesArray:
    xScatter.append(i.x)
    yScatter.append(i.y)
    for j in i.arestas:
        # print(j)
        xData = [j.v1.x, j.v2.x]
        yData = [j.v1.y, j.v2.y]
        ax.plot(xData, yData)

ax.scatter(xScatter, yScatter)
ax.set_xlim(-0.5)
ax.set_ylim(-0.5)
ax.grid(True)
plt.show()
