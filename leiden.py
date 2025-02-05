import networkx as nx
import random
from collections import deque
import matplotlib.pyplot as plt


class Leiden:

    def __init__(self, graph: nx.Graph):

        self.graph = graph
        # self.communities = []
        # self.allNodes = list(graph.nodes)

    def setCommunities(self, inputCommunity: list=None, graph: nx.Graph=None) -> list:
        # Sets all nodes as their own communities during fast local movement
        # Can either be set with a graph during the initial step
        # or a list of communities during refinement step
        outputCommunities = []
        if inputCommunity:
            # Used to set communities during refinement step (as of now)
            for node in inputCommunity:
                newCommunity = [0.0, node]
                outputCommunities.append(newCommunity)
            return outputCommunities
        else:
            # Used to set communities during fast local node movement step
            allNodes = list(graph.nodes)
            for node in allNodes:
                newCommunity = [0.0, node]
                outputCommunities.append(newCommunity)
        return outputCommunities

    def moveNodesFast(self, graph: nx.Graph, inputCommunity: list=None) -> list | nx.Graph:
        # Fast local node movement step of Leiden algorithm

        # Get communities
        communities = self.setCommunities(inputCommunity, graph)

        # Get random order of node movement
        nodeOrderQueue = self.setRandQueue(communities)

        while nodeOrderQueue:

            idealCommunity = []

            # Gets first node to move
            curr_node = nodeOrderQueue.popleft()

            # Sets top modularity to 0 to be compared
            currTopMod = 0

            # Gets modularity of current community
            curr_ModCommunity = self.getMod(curr_node, None, communities)

            # Examines every possible community
            for community in communities:
                eval_ModCommunity = self.getMod(0, community, communities)

                # Skip if community has current node in it
                # Don't want to slice community list as it's used later
                checkCommunity = community
                if curr_node in checkCommunity[1:]:
                    continue
                else:
                    # Get modularity of first node in examined community
                    modVal = self.modularity(curr_node, community, graph)

                    # If modularity is increased, track mod and community
                    if modVal > (curr_ModCommunity + eval_ModCommunity):
                        if modVal > currTopMod:
                            currTopMod = modVal
                            idealCommunity = community

            if not idealCommunity:
                # If modularity isn't increased in any community,
                # leave node where it was
                continue
            else:
                # If modularity is increased, add node to new community
                communities = self.addNodeToCommunity(curr_node, currTopMod, idealCommunity, communities)

                # If any neighbors of node aren't in same community
                # or already in the queue, then add to back of queue
                changeNeighbors = self.getChangedNeighbors(curr_node,
                                                           idealCommunity,
                                                           nodeOrderQueue,
                                                           graph,
                                                           communities)
                nodeOrderQueue.extend(changeNeighbors)
        
        return communities, graph

    def refineCommunities(self, communities, graph: nx.Graph) -> list | nx.Graph:
        # Community Refinement step of Leiden algorithm
        refinedCommunities = []
        for community in communities:
            newRefCommunity, g = self.moveNodesFast(graph, community[1:])
            for subcommunity in newRefCommunity:
                refinedCommunities.append(subcommunity)
        
        return refinedCommunities, graph

    def modularity(self, node, community: list, graph: nx.Graph) -> float:
        # Calculates modularity of node and community

        community.append(node)

        # Gets total weight of graph, m value in modularity calc
        allEdgeWeight = self.graph.size(weight="weight")

        # Returns weight of nodes in compared community as a dictionary,
        # k_i & k_j in modularity calc
        nodeIndividualWeights = {}
        for i in community[1:]:
            nodeIndividualWeights[i] = self.nodeWeight(i, graph)

        modList = []
        k = 1
        for i in range(k, (len(community)-1)):
            m = k + 1
            for j in range(m, (len(community))):
                # Make sure not evaluating the same nodes against each other
                if community[i] == community[j]:
                    continue

                # Returns weight between two nodes, A_ij in modularity calc
                twoNodesEdgeWeight = self.graph.get_edge_data(community[i],
                                                              community[j],
                                                              default=0)
                if type(twoNodesEdgeWeight) is int and twoNodesEdgeWeight == 0:
                    twoNodesEdgeWeight = float(twoNodesEdgeWeight)
                else:
                    twoNodesEdgeWeight = twoNodesEdgeWeight['weight']

                # Calculates modularity
                modularity = ((1.0 / (2.0 * (allEdgeWeight))) * (twoNodesEdgeWeight - (
                             ((nodeIndividualWeights[community[i]]) *
                              (nodeIndividualWeights[community[j]])) / (2.0 * (allEdgeWeight)))))
                modList.append(modularity)
                m += 1
            k += 1
        # Removes node from community after it was added for evaluation
        # Will get added back into a community after comparing modularities
        community.pop()

        if len(modList) == 1:
            # If only calculating modularity for 2 nodes
            return modList[0]
        else:
            # If calculating modularity for 2+ nodes
            totalModularity = 0
            for i in modList:
                totalModularity += i
            return totalModularity

    def nodeWeight(self, node, graph: nx.Graph) -> float:
        # Calculates weight of a node through sum of edge weights
        weight = 0
        nodeNeighbors = graph.neighbors(node)
        for neighbor in nodeNeighbors:
            weight += self.graph[node][neighbor]["weight"]

        return weight

    def getMod(self, node, community=None, communities=None) -> float:
        # Gets mod value of a specific node or community from current config
        #
        # Returns modularity of a given nodes community
        if not community:
            for findCommunity in communities:
                if node in findCommunity:
                    return findCommunity[0]
        # Returns modularity of a community
        else:
            return community[0]

    def setRandQueue(self, inputCommunities) -> deque:
        # Sets the random queue for local node movement order
        randQueue = deque()
        seen = set()

        while len(randQueue) != len(inputCommunities):
            valIndex = random.choice(inputCommunities)
            val = valIndex[1]
            if val not in seen:
                # Makes sure nodes aren't added 2+ times to queue
                randQueue.append(val)
                seen.add(val)

        return randQueue

    def addNodeToCommunity(self, node, mod, inputCommunity: list, communities: list) -> list:
        # Adds node to a community after evaluating modularity
        for checkCommunity in communities:
            # Removes node from past community
            examineComm = checkCommunity[1:]
            if node in examineComm:
                checkCommunity.remove(node)

                # If past community is now empty, delete community
                if (len(checkCommunity) == 1):
                    communities.remove(checkCommunity)

        for checkCommunity in communities:
            # Adds node to new community, replace modularity
            if checkCommunity == inputCommunity:
                checkCommunity.append(node)
                checkCommunity[0] = mod

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

    def runLeiden(self):
        # Runs leiden in correct implementation order
        # firstCommunities = self.setFirstCommunities()
        localmovementCommunities, localmovementGraph = self.moveNodesFast(self.graph)
        print(f"local node movement communities: {localmovementCommunities}")
        refinedCommunities, refinedGraph = self.refineCommunities(localmovementCommunities, localmovementGraph)
        print(f"refined communities: {refinedCommunities}")


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

    G.add_edge(0, 1, weight=0.6)
    G.add_edge(0, 2, weight=0.2)
    G.add_edge(2, 3, weight=0.1)
    G.add_edge(2, 4, weight=0.7)
    G.add_edge(2, 5, weight=0.9)
    G.add_edge(0, 3, weight=0.3)

    return G


# def drawgraph(G: nx.Graph) -> None:
#     # Draws graph using NetworkX
#     #
#     # Positions for all nodes - seed for reproducibility
#     pos = nx.spring_layout(G, seed=7)

#     nx.draw(G, pos)

#     nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")

#     edge_labels = nx.get_edge_attributes(G, "weight")
#     nx.draw_networkx_edge_labels(G, pos, edge_labels)

#     ax = plt.gca()
#     ax.margins(0.08)
#     plt.axis("off")
#     plt.tight_layout()
#     plt.show()

def main():
    leidenGraph = Leiden(creategraph())

    leidenGraph.runLeiden()


if __name__ == "__main__":
    main()
