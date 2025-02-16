import pandas as pd
import math
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')

#git token: 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

#constructing a dictionary that leads each geocode to its census tract
node_data_file = "mn_xwalk.csv"
edge_data_file = "mn_od_main_JT00_2022.csv"
nodeData = pd.read_csv(node_data_file)
edgeData = pd.read_csv(edge_data_file)
tractDictionary  = {}
weightsDictionary = {}
coordsDictionary = {}
graph1 = nx.Graph()

for i in range(1, len(nodeData)):
    if nodeData.iloc[i,5] == "Hennepin County, MN":
        geocode = nodeData.iloc[i,0]
        censusTract = nodeData.iloc[i,6]
        latitude = nodeData.iloc[i, 38] 
        longitude = nodeData.iloc[i,39]
        tractDictionary[geocode] = censusTract
        coordsDictionary[geocode] = (latitude, longitude)
print("done adding nodes")

centroid_totals = {}
for key in coordsDictionary:
    tract = tractDictionary[key]
    if tract in centroid_totals:
        centroid_totals[tract] = (centroid_totals[tract][0] + coordsDictionary[key][0], 
                                            centroid_totals[tract][1] + coordsDictionary[key][1], 
                                            centroid_totals[tract][2] + 1)
    else:
        centroid_totals[tract] = (coordsDictionary[key][0], coordsDictionary[key][1], 1)

centroidDictionary = {}
for tract in centroid_totals:
    centroidDictionary[tract] = (centroid_totals[tract][0]/centroid_totals[tract][2], 
                                 centroid_totals[tract][1]/centroid_totals[tract][2])
    graph1.add_node(tract, children = [], pos=(centroidDictionary[tract][0], centroidDictionary[tract][1]))


print(len(edgeData))
for i in range(1, len(edgeData)):
    start_geocode = edgeData.iloc[i,0]
    dest_geocode = edgeData.iloc[i,1]
    if start_geocode in tractDictionary and dest_geocode in tractDictionary:
        start_tract = tractDictionary[start_geocode]
        dest_tract = tractDictionary[dest_geocode]

        key = (start_tract, dest_tract)
        if key not in weightsDictionary:
            weightsDictionary[key] = 1
        else:
            weightsDictionary[key] += 1

print("created weight dictionary")

edgeCount = 0
for key in weightsDictionary:
    source = key[0]
    dest = key[1]
    graph1.add_edge(source, dest, weight=weightsDictionary[key])
    edgeCount += 1
print("added", edgeCount, "edges")

plt.figure(figsize=(6, 6))
nx.draw(graph1)
plt.show()