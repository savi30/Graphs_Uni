import time
from graph import DirectedGraph, UndirectedGraph
import graphAlgorithms


def main():
     # graph = DirectedGraph("smallTest.txt")
     # start = time.time()
     # graphAlgorithms.findHighestCostPath(graph, 0, 5)
     graph = UndirectedGraph("smallTestUndirected.txt")
     print(graphAlgorithms.findHamiltonianCycle(graph))

main()
