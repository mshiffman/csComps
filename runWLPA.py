from WLPA import LPA
import time
import pickle

stats = {"runtime":[],"communities":[] }



print("\n")
with open("graphLPA.pkl", 'rb') as f:
    G = pickle.load(f)
    

# for i in dict(G.degree()).values():
#     print(i)

graph = LPA(G)
start = time.time()
result = graph.WLPA(1, 1000)
end = time.time()
runtime = end - start
stats["runtime"].append(runtime)
stats["communities"].append(result)


for i in result:
    print(result[i])
    print("\n\n")

print(len(result))
print(runtime)
