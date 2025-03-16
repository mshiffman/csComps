from girvanNewman import GirvanNewman
import time
import pickle
import networkx as nx



girvanStats1 = {"runtime":[], "results":[]}
girvanStats2 = {"runtime":[], "results":[]}
girvanStats3 = {"runtime":[], "results":[]}
girvanStats4 = {"runtime":[], "results":[]}




print("\n")
with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)
    

mapping = {node: int(node) for node in G.nodes()}
G = nx.relabel_nodes(G, mapping)


# import random

# def get_random_subgraph(graph, num_nodes):
#     sampled_nodes = random.sample(list(graph.nodes), num_nodes)
#     subgraph = graph.subgraph(sampled_nodes).copy()
#     return subgraph

# # Example usage
# num_nodes_to_extract = 50  # Adjust as needed
# G = get_random_subgraph(G, num_nodes_to_extract)



    
girvan4Graph = GirvanNewman(G)
girvan4Start = time.time()
girvan4Result = girvan4Graph.girvanNewmanAlgo(True, "dendrogram")
girvan4End = time.time()
girvan4Runtime = girvan4End - girvan4Start
girvanStats4["runtime"].append(girvan4Runtime)
girvanStats4["results"].append(girvan4Result)
print("Runtime", girvan4Runtime)


with open('GirvanAlgoResults/girvanStats4.pkl', 'wb') as f:
    pickle.dump(girvanStats4, f)

# print("dendrogram\n",girvanStats4)

def bestModularitySplit(graph, dendrogram, minCommunities=7, maxCommunities=15):
    bestPartition = None
    bestModularity = float("-inf")

    for communities in dendrogram:
        numCommunities = len(communities)
        
        if minCommunities <= numCommunities <= maxCommunities:
            modularityScore = GirvanNewman(graph).modularity(graph, communities) 
                
            if modularityScore > bestModularity:
                bestModularity = modularityScore
                bestPartition = communities

    return bestPartition, bestModularity

# Example usage
bestPartition, bestModularity = bestModularitySplit(girvan4Graph.originalGraph, girvan4Result)

with open('GirvanAlgoResults/girvanStats4BestMod.pkl', 'wb') as f:
    pickle.dump(bestPartition, f)

print("Best Partition:", bestPartition)
print("Best Modularity:", bestModularity)
print("Runtime", girvan4Runtime)





# print("\n")
# with open("graphGN.pkl", 'rb') as f:
#     G = pickle.load(f)
# girvan3Graph = GirvanNewman(G)
# girvan3Start = time.time()
# girvan3Result = girvan3Graph.girvanNewmanAlgo(True, "numEdges75")
# girvan3End = time.time()
# girvan3Runtime = girvan3End - girvan3Start
# girvanStats3["runtime"].append(girvan3Runtime)
# girvanStats3["results"].append(girvan3Result)

# with open('GirvanAlgoResults/girvanStats3.pkl', 'wb') as f:
#     pickle.dump(girvanStats3, f)

# print("numEdges\n",girvanStats3)







# with open("graphGN.pkl", 'rb') as f:
#     G = pickle.load(f)

# girvan1Graph = GirvanNewman(G)
# girvan1Start = time.time()
# girvan1Result = girvan1Graph.girvanNewmanAlgo(True, "modularity")
# girvan1End = time.time()
# girvan1Runtime = girvan1End - girvan1Start
# girvanStats1["runtime"].append(girvan1Runtime)
# girvanStats1["results"].append(girvan1Result)

# with open('GirvanAlgoResults/girvanStats1.pkl', 'wb') as f:
#     pickle.dump(girvanStats1, f)
# print("Modularity\n", girvanStats1)









# print("\n")
# with open("graphGN.pkl", 'rb') as f:
#     G = pickle.load(f)
# girvan2Graph = GirvanNewman(G)
# girvan2Start = time.time()
# girvan2Result = girvan2Graph.girvanNewmanAlgo(True, "modularityNum")
# girvan2End = time.time()
# girvan2Runtime = girvan2End - girvan2Start
# girvanStats2["runtime"].append(girvan2Runtime)
# girvanStats2["results"].append(girvan2Result)

# with open('GirvanAlgoResults/girvanStats2.pkl', 'wb') as f:
#     pickle.dump(girvanStats2, f)
    
# print("ModularityNum\n",girvanStats2)




print("\n\nAll code executed")