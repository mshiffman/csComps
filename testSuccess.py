import csv
import pickle
import networkx as nx


#Conductance eq source: https://www.youtube.com/watch?v=Q_kJGm1xf6s
def graphAvgConductance(graph, communities):
   '''
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

#Clique Number

#density eq source https://www.youtube.com/watch?v=Q_kJGm1xf6s
def graphAvgDensity(graph, communities):
   '''
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

#Constant Potts Model source: https://journals.aps.org/pre/abstract/10.1103/PhysRevE.84.016114#s2
def constantPotts(graph, communities, resolution):
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


communities1 = []
with open('WLPA5.csv', 'r') as file:
    reader = csv.reader(file)
    for community in reader:
      communities1.append(community)


#to open pickle file:
fileName = 'graphLPA.pkl'
with open(fileName, 'rb') as f:
   G1 = pickle.load(f)


communities2 = []
with open('LouvainData/louvain_communities_1_3.csv', 'r') as file:
    reader = csv.reader(file)
    for community in reader:
      communities2.append(community)


#to open pickle file:
fileName = 'graph.pkl'
with open(fileName, 'rb') as f:
   G2 = pickle.load(f)
   
communities3 = []
with open('leidenData/leiden_communities_1_3.csv', 'r') as file:
    reader = csv.reader(file)
    for community in reader:
      communities3.append(community)



communities1 = [[int(node) for node in community] for community in communities1]
mapping = {node: int(node) for node in G1.nodes()}
G1 = nx.relabel_nodes(G1, mapping)

communities2 = [[int(node) for node in community] for community in communities2]
communities3 = [[int(node) for node in community] for community in communities3]
mapping = {node: int(node) for node in G2.nodes()}
G2 = nx.relabel_nodes(G2, mapping)




print("WLPA mod:", modularity(G1, communities1))

print("Louvain mod:",modularity(G2, communities2))

print("Leiden mod:",modularity(G2, communities3))


print("WLPA den:", graphAvgDensity(G1, communities1))

print("Louvain den:",graphAvgDensity(G2, communities2))

print("Leiden den:",graphAvgDensity(G2, communities3))


print("WLPA con:", graphAvgConductance(G1, communities1))

print("Louvain con:",graphAvgConductance(G2, communities2))

print("Leiden con:",graphAvgConductance(G2, communities3))
