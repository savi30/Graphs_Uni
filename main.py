class DirectedGraph:
    def __init__(self):
        self.__inbound = {}
        self.__outbound = {}
        self.__cost = {}

    def addVertex(self, v):
        if not self.vertexExists(v):
            self.__inbound[v] = []
            self.__outbound[v] = []

    def vertexExists(self,v):
        if v in self.__outbound or v in self.__inbound:
            return True
        return False

    def edgeExists(self,x,y):
        return y in self.__outbound[x]

    def addEdge(self,x,y,cost):
        if not self.vertexExists(x):
            self.addVertex(x)
        if not self.edgeExists(x,y):
            self.__outbound[x].append(y)
            self.__cost[(x,y)] = cost

    def removeEdge(self,x,y):
        if self.edgeExists(x,y):
            self.__outbound[x].remove(y)
            del self.__cost[(x,y)]

    def removeVertex(self,v):
        if self.vertexExists(v):
            for el in self.__outbound[v]:
                del self.__cost[(v,el)]
            for el in self.__inbound[v]:
                del self.__cost[(v,el)]

    def getInbound(self,v):
        if self.vertexExists(v):
            return self.__inbound[v]

    def getOutbound(self,v):
        if self.vertexExists(v):
            return  self.__outbound[v]

    def getCost(self,x,y):
        if self.edgeExists(x,y):
            return self.__cost[(x,y)]

    def getVerticesNumber(self):
        return len(self.__outbound)

    def setCost(self,x,y,newCost):
        if self.edgeExists(x,y):
            self.__cost[(x,y)] = newCost

def main():

    graph = DirectedGraph()
    graph.addEdge(0, 0, 1)
    graph.addEdge(0, 1, 7)
    graph.addEdge(1, 2, 2)
    graph.addEdge(2, 1, -1)
    graph.addEdge(1, 3, 8)
    graph.addEdge(2, 3, 5)

    print(graph.getInbound(0))
    print(graph.getOutbound(0))

    print(graph.getVerticesNumber())
    print(graph.getCost(0,1))
    graph.setCost(0,1,-400)
    print(graph.getCost(0,1))




main()