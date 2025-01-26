import pandas as pd
import math
import networkx as nx
import pickle


#update file names & add to folder
edgeWeightFile = ""
mainFile = ""

weightData = pd.read_csv(edgeWeightFile)
nodeData = pd.read_csv(mainFile)

locations = {}

graph1 = nx.MultiGraph()
graph2 = nx.Graph()

for i in range(len(weightData)):
    geoCode = weightData[i][0]
    lattitude = weightData[i][37] #may have counted wrong
    longitude = weightData[i][38]
    if geoCode not in locations:
        locations[geoCode] = [lattitude, longitude]


for i in range(len(nodeData)):
    sourceNode = nodeData[i][0]
    destNode = nodeData[i][1]
    asq = (abs(locations[sourceNode][0]- locations[destNode][0]))**2
    bsq = (abs(locations[sourceNode][1]- locations[destNode][1]))**2
    c = math.sqrt(asq+bsq) #edge weight found using pythagorean theorem to calculate distance
    graph1.add_edge(sourceNode, destNode, c)


tripCount = {}


#edge weight based on number of trips
for i in range(len(nodeData)):
    sourceNode = int(nodeData[i][0])
    destNode = int(nodeData[i][1])

    if sourceNode<destNode:
        key = [sourceNode, destNode]
    else:
        key = [sourceNode, destNode]
    
    if key not in tripCount:
        tripCount[key]= 0
    else:
        tripCount[key]+=1
    

for i in range(len(tripCount)):
    source, dest = i
    graph2.add_edge(source,dest, tripCount[i])


#save graphs as files
with open('graph1.pkl', 'wb') as f:
    pickle.dump(graph1, f)

with open('graph2.pkl', 'wb') as f:
    pickle.dump(graph2, f)
    
#to open pickle file:
#with open('graph1.pkl', 'rb') as f:
#    graph1 = pickle.load(f)
