from collections import deque
import random
import networkx as nx

class LPA:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
    
    def bfs(self, sourceNode, maxDepth):
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
            targetNode = int(targetNode)
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
            inBetweenNode = int(inBetweenNode)
            stack.append(inBetweenNode)
            dist = distance[inBetweenNode]
            if dist>maxDepth:
                continue
            for neighborNode in self.graph.neighbors(inBetweenNode):
                neighborNode = int(neighborNode)
                if distance[neighborNode] == -1:
                    queue.append(neighborNode)
                    distance[neighborNode]=dist+1
                if distance[neighborNode]==dist+1:
                    sigma[neighborNode]+=sigma[inBetweenNode]
                    parents[neighborNode].append(inBetweenNode)
        return stack, parents, sigma, delta
    
    def calculateEdgeBetweenness(self, maxDepth):
        '''
        Uses a graph and returns the edgeBetwenness of the edges in the graph
        Implemented Brandes algorithm for betweenness found at 
        https://www.tandfonline.com/doi/epdf/10.1080/0022250X.2001.9990249?needAccess=true
        '''

        edgeBetweenness = {}
        for edge in self.graph.edges:
            edge = tuple(sorted((int(edge[0]), int(edge[1]))))
            edgeBetweenness[edge] = 0
                    
        for sourceNode in self.graph.nodes:
            sourceNode = int(sourceNode)
            stack, parents, sigma, delta = self.bfs(sourceNode, maxDepth)
  
            while len(stack)>0:
                node = stack.pop()
                node = int(node)
                for otherNode in parents[node]:
                    otherNode = int(otherNode)
                    edge = tuple(sorted((otherNode, node)))
                    edgeBetweenness[edge]+= (sigma[otherNode] / sigma[node]) * (1 + delta[node])
                    delta[otherNode] += (sigma[otherNode] / sigma[node]) * (1 + delta[node])


        for edge in edgeBetweenness:
                edgeBetweenness[edge]/=2 #because graph is undirected, edges are counted twice

        return edgeBetweenness
    

    def WLPA(self, maxDepth, maxIter):
        labels={}
        commCount={}
        for vertex in self.graph.nodes():
            labels[vertex]=vertex
            commCount[vertex]=1

            
        edgeB = self.calculateEdgeBetweenness(maxDepth)
        
        numIter = 0
        targetComms = 10
        maxCommSize = len(self.graph)//targetComms
        minCommSize = len(self.graph)//(targetComms*2)
        while True:
            changes =0
            nodes = list(self.graph.nodes) 
            random.shuffle(nodes)
            
            if numIter == maxIter:
                print("broke due to iterations")
                break
            for vertex in nodes:
                neighborsByEB = {}
                for neighbor in self.graph.neighbors(vertex):
                    neighborsByEB[neighbor]=edgeB[tuple(sorted((vertex, neighbor)))]
                sortedTemp = sorted(neighborsByEB.items(), key=lambda item: item[1])

                sortedNeighbors = []
                for n,b in sortedTemp:
                    sortedNeighbors.append(n)
                
                halfSize = max(1, len(sortedNeighbors) // 2)
                checkNeighbors =sortedNeighbors[:halfSize]
                # checkNeighbors = sortedNeighbors[:]
                
                labelWeights = {}
                for nbr in checkNeighbors:
                    edgeWeight = self.graph[vertex][nbr].get("weight", 1)
                    nbrLabel = labels[nbr]
                    if nbrLabel in labelWeights:
                        labelWeights[nbrLabel]+=edgeWeight
                    else:
                        labelWeights[nbrLabel]=edgeWeight
                
                
                if len(labelWeights)>0:
                    # newLabel = max(labelWeights, key=labelWeights.get)
                    sortedLabels = sorted(labelWeights.items(), key=lambda x: x[1], reverse=True)

                    
                    oldLabel = labels[vertex]
                    for newLabel, _ in sortedLabels: 
                        if oldLabel != newLabel:
                            if commCount[oldLabel] < minCommSize and commCount[newLabel] < maxCommSize:
                                commCount[oldLabel] -= 1
                                commCount[newLabel] += 1
                                labels[vertex] = newLabel
                                changes += 1
                                break 
                            
            communities = self.getCommunities(labels)
            if changes ==0:
                print("broke due to convergence")
                break
                    
            numIter +=1
                    
        
        return communities
                

        
    def getCommunities(self, labels):
        communities = {}
        
        for node,label in labels.items():
            if label not in communities:
                communities[label]=[node]
            else:
                communities[label].append(node)
        return communities
            

# G = nx.Graph()
# G.add_edges_from([
#     (1, 2, {'weight': 1}),
#     (2, 3, {'weight': 1}),
#     (3, 1, {'weight': 1}),
#     (3, 4, {'weight': 1}),
#     (4, 5, {'weight': 1}),
#     (5, 6, {'weight': 1}),
#     (4, 6, {'weight': 1})
# ])

# # Run the WLBA-LEB algorithm
# graphW = WLPA_LEB(G)

# maxIter = 100

# communities = graphW.WLPA(3, maxIter)
# print("Communities:", communities)