import pytest
import networkx as nx
from oldgirvanNewman import GirvanNewman

#test graph
G = nx.Graph()
G.add_edge(0, 1, weight=4)
G.add_edge(0, 3, weight=1)
G.add_edge(1, 4, weight=1)
G.add_edge(0, 4, weight=1)
G.add_edge(2, 4, weight=2)
G.add_edge(3, 4, weight=4)
G.add_edge(0, 4, weight=2)

gnGraph = GirvanNewman(G)



def testEdgeBetweennness():
    codedEdgeB = sorted(gnGraph.edgebetweenness(), key = lambda pair: pair[1])
    builtin = sorted(nx.edge_betweenness_centrality(G).items(), key = lambda pair: pair[1])
    assert codedEdgeB == builtin





