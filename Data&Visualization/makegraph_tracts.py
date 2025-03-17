import pandas as pd
import networkx as nx
import louvain_fixed
import random
import csv
import pickle

import matplotlib.pyplot as plt

# setting up all the dictionaries we'll need
node_data_file = "mn_xwalk.csv"
edge_data_file = "mn_od_main_JT00_2022.csv"
nodeData = pd.read_csv(node_data_file)
edgeData = pd.read_csv(edge_data_file)
tractDictionary  = {}
weightsDictionary = {}
coordsDictionary = {}
graph1 = nx.Graph()
graph2 = nx.Graph()

# creating a dictionary tracking the tract and coordinates of each geocode
for i in range(1, len(nodeData)):
    if nodeData.iloc[i,5] == "Hennepin County, MN":
        geocode = nodeData.iloc[i,0]
        censusTract = nodeData.iloc[i,6]
        latitude = nodeData.iloc[i, 38] 
        longitude = nodeData.iloc[i,39]
        tractDictionary[geocode] = censusTract
        coordsDictionary[geocode] = (latitude, longitude)

# Finding the population centroids of each tract, through averaging out the values
# of all geocodes in the tract
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
    # storing the position of each node for eventual graphics
    centroidDictionary[tract] = (centroid_totals[tract][0]/centroid_totals[tract][2], 
                                 centroid_totals[tract][1]/centroid_totals[tract][2])
    graph1.add_node(tract, children = [], pos=(centroidDictionary[tract][0], centroidDictionary[tract][1]), color=None)
    graph2.add_node(tract, children = [], pos=(centroidDictionary[tract][0], centroidDictionary[tract][1]), color=None)

#using the geocode and tract data combined to weight edges
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
edgeCount = 0
for key in weightsDictionary:
    source = key[0]
    dest = key[1]
    graph1.add_edge(source, dest, weight=weightsDictionary[key])
    graph2.add_edge(source, dest, weight=1/weightsDictionary[key])
    edgeCount += 1

# #saving the graph to pkl
with open('graph.pkl', 'wb') as f:
    pickle.dump(graph1, f)
with open('graphGN.pkl', 'wb') as f:
    pickle.dump(graph2, f)

#storing the centroids so we can work with them
with open('coordinate_data.csv', 'w', newline = '') as file:
    writer = csv.writer(file)
    writer.writerow(["Tract", "Latitude", "Longitude"])
    for tract in centroidDictionary.keys():
        row = [tract, centroidDictionary[tract][0], centroidDictionary[tract][1]]
        writer.writerow(row)