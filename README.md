# csComps

Algorithms contains the code for the Leiden, Louvain, Girvan-Newman, LPA, WLPA-LEB, and modified version of WLPA-LEB algorithms.


Data and Visualization contains the code used to create the graph from the dataset. The csv files used are too big to upload to github but can be found at the US Census' page for origin-destination data: "mn_od_main_JT00_2022.csv" and "mv_xwalk.csv". It also contains the program used to display the communities on a map using the package Folium.


Graphs contains the pickle files of the graphs used. They are in pickle format for ease of reuse.


Metrics contains the code used to test the modularity, conductance, and density of the community divisions.


Results contains the community divisions produced as well as the maps of those communities.


Run Algs contains the code to run the algorithms on the dataset, and saves the results into either csv or pickle format. 


