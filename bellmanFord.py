def bellmanFord(self, sourceNode):
    distance = {}
    paths = {}

    for node in self.graph.nodes:
        if node == sourceNode:
            distance[node]=0
            paths[sourceNode] = [[sourceNode]]
        else:
            distance[node]=float('inf')
            paths[node]=[]

    for i in range(len(self.graph.nodes)-1):

        for node1, node2, data in self.graph.edges(data=True):
            weight = data.get('weight')
            

            if distance[node1]+weight < distance[node2]:
                distance[node2]=distance[node1]+weight
                updatedPaths = []
                for eachPath in paths[node1]:
                    updatedPaths.append(eachPath+[node2])
                paths[node2]= updatedPaths


            elif distance[node1]+weight == distance[node2]:
                for eachPath in paths[node1]:
                    if eachPath+[node2] not in paths[node2]:
                        paths[node2].append(eachPath+[node2])


            if distance[node2] + weight < distance[node1]:
                distance[node1] = distance[node2] + weight
                updatedPaths = []
                for eachPath in paths[node1]:
                    updatedPaths.append(eachPath+[node1])
                paths[node1] = updatedPaths


            elif distance[node2] + weight == distance[node1]:
                for eachPath in paths[node2]:
                    if eachPath+[node1] not in paths[node1]:
                        paths[node1].append(eachPath+[node1])


    return paths