import pickle
import networkx as nx

with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)
with open("graph.pkl", 'rb') as f:
    G = pickle.load(f)

print(G.number_of_nodes())
print(G.number_of_edges())

with open("girvanStats.pkl", 'rb') as f:
    girvanStats = pickle.load(f)


# print(girvanStats)
# for i in range(len(girvanStats["results"])):
#     for j in range(len(girvanStats["results"][i])):
#         print(j)
#         print(len(girvanStats["results"][i][j]))
#         print(girvanStats["results"][i][j])
#         print("\n")