from collections import deque
from heapq import heappop, heappush
import matplotlib.pyplot as plt
import networkx as nx

class GirvanNewman:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.originalGraph = graph

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

                        edgeWeight = self.graph[inBetweenNode][neighborNode].get("weight", 1)
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
    


    def girvanNewmanAlgo(self, weight, method):
        '''
        https://medium.com/smucs/community-detection-label-propagation-vs-girvan-newman-part-1-c7f8680062c8#:~:text=Well%2C%20this%20is%20the%20result,of%20modularity%20comes%20into%20play.&text=Essentially%2C%20modularity%20measures%20how%20strong,graph%20into%20separate%20communities%20is.
        '''
        
        if method == "modularity":
            bestPartition = None
            bestModularity = float("-inf")
            while len(self.graph.edges)>0:
                edgeBetweenness = self.calculateEdgeBetweenness(weight)
                highestEdge = max(edgeBetweenness, key=edgeBetweenness.get)
                self.graph.remove_edge(*highestEdge)

                communities = self.getCommunities()
                curModularity = self.modularity(self.originalGraph,communities)
                if curModularity>bestModularity:
                    bestModularity=curModularity
                    bestPartition = communities
                else:
                    break
            return bestPartition
        elif method == "modularityNum":
            bestPartition = None
            bestModularity = float("-inf")
            while len(self.graph.edges)>0:
                edgeBetweenness = self.calculateEdgeBetweenness(weight)
                highestEdge = max(edgeBetweenness, key=edgeBetweenness.get)
                self.graph.remove_edge(*highestEdge)

                communities = self.getCommunities()
                curModularity = self.modularity(self.originalGraph,communities)
                if curModularity>bestModularity:
                    bestModularity=curModularity
                    bestPartition = communities
                    if len(communities)>15:
                        break
                else:
                    if len(communities)<7 or len(communities)>15:
                        break
            return bestPartition
        elif method == "numEdges75":
            totalEdges = len(self.graph.edges())
            while len(self.graph.edges)>totalEdges*.25:
                edgeBetweenness = self.calculateEdgeBetweenness(weight)
                highestEdge = max(edgeBetweenness, key=edgeBetweenness.get)
                self.graph.remove_edge(*highestEdge)
                communities = self.getCommunities()
            return communities
        elif method == "dendrogram":
            dendrogram = []
            while len(self.graph.edges)>0:
                edgeBetweenness = self.calculateEdgeBetweenness(weight)
                highestEdge = max(edgeBetweenness, key=edgeBetweenness.get)
                self.graph.remove_edge(*highestEdge)
                communities = self.getCommunities()
                if len(dendrogram)==0 or dendrogram[-1]!=communities:
                    dendrogram.append(sorted(communities))
            return dendrogram
        else:
            return False
        
                
    def getCommunities(self):
        '''
        Get the communities in a graph
        '''
        visited = {}
        communities = []

        for node in self.graph.nodes():
            visited[node] = False
        
        for node in self.graph.nodes():
            if visited[node]==False:
                curCommunity, visited = self.connectedBFS(node, visited)
                communities.append(sorted(curCommunity))

        return communities
                

    def connectedBFS(self, node, visited):
        '''
        Use BFS to find all connected nodes
        '''
        queue = deque([node])
        curCommunity = [node]
        visited[node]=True

        while len(queue)>0:
            inBetweenNode = queue.popleft()         
            for neighborNode in self.graph.neighbors(inBetweenNode):
                if visited[neighborNode]==False:
                    queue.append(neighborNode)
                    visited[neighborNode]= True
                    curCommunity.append(neighborNode)
        return curCommunity, visited

    def modularity(self, graph: nx.Graph, communities: list) -> float:
        self.setFixedDegrees(graph)
        # Calculates modularity of the graph

        degree_sum = sum(self.fixedDegree.values())
        m = degree_sum/2

        totalSum = 0
        for community in communities:
            if len(community) != 0:
                community = set(community)
                sumC = sum(weight * (2 if u != v else 1) for u,v,weight in graph.edges(community, data="weight", default = 0) if v in community)
                sumCHat = sum(self.fixedDegree[node] for node in community)
                totalSum += (sumC - ((sumCHat**2)/(2*m)))
        return totalSum / (2 * m)

    def setFixedDegrees(self, graph: nx.Graph) -> None:
        #Used to calculate modularity for current graph & community division
        self.fixedDegree = {
            node: deg - (graph.get_edge_data(node, node, {}).get("weight", 0)) 
            for node, deg in graph.degree(weight="weight")
            }

    # def modularity(self, graph, communities):
    #     '''
    #     m = number of edges (unweighted), weighted = 1/2*sum(all weights for nodes i,j)
    #     Aij = edge weight for the edge between i and j
    #     Ki = weighted degree of i
    #     Kj = weighted degree of j
    #     delta 1 if in same community, 0 if not
    #     mod = 1/2m * sum(Aij- ((ki*kj)/2m)* delta)
    #     '''

    #     m = graph.size(weight="weight")
    #     summation = 0.0
    #     for i in graph.nodes():
    #         for j in graph.nodes():
    #             if graph.has_edge(i,j):
    #                 Aij = graph[i][j].get("weight", 1)
    #             else:
    #                 Aij = 0
    #             Ki = self.getDegree(i, graph)
    #             Kj = self.getDegree(j, graph)

    #             com1 = self.getCommunity(i, communities)
    #             com2 = self.getCommunity(j, communities)
    #             if com1 == com2:
    #                 delta = 1
    #             else:
    #                 delta = 0
    #             summation += (Aij - ((Ki*Kj)/(2*m)))* delta
        
    #     modScore = 1/ (2*m) * summation
    #     return modScore 

    # def getDegree(self, node, graph):
    #     '''
    #     returns the degree of a node
    #     '''
    #     degree = 0
    #     for neighbor in graph.neighbors(node):
    #         edge = graph[node][neighbor].get("weight", 1)
    #         degree +=edge
    #     return degree  

    # def getCommunity(self, node, communities):
    #     '''
    #     returns the index of the community a node belongs to
    #     '''
    #     for i in range(len(communities)):
    #         if node in communities[i]:
    #             return i




def main():

    G = nx.Graph()
    G.add_weighted_edges_from([
        ("A", "B", 1),
        ("B", "C", 2),
        ("A", "C", 2), 
        ("C", "D", 1),
        ("D", "E", 2),
        ("B", "E", 3)
    ])
    gnG = GirvanNewman(G)
    # nx.draw(G, with_labels=True)
    # plt.show()
    
    #Weighted Edges
    print("weighted")
    print(gnG.girvanNewmanAlgo(True, "numEdges75"))

    G = nx.Graph()
    G.add_weighted_edges_from([
        ("A", "B", 1),
        ("B", "C", 2),
        ("A", "C", 2), 
        ("C", "D", 1),
        ("D", "E", 2),
        ("B", "E", 3)
    ])
    gnG = GirvanNewman(G)
    #unweighted edges
    print("unweighted")
    print(gnG.girvanNewmanAlgo(False, "numEdges75"))
if __name__ == "__main__":
    main()