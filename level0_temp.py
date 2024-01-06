import json
import numpy as np
from typing import List
import math
res=[]
def nearest_neighbour(c):
    global cost
    adj_vertex = 999
    min_val = 10000
    visited[c] = 1
    print((c + 1), end=" ")
    res.append(c-1)
    for k in range(n):
        if (tsp_g[c][k] != 0) and (visited[k] == 0):
            if tsp_g[c][k] < min_val:
                min_val = tsp_g[c][k]
                adj_vertex = k
    if min_val != 999:
        cost = cost + min_val
    if adj_vertex == 999:
        adj_vertex = 0
        print((adj_vertex + 1), end=" ")
        cost = cost + tsp_g[c][adj_vertex]
        return
    nearest_neighbour(adj_vertex)


with open('Input data\level0.json','r') as f:
    data = json.load(f)

#print(data)
    
fromneigh_dist=[]
for i in range (0,20):
    i = str(i)
    tempn = data["neighbourhoods"]["n"+i]["distances"]
    fromneigh_dist.append(tempn)

#print("Distance of neighbouurs: ",fromneigh_dist)

fromrest_dist = []
tempr = data["restaurants"]["r0"]["neighbourhood_distance"]
fromrest_dist.extend(tempr)

temprest = [0]
temprest.extend(fromrest_dist)
#print(temprest)
#print("Distance of neighbourhood from rest: ",fromrest_dist)


fromneigh_dist.insert(0,fromrest_dist)
#print(fromneigh_dist)
matrix = fromneigh_dist
#print(matrix)

output = [[v, *subl] for v, subl in zip(temprest, matrix)]
#print(output)
neighbourhood =["r0","n0","n1","n2","n3","n4","n5","n6","n7","n8","n9","n10","n11","n12","n13","n14","n15","n16","n17","n18","n19"]

n = 21
cost = 0
visited = np.zeros(n, dtype=int)
tsp_g = np.array(output)
print("Shortest Path:", end=" ")
nearest_neighbour(0)
print()

route =[]
route.append("r0")
for i in range (1,len(res)):
    s='n'+str(res[i])
    route.append(s)
route.append("r0")
p={"v0":{"path":route}}
json_object = json.dumps(p, indent=4)
with open("level0_output.json", "w") as outfile:
    outfile.write(json_object)