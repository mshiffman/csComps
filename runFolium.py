import folium
import csv
import random

coordinates = {}
with open('coordinate_data.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for line in reader:
        tract, lat, long = line[0], line[1], line[2]
        coordinates[tract] = [lat, long, None]

with open('LouvainData/louvain_communities_1_9.csv', 'r') as file:
    reader = csv.reader(file)
    lineNum = 0
    for community in reader:
        for tract in community:
            coordinates[tract][2] = lineNum
        lineNum += 1

def randomColors(n):
    return ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(n)]

colors = randomColors(lineNum+1)
print(colors)

map = folium.Map(location=[45, -93.3])
for coord in coordinates.values():
    lat = coord[0]
    long = coord[1]
    community = coord[2]
    folium.CircleMarker(location=[lat,long],
                        radius = 5,
                        color = colors[community],
                        fill = True
                        ).add_to(map)
map.save('map.html')