import json

from typing import List
import math

def nearest_neighbour(mat):
    global route
    for i in range(len(mat)):
        if(mat[i]!=0 and ('n'+str(i)) not in route):
            m=mat[i]
            break
    for i in mat:
        if (i!=0 and i<m and ('n'+str(mat.index(i))) not in route):
            m=i
    return mat.index(m)


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

route =[]
while(len(route)!=21):
    i=nearest_neighbour(output)
    route.append("n"+str(i))

route.append("r0")
p={"v0":{"Route traversed by steve":route}}
json_object = json.dumps(p, indent=4)
with open("level0_op.json", "w") as outfile:
    outfile.write(json_object)