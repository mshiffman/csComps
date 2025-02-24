import pickle
import networkx
import csv
import datetime
import louvain

filePath = 'graph.pkl'
with open(filePath, 'rb') as f:
    graph = pickle.load(f)

print("graph loaded")

start_time = datetime.datetime.now()
l_1 = louvain.Louvain(graph)
l_1.run(1)

with open('communities_1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l_1.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")


start_time = datetime.datetime.now()
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
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")