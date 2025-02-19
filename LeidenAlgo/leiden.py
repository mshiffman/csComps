# Leiden algorithm implementation, Carleton College Computer Science 2025 Comps

import networkx as nx
import random
from collections import deque
import matplotlib.pyplot as plt
import igraph as ig
import leidenalg as lg


class Leiden:

    def __init__(self, graph: nx.Graph):

        self.graph = graph

    def setRefinedCommunities(self, community: list) -> list:
        # Sets communities during refinement step
        outputCommunities = []
        # Used to set communities during refinement step
        for node in community:
            newCommunity = [node]
            outputCommunities.append(newCommunity)
        return outputCommunities
    
    def setInitialCommunities(self, graph: nx.Graph) -> list:
        # Used to set communities during fast local node movement step
        allNodes = list(graph.nodes)
        outputCommunities = []
        for node in allNodes:
            newCommunity = [node]
            outputCommunities.append(newCommunity)
        return outputCommunities

    def moveNodesFast(self, graph: nx.Graph, communities: list) -> list | nx.Graph:
        # Fast local node movement step of Leiden algorithm

        if len(communities) == 1:
            # If only one community inputted, then no need to check node movement in communities
            return communities, graph

        # Get random order of node movement
        nodeOrderQueue = self.setRandQueue(communities)

        while nodeOrderQueue:

            idealCommunity = []

            # Gets first node to move
            curr_node = nodeOrderQueue.popleft()

            # Gets current graph modularity
            currTopMod = self.modularity(graph, communities)

            node_CurrCommunityIndex = self.findCommunity(curr_node, communities)
            node_CurrCommunity = communities[node_CurrCommunityIndex]
            idealCommunity = node_CurrCommunity

            # Examines every possible community
            for community in communities:

                if node_CurrCommunityIndex != communities.index(community):
                    # Removes node from past communities
                    communities = self.removeNodefromCommunities(curr_node, communities)

                    # Adds node to new communities
                    communities = self.addNodeToCommunity(curr_node, community, communities)

                    # Examines modularity of test communities
                    modVal = self.modularity(graph, communities)

                    # If modularity is increased, track mod and community
                    print(f"current top modularity: {currTopMod}")
                    print(f"checking mod of community {communities}: {modVal}")
                    if modVal > currTopMod:
                        currTopMod = modVal
                        # idealCommunity = copy.copy(community)
                        # idealCommunity.remove(curr_node)
                        idealCommunity = community

            if node_CurrCommunity != idealCommunity:
                # If modularity is increased, add node to new community after removing from past
                communities = self.removeNodefromCommunities(curr_node, communities)
                communities = self.removeEmptyCommunities(communities)
                communities = self.addNodeToCommunity(curr_node, idealCommunity, communities)

                # If any neighbors of node aren't in same community
                # or already in the queue, then add to back of queue
                changeNeighbors = self.getChangedNeighbors(curr_node, idealCommunity,
                                                           nodeOrderQueue, graph,
                                                           communities)
                print(f"Neighbors to change: {changeNeighbors}")
                nodeOrderQueue.extend(changeNeighbors)
                print(f"added node to new community: {communities}")
            else:
                communities = self.removeNodefromCommunities(curr_node, communities)
                communities[node_CurrCommunityIndex].append(curr_node)
                communities[node_CurrCommunityIndex].sort()
            print(f"new communities: {communities}")

        return communities, graph

    def refineCommunities(self, communities, graph: nx.Graph) -> list | nx.Graph:
        # Community Refinement step of Leiden algorithm
        refinedCommunities = []
        for community in communities:
            inputCommunities = self.setRefinedCommunities(community)

            # Creates new graph to refine based on communities
            refineGraphInput = nx.Graph()
            for node in community:
                # Adds nodes to the graph
                if graph.has_node(node):
                    refineGraphInput.add_node(node)
            seenEdge = set()
            for i in refineGraphInput.nodes:
                for j in refineGraphInput.nodes:
                    # Adds edges to the graph
                    if graph.has_edge(i, j):
                        checkEdge = tuple(sorted([i, j]))
                        if checkEdge not in seenEdge:
                            edge_weight = graph[i][j]["weight"]
                            refineGraphInput.add_edge(i, j, weight=edge_weight) # RIGHT NOW DOESN'T ACCOUNT FOR EDGES FROM NODE INSIDE TO NODE OUTSIDE SUBGRAPH
                        seenEdge.add(checkEdge)
            
            # Re-routes edges from nodes inside subgraph spanning to nodes
            # outside subgraph, to become edges looping from node inside
            # subgraph back into itself- NEEDS REWORKING, likely can't loop back into itself                    !!!!!!!!
            # and will need to create new graph and have new refinement func
            # for u, v, data in graph.edges(data=True):
            #     if (u in refineGraphInput.nodes and v not in refineGraphInput.nodes):
            #         refineGraphInput.add_edge(u, u, weight=data['weight'])
            #     elif (v in refineGraphInput.nodes and u not in refineGraphInput.nodes):
            #         refineGraphInput.add_edge(v, v, weight=data['weight'])

            newRefCommunity, g = self.moveNodesFast(refineGraphInput, inputCommunities)
            for subcommunity in newRefCommunity:
                refinedCommunities.append(subcommunity)

        return refinedCommunities, graph

    def agglomerateCommunities(self, refinedCommunities: list, graph: nx.Graph, fastMoveCommunities: list) -> list | nx.Graph:
        # Agglomeration step of Leiden algorithm

        # Creates new agglomerated graph
        aggGraph = nx.Graph()

        # Creates new communities to return
        newCommunities = []
        seen = set()

        for community in fastMoveCommunities:
            # Loop is to create the new nodes, as well as add the nodes
            # to new communities based on communities found in the
            # fast local movement step

            subCommunity = []

            for node in community:

                # Makes sure node's community hasn't already been added
                if node in seen:
                    continue

                # Find refined community of node
                findRefComm_index = self.findCommunity(node, refinedCommunities)
                findRefComm = refinedCommunities[findRefComm_index]
                
                newNode = self.createNode(findRefComm)

                aggGraph.add_node(newNode)
                subCommunity.append(newNode)

                # Adds nodes already created in the graph to seen
                for checkNode in findRefComm:
                    seen.add(checkNode)

            newCommunities.append(subCommunity)

        # Set to keep track of edges added to graph
        completedEdge = set()

        for community in refinedCommunities:

            for node in community:
                # Finds neighbors of a node in a community
                nodeNeighbors = list(graph.neighbors(node))

                for neighbor in nodeNeighbors:
                    # Finds the communities of a neighbor
                    neighborCommunity_index = self.findCommunity(neighbor, refinedCommunities)
                    neighborCommunity = refinedCommunities[neighborCommunity_index]

                    # If the community of provided node and its neighbor
                    # are not the same community, an edge must span
                    # between communities, and thus and edge must span
                    # between agglomerated nodes
                    communityNode = self.createNode(community)
                    neighborNode = self.createNode(neighborCommunity)

                    checkEdge = tuple(sorted([node, neighbor]))
                    # Makes sure edge hasn't already been added before
                    if checkEdge not in completedEdge:

                        # Finds edge weight of the given node and neighbor
                        edge_weight = graph[node][neighbor]["weight"]

                        if aggGraph.has_edge(communityNode, neighborNode):
                            # If there already is edge between agglomerated
                            # nodes, increases that edge weight with the
                            # newly found edge weight
                            aggGraph[communityNode][neighborNode]["weight"] += edge_weight
                        else:
                            # If there is no edge present, then a new one
                            # with the newly found edge weight is created
                            aggGraph.add_edge(communityNode, neighborNode, weight=edge_weight)

                        completedEdge.add(checkEdge)

        return newCommunities, aggGraph

    def modularity(self, graph: nx.Graph, communities: list) -> float:
        # Calculates modularity of the graph

        return nx.community.modularity(graph, communities, weight='weight')
    
    def delta(self, node_i, node_j, communities: list) -> int:
        # Delta value in modularity calculation,
        # returns 1 if two nodes are in same community
        # or 0 if they are not
        if self.findCommunity(node_i, communities) == self.findCommunity(node_j, communities):
            return 1
        else:
            return 0

    def nodeWeight(self, node, graph: nx.Graph) -> float:
        # Calculates weight of a node through sum of edge weights
        weight = 0
        for neighbor in graph.neighbors(node):
            weight += graph[node][neighbor]["weight"]

        return weight

    def setRandQueue(self, inputCommunities) -> deque:
        # Sets the random queue for local node movement order
        randQueue = deque()
        seen = set()

        while len(randQueue) != len(inputCommunities):
            valIndex = random.choice(inputCommunities)
            val = valIndex[0]                                               # No mod val in lists, just use first val now
            if val not in seen:
                # Makes sure nodes aren't added 2+ times to queue
                randQueue.append(val)
                seen.add(val)

        return randQueue

    def removeNodefromCommunities(self, node, communities: list) -> list:
        for checkCommunity in communities:
            # Removes node from past community
            if node in checkCommunity:
                checkCommunity.remove(node)

                # # If past community is now empty, delete community
                # if not checkCommunity:
                #     communities.remove(checkCommunity)
        return communities

    def removeEmptyCommunities(self, communities: list) -> list:
        for community in communities:
            # If past community is now empty, delete community
                if not community:
                    communities.remove(community)
        return communities

    def addNodeToCommunity(self, node, inputCommunity: list, communities: list) -> list:
        # Adds node to a community

        for checkCommunity in communities:
            # Adds node to new community
            if checkCommunity == inputCommunity:
                checkCommunity.append(node)
                checkCommunity.sort()

        return communities

    def getChangedNeighbors(self, node, community: list, curr_Queue, graph: nx.Graph, communities) -> list:
        # Gets neighbors not in new community of node to add to back of queue
        neighborsToChange = []
        nodeNeighbors = nx.neighbors(graph, node)

        for neighbor in nodeNeighbors:
            # Makes sure neighbors aren't in subcommunity or queue,
            # but are a node in the current config of outer communities
            if neighbor not in community and neighbor not in curr_Queue:
                neighborsToChange.append(neighbor)

        return neighborsToChange
    
    def findCommunity(self, node, communities: list) -> int:
        # Gets the index of a community of a specific node
        for community_index in range(0, len(communities)):
            if node in communities[community_index]:
                return community_index
        return None

    def createNode(self, community: list) -> tuple:
        if any(type(i) == tuple for i in community):
            nodeList = [i for tup in community for i in tup]
            newNode = tuple(nodeList)
        else:
            # Create new node and add to graph, append to new community
            newNode = tuple(community)
        return newNode

    def unravelCommunities(self, communities: list) -> list:
        # Unravels communities of tuples (list of list of tuples)
        # into just a list of list of values

        unraveledCommunities = []
        for community in communities:
            if any(type(i) == tuple for i in community):
                nodeList = [i for tup in community for i in tup]
            else:
                nodeList = [i for i in community]
            unraveledCommunities.append(nodeList)
        
        return unraveledCommunities

    def runLeiden(self):
        # Runs leiden in correct implementation order

        # Sets to inputted graph, finds initial communities
        newGraph = self.graph
        newCommunities = self.setInitialCommunities(newGraph)

        # Sets initial agglomerated graph, used
        # if fast local movement step yields
        # ideal communities for final step,
        # and agglomeratedGraph hasn't been set yet
        agglomeratedGraph = None

        completed = False
        numIterations = 10
        while numIterations > 0:
            numIterations -= 1
            if numIterations == 0:
                print("Ran out of iterations\n")

            # Run fast local movement step,
            # return new community partitions and graph
            localmovementCommunities, localmovementGraph = self.moveNodesFast(newGraph, newCommunities)
            print(f"local movement communities: {localmovementCommunities}")
            print(f"local movement graph: {localmovementGraph}")

            # If all communities only have a single node,
            # then they can't be refined further and the graph
            # is set in its ideal community separation config
            for community in localmovementCommunities:
                if len(community) > 1:
                    completed = False
                    break
                completed = True

            if not completed:

                # Run refinement step,
                # return new community partitions and graph
                refinedCommunities, refinedGraph = self.refineCommunities(localmovementCommunities, localmovementGraph)
                print(f"refined communities: {refinedCommunities}")
                print(f"refined graph: {refinedGraph}")

                # Run agglomeration step,
                # return new community partitions and new graph
                agglomeratedCommunities, agglomeratedGraph = self.agglomerateCommunities(refinedCommunities, refinedGraph, localmovementCommunities)
                newGraph = agglomeratedGraph
                newCommunities = agglomeratedCommunities
                print(f"agglomerated communities: {agglomeratedCommunities}")
                print(f"Final graph {agglomeratedGraph}. Nodes: {agglomeratedGraph.nodes}. Edges:")
                edges_with_weights = agglomeratedGraph.edges(data=True)
                for u, v, data in edges_with_weights:
                    print(f"Edge: ({u}, {v}), Weight: {data['weight']}")
            
            else:
                # If leiden runthrough is completed
                print("completed\n")
                break


        if completed and agglomeratedGraph == None:
            # If initial community separation results
            # in the final community separation
            finalCommunities = self.unravelCommunities(localmovementCommunities)
            return localmovementGraph, finalCommunities
        else:
            finalCommunities = self.unravelCommunities(localmovementCommunities)
            return agglomeratedGraph, finalCommunities


def creategraph() -> nx.Graph:
    # Creates NetworkX graph to test
    G = nx.Graph()
    # G.add_edge(0, 1, weight=4)
    # G.add_edge(0, 2, weight=1)
    # G.add_edge(1, 2, weight=1)
    # G.add_edge(1, 3, weight=1)
    # G.add_edge(2, 3, weight=2)
    # G.add_edge(2, 4, weight=4)
    # G.add_edge(3, 4, weight=2)

    # # Set the random seed for reproducibility
    # random.seed(40)
    # G = nx.erdos_renyi_graph(40, 0.4, seed=40)
    # for u, v in G.edges():
    #     G[u][v]['weight'] = random.uniform(0.1, 1.0)

    # Create a networkx graph with 10 nodes
    G = nx.Graph()

    # Add nodes
    nodes = list(range(10))
    G.add_nodes_from(nodes)

    # Add edges within community 1 (nodes 0-3)
    G.add_edges_from([(0, 1), (1, 2), (2, 3), (0, 2)])

    # Add edges within community 2 (nodes 4-6)
    G.add_edges_from([(4, 5), (5, 6), (4, 6)])

    # Add edges within community 3 (nodes 7-9)
    G.add_edges_from([(7, 8), (8, 9), (7, 9)])

    # Add sparse edges between communities
    G.add_edges_from([(3, 4), (6, 7)])

    # Optionally, assign random weights to edges for more complexity
    for u, v in G.edges():
        G[u][v]['weight'] = 1.0  # Hard-coding weights for simplicity
    print("NX graph made")

    return G


def main():
    leidenGraph = Leiden(creategraph())

    graph, communities = leidenGraph.runLeiden()

    print(f"final communities: {communities}")
    print(f"Final graph {graph}. Nodes: {graph.nodes}. Edges:")
    edges_with_weights = graph.edges(data=True)
    for u, v, data in edges_with_weights:
        print(f"Edge: ({u}, {v}), Weight: {data['weight']}")

    # Create an igraph graph with 10 nodes
    H = ig.Graph()

    # Add 10 nodes
    H.add_vertices(10)

    # Add edges within community 1 (nodes 0-3)
    H.add_edges([(0, 1), (1, 2), (2, 3), (0, 2)])

    # Add edges within community 2 (nodes 4-6)
    H.add_edges([(4, 5), (5, 6), (4, 6)])

    # Add edges within community 3 (nodes 7-9)
    H.add_edges([(7, 8), (8, 9), (7, 9)])

    # Add sparse edges between communities
    H.add_edges([(3, 4), (6, 7)])

    # Optionally, assign random weights to edges
    H.es['weight'] = [1.0] * len(H.es)    

    # # Set the random seed for reproducibility
    # random.seed(40)
    # # Create an Erdős-Rényi graph with 40 nodes and probability of edge creation 0.4
    # H = ig.Graph.Erdos_Renyi(n=40, p=0.4, directed=False)
    # # Assign random weights to each edge
    # for edge in H.es:
    #     edge['weight'] = random.uniform(0.1, 1.0)
    print("igraph graph created")

    # # Create an empty graph
    # H = ig.Graph()

    # # Add vertices (nodes) for the graph (5 nodes in total)
    # H.add_vertices(5)

    # # Add edges along with weights
    # edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)]
    # weights = [4, 1, 1, 1, 2, 4, 2]

    # # Add edges with weights
    # H.add_edges(edges)
    # H.es['weight'] = weights

    testPartition = lg.find_partition(H, lg.ModularityVertexPartition)
    
    print(f"leiden library result: {testPartition}")


if __name__ == "__main__":
    main()
