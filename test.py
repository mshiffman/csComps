import networkx as nx
import pickle
import time

print("\n")
with open("graphWLPA.pkl", 'rb') as f:
    G = pickle.load(f)

with open("graphLPA.pkl", 'rb') as f:
    G2 = pickle.load(f)

start = time.time()
communities = nx.algorithms.community.label_propagation_communities(G)
print(len(communities))
print(nx.community.modularity(G, nx.community.label_propagation_communities(G)))



communities = nx.algorithms.community.label_propagation_communities(G)
print(len(communities))
print(nx.community.modularity(G2, nx.community.label_propagation_communities(G2)))
