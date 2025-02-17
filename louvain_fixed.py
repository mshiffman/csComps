import networkx as nx
import random

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

        self.G = self.originalGraph
        


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
        #might want to add resolution to alter the communities
        return nx.community.modularity(self.G, self.communities, resolution=1.2)
 

    def nodeWeight(self, node):
        total = 0
        for neighbor in self.G.neighbors(node):
            weight = self.G.get_edge_data(neighbor, node)["weight"]
            total += weight
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
    graph = nx.erdos_renyi_graph(40, 0.4, seed=40)
    for u, v in graph.edges():
        graph[u][v]['weight'] = random.uniform(0.1, 1.0)
    print("graph made")
    
    '''graph = nx.Graph()
    graph.add_edge(0, 1, weight=4)
    graph.add_edge(0, 2, weight=1)
    graph.add_edge(1, 2, weight=1)
    graph.add_edge(1, 3, weight=1)
    graph.add_edge(2, 3, weight=2)
    graph.add_edge(2, 4, weight=4)
    graph.add_edge(3, 4, weight=2)'''

    l = Louvain(graph)
    l.run()
    print(l.nestedCommunities)
    print(nx.community.louvain_communities(graph))
    

if __name__ == "__main__":
    main()