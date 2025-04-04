from collections import defaultdict, deque
from heapq import heappop, heappush
import matplotlib.pyplot as plt
import networkx as nx
import time

class GirvanNewman:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.originalGraph = graph

    def bfs(self, sourceNode):
        '''
        BFS code adapted from Brandes
        
        Args: 
            sourceNode: The node to run BFS from
        
        Returns:
            stack: the order to calculate EBC
            parents: the parent nodes of a given node
            sigma: number of shortest paths from s to t using edge
            delta: number of shortest paths from s to t
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
        
        Args: 
            sourceNode: The node to run Dijkstra's from
        
        Returns:
            stack: the order to calculate EBC
            parents: the parent nodes of a given node
            sigma: number of shortest paths from s to t using edge
            delta: number of shortest paths from s to t
        '''
        stack = []
        parents = defaultdict(list)
        sigma = defaultdict(int)
        distance = {}
        delta = defaultdict(int)
        pQueue = []
        edgeCount = {}
        maxDepth = 2
        #initialize
        for targetNode in self.graph.nodes:
            distance[targetNode]=float("inf")
            edgeCount[targetNode]=float("inf")


        sigma[sourceNode] = 1
        distance[sourceNode] = 0
        heappush(pQueue, (0, sourceNode))
        edgeCount[sourceNode] = 0 

        while len(pQueue)>0:
                dist, inBetweenNode = heappop(pQueue)
                
                if edgeCount[inBetweenNode] >= maxDepth:
                    continue
                
                stack.append(inBetweenNode)

                if dist <= distance[inBetweenNode]:
                    for neighborNode in self.graph.neighbors(inBetweenNode):

                        edgeWeight = self.graph[inBetweenNode][neighborNode].get("weight", 1)
                        newDist = distance[inBetweenNode]+edgeWeight

                        if newDist < distance[neighborNode]:
                            heappush(pQueue, (newDist, neighborNode))
                            distance[neighborNode]=newDist 
                            parents[neighborNode]=[inBetweenNode]
                            edgeCount[neighborNode] = edgeCount[inBetweenNode] + 1
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
        
        Args: 
            weight=True if edge weights hsould be considered
        
        Returns:
            EBC calculations for each edge
        '''

        edgeBetweenness = {}
        for edge in self.graph.edges:
            edge = tuple(sorted((edge[0], edge[1])))
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
        Runs GN
        
        Args:
            weight = True if edge weight values should be used
            method: stopping condition. Only ran with dendrogram case for paper
        Returns:
            community divisions
        '''
        
        mapping = {node: int(node) for node in self.graph.nodes()}
        self.graph = nx.relabel_nodes(self.graph, mapping)
        
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
        Returns: the communities in a graph
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
        
        Args: 
            node: source node to find connected components from
            visited: dictionary of if we have visited a node yet
        
        Returns:
            community of nodes from source node
            visted dictionary
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
        '''
        Args:
            graph: input graph
            communities: list of lists (representing community structure)
            
        Returns:
            modularity score for graph with that community divisions
        '''
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
        '''
        helper function: Used to calculate modularity for current graph & community division
        '''
        self.fixedDegree = {
            node: deg - (graph.get_edge_data(node, node, {}).get("weight", 0)) 
            for node, deg in graph.degree(weight="weight")
            }

