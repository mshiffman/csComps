import csv
import pickle
import networkx as nx
import pandas as pd

'''
This is the code we used for metrics.
'''
def graphAvgConductance(graph, communities):
   '''
   Conductance is the fraction of edges leaving the community
   https://www.sciencedirect.com/science/article/pii/S0370157316302964#s000015
   '''
   totalConductance = 0
   commCount = 0
   for community in communities:
      size = len(community)
      if size>1:
         internalEdges = graph.subgraph(community).number_of_edges()
         externalEdges = 0
         for node in community:
            for neighbor in graph.neighbors(node):
               if neighbor not in community:
                  externalEdges +=1
         num = externalEdges
         den = 2* internalEdges + externalEdges
         if den == 0:
            conductance = 0
         else:
            conductance = num/den
         totalConductance += conductance
         commCount +=1
   if commCount>0:
      return totalConductance/commCount
   else:
      return 0

def graphAvgConductanceWeight(graph, communities):
    '''
    Compute the average conductance of a graph using weighted edges.
    https://www.sciencedirect.com/science/article/pii/S0370157316302964#s000015
    '''
    totalConductance = 0
    commCount = 0
    
    for community in communities:
        size = len(community)
        if size > 1:
            internalWeight = 0
            externalWeight = 0
            
            for u in community:
                for v in graph.neighbors(u):
                    weight = graph[u][v].get('weight', 1)
                    if v in community:
                        internalWeight += weight
                    else:
                        externalWeight += weight
            
            internalWeight /= 2
            
            num = externalWeight
            den = 2 * internalWeight + externalWeight
            
            if den == 0:
                conductance = 0
            else:
                conductance = num / den
            
            totalConductance += conductance
            commCount += 1
    
    if commCount > 0:
        return totalConductance / commCount
    else:
        return 0

def graphAvgDensity(graph, communities):
   '''
   How connected a community internally is
   https://www.sciencedirect.com/topics/computer-science/network-density
   '''
   totalDensity = 0
   commCount = 0
   for community in communities:
      size = len(community)
      if size >1:
         numEdges = graph.subgraph(community).number_of_edges()
         num= 2 * numEdges
         den = size * (size-1)
         commDensity = num/den
         totalDensity+=commDensity
         commCount +=1
   if commCount>0:
      return totalDensity/commCount
   else:
      return 0

def constantPotts(graph, communities, resolution):
   '''
   Did not end up using
   https://journals.aps.org/pre/abstract/10.1103/PhysRevE.84.016114#s2
   '''
   summation = 0
   for community in communities:
      for nodeI in community:
         for nodeJ in community:
            if nodeI != nodeJ:
               if graph.has_edge(nodeI,nodeJ):
                  Wij = graph[nodeI][nodeJ].get("weight", 1)
               else:
                  Wij = 0
               summation += Wij - resolution
   return -summation/2

def modularity(graph, communities):
   '''
   m = number of edges (unweighted), weighted = 1/2*sum(all weights for nodes i,j)
   Aij = edge weight for the edge between i and j
   Ki = weighted degree of i
   Kj = weighted degree of j
   delta 1 if in same community, 0 if not
   mod = 1/2m * sum(Aij- ((ki*kj)/2m)* delta)
   '''

   m = graph.size(weight="weight")
   summation = 0.0
   for i in graph.nodes():
      for j in graph.nodes():
            if graph.has_edge(i,j):
               Aij = graph[i][j].get("weight", 1)
            else:
               Aij = 0
            Ki = getDegree(i, graph)
            Kj = getDegree(j, graph)

            com1 = getCommunity(i, communities)
            com2 = getCommunity(j, communities)
            if com1 == com2:
               delta = 1
            else:
               delta = 0
            summation += (Aij - ((Ki*Kj)/(2*m)))* delta
   
   modScore = 1/ (2*m) * summation
   return modScore 

def getDegree(node, graph):
   '''
   returns the degree of a node
   '''
   degree = 0
   for neighbor in graph.neighbors(node):
      edge = graph[node][neighbor].get("weight", 1)
      degree +=edge
   return degree  

def getCommunity(node, communities):
   '''
   returns the index of the community a node belongs to
   '''
   for i in range(len(communities)):
      if node in communities[i]:
            return i


# #to open pickle file:
# fileName = 'graphGN.pkl'
# with open(fileName, 'rb') as f:
#    G1 = pickle.load(f)

# mapping = {node: int(node) for node in G1.nodes()}
# G1 = nx.relabel_nodes(G1, mapping)

# #to open pickle file:
# fileName = 'graph.pkl'
# with open(fileName, 'rb') as f:
#    G2 = pickle.load(f)

# mapping = {node: int(node) for node in G2.nodes()}
# G2 = nx.relabel_nodes(G2, mapping)


# communities1 = []
# with open('WLPA5.csv', 'r') as file:
#     reader = csv.reader(file)
#     for community in reader:
#       communities1.append(community)

# communities2 = []
# with open('LouvainData/louvain_communities_1.csv', 'r') as file:
#     reader = csv.reader(file)
#     for community in reader:
#       communities2.append(community)


# communities3 = []
# with open('leidenData/leiden_communities_1.csv', 'r') as file:
#     reader = csv.reader(file)
#     for community in reader:
#       communities3.append(community)


# communities6 = []
# with open('WLPA5.csv', 'r') as file:
#     reader = csv.reader(file)
#     for community in reader:
#       communities6.append(community)

# communities7 = []
# with open('WLPA_5_2.csv', 'r') as file:
#     reader = csv.reader(file)
#     for community in reader:
#       communities7.append(community)

# communities8 = []
# with open('LPA_run.csv', 'r') as file:
#     reader = csv.reader(file)
#     for community in reader:
#       communities8.append(community)
      
# communities1 = [[int(node) for node in community] for community in communities1]
# communities2 = [[int(node) for node in community] for community in communities2]
# communities3 = [[int(node) for node in community] for community in communities3]
# communities4 = [[int(node) for node in community] for community in communities4]
# communities5 = [[int(node) for node in community] for community in communities5]
# communities6 = [[int(node) for node in community] for community in communities6]
# communities7 = [[int(node) for node in community] for community in communities7]
# communities8 = [[int(node) for node in community] for community in communities8]


# louvain_mod = modularity(G2, communities2)
# louvain_den = graphAvgDensity(G2, communities2)
# louvain_con = graphAvgConductanceWeight(G2, communities2)


# leiden_mod = modularity(G2, communities3)
# leiden_den = graphAvgDensity(G2, communities3)
# leiden_con = graphAvgConductanceWeight(G2, communities3)


# gn_mod1 = modularity(G1, communities4)
# gn_den1 = graphAvgDensity(G1, communities4)
# gn_con1 = graphAvgConductanceWeight(G1, communities4)

# gn_mod2 = modularity(G1, communities5)
# gn_den2 = graphAvgDensity(G1, communities5)
# gn_con2 = graphAvgConductanceWeight(G1, communities5)

# wlpaModified1_mod = modularity(G2, communities1)
# wlpaModified1_den = graphAvgDensity(G2, communities1)
# wlpaModified1_con = graphAvgConductanceWeight(G2, communities1)

# wlpa1_mod = modularity(G2, communities6)
# wlpa1_den = graphAvgDensity(G2, communities6)
# wlpa1_con = graphAvgConductanceWeight(G2, communities6)

# wlpa2_mod = modularity(G2, communities7)
# wlpa2_den = graphAvgDensity(G2, communities7)
# wlpa2_con = graphAvgConductanceWeight(G2, communities7)

# lpa_mod = modularity(G2, communities8)
# lpa_den = graphAvgDensity(G2, communities8)
# lpa_con = graphAvgConductanceWeight(G2, communities8)
