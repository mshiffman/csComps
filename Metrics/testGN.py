import pickle
import networkx as nx
from Metrics.testSuccess import *

# with open("graphGN.pkl", 'rb') as f:
#     G = pickle.load(f)
with open("graph.pkl", 'rb') as f:
    G = pickle.load(f)

print(G.number_of_nodes())
print(G.number_of_edges())

with open("GirvanAlgoResults/girvanStats4.pkl", 'rb') as f:
    girvanStats = pickle.load(f)

def bestModularitySplit(graph, dendrogram, minCommunities=7, maxCommunities=329):
    bestPartition = None
    bestModularity = float("-inf")

    for communities in dendrogram:
        numCommunities = len(communities)
        
        if minCommunities <= numCommunities <= maxCommunities:
            modularityScore = modularity(graph, communities) 
                
            if modularityScore > bestModularity:
                bestModularity = modularityScore
                bestPartition = communities

    return bestPartition, bestModularity

bestPartition, bestModularity= bestModularitySplit(G, girvanStats["results"][0])

with open('GirvanAlgoResults/girvanStatsDepth1BestModMax329.pkl', 'wb') as f:
    pickle.dump(bestPartition, f)

print("Best Partition:", bestPartition)
print("Best Modularity:", bestModularity)



# print(girvanStats)
# for i in range(len(girvanStats["results"])):
#     for j in range(len(girvanStats["results"][i])):
#         print(j)
#         print(len(girvanStats["results"][i][j]))
#         print(girvanStats["results"][i][j])
#         print("\n")