import pandas as pd
import networkx as nx
import louvain_fixed
import random
import csv
import pickle

#must be in this order i think
# import matplotlib
# matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import datetime

start_time = datetime.datetime.now()

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
    #if nodeData.iloc[i,15] == "Brooklyn Center city, MN":
        geocode = nodeData.iloc[i,0]
        censusTract = nodeData.iloc[i,6]
        latitude = nodeData.iloc[i, 38] 
        longitude = nodeData.iloc[i,39]
        tractDictionary[geocode] = censusTract
        coordsDictionary[geocode] = (latitude, longitude)

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
    graph1.add_node(tract, children = [], pos=(centroidDictionary[tract][0], centroidDictionary[tract][1]), color=None)

for i in range(1, len(edgeData)):
    start_geocode = edgeData.iloc[i,0]
    dest_geocode = edgeData.iloc[i,1]
    if start_geocode in tractDictionary and dest_geocode in tractDictionary:
        start_tract = tractDictionary[start_geocode]
        dest_tract = tractDictionary[dest_geocode]
        if start_tract != dest_tract:
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

with open('graph.pkl', 'wb') as f:
    pickle.dump(graph1, f)

#run the louvain algorithm on the tract graph
l = louvain_fixed.Louvain(graph1)
l.run()

#creating a csv storing communities
with open('louvain_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

with open('coordinate_data.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow(["Tract", "Latitude", "Longitude"])
    for tract in centroidDictionary.keys():
        row = [tract, centroidDictionary[tract][0], centroidDictionary[tract][1]]
        writer.writerow(row)

''' this is a bunch of business we don't need right now
def randomColors(n):
    return [(random.random(), random.random(), random.random()) for _ in range(n)]

#assigning the colors
colors = randomColors(len(l.nestedCommunities))
count = 0
for comm in l.nestedCommunities:
    currentColor = colors[count]
    count += 1
    for node in comm:
        nx.set_node_attributes(l.G, {node: {"color": currentColor}})

node_colors = [l.G.nodes[n]["color"] for n in l.G.nodes]
    
plt.figure(figsize=(6, 6))
nx.draw(graph1, node_color=node_colors)
#plt.show()
plt.savefig("/home/gordong/Desktop/louvain_1.3.svg")
'''
end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")