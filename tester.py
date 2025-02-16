import networkx as nx

# Create a weighted graph
G = nx.Graph()
edges = [(0,1,4), (0,2,1), (1,2,1), (1,3,1), (2,3,2), (2,4,4), (3,4,2)]
G.add_weighted_edges_from(edges)

# Define each node as its own community
partition = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}

# Compute modularity
Q = nx.community.modularity(G, [{n} for n in G.nodes()])
print(Q)  # Should return -0.2067
