import networkx as nx
import random
import math

class Louvain:

    def __init__(self, graph):
        self.G = graph
        self.originalGraph = graph
        self.communities = []
        self.nestedCommunities = []
    
    def run(self):

        self.singletonCommunities()
        improved = True
        firstIteration = True

        #general while loop, runs both phases until nothing is changed
        while improved:
            improved = False
            #running phase 1 until modularity reaches a local maxima
            changesMade = True
            iterations = 0
            while changesMade and iterations < 1000:
                iterations += 1
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

            for i in range(len(self.communities)):
                # Will need to unfold the nested structure eventually with some recursive algorithm. 
                newGraph.add_node(i)
            
            #creating edges, with weight based on totals
            for i in self.G.nodes:
                for j in self.G.nodes:        
                    if self.G.has_edge(i,j):
                        comm_iIndex = self.findCommunity(i)
                        comm_jIndex = self.findCommunity(j)
                        if newGraph.has_edge(comm_iIndex,comm_jIndex):
                            newGraph[comm_iIndex][comm_jIndex]['weight'] += self.G[i][j]['weight']
                        else:
                            newGraph.add_edge(comm_iIndex,comm_jIndex, weight=self.G[i][j]['weight'])
            self.G = newGraph
            self.singletonCommunities()
        


    def singletonCommunities(self):
        self.communities = []
        for node in self.G.nodes:
            node_as_list = [node]
            self.communities.append(node_as_list)


    def nodeToCommunity(self, node, destNode):
        for comm in self.communities:
            if node in comm:
                comm.remove(node)
            if destNode in comm:
                comm.append(node)

    def nodeMovement(self, node):
        originalCommunity = self.findCommunity(node)
        nodeMoved = False
        curMod = self.modularity()
        bestNeighbor = node
        for neighbor in nx.neighbors(self.G, node):
            if self.findCommunity(node) != self.findCommunity(neighbor):
                self.nodeToCommunity(node,neighbor)
            if self.modularity() > curMod:
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
                    

    def modularity(self):
    #finding the total weight of all edges in the graph
        m = 0
        for i in self.G.nodes:
            for j in self.G.nodes:
                if self.G.has_edge(i,j):
                    m += self.G.edges[i,j]["weight"]
        m = m / 2

        #calculating the summation part of the modularity algorithm by iterating through edges
        total = 0
        for i in self.G.nodes():
            for j in self.G.nodes():
                if self.G.has_edge(i,j):
                    A = self.G.get_edge_data(i,j)["weight"]
                else:
                    A = 0
                k_i = self.nodeWeight(i)
                k_j = self.nodeWeight(j)
                total += (A - ((k_i * k_j)/(2*m))) * self.delta(i,j)
        #finally, multiplying by 1/2m
        return total/(2 * m)
    

    def nodeWeight(self, node):
        total = 0
        for otherNode in self.G.nodes:
            if self.G.has_edge(node, otherNode):
                total += self.G.edges[node,otherNode]["weight"]
        return total

    def findCommunity(self, node):
        for c_index in range(len(self.communities)):
            if node in self.communities[c_index]:
                return c_index
        print("Error: node",node,"is not part of a community.")

    def delta(self,node_i, node_j):
        if self.findCommunity(node_i) == self.findCommunity(node_j):
            return 1
        else: 
            return 0

    

def main():
    # Create a graph
    '''
    graph = nx.erdos_renyi_graph(15, 0.2, seed=40)
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.uniform(1, 5)
    print("graph made")
    '''
    
    
    graph = nx.Graph()
    graph.add_edge(0, 0, weight = 14)
    graph.add_edge(1, 1, weight=16)
    graph.add_edge(2, 2, weight=2)
    graph.add_edge(3, 3, weight=4)
    graph.add_edge(0, 1, weight=1)
    graph.add_edge(0, 2, weight=1)
    graph.add_edge(3, 2, weight=1)
    graph.add_edge(0, 3, weight=4)
    graph.add_edge(1, 2, weight=3)
    #l = Louvain(graph)
    #l.singletonCommunities()
    #print(nx.community.modularity(l.G, l.communities))
    #print(l.modularity())
    

    l = Louvain(graph)
    l.run()
    print(l.nestedCommunities)
    print(nx.community.louvain_communities(graph))
    
    

if __name__ == "__main__":
    main()