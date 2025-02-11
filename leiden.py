# Leiden algorithm implementation, Carleton College Computer Science 2025 Comps

import networkx as nx
import random
from collections import deque
import matplotlib.pyplot as plt


class Leiden:

    def __init__(self, graph: nx.Graph):

        self.graph = graph

    def setInitialorRefinedCommunities(self, inputCommunity: list = None, graph: nx.Graph = None) -> list:
        # Sets communities with a graph during the initial step
        # or a list of communities during refinement step
        # This method should be broken out into two separate methods

        outputCommunities = []
        if inputCommunity:
            # Used to set communities during refinement step
            for node in inputCommunity:
                newCommunity = [node]
                outputCommunities.append(newCommunity)
            return outputCommunities
        else:
            # Used to set communities during fast local node movement step
            allNodes = list(graph.nodes)
            for node in allNodes:
                newCommunity = [node]
                outputCommunities.append(newCommunity)
        return outputCommunities

    def moveNodesFast(self, graph: nx.Graph, communityToRefine: list = None, inputCommunities: list = None) -> list | nx.Graph:
        # Fast local node movement step of Leiden algorithm

        if inputCommunities:
            # Communities are inputted in fast local move
            communities = inputCommunities
        elif communityToRefine:
            # Get communities if in refinement step
            communities = self.setInitialorRefinedCommunities(communityToRefine, graph)

        if len(communities) == 1:
            # If only one community inputted, then that should be final set of communities
            return communities, graph

        # Get random order of node movement
        nodeOrderQueue = self.setRandQueue(communities)

        while nodeOrderQueue:

            idealCommunity = []

            # Gets first node to move
            curr_node = nodeOrderQueue.popleft()

            # Sets test communities for node movement
            testCommunities = communities

            # Gets current graph modularity
            currTopMod = self.modularity(graph, communities)

            # Examines every possible community
            for community in communities:

                # Sets test community for node movement
                testCommunity = community

                # Skip if community has current node in it
                if curr_node in community:
                    continue
                else:
                    # Adds node to test communities
                    checkCommunities = self.addNodeToCommunity(curr_node, testCommunity, testCommunities)

                    # Examines modularity of test communities
                    modVal = self.modularity(graph, checkCommunities)

                    # If modularity is increased, track mod and community
                    if modVal > currTopMod:
                        currTopMod = modVal
                        idealCommunity = community

            if not idealCommunity:
                # If modularity isn't increased in any community,
                # leave node where it was
                continue
            else:
                # If modularity is increased, add node to new community
                communities = self.addNodeToCommunity(curr_node, idealCommunity, communities)

                # If any neighbors of node aren't in same community
                # or already in the queue, then add to back of queue
                changeNeighbors = self.getChangedNeighbors(curr_node, idealCommunity,
                                                           nodeOrderQueue, graph,
                                                           communities)
                nodeOrderQueue.extend(changeNeighbors)

        return communities, graph

    def refineCommunities(self, communities, graph: nx.Graph) -> list | nx.Graph:
        # Community Refinement step of Leiden algorithm
        refinedCommunities = []
        for community in communities:
            newRefCommunity, g = self.moveNodesFast(graph, community)
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
                findRefComm = self.getCommunity(node, refinedCommunities)

                # Create new node and add to graph, append to new community
                newNode = tuple(findRefComm)
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
                    neighborCommunity = self.getCommunity(neighbor, refinedCommunities)

                    if community != neighborCommunity:
                        # If the community of provided node and its neighbor
                        # are not the same community, an edge must span
                        # between communities, and thus and edge must span
                        # between agglomerated nodes
                        communityNode = tuple(community)
                        neighborNode = tuple(neighborCommunity)

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

        # M value in mod calculation,
        # total weight of all edges in graph
        m_Val = graph.size(weight="weight")

        sum = 0
        for i in graph.nodes:
            for j in graph.nodes:

                # Calculates summation step of mod calculation,
                # iterating through all edges

                # A value in mod calculation
                if graph.has_edge(i, j):
                    a_Val = graph.get_edge_data(i, j)["weight"]
                else:
                    a_Val = 0.0
                
                # ki and kj value in mod calculation
                ki_Val = self.nodeWeight(i, graph)
                kj_Val = self.nodeWeight(j, graph)
                
                # Actual modularity calculation
                sum += (a_Val - ((ki_Val * kj_Val) / (2.0 * m_Val))) * self.delta(i, j, communities)
        
        return sum / (2 * m_Val)
    
    def delta(self, node_i, node_j, communities: list) -> int:
        # Delta value in modularity calculation,
        # returns 1 if two nodes are in same community
        # or 0 if they are not
        if self.getCommunity(node_i, communities) == self.getCommunity(node_j, communities):
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

    def addNodeToCommunity(self, node, inputCommunity: list, communities: list) -> list:   # This is being revamped
        # Adds node to a community after evaluating modularity
        for checkCommunity in communities:
            # Removes node from past community
            if node in checkCommunity:
                checkCommunity.remove(node)

                # If past community is now empty, delete community
                if not checkCommunity:
                    communities.remove(checkCommunity)

        for checkCommunity in communities:
            # Adds node to new community
            if checkCommunity == inputCommunity:
                checkCommunity.append(node)

        return communities

    def getChangedNeighbors(self, node, community: list, curr_Queue, graph: nx.Graph, communities) -> list:
        # Gets neighbors not in new community of node to add to back of queue
        neighborsToChange = []
        nodeNeighbors = graph.neighbors(node)
        allNodesinCommunities = [i for sublist in communities for i in communities]

        for neighbor in nodeNeighbors:
            # Makes sure neighbors aren't in subcommunity or queue,
            # but are a node in the current config of outer communities
            if neighbor not in community and neighbor not in curr_Queue and neighbor in allNodesinCommunities:
                neighborsToChange.append(neighbor)

        return neighborsToChange

    def getCommunity(self, node, communities: list) -> list:
        # Gets the community of a specific node
        for community in communities:
            if node in community:
                return community
        return None

    def runLeiden(self):
        # Runs leiden in correct implementation order

        # Sets to inputted graph, finds initial communities
        newGraph = self.graph
        newCommunities = self.setInitialorRefinedCommunities(newGraph)

        # Sets initial agglomerated graph, used
        # if fast local movement step yields
        # ideal communities for final step,
        # and agglomeratedGraph hasn't been set yet
        agglomeratedGraph = None

        completed = False
        while not completed:
            # Run fast local movement step,
            # return new community partitions and graph
            localmovementCommunities, localmovementGraph = self.moveNodesFast(newGraph, None, newCommunities)

            # If all communities only have a single node,
            # then they can't be refined further and the graph
            # is set in its ideal community separation config
            for community in localmovementCommunities:
                if len(community) > 1:
                    completed = False
                    break
                completed = True

            if completed == False:

                # Run refinement step,
                # return new community partitions and graph
                refinedCommunities, refinedGraph = self.refineCommunities(localmovementCommunities, localmovementGraph)

                # Run agglomeration step,
                # return new community partitions and new graph
                agglomeratedCommunities, agglomeratedGraph = self.agglomerateCommunities(refinedCommunities, refinedGraph, localmovementCommunities)
                newGraph = agglomeratedGraph
                newCommunities = agglomeratedCommunities

        if completed and agglomeratedGraph == None:
                # If initial community separation results
                # in the final community separation
                return localmovementGraph, localmovementCommunities
        else:
            return agglomeratedGraph, localmovementCommunities


def creategraph() -> nx.Graph:
    # Creates NetworkX graph to test
    G = nx.Graph()
    G.add_edge(0, 1, weight=4)
    G.add_edge(0, 2, weight=1)
    G.add_edge(1, 2, weight=1)
    G.add_edge(1, 3, weight=1)
    G.add_edge(2, 3, weight=2)
    G.add_edge(2, 4, weight=4)
    G.add_edge(3, 4, weight=2)

    # G.add_edge(0, 1, weight=0.6)
    # G.add_edge(0, 2, weight=0.2)
    # G.add_edge(2, 3, weight=0.1)
    # G.add_edge(2, 4, weight=0.7)
    # G.add_edge(2, 5, weight=0.9)
    # G.add_edge(0, 3, weight=0.3)

    return G


def main():
    leidenGraph = Leiden(creategraph())

    graph, communities = leidenGraph.runLeiden()

    print(f"final communities: {communities}")
    print(f"Final graph {graph}. Nodes: {graph.nodes}. Edges:")
    edges_with_weights = graph.edges(data=True)
    for u, v, data in edges_with_weights:
        print(f"Edge: ({u}, {v}), Weight: {data['weight']}")


if __name__ == "__main__":
    main()
