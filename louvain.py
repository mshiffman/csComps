import networkx as nx

class Louvain:

    def __init__(self):
        self.G = nx.Graph()
        self.communities = []
        self.nodeMapping = {}

    def run(self):

        self.singletonCommunities()
        
        #running phase 1 until modularity reaches a local maxima
        changesMade = True
        while changesMade:
            changesMade = False
            for node in self.G.nodes:
                if self.nodeMovement(node) == True:
                    changesMade = True
        
        #creating new graph
        newGraph = nx.Graph()
        for i in range(len(self.communities)):
            newGraph.add_node(i)
        
        #creating new nodes and edges
        for i in self.G.nodes:
            for j in self.G.nodes:
                if self.G.has_edge(i,j):
                    comm_iIndex = self.findCommunity(i)
                    comm_jIndex = self.findCommunity(j)
                    if newGraph.has_edge(comm_iIndex,comm_jIndex):
                        newGraph.edges[comm_iIndex][comm_jIndex]['weight'] += self.G[i][j]['weight']
                    else:
                        newGraph.add_edge(comm_iIndex,comm_jIndex, weight=self.G[i][j]['weight'])
        
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
                self.nodeMapping[node] = comm
        
        

    def nodeMovement(self, node):
        nodeMoved = False
        curMod = self.modularity()
        bestIndex = self.findCommunity(node)
        for neighbor in nx.neighbors(self.G, node):
            self.nodeToCommunity(node,neighbor)
            if self.modularity() > curMod:
                nodeMoved = True
                bestIndex = self.findCommunity(neighbor)
        self.nodeToCommunity(self.communities[bestIndex])
        return nodeMoved
                    

    def modularity(self):
        edgeData = self.G.edges(data=True)

        #finding the total weight of all edges in the graph
        m = 0
        for edge in edgeData:
            edgeWeight = edge[2]['weight']
            m += edgeWeight

        #calculating the summation part of the modularity algorithm by iterating through edges
        sum = 0
        for i in self.G.nodes():
            for j in self.G.nodes():
                if self.G.has_edge(i,j):
                    A = self.G.get_edge_data(i,j)["weight"]
                else:
                    A = 0
                k_i = self.nodeWeight(i)
                k_j = self.nodeWeight(j)
                sum += [A - ((k_i * k_j)/2*m)] * self.delta(i,j)
        
        #finally, multiplying by 1/2m
        return sum/(2 * m)

    def nodeWeight(self, node):
        total = 0
        for neighbor in self.G.neighbors(node):
            weight = self.G.get_edge_data(neighbor, node)["weight"]
            total += weight
        return total

    def findCommunity(self, node):
        for c_index in range(len(self.communities)):
            if node in self.communities(c_index):
                return c_index
        print("Error: node",node,"is not part of a community.")

    def delta(self,node_i, node_j):
        if self.findCommunity(node_i) == self.findCommunity(node_j):
            return 1
        else: 
            return 0
    

def main():
    # Create a graph
    G = nx.Graph()

    # Add edges with weights
    G.add_edge("A", "B", weight=5)
    G.add_edge("A", "C", weight=3)
    G.add_edge("B", "C", weight=2)
    G.add_edge("C", "D", weight=4)
    G.add_edge("A","A", weight = 2)
    G.edges["C", "D"]['weight'] += 6

    print(G.get_edge_data("A", "A")["weight"])
    

if __name__ == "__main__":
    main()