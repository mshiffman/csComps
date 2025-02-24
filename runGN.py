from girvanNewman import GirvanNewman
# import networkx as nx
from testSuccess import *
import time

girvanStats = {"runtime":[], "modularity":[], "avgConductance":[], "avgDensity":[], "constantPotts":[], "results":[]}
with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)

girvanGraph = GirvanNewman(G)
girvanStart = time.time()
girvanResult = girvanGraph.girvanNewmanAlgo(True)
girvanEnd = time.time()
girvanRuntime = girvanEnd - girvanStart
girvanStats["runtime"].append(girvanRuntime)
girvanStats["results"].append(girvanResult)

with open("graphGN.pkl", 'rb') as f:
    G = pickle.load(f)
    
girvanStats["modularity"].append(modularity(G, girvanStats["results"][0]))
girvanStats["avgConductance"].append(graphAvgConductance(G,girvanStats["results"][0]))
girvanStats["avgDensity"].append(graphAvgDensity(G,girvanStats["results"][0]))
girvanStats["constantPotts"].append(constantPotts(G,girvanStats["results"][0], 1))

with open('girvanStats.pkl', 'wb') as f:
    pickle.dump(girvanStats, f)
