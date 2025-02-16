import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class GirvanNewman:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    def shortestPaths(self, source):

        allPathsList = []

        parentDict = self.bfsForshortestPath(source)


        for eachNode in parentDict:
            if eachNode != None and eachNode!= source:

                eachPath = []
                queue = deque()
                queue.append(eachNode)

                while len(queue) > 0:
                    node = queue.popleft()
                    eachPath.insert(0,node)
                    if node == source:
                        break
                    for parent in parentDict[node]:
                        queue.append(parent)
                
                allPathsList.append(eachPath)
                
        return allPathsList


    def bfsForshortestPath(self, source):
        '''
        Finds the shortest path between the source node and all other nodes in the graph
        '''
        distance = {}
        parent = {}

        for i in self.graph.nodes:
            distance[i] = float('inf')
            parent[i] = []
        
        queue = deque()
        distance[source]= 0
        queue.append(source)


        while len(queue) > 0:
            curNode = queue.popleft()
            for neighbor in self.graph[curNode]:
                if distance[neighbor] == float('inf'):
                    queue.append(neighbor)
                    distance[neighbor] =  distance[curNode]+1
                    parent[neighbor].append(curNode)
                elif distance[neighbor] == distance[curNode] + 1:
                    parent[neighbor].append(curNode)
        return parent


    def edgeBetweenness(self):
        '''
        Uses the data from shortest paths to calculate the edge betweenness of every edge in the graph
        return a dictionary (unsorted) of edge betweenness values
        '''
        edgeBetweenness = {}

        #for each node check all of its shortest paths
        for node in self.graph.nodes:
            nodesShortestPaths = self.shortestPaths(node)

            #for each target node of the source node
            for path in nodesShortestPaths:
                pathLen = len(path) - 1 

                #get each edge in the path for the node
                for i in range(pathLen):
                    edge = tuple(sorted((path[i], path[i + 1])))
                    if edge not in edgeBetweenness:
                        edgeBetweenness[edge] = 0
                    edgeBetweenness[edge] += 1

        
        for edge in edgeBetweenness:
            edgeBetweenness[edge] = (edgeBetweenness[edge]/2)/10  
        return edgeBetweenness
    
    def girvanNewmanAlgo(self):
        '''
        Uses self.graph and self.edgebetweenness to calculate which edge to remove.
        That edge is deleted from the graph and the process is repeated.
        Repeats until no nodes left.
        Since we are doing this to detect communities, it saves an svg of some of the steps of this process
        Rn works when using networkx built in edgebetweenness
        '''  
        iter = 0
        while len(self.graph.edges) >0:
            edgeB2 = sorted(nx.edge_betweenness_centrality(self.graph).items(), key = lambda pair: pair[1])
            edgeB = sorted(self.edgeBetweenness().items(), key = lambda pair: pair[1])
            print("edgeB1", edgeB)
            print("edgeB2", edgeB2, "\n")
            highestEdge = edgeB[-1][0] #print to make sure this works
            self.graph.remove_edge(*highestEdge)
            iter +=1  
            pos = nx.spring_layout(self.graph, seed=7)
            nx.draw_networkx_labels(self.graph, pos, font_size=20, font_family="sans-serif")
            nx.draw(self.graph, pos)
            plt.show()
        

def creategraph() -> nx.Graph:
    # Creates NetworkX graph to test
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(0, 3)
    G.add_edge(1, 4)
    G.add_edge(2, 4)
    G.add_edge(3, 4)
    G.add_edge(0, 4)

    pos = nx.spring_layout(G, seed=7)
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

    nx.draw(G, pos)
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()
    return G

graph = creategraph()

def main():
    
    testGraph = GirvanNewman(graph)

    testGraph.girvanNewmanAlgo()


if __name__ == "__main__":
    main()