import random


class vertice:
    x: None
    y: None


def generateKNN(v, k, seed=None):
    # v é o número de vértices à serem gerados, k é o número de vizinhos que cada vértice terá
    # e seed é a semente utilizada para a geração aleatória
    random.seed(seed)
    verticesArray = []
