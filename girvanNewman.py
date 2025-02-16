from collections import deque
from heapq import heappop, heappush
import matplotlib.pyplot as plt
import networkx as nx

class GirvanNewman:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def bfs(self, sourceNode):
        '''
        BFS code adapted from Brandes
        '''
        stack = []
        parents = {}
        sigma = {}
        distance = {}
        delta = {}
        queue = deque([sourceNode])

        for targetNode in self.graph.nodes:
            if targetNode == sourceNode:
                sigma[sourceNode]=1
                distance[targetNode]=0
            else:
                sigma[targetNode]=0
                distance[targetNode]=-1
            delta[targetNode]=0
            parents[targetNode]=[]

        while len(queue)>0:
                inBetweenNode = queue.popleft()
                stack.append(inBetweenNode)
                
                for neighborNode in self.graph.neighbors(inBetweenNode):
                    if distance[neighborNode] == -1:
                        queue.append(neighborNode)
                        distance[neighborNode]=distance[inBetweenNode]+1
                    if distance[neighborNode]==distance[inBetweenNode]+1:
                        sigma[neighborNode]+=sigma[inBetweenNode]
                        parents[neighborNode].append(inBetweenNode)
        return stack, parents, sigma, delta


    def dijkstras(self, sourceNode):
        '''
        adapted bfs algorithm to dijkstras
        '''
        stack = []
        parents = {}
        sigma = {}
        distance = {}
        delta = {}
        pQueue = []

        #initialize
        for targetNode in self.graph.nodes:
            if targetNode == sourceNode:
                sigma[sourceNode]=1
                distance[targetNode]=0
                heappush(pQueue, (0, sourceNode))
            else:
                sigma[targetNode]=0
                distance[targetNode]=float("inf")
            delta[targetNode]=0
            parents[targetNode]=[]

        while len(pQueue)>0:
                dist, inBetweenNode = heappop(pQueue)

                stack.append(inBetweenNode)
                if dist <= distance[inBetweenNode]:
                    for neighborNode in self.graph.neighbors(inBetweenNode):

                        edgeWeight = self.graph[inBetweenNode][neighborNode].get('weight', 1)
                        newDist = distance[inBetweenNode]+edgeWeight

                        if newDist < distance[neighborNode]:
                            heappush(pQueue, (newDist, neighborNode))
                            distance[neighborNode]=newDist 
                            parents[neighborNode]=[inBetweenNode]
                        if distance[neighborNode]==newDist:
                            sigma[neighborNode]+=sigma[inBetweenNode]
                            if inBetweenNode not in parents[neighborNode]:
                                parents[neighborNode].append(inBetweenNode)
        return stack, parents, sigma, delta

 
    def calculateEdgeBetweenness(self, weight = True):
        '''
        Uses a graph and returns the edgeBetwenness of the edges in the graph
        Implemented Brandes algorithm for betweenness found at 
        https://www.tandfonline.com/doi/epdf/10.1080/0022250X.2001.9990249?needAccess=true
        '''

        edgeBetweenness = {}
        for edge in self.graph.edges:
            edgeBetweenness[edge] = 0
        
        for sourceNode in self.graph.nodes:

            if weight == False:
                stack, parents, sigma, delta = self.bfs(sourceNode)
                
            elif weight == True:
                stack, parents, sigma, delta = self.dijkstras(sourceNode)
  
            while len(stack)>0:
                node = stack.pop()
                for otherNode in parents[node]:
                    edge = tuple(sorted((otherNode, node)))
                    edgeBetweenness[edge]+= (sigma[otherNode] / sigma[node]) * (1 + delta[node])
                    delta[otherNode] += (sigma[otherNode] / sigma[node]) * (1 + delta[node])


        for edge in edgeBetweenness:
                edgeBetweenness[edge]/=2 #because graph is undirected, edges are counted twice

        return edgeBetweenness
    


    def girvanNewmanAlgo(self, weight):
        while len(self.graph.edges)>0:
            edgeBetweenness = self.calculateEdgeBetweenness(weight)
            highestEdge = max(edgeBetweenness, key=edgeBetweenness.get)
            self.graph.remove_edge(*highestEdge)
            self.checkAgainstNX(weight)
            self.plotGraph()

    def plotGraph(self):
        nx.draw(self.graph)
        plt.show()
    
    def checkAgainstNX(self, weight):
        if weight == True:
            customEbc = self.calculateEdgeBetweenness(weight=True)
            nxEbc = nx.edge_betweenness_centrality(self.graph, weight="weight", normalized=False)
        else:
            customEbc = self.calculateEdgeBetweenness(weight=False)
            nxEbc = nx.edge_betweenness_centrality(self.graph, weight=False, normalized=False)

        #used chatGPT for formatting this output
        print(f"{'Edge':<10} {'Custom':<10} {'NetworkX':<10}")
        print("=" * 30)
        for edge in self.graph.edges():
            print(f"{str(edge):<10} {customEbc[edge]:<10.6f} {nxEbc[edge]:<10.6f}")

        assert all(abs(customEbc[e] - nxEbc[e]) < 1e-6 for e in self.graph.edges()), "Mismatch in results!"


G = nx.Graph()
G.add_weighted_edges_from([
    ('A', 'B', 1),
    ('B', 'C', 2),
    ('A', 'C', 2), 
    ('C', 'D', 1),
    ('D', 'E', 2),
    ('B', 'E', 3)
])
gnG = GirvanNewman(G)
#Weighted Edges
print("weighted")
gnG.girvanNewmanAlgo(True)

G = nx.Graph()
G.add_weighted_edges_from([
    ('A', 'B', 1),
    ('B', 'C', 2),
    ('A', 'C', 2), 
    ('C', 'D', 1),
    ('D', 'E', 2),
    ('B', 'E', 3)
])
gnG = GirvanNewman(G)
#unweighted edges
print("unweighted")
gnG.girvanNewmanAlgo(False)