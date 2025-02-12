from collections import deque
import heapq
import matplotlib.pyplot as plt
import networkx as nx

class GirvanNewman:
    def __init__(self, graph: nx.Graph):
        self.graph = graph

    # def dijkstras(self, sourceNode):
    #     distance = {}
    #     sigma = {}
    #     parents={}
    #     for node in self.graph.nodes:
    #         distance[node]= float('inf')
    #         if node == sourceNode:
    #             distance[sourceNode]=0
    #             sigma[sourceNode]=1
    #         else:
    #             sigma[sourceNode]=0
    #         parents[node]=[]
        

    #     queue = [(0, sourceNode)]

    #     while len(queue)>0:
    #         dist, curNode = heapq.heapop(queue)
    #         if dist <= distance[curNode]:



    def calculateEdgeBetweenness(self):
        '''
        Uses a graph and returns the edgeBetwenness of the edges in the graph
        Implemented Brandes algorithm for betweenness found at https://www.tandfonline.com/doi/epdf/10.1080/0022250X.2001.9990249?needAccess=true
        '''

        edgeBetweenness = {}
        for edge in self.graph.edges:
            edgeBetweenness[edge] = 0
        
        for sourceNode in self.graph.nodes:

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


            #BFS
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
            
            #calculate edgeBetweenness
            while len(stack)>0:
                node = stack.pop()
                for otherNode in parents[node]:
                    edge = tuple(sorted((otherNode, node)))
                    edgeBetweenness[edge]+= (sigma[otherNode] / sigma[node]) * (1 + delta[node])
                    delta[otherNode] += (sigma[otherNode] / sigma[node]) * (1 + delta[node])

        for edge in edgeBetweenness:
            edgeBetweenness[edge]/=2
        
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
    