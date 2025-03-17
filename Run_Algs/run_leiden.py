import pickle
import networkx
import csv
import datetime
from Algorithms import leiden
import louvain

# Test 1: 1.1 Res

filePath = 'graph.pkl'
with open(filePath, 'rb') as f:
    graph = pickle.load(f)

print("graph 2 loaded")

start_time = datetime.datetime.now()
l_1 = leiden.Leiden(graph,1.1)
communities = l_1.runLeiden()

with open('leiden_communities_1_1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in communities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time of Leiden for resolution 1.1 in seconds: {execution_time.total_seconds():.4f} seconds")

# Test 2: 1.2 Res

filePath = 'graph.pkl'
with open(filePath, 'rb') as f:
    graph = pickle.load(f)

print("graph 3 loaded")

start_time = datetime.datetime.now()
l_2 = leiden.Leiden(graph,1.2)
communities = l_2.runLeiden()

with open('leiden_communities_1_2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in communities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time of Leiden for resolution 1.2 in seconds: {execution_time.total_seconds():.4f} seconds")

# Test 3: 1.3 Res

filePath = 'graph.pkl'
with open(filePath, 'rb') as f:
    graph = pickle.load(f)

print("graph loaded")

start_time = datetime.datetime.now()
l_3 = leiden.Leiden(graph,1.3)
communities = l_3.runLeiden()

with open('leiden_communities_1_3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in communities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time of Leiden for resolution 1.3 in seconds: {execution_time.total_seconds():.4f} seconds")



# start_time = datetime.datetime.now()
# l_1 = louvain.Louvain(graph)
# l_1.run(1)

# with open('louvain_communities_1.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     for comm in l_1.nestedCommunities:
#         writer.writerow(comm)

# end_time = datetime.datetime.now()
# execution_time = end_time - start_time
# print(f"Execution time of Louvain for resolution 1 in seconds: {execution_time.total_seconds():.4f} seconds")


'''start_time = datetime.datetime.now()
l_2 = louvain.Louvain(graph)
l_2.run(1.1)

with open('communities_2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l_2.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l_3 = louvain.Louvain(graph)
l_3.run(1.2)

with open('communities_3.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l_3.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l_4 = louvain.Louvain(graph)
l_4.run(1.3)

with open('communities_4.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l_4.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")'''