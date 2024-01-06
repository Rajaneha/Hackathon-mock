import json
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
print(output)

