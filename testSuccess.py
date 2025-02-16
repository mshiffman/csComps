import pickle
import networkx
from leiden import Leiden

#Conductance eq source: https://www.youtube.com/watch?v=Q_kJGm1xf6s
def graphAvgConductance(graph, communities):
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
   totalDensity = 0
   commCount = 0
   for community in communities:
      size = len(community)
      if size >1:
         for node in range(size):
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
      edgesInComm = graph.subgraph(community).number_of_edges()
      nodesInComm = len(graph.subgraph(community))
      thisComm = edgesInComm - resolution*(nodesInComm**2)
      summation+=thisComm
   return -summation

def graphModularity(graph, communities):
   edges = graph.size(weight = "weight")
   accum_Modularity = 0.0

   for eachCommunity in range(len(communities)):
      for eachNode in eachCommunity:
         accum_Modularity+= Leiden.modularity(eachNode, eachCommunity, graph)

   return accum_Modularity/(2*edges)

#to open pickle file:
fileName = 'graph1.pkl'
with open(fileName, 'rb') as f:
   graph1 = pickle.load(f)

graphAvgDensity(graph1, communities=[])