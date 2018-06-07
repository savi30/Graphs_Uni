import copy


class DirectedGraph:

    def __init__(self, filename="1k.txt"):
        self.__inbound = {}
        self.__outbound = {}
        self.__cost = {}
        self.__loadFromFile(filename)

    """
    Adds a new vertex to the inbound and outbound disctionaries
    Initially the vertex's inbound and outbound edges are empty
    """

    def addVertex(self, v):
        if not self.vertexExists(v):
            self.__inbound[v] = []
            self.__outbound[v] = []

    """
    Checks if a vertex already exists
    """

    def vertexExists(self, v):
        if v in self.__outbound or v in self.__inbound:
            return True
        return False

    """
    Checks if the edge from x to y exists
    """

    def edgeExists(self, x, y):
        return y in self.__outbound[x]

    """
    Adds a new edge to the graph if it does not exists already
    Also checks if the vertices involved exist and adds them to
    the inbound and outbound disctionaries if they don't exist
    """

    def addEdge(self, x, y, cost):
        if not self.vertexExists(x):
            self.addVertex(x)
        if not self.vertexExists(y):
            self.addVertex(y)
        if not self.edgeExists(x, y):
            self.__outbound[x].append(y)
            self.__inbound[y].append(x)
            self.__cost[(x, y)] = cost

    """
    Removes an edge and its corresponding cost from the graph if it exists
    """

    def removeEdge(self, x, y):
        if self.edgeExists(x, y):
            self.__outbound[x].remove(y)
            del self.__cost[(x, y)]

    """
    Removes a vertex and all its references from the graph (inbounds, outbound and cost)
    """

    def removeVertex(self, v):
        if self.vertexExists(v):
            for el in self.__outbound[v]:
                del self.__cost[(v, el)]
            for el in self.__inbound[v]:
                del self.__cost[(v, el)]
            del self.__inbound[v]
            del self.__outbound[v]

    """
    Returns all the inbound edges of a given vertex v
    That is all the edges that start from x and go to v where x is a valid vertex.
    """

    def getInbound(self, v):
        if self.vertexExists(v):
            return self.__inbound[v]

    """
    Returns all the outbound edges of a given vertex v
    That is all the edges that start from v and go to x where x is a valid vertex.
    """

    def getOutbound(self, v):
        if self.vertexExists(v):
            return self.__outbound[v]

    """
    Returns the cost associated with an edge
    """

    def getCost(self, x, y):
        if self.edgeExists(x, y):
            return self.__cost[(x, y)]

    """
    Returns a dictionary with all the costs of the graph
    """
    def getCosts(self):
        return self.__cost

    """
    Returns the number if vertices in the graph
    """

    def getVerticesNumber(self):
        return len(self.__outbound)

    """
    Sets a new cost for a given edge
    x, y source and target of the edge
    """

    def setCost(self, x, y, newCost):
        if self.edgeExists(x, y):
            self.__cost[(x, y)] = newCost

    def getInDegree(self, v):
        if self.vertexExists(v):
            return len(self.__inbound[v])

    def getOutDegree(self, v):
        if self.vertexExists(v):
            return len(self.__outbound[v])

    def getVertices(self):
        return self.__outbound

    def __loadFromFile(self, filename):
        with open(filename, "r") as f:
            args = f.readline()
            args = args.split(" ")
            for x in range(0, int(args[0])):
                self.addVertex(x)
            for line in f:
                item = line.strip()
                item = item.split(" ")
                item = [x.strip() for x in item]
                self.addEdge(int(item[0]), int(item[1]), int(item[2]))

    def copy(self):
        '''
        Generates a deep copy of the graph
        :return:
        '''
        return copy.deepcopy(self)


class UndirectedGraph:
    def __init__(self, filename):
        self.__edge = {}
        self.__cost = {}
        self.__loadFromFile(filename)

    def parseX(self):
        '''Returns an iterable object that parses all the
        vertices of the graph'''
        return self.__edge.keys()

    def parseN(self, x):
        '''Returns an iterable object that parses all the
        inbound neighbours of x'''
        return self.__edge[x]

    def isEdge(self, x, y):
        '''Returns True if there is an edge from x to y'''
        return y in self.__edge[x]

    def addVertex(self, v):
        self.__edge[v] = []

    def getCosts(self):
        return self.__cost

    def addEdge(self, x, y, cost):
        '''
        Adds an edge between x and y
        Pre: x and y must be vertices
        out: returns True if there was no edge or
        returns False if there was already an edge
        '''
        if self.isEdge(x, y):
            return False
        self.__edge[y].append(x)
        self.__edge[x].append(y)
        self.__cost[(x, y)] = cost
        self.__cost[(y, x)] = cost
        return True

    def __loadFromFile(self,filename):
        with open(filename, "r") as f:
            args = f.readline()
            args = args.split(" ")
            for x in range(0, int(args[0])):
                self.addVertex(x)
            for line in f:
                item = line.strip()
                item = item.split(" ")
                item = [x.strip() for x in item]
                self.addEdge(int(item[0]), int(item[1]), int(item[2]))