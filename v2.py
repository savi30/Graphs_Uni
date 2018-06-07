
import time

class GraphException(Exception):
    '''
    Exception class for graph errors
    '''

    def __init__(self, msg):
        self.__msg = msg

    def __str__(self):
        return self.__msg


class EdgeProperty:
    '''
    Instances of this class act like a map linking an edge to a certain property(cost)
    '''
    def __init__(self, n, edges):
        self.__map = {}
        self.__n = n
        for edge in edges:
            self.__map[(edge[0], edge[1])] = edge[2]

    def getCost(self, edge):
        '''
        Return the cost of the given edge
        :param edge: (start point, target point)
        :return: int
        '''
        return self.__map[edge]

    def setCost(self, edge, newCost):
        '''
        Set a new cost for the given edge
        :param edge: (start point, target point)
        :param newCost: int >= 0
        '''
        self.__map[edge] = newCost

    def removeKey(self, edge):
        '''
        Remove the cost on given edge
        :param edge: (start point, target point)
        '''
        del self.__map[edge]



class Graph:
    '''
      Read-only functions:
        - parse the set of vertices
        - parse Nout(x)
        - parse Nin(x)
        - test if (x,y) is an edge
      Functions for creating the graph:
        -
      Representation : vector of lists of outbound neighbours
    '''

    def __init__(self, n, edges):
        '''
          n = nr of vertices (int) - vertices are numbered from 0 to n-1
          m = nr of edges (int)
          edges = list of tuples of 2 vertices each
        '''
        self.__n = n
        self.__out = {}
        self.__in = {}
        self.__cost = EdgeProperty(n, edges)

        for i in range(n):
            self.__out[i] = []
            self.__in[i] = []

        for edge in edges:
            self.__out[edge[0]].append(edge[1])
            self.__in[edge[1]].append(edge[0])

    def parseX(self):
        '''
        Returns an iterable containing all the vertices in the graph
        '''
        return [x for x in self.__in]

    def parseNout(self, x):
        '''
        Returns an iterable containing all the outbound neighbours of x
        '''
        return self.__out[x]

    def parseNin(self, x):
        '''
        Returns an iterable containing all the inbound neighbours of x
        '''
        return self.__in[x]

    def getN(self):
        '''
        Return the number of vertices
        '''
        return self.__n

    def isEdge(self, x, y):
        '''
        Return True if there exists an edge from x to y, False otherwise
        :param x: int
        :param y: int
        Raise GraphException if x or y is not a valid vertex
        '''
        if x not in self.__in:
            raise GraphException("Invalid vertex!")
        if y not in self.__in:
            raise GraphException("Invalid vertex!")
        if y in self.__out[x]:
            return True
        return False

    def getInDegree(self, x):
        '''
        Return the in degree of vertex x
        :param x: int
        Raise GraphException if x is not a valid vertex
        '''
        if x not in self.__in:
            raise GraphException("Invalid vertex!")
        return len(self.__in[x])

    def getOutDegree(self, x):
        '''
        Return the out degree of vertex x
        :param x: int
        Raise GraphException if x is not a valid vertex
        '''
        if x not in self.__out:
            raise GraphException("Invalid vertex!")
        return len(self.__out[x])

    def getCost(self, x, y):
        '''
        Return the cost of the edge(x,y)
        :param x: int
        :param y: int
        Raise GraphException if x or y is not a valid vertex
        '''
        if x not in self.__in:
            raise GraphException("Invalid vertex!")
        if y not in self.__in:
            raise GraphException("Invalid vertex!")
        return self.__cost.getCost((x, y))

    def setCost(self, x, y, newCost):
        '''
        Set a new cost for edge(x,y)
        :param x: int
        :param y: int
        :param newCost: int > 0
        Raise GraphException if x or y is not a valid vertex
        '''
        # if x not in self.__in:
        #     raise GraphException("Invalid vertex!")
        # if y not in self.__in:
        #     raise GraphException("Invalid vertex!")
        self.__cost.setCost((x, y), newCost)

    def removeCost(self, x, y):
        '''
        Remove the cost from given edge
        :param x: start point
        :param y: target point
        Raise GraphException if x or y is not a valid vertex
        '''
        if x not in self.__in:
            raise GraphException("Invalid vertex!")
        if y not in self.__in:
            raise GraphException("Invalid vertex!")
        self.__cost.removeKey((x,y))

    def addEdge(self, x, y):
        '''
        Add a new edge to the graph
        :param x: int - start point
        :param y: int - target point
        Raise GraphException if x or y is not a valid vertex
        '''
        # if x not in self.__in:
        #     raise GraphException("Invalid vertex!")
        # if y not in self.__in:
        #     raise GraphException("Invalid vertex!")
        self.__out[x].append(y)
        self.__in[y].append(x)

    def removeEdge(self, x, y):
        '''
        Remove the given edge
        :param x: int - start point
        :param y: int - target point
        Raise GraphException if x or y is not a valid vertex
        '''
        if x not in self.__in:
            raise GraphException("Invalid vertex!")
        if y not in self.__in:
            raise GraphException("Invalid vertex!")
        self.removeCost(x, y)
        self.__out[x].remove(y)
        self.__in[y].remove(x)

    def isVertex(self, v):
        '''
        Return True if v is a vertex of the graph, False otherwise
        :param v: int
        :return: True/False
        '''
        if v in self.__in:
            return True
        return False

    def addVertex(self, v):
        '''
        Add a new vertex to the graph
        :param: v - int
        Raises GraphException if v is already a vertex of the graph
        '''
        # if v in self.__in:
        #     raise GraphException("Vertex already exists!")
        self.__n += 1
        self.__in[v] = []
        self.__out[v] = []

    def removeVerex(self, v):
        '''
        Remove the given vertex from the list
        :param v: int
        Raises GraphException if v is not a valid vertex
        '''
        # if v not in self.__in:
        #     raise GraphException("Invalid vertex!")
        for y in self.parseNout(v):
            self.removeCost(v, y)
            self.__in[y].remove(v)
        for x in self.parseNin(v):
            self.removeCost(x, v)
            self.__out[x].remove(v)

        del self.__in[v]
        del self.__out[v]




def readGraphFromFile1():
    '''
    Read a graph from file and return an instance of Graph
    '''
    edges = []
    with open("1k.txt", "r") as f:
        line1 = f.readline()
        line1 = line1.split(" ")
        g = Graph(0, [])
        for line in f.readlines():
            line = line.split(" ")
            if len(line) >= 3:
                edge = [int(line[0]), int(line[1]), int(line[2])]
                if not g.isVertex(edge[0]):
                    g.addVertex(edge[0])
                if not g.isVertex(edge[1]):
                    g.addVertex(edge[1])
                g.addEdge(edge[0], edge[1])
                g.setCost(edge[0], edge[1], edge[2])
        return g

def readGraphFromFile():
    '''
    Read a graph from file and return an instance of Graph
    '''
    edges = []
    with open("1k.txt", "r") as f:
        line1 = f.readline()
        line1 = line1.split(" ")
        edges = []
        for line in f.readlines():
            line = line.split(" ")
            if len(line) >= 3:
                edge = [int(line[0]), int(line[1]), int(line[2])]
                edges.append(edge)
        return Graph(int(line1[0]), edges)

def testBigGraph():

    print("Read graph")
    start = time.time()
    g = readGraphFromFile()
    print(time.time() - start)

    print("ParseNout")
    start = time.time()
    for x in g.parseX():
        out = [y for y in g.parseNout(x)]
    print(time.time() - start)
    start = time.time()

    print("parseNin")
    for x in g.parseX():
        inList = [y for y in g.parseNin(x)]
    print(time.time() - start)
    print("ParseNout + cost")
    start = time.time()
    for x in g.parseX():
        out = [g.getCost(x, y) for y in g.parseNout(x)]
    print(time.time() - start)
    # print("cost only:")
    # start = time.time()
    # print(g.getCost(83106, 34380))
    # print(time.time() - start)
    print("\n")

    print("Read graph")
    start = time.time()
    g1 = readGraphFromFile1()
    print(time.time() - start)

    print("ParseNout")
    start = time.time()
    for x in g1.parseX():
        out = [y for y in g1.parseNout(x)]
    print(time.time() - start)
    start = time.time()

    print("parseNin")
    for x in g1.parseX():
        inList = [y for y in g1.parseNin(x)]
    print(time.time() - start)
    print("ParseNout + cost")
    start = time.time()
    for x in g1.parseX():
        out = [g1.getCost(x, y) for y in g1.parseNout(x)]
    print(time.time() - start)
    # print("cost only:")
    # start = time.time()
    # print(g.getCost(83106, 34380))
    # print(time.time() - start)
def main():
    testBigGraph()


main()