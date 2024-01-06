import json
with open('Input data\level0.json','r') as f:
    data = json.load(f)

#print(data)
    
neigh_dist=[]
for i in range (0,19):
    i = str(i)
    temp = data["neighbourhoods"]["n"+i]["distances"]
    neigh_dist.append(temp)

print(neigh_dist)


