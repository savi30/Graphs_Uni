import heapq
import math


def BFS(G, start):
    """
    Standard BFS search
    :param G:The graph on which the search is performed
    :param start: the starting vertex
    :return: a dictionary of distances(how many steps to reach the vertex) and a dictionary containing
        the parent of each vertex
    """
    distances = {start: 0}
    parent = {start: None}
    queue = [start]
    while len(queue) > 0:
        node = queue[0]
        for i in G.getOutbound(node):
            if i in distances.keys():
                continue
            parent[i] = node
            distances[i] = distances[node] + 1
            queue.append(i)
        queue.pop(0)
    return distances, parent


def shortestPathReverseBFS(G, start, target):
    """
    Performs a reverse breath first traversal of the spanning tree of  G
    :param G: The graph on which the search is performed
    :param start:  the starting vertex
    :param target:  the end vertex
    :return: the shortest path from start to target if it exists, none otherwise
    """
    distances, parent = BFS(G, start)
    if target not in parent.keys():
        return None

    result = []
    current = target
    while current != start:
        result.append(current)
        current = parent[current]

    result.append(start)
    result.reverse()
    return result


def DFS(G):
    """
    Performs a depth-first search on a give graph
    :param G: the graph to be searched
    :return: a list that represents the depth-first forest
    """
    parent = {}
    for v in G.getVertices():
        if v not in parent:
            parent[v] = None
            DFSVisit(G, v, parent)
    return parent


def DFSVisit(G, s, parent,):
    """
    Recursively visits every vertex in a depth-fist manner
    :param G: a given graph
    :param s: the current vertex
    :param parent: a list that represent the depth-fist forrest up to this point
                    keeps track of the vertices visited so far
    """
    for v in G.getOutbound(s):
        if v not in parent:
            parent[v] = s
            DFSVisit(G, v, parent)


def BellmanFord(G, w, s):
    """
    """
    dist = {}
    parent = {s: None}
    for e in G.getVertices().keys():
        dist[e] = math.inf
    dist[s] = 0
    v = G.getVertices()

    for i in range(1, G.getVerticesNumber()):
        for x in v:
            for e in v[x]:
                if dist[e] > dist[x] + w[(x, e)]:
                    dist[e] = dist[x] + w[(x, e)]
                    parent[e] = x

    for x in v:
        for e in v[x]:
            if dist[e] > dist[x] + w[(x, e)]:
                return {}, {}
    return dist, parent


def lowestCostPath(G, s, t):
    """
    Write a program that, given a graph with costs and two vertices,
    finds a lowest cost walk between the given vertices,
    or prints a message if there are negative cost cycles accessible from the starting vertex.
    The program will use the Ford's algorithm.
    """
    res, parent = BellmanFord(G, G.getCosts(), s)
    if res == {}:
        print("negative cycle detected")
        return
    if t not in parent:
        print("can't reach "+str(t)+" from "+str(s))
        return
    current = t
    res = []
    while parent[current] is not None:
        res.append(parent[current])
        current = parent[current]
    res = res[::-1]
    print(res)


def topologicalSortKahn(g):
    """
    Returns the list of vertices sorted topologically (or None if g is not DAG)
    """
    sortedList = []
    s = set()
    inbound = {}
    for v in g.getVertices():
        inbound[v] = g.getInDegree(v)
        if inbound[v] == 0:
            s.add(v)
            sortedList.append(v)

    while len(s) > 0:
        x = s.pop()
        sortedList.append(x)
        for v in g.getOutbound(x):
            inbound[v] -= 1
            if inbound[v] == 0:
                s.add(v)
    for e in inbound:
        if inbound[e] != 0:
            return None
    return sortedList


def findHighestCostPath(G, s, t):
    """
    Negates all the costs of the graph and runs bellman-ford thus giving the highest cost path
    """
    if topologicalSortKahn(G) is not None:
        costs = G.getCosts()
        for e in costs:
            costs[e] = -costs[e]
        res, parent = BellmanFord(G, costs, s)
        if res == {}:
            print("not a DAG -> resulting from bellman-ford with negated costs")
            return
        if t not in parent:
            print("can't reach "+str(t)+" from "+str(s))
            return
        current = t
        res = []
        while parent[current] is not None:
            res.append(parent[current])
            current = parent[current]
        res = res[::-1]
        print(res)
    else:
        print("graph is not a DAG")


def findHamiltonianCycle(G):
    """
    Find the lowest cost hamiltonian cycle by using the nearest neighbour approach
    """
    visited = []
    a = list(G.parseX())[0]
    visited.append(a)
    costs = G.getCosts()

    while len(visited) < len(G.parseX()):
        currLevel = {}
        for v in G.parseN(a):
            if v not in visited:
                currLevel[v] = costs[(a, v)]
        if currLevel == {}:
            return None
        a = min(currLevel, key=currLevel.get)
        visited.append(a)

    return visited
