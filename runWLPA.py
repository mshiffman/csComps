from WLPA import LPA
import datetime
import pickle
import csv


print("\n")
with open("graphLPA.pkl", 'rb') as f:
    G = pickle.load(f)

graph = LPA(G)
start = datetime.datetime.now()
result = graph.WLPA_Mod(3, 5, 5)
# result = graph.LPA()
end = datetime.datetime.now()
runtime = end - start


# with open('WLPA5.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for commName in result:
#         writer.writerow(result[commName])
        
print(f"Execution time in seconds: {runtime.total_seconds():.4f} seconds")
print(len(result))
for i in result:
    print(result[i])
    print("\n\n")
    print("length:", len(result[i]))
    print("\n\n")

print(len(result))
print(runtime)