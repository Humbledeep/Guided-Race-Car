# IGNORE THIS CODE

import numpy as np
import matplotlib.pyplot as plt

class Node():
    def __init__(self, id, color, x = 0, y = 0, z = 0):
        self._id = id
        self._color = color
        self._x = x
        self._y = y
        self._z = z
        self._adjacent = []

    def getColor(self):
        return self._color
    
    def getPosition(self):
        return(self._x, self._y, self._z)
    
    def getAdjacent(self):
        return self._adjacent
    
    def setColor(self, color):
        self._color = color
    
    def setPosition(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def addAdjacent(self, node_id):
        self._adjacent.append(node_id)

class Graph():
    def __init__(self):
        self._counter = 0
        self._graph = {}

    def add_node(self, color, x, y, z):
        id = self._counter
        self._graph[id] = Node(self._counter, color, x, y, z)
        self._counter += 1
        return id

    def add_edge(self, node_id1, node_id2):
        self._graph[node_id1].addAdjacent(node_id2)
        self._graph[node_id2].addAdjacent(node_id1)

    def getGraph(self):
        return self._graph
    
    def plot(self):
        # fig = plt.subplots()
        x_l = []
        y_l = []
        colors = []

        for n in self._graph:
            # Nodes
            x, y, z = self._graph[n].getPosition()
            x_l.append(x)
            y_l.append(y)
            colors.append(self._graph[n].getColor())

            # Edges
            adjacents = self._graph[n].getAdjacent()
            print(n, adjacents)
            for adj in adjacents:
                x_adj, y_adj, z_adj = self._graph[adj].getPosition()
                plt.plot([x, x_adj], [y, y_adj], color='black')

        x_l = np.array(x_l)
        y_l = np.array(y_l)
        colors = np.array(colors)

        plt.scatter(x_l, y_l, c=colors)
        plt.show()

if __name__ == "__main__":
    G = Graph()
    n0 = G.add_node('red', 3, 1, 0)
    n1 = G.add_node('red', 3, 2, 0)
    n2 = G.add_node('red', 3, 3, 0)
    n3 = G.add_node('blue', 1, 1, 0)
    n4 = G.add_node('blue', 1, 2, 0)
    n5 = G.add_node('blue', 1, 3, 0)
    G.add_edge(n0, n1)
    G.add_edge(n1, n2)
    G.add_edge(n3, n4)
    G.add_edge(n4, n5)
    G.plot()