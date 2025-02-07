import networkx as nx

class Louvain:

    def __init__(self):
        self.G = nx.Graph()
        self.communities = []

    def run(self, G: nx.Graph):

        #placing each node in its own community to begin
        for node in G.nodes:
            node_as_list = [node]
            self.communities.append(node_as_list)
        
        #running phase 1 until modularity reaches a local maxima
        changesMade = True
        while changesMade:
            changesMade = False
            for node in G.nodes:
                if self.nodeMovement(node) == True:
                    changesMade = True
        
        #creating new graph
        newGraph = nx.Graph()

                    

        


    def nodeToCommunity(self, node, destNode):
        for comm in self.communities:
            if node in comm:
                comm.remove(node)
            if destNode in comm:
                comm.append(node)
        
        

    def nodeMovement(self, node):
        nodeMoved = False
        curMod = self.modularity()
        bestCommunity = self.findCommunity(node)
        for neighbor in nx.neighbors(self.G, node):
            self.nodeToCommunity(node,neighbor)
            if self.modularity() > curMod:
                nodeMoved = True
                bestCommunity = self.findCommunity(j)
        self.nodeToCommunity(bestCommunity)
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
        for c in self.communities:
            if node in c:
                return c
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

    print(G.get_edge_data("A", "B")["weight"])
    

if __name__ == "__main__":
    main()