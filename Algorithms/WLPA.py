from collections import deque
import random
import networkx as nx

'''
Code for LPA, WLPA-LEB, and modified version of WLPA-LEB
'''
class LPA:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.allLabelWeights ={}
        self.commCount={}
    
    def bfs(self, sourceNode, maxDepth):
        '''
        BFS code adapted from Brandes
        
        Args: 
            sourceNode: The node to run BFS from
            maxDepth: how deep to run BFS from every node
        
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
        Args: 
            weight=True if edge weights hsould be considered
        
        Returns:
            EBC calculations for each edge
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
    
    
    def calculateLabelWeights(self, edgeB, vertex, labels):
        '''
        helper function to calculate the value of the label
        
        Args:
            edgeB: dictionary of edge betweenness values
            vertex: given node
            labels: labels of nearby nodes
        Returns:
            weights of labels to connected nodes
        '''
        
        neighborsByEB = {}
        for neighbor in self.graph.neighbors(vertex):
            key = tuple(sorted((vertex, neighbor)))
            neighborsByEB[neighbor] = edgeB[key]

        sortedNeighbors = []
        for neighbor, value in sorted(neighborsByEB.items(), key=lambda item: item[1]):
            sortedNeighbors.append(neighbor)

        
        halfSize = max(1, len(sortedNeighbors) // 2)
        checkNeighbors = sortedNeighbors[:halfSize]
        # checkNeighbors = sortedNeighbors[:]
        
        labelWeights = {}
        for nbr in checkNeighbors:
            edgeWeight = self.graph[vertex][nbr].get("weight", 1)
            nbrLabel = labels[nbr]
            labelWeights[nbrLabel] = labelWeights.get(nbrLabel, 0) + edgeWeight
        return labelWeights
    
    
    def getCommunitySizes(self,community):
        '''
        Args: 
            community: name of community you want to find the size for
        Returns:
            Size of the community
        '''
        communitySize = 0
        for node, weight in self.communityWeights[community].items():
            communitySize+=1
        return communitySize
    
    
    def moveNode(self, labels, vertex, labelWeights, reassignList, changes):
        '''
        helper function to move node into correct community for modified version
        Args: 
            labels: dictionary of labels
            vertex: node to move
            labelWeights: dictionary of labels and weights
            reassignList: nodes to reassign
        Returns:
            changes: number of changes made
            labels: dictionary of node labels
            reassignList: nodes to reassign
        '''
        oldLabel = labels[vertex]
        
        for newLabel, _ in sorted(labelWeights.items(), key=lambda x: x[1], reverse=True):
            if oldLabel != newLabel:
                
                commSize = self.getCommunitySizes(labels, newLabel)                
                
                #if it can move to the community
                if commSize < self.maxCommSize:
                    labels[vertex] = newLabel
                    changes += 1
                    if vertex in self.communityWeights[oldLabel]:
                        del self.communityWeights[oldLabel][vertex]
                    self.communityWeights[newLabel][vertex] = labelWeights.get(newLabel, 0)
                    break
                
                else:
                    communities = self.getCommunities(labels)
                    weakestNode = None
                    weakestNodeWeight = float('inf')  

                    # check all nodes to find weakest
                    for node, weight in self.communityWeights[newLabel].items():
                        if weight < weakestNodeWeight:
                            weakestNodeWeight = weight
                            weakestNode = node
                            

                    # found weakest node, reassign
                    if weakestNode !=None:
                        nodeWeight = labelWeights.get(newLabel)
                        
                        if nodeWeight > weakestNodeWeight:
                            if vertex in self.communityWeights[oldLabel]:
                                del self.communityWeights[oldLabel][vertex]
                            self.communityWeights[newLabel][vertex] = nodeWeight

                            
                            labels[vertex] = newLabel
                            changes += 1
                            
                            del self.communityWeights[newLabel][weakestNode]
                            self.communityWeights[weakestNode][weakestNode] = 0
                            labels[weakestNode] = weakestNode
                            reassignList.append(weakestNode) 
                            break
                    else:
                        print("No weakest node", communities[newLabel])
        return changes, labels, reassignList

    
    def WLPA_Mod(self, maxDepth, maxIter, targetComms):
        '''
        modifed version of wlpa-leb
        Args:
            maxDepth: depth for EBC calculations
            maxIter: iteration limit
            targetComms: goal number of communities
        Returns:
            Community divisions
        '''
        labels = {}
        self.allLabelWeights = {}
        self.communityWeights = {} 
        self.communitySize = {}


        for vertex in self.graph.nodes():
            labels[vertex] = vertex
            self.allLabelWeights[vertex] = {}
            self.communityWeights[vertex]={vertex:0}
            self.communitySize[vertex] =1
        
        edgeB = self.calculateEdgeBetweenness(maxDepth)
        
        numIter = 0
        self.maxCommSize = len(self.graph) // targetComms

        while True:
            changes = 0
            nodes = list(self.graph.nodes())
            random.shuffle(nodes)
            reassignList = []
            
            if numIter == maxIter:
                break
            
            for vertex in nodes:
                labelWeights = self.calculateLabelWeights(edgeB,vertex, labels)
                self.allLabelWeights[vertex] = labelWeights
                
                if labelWeights:
                    changes, labels, reassignList = self.moveNode(labels,vertex, labelWeights, reassignList, changes)
            
            
            
            its = 0
            while len(reassignList)>0:
                random.shuffle(reassignList)

                for weakNode in reassignList:
                    labelWeights = self.allLabelWeights[weakNode]
                    reassignList.remove(weakNode)
                    changes, labels, reassignList = self.moveNode(labels, weakNode, labelWeights,reassignList, changes)
                    
                
                its +=1
                if its>1000:
                    break



            communities = self.getCommunities(labels)
            if changes == 0:
                print("broke due to convergence")
                break

            numIter += 1

        return communities

                
    def WLPA(self, maxDepth, maxIter):
        '''
        code for wlpa-leb
        Args:
            maxDepth: depth for EBC
            maxIter: maximum number of iterations
        Returns:
            community divisions
        '''
        labels={}
        commCount={}
        for vertex in self.graph.nodes():
            labels[vertex]=vertex
            commCount[vertex]=1

            
        edgeB = self.calculateEdgeBetweenness(maxDepth)
        
        numIter = 0

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
                
                labelWeights = {}
                for nbr in checkNeighbors:
                    edgeWeight = self.graph[vertex][nbr].get("weight", 1)
                    nbrLabel = labels[nbr]
                    if nbrLabel in labelWeights:
                        labelWeights[nbrLabel]+=edgeWeight
                    else:
                        labelWeights[nbrLabel]=edgeWeight
                
                
                if len(labelWeights)>0:
                    newLabel = max(labelWeights, key=labelWeights.get)

                    
                    oldLabel = labels[vertex]

                    if oldLabel != newLabel:
                        commCount[oldLabel] -= 1
                        commCount[newLabel] += 1
                        labels[vertex] = newLabel
                        changes += 1
                        break         
            if changes ==0:
                print("broke due to convergence")
                break
                    
            numIter +=1
                    
        communities = self.getCommunities(labels)    
        return communities
        
    def getCommunities(self, labels):
        '''
        helper function to return communities
        Args:
            labels: dictionary of node labels
        Returns:
            communities in graph
        '''
        communities = {}
        
        for node,label in labels.items():
            if label not in communities:
                communities[label]=[node]
            else:
                communities[label].append(node)
        return communities
    
    def LPA(self):
        '''
        LPA algorithm
        Returns:
            community divisions
        '''
        colors = self.colorNodes()
        
        labels={}
        for vertex in self.graph.nodes():
            labels[vertex]=vertex

        i = 0 
        while True:
            changes = 0
            i+=1
            
            for color, nodes in colors.items():
                for node in nodes:
                    changes, labels = self.updateLabel(node, changes, labels)

                
            if changes ==0:
                break
            
        communities = self.getCommunities(labels)
        return communities 
    
    def updateLabel(self, node, changes, labels):
        '''
        Updating label helper function for LPA
        
        Args:
            node: node to update label of
            changes: number of changes
            labels: dictionary of labels
        Returns:
            changes: number of changes
            labels: dictionary of labels
        '''
        neighborLabels = {}

        for neighbor in self.graph.neighbors(node):
            neighborLabel = labels[neighbor]
            
            if neighborLabel in neighborLabels:
                neighborLabels[neighborLabel]+=1
            else:
                neighborLabels[neighborLabel]=1
            
        
        if len(neighborLabels)>0:
            newLabel = max(neighborLabels, key=neighborLabels.get)
            
            if labels[node] != newLabel:
                changes +=1
                labels[node]= newLabel
        return changes, labels
                
    def colorNodes(self):
        '''
        Welsh-Powell graph coloring algorithm
        
        Returns:
            graph coloring divisions
        '''
        nodes = list(self.graph.nodes())
        colors = {}
        nodeColors = {}
        color = 0
        
        while True:
            uncolored = []
            colors[color]=[]
            
            
            for node in nodes:
                
                canAssign = True
                for neighbor in self.graph.neighbors(node):
                    if neighbor in nodeColors and nodeColors[neighbor]==color:
                        canAssign = False
                
                if canAssign == True:
                    colors[color].append(node)
                    nodeColors[node]= color
                else: 
                    uncolored.append(node)
            
            if len(uncolored)==0:
                break
            
            nodes = uncolored
            color +=1
        return colors
