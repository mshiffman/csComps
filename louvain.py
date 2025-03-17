import networkx as nx
import random
import math
from datetime import datetime

class Louvain:


    def __init__(self, graph, resolution = 1):
        """
        Creates a new Louvain object.

        Args:
            graph: the NX graph to run the algorithm on
            resolution: the resolution parameter gamma, default value 1

        Returns:
            A new Louvain object.
        """
        self.resolution = resolution
        self.G = graph
        self.originalGraph = graph
        self.communities = []
        self.nestedCommunities = []

    def run(self):
        """
        Creates a new Louvain object.

        Args:
            None

        Returns:
            Nothing
        """

        #creates a partition of each n
        self.singletonCommunities()
        improved = True
        firstIteration = True


        #general while loop, runs both phases until nothing is changed
        while improved:
            improved = False
            #running phase 1 until modularity reaches a local maxima
            changesMade = True
            while changesMade:
                changesMade = False
                for node in self.G.nodes:
                    if self.nodeMovement(node) == True:
                        changesMade = True
                        improved = True

            #creating new graph & adding nodes
            newGraph = nx.Graph()
            self.communities = [x for x in self.communities if x != []]
            
            #doing the nesting
            if firstIteration:
                self.nestedCommunities = self.communities
                firstIteration = False
            else:
                temp = []
                for i in range(len(self.communities)):
                    tempInner = []
                    for j in range(len(self.communities[i])):
                        currentComm = self.communities[i][j]
                        tempInner += self.nestedCommunities[currentComm]
                    temp.append(tempInner)
                self.nestedCommunities = temp

            #Adding nodes for each community to the new graph
            for i in range(len(self.communities)):
                newGraph.add_node(i)

            #Adding the weights for edges in the new graph
            for i, j, weight in self.G.edges(data="weight"):
                comm_iIndex = self.findCommunity(i)
                comm_jIndex = self.findCommunity(j)
                if newGraph.has_edge(comm_iIndex,comm_jIndex):
                    newGraph[comm_iIndex][comm_jIndex]['weight'] += weight
                else:
                    newGraph.add_edge(comm_iIndex,comm_jIndex, weight=weight)
            
            #resetting self.G and self.communities for the new iteration
            self.G = newGraph
            self.singletonCommunities()
    
    
    def singletonCommunities(self):
        """
        Places each node into its own community. 

        Args:
            None

        Returns:
            Nothing
        """
        self.fixedDegree = { node: (deg - (self.G.get_edge_data(node, node, {}).get("weight", 0))) 
            for node, deg in self.G.degree(weight="weight")}
        self.communities = []
        for node in self.G.nodes:
            node_as_list = [node]
            self.communities.append(node_as_list)

    def nodeToCommunity(self, node, destNode):
        """
        Moves a node to the community of a particular node. 

        Args:
            node: The node to be moved
            destNode: The node who's community node will be moved into.

        Returns:
            Nothing
        """
        for comm in self.communities:
            if node in comm:
                comm.remove(node)
            if destNode in comm:
                comm.append(node)
    
    def nodeMovement(self, node):
        """
        Attempts to move a node to the community among those of its neighbors
        that will lead to the highest gain in modularity, or keep it as is if no such
        gain exists. 

        Args:
            node: the node to be moved.

        Returns:
            True if the node was moved, False if not.
        """
        originalCommunity = self.findCommunity(node)
        nodeMoved = False
        curMod = self.modularity()
        bestNeighbor = node
        for neighbor in nx.neighbors(self.G, node):
            if self.findCommunity(node) != self.findCommunity(neighbor):
                self.nodeToCommunity(node,neighbor)
                newMod = self.modularity()
                if newMod > curMod:
                    curMod = newMod
                    nodeMoved = True
                    bestNeighbor = neighbor
        if node != bestNeighbor:
            self.nodeToCommunity(node, bestNeighbor)
        else:
            for community in self.communities:
                if node in community:
                    community.remove(node)
            self.communities[originalCommunity].append(node)
        return nodeMoved

    def findCommunity(self, node):
        """
        Returns the community of a node.

        Args:
            node: The node who's community we're looking to find.

        Returns:
            The index of the community of that node. 
        """
        for c_index in range(len(self.communities)):
            if node in self.communities[c_index]:
                return c_index
        print("Error: node",node,"is not part of a community.")

    def modularity(self):
        """
        Returns the modularity of the current graph and partition.

        Args:
            None

        Returns:
            A modularity value [-1,1]
        """
        degree_sum = sum(self.fixedDegree.values())
        m = degree_sum/2

        totalSum = 0
        for community in self.communities:
            if len(community) != 0:
                community = set(community)
                sumC = sum(weight * (2 if u != v else 1) for u,v,weight in self.G.edges(community, data="weight", default = 0) if v in community)
                sumCHat = sum(self.fixedDegree[node] for node in community)
                totalSum += (sumC - self.resolution * ((sumCHat**2)/(2*m)))
        return totalSum / (2 * m)