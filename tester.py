import csv

lst = [[1,2,3,4,5,6,7,8,9],
       [1,2,3,4,5,6,7,8,9],
       [1,2,3,4,5,6,7,8,9]]

with open('louvain_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for item in lst:
        writer.writerow(item)
    
