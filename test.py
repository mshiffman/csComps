import pickle
import networkx as nx


G = nx.Graph()
G.add_weighted_edges_from([
    ("A", "B", 1),
    ("B", "C", 2),
    ("A", "C", 2), 
    ("C", "D", 1),
    ("D", "E", 2),
    ("B", "E", 3)
])

with open('graph1.pkl', 'wb') as f:
    pickle.dump(G, f)