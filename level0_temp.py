import json
from sys import maxsize
from itertools import permutations

from typing import List
import math

def nearest_neighbor(neighbourhood, output):
    unvisited = set(neighbourhood)
    current = neighbourhood[0]
    unvisited.remove(current)
    tour = [current]
    while unvisited:
        next_city = min(unvisited, key=lambda city: output[neighbourhood.index(current)][neighbourhood.index(city)])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    return tour


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
neighbourhood =["r0","n0","n1","n2","n3","n4","n5","n6","n7","n7","n8","n9","n10","n11","n12","n13","n14","n15","n16","n17","n18","n19"]
final_result = nearest_neighbor(neighbourhood,output)
print(final_result)
