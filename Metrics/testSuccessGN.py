from Metrics.testSuccess import *


with open("graph.pkl", 'rb') as f:
    G = pickle.load(f)
    
with open("GirvanAlgoResults/girvanStatsDepth2BestModMax329.pkl", 'rb') as f:
    communities4 = pickle.load(f)
    

print("Number of communities", len(communities4))
gn_mod1 = modularity(G, communities4)
gn_den1 = graphAvgDensity(G, communities4)
gn_con1 = graphAvgConductanceWeight(G, communities4)

# gn_mod2 = modularity(G1, communities5)
# gn_den2 = graphAvgDensity(G1, communities5)
# gn_con2 = graphAvgConductanceWeight(G1, communities5)
    
print("modularity", gn_mod1)
print("conductance", gn_con1)
print("density", gn_den1)