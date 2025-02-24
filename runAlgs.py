
import time
from leiden import Leiden
from louvain import Louvain
from girvanNewman import GirvanNewman
import networkx as nx
from testSuccess import *

leidenStats = {"runtime":[], "modularity":[], "avgConductance":[], "avgDensity":[], "constantPotts":[], "results":[]}
louvainStats = {"runtime":[], "modularity":[], "avgConductance":[], "avgDensity":[], "constantPotts":[], "results":[]}
girvanStats = {"runtime":[], "modularity":[], "avgConductance":[], "avgDensity":[], "constantPotts":[], "results":[]}
# leidenStats = {"runtime":[], "results":[]}
# louvainStats = {"runtime":[], "results":[]}
# girvanStats = {"runtime":[], "results":[]}

def run(num):
    for i in range(num):
        # with open("graph.pkl", 'rb') as f:
        #     G = pickle.load(f)
        # leidenGraph = Leiden(G)
        # leidenStart = time.time()
        # graph, leidenResult = leidenGraph.runLeiden()
        # leidenEnd = time.time()
        # leidenRuntime = leidenEnd - leidenStart
        # leidenStats["runtime"].append(leidenRuntime)
        # leidenStats["results"].append(leidenResult)
        
        # with open("graph.pkl", 'rb') as f:
        #     G = pickle.load(f)
        
        # resolution = 1
        # louvainGraph = Louvain(G)
        # louvainStart = time.time()
        # louvainResult = louvainGraph.run()
        # louvainEnd = time.time()
        # louvainRuntime = louvainEnd - louvainStart
        # louvainStats["runtime"].append(louvainRuntime)
        # louvainStats["results"].append(louvainResult)
        
        with open("graph1.pkl", 'rb') as f:
            G = pickle.load(f)

        girvanGraph = GirvanNewman(G)
        girvanStart = time.time()
        girvanResult = girvanGraph.girvanNewmanAlgo(True)
        girvanEnd = time.time()
        girvanRuntime = girvanEnd - girvanStart
        girvanStats["runtime"].append(girvanRuntime)
        girvanStats["results"].append(girvanResult)



def otherStats():
    for i in range(len(girvanStats["results"])):
        with open("graph1.pkl", 'rb') as f:
            G = pickle.load(f)
        # leidenStats["modularity"].append(modularity(G,leidenStats["results"][i]))
        # leidenStats["avgConductance"].append(graphAvgConductance(G,leidenStats["results"][i]))
        # leidenStats["avgDensity"].append(graphAvgDensity(G,leidenStats["results"][i]))
        # leidenStats["constantPotts"].append(constantPotts(G,leidenStats["results"][i], 1))
        
        
        girvanStats["modularity"].append(modularity(G, girvanStats["results"][i]))
        girvanStats["avgConductance"].append(graphAvgConductance(G,girvanStats["results"][i]))
        girvanStats["avgDensity"].append(graphAvgDensity(G,girvanStats["results"][i]))
        girvanStats["constantPotts"].append(constantPotts(G,girvanStats["results"][i], 1))

run(1)    
otherStats()
        
# print(leidenStats)
# print(louvainStats)
print(girvanStats)

# with open('leidenStats.pkl', 'wb') as f:
#     pickle.dump(leidenStats, f)

# with open('louvainStats.pkl', 'wb') as f:
#     pickle.dump(louvainStats, f)

# with open('girvanStats.pkl', 'wb') as f:
#     pickle.dump(girvanStats, f)

