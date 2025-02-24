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
l = louvain.Louvain(graph,resolution=1.4)
l.run()

with open('louvain_communities_1_4.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l = louvain.Louvain(graph,resolution=1.5)
l.run()

with open('louvain_communities_1_5.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l = louvain.Louvain(graph,resolution=1.6)
l.run()

with open('louvain_communities_1_6.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l = louvain.Louvain(graph,resolution=1.7)
l.run()

with open('louvain_communities_1_7.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l = louvain.Louvain(graph,resolution=1.8)
l.run()

with open('louvain_communities_1_8.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l = louvain.Louvain(graph,resolution=1.9)
l.run()

with open('louvain_communities_1_9.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")

start_time = datetime.datetime.now()
l = louvain.Louvain(graph,resolution=2)
l.run()

with open('louvain_communities_2.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for comm in l.nestedCommunities:
        writer.writerow(comm)

end_time = datetime.datetime.now()
execution_time = end_time - start_time
print(f"Execution time in seconds: {execution_time.total_seconds():.4f} seconds")


