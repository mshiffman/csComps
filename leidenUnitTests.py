import pytest
import networkx as nx
from leiden import Leiden

# def testModAgainstNx():
#     nxG = nx.Graph()
#     nxG.add_edges_from([("a", "b"), ("b", "c"), ("d", "e"), ("e", "f")])  
#     communities = [["a", "b", "c"], ["d","e", "f"]]
#     classG = Leiden(nxG)
#     mod = classG.modularity("a", communities[0], nxG)
    
#     assert mod == nx.community.modularity(nxG, communities)

def testModNoNode():
    nxG = nx.Graph()
    nxG.add_edges_from([("a", "b"), ("b", "c"), ("d", "e"), ("e", "f")])  
    communities = [["a", "b", "c"], ["d","e", "f"]]
    classG = Leiden(nxG)
    
    with pytest.raises(ValueError):
        classG.modularity("g", communities[0], nxG) 

def testModNoCommunity():
    nxG = nx.Graph()
    nxG.add_edges_from([("a", "b"), ("b", "c"), ("d", "e"), ("e", "f")])  
    communities = [[], []]
    classG = Leiden(nxG)
    assert classG.modularity("a", communities[0], nxG) > 0

def testModEmptyGraph():
    nxG = nx.Graph()
    nxG.add_edges_from([])  
    communities = [[]]
    classG = Leiden(nxG)
    assert classG.modularity("a", communities[0], nxG) == 0