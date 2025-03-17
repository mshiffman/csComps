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


with open('LouvainData/louvain_communities_1_5.csv', 'r') as file:
    reader = csv.reader(file)
    lineNum = 0
    for community in reader:
        for tract in community:
            coordinates[tract][2] = lineNum
        lineNum += 1

def randomColors(n):
    return ["#{:06x}".format(random.randint(0, 0xFFFFFF)) for _ in range(n)]

colors = randomColors(lineNum+1)

colors = [
    "#95A5A6", "#F4A261", "#FDCB58", "#81C784", "#2A9D8F", "#008080", 
    "#56CCF2", "#457B9D", "#1D3557", "#8E44AD", "#E84393", "#FF6B81",
    "#A67C52","#E63946"
]

#communities for solo visualization:
#community 7: I-494 corridor
#community 10: SE MPLS to downtown
#community 14: Near North -- Powderhorn

map_all = folium.Map(location=[45, -93.3])
map7 = folium.Map(location=[45, -93.3])
map10 = folium.Map(location=[45, -93.3])
map14 = folium.Map(location=[45,-93.3])

folium.Map(location=[45, -93.3])
for coord in coordinates.values():
    lat = coord[0]
    long = coord[1]
    community = coord[2]
    folium.CircleMarker(location=[lat,long],
                        radius = 3,
                        color = colors[community],
                        fill = True,
                        fill_color = colors[community],
                        fill_opacity = 1
                        ).add_to(map_all)
    if community == 6:
        folium.CircleMarker(location=[lat,long],
                        radius = 5,
                        color = colors[community],
                        fill = True,
                        fill_color = colors[community],
                        fill_opacity = 1
                        ).add_to(map7)
    if community == 9:
        folium.CircleMarker(location=[lat,long],
                        radius = 5,
                        color = colors[community],
                        fill = True,
                        fill_color = colors[community],
                        fill_opacity = 1
                        ).add_to(map10)
    if community == 13:
        folium.CircleMarker(location=[lat,long],
                        radius = 5,
                        color = colors[community],
                        fill = True,
                        fill_color = colors[community],
                        fill_opacity = 1
                        ).add_to(map14)
    
map_all.save('map_all.html')
map7.save('map7.html')
map10.save('map10.html')
map14.save('map14.html')