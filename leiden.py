import networkx as nx
import math
from typing import List


class Leiden:

    def __init__(self, graph: nx.Graph):

        self.graph = graph
        self.communities = []




    def setCommunities(self, graph: nx.Graph) -> None:
        # Sets all nodes as their own communities during first step in Leiden
        self.communities.append()#for loop going through all communities

    def modularity(self, node, community: List, graph: nx.Graph) ->float:

        if len(community) < 1:                                                              # If nothing in community, then this shouldn't increase modularity - so return worst possible value
            return -1
        
        community.append(node)                                                              # Adds node to community

        allEdgeWeight = graph.size(weight = "weight")                                       # Gets total weight of graph, m value in modularity calc

        nodeIndividualWeights = {}
        for i in community:
            nodeIndividualWeights[i] = self.nodeWeight(i, graph)                            # Returns weight of nodes in compared community as a dictionary, k_i & k_j in modularity calc

        modList = []
        for i in community[:-1]:
            for j in community[i+1:]:
                if i == j:
                    continue
                
                twoNodesEdgeWeight = graph.get_edge_data(i, j, default = 0)                 # Returns weight between two nodes, A_ij in modularity calc

                modularity = ((1 / 2(allEdgeWeight)) * (twoNodesEdgeWeight - ((nodeIndividualWeights[i] * nodeIndividualWeights[j]) / 2(allEdgeWeight))))
                modList.append(modularity)

        if len(modList) == 1:                                                               # If only calculating modularity for 2 nodes
            return modList[0]
        else:                                                                               # If calculating modularity for 2+ nodes
            totalModularity = 0
            for i in modList:
                totalModularity += i
            return totalModularity
    
    def nodeWeight(self, node, graph: nx.Graph) -> int:
        weight = 0
        nodeNeighbors = graph.neighbors(node)
        for neighbor in nodeNeighbors:
            weight += graph[node][neighbor]["weight"]

        return weight