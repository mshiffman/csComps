from girvanNewman import GirvanNewman
# import networkx as nx
from testSuccess import *
import time

girvanStats1 = {"runtime":[], "results":[]}
girvanStats2 = {"runtime":[], "results":[]}
girvanStats3 = {"runtime":[], "results":[]}
girvanStats4 = {"runtime":[], "results":[]}

with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)

girvan1Graph = GirvanNewman(G)
girvan1Start = time.time()
girvan1Result = girvan1Graph.girvanNewmanAlgo(True, "modularity")
girvan1End = time.time()
girvan1Runtime = girvan1End - girvan1Start
girvanStats1["runtime"].append(girvan1Runtime)
girvanStats1["results"].append(girvan1Result)

with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)
girvan2Graph = GirvanNewman(G)
girvan2Start = time.time()
girvan2Result = girvan2Graph.girvanNewmanAlgo(True, "constantPotts")
girvan2End = time.time()
girvanRuntime = girvan2End - girvan2Start
girvanStats2["runtime"].append(girvanRuntime)
girvanStats2["results"].append(girvan2Result)


with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)
girvan2Graph = GirvanNewman(G)
girvan2Start = time.time()
girvan2Result = girvan2Graph.girvanNewmanAlgo(True, "constantPotts")
girvan2End = time.time()
girvanRuntime = girvan2End - girvan2Start
girvanStats2["runtime"].append(girvanRuntime)
girvanStats2["results"].append(girvan2Result)






with open('girvanStats2.pkl', 'wb') as f:
    pickle.dump(girvanStats, f)

print(girvanStats)

# girvanStats["modularity"].append(modularity(G, girvanStats["results"][0]))
# girvanStats["avgConductance"].append(graphAvgConductance(G,girvanStats["results"][0]))
# girvanStats["avgDensity"].append(graphAvgDensity(G,girvanStats["results"][0]))
# girvanStats["constantPotts"].append(constantPotts(G,girvanStats["results"][0], 1))