import numpy as np
import json
def nearest_neighbour(c, tsp_g):
    n = len(tsp_g)
    visited = set()
    visited.add(c-1)
    path = [c-1]
    total_cost = 0

    for _ in range(n-1):
        min_val = float('inf')
        nearest_vertex = None
        for k in range(n):
            if tsp_g[c][k] != 0 and k not in visited:
                if tsp_g[c][k] < min_val:
                    min_val = tsp_g[c][k]
                    nearest_vertex = k
        if nearest_vertex is not None:
            total_cost += min_val
            visited.add(nearest_vertex)
            path.append(nearest_vertex)
            c = nearest_vertex

    total_cost += tsp_g[path[-1]][path[0]]
    return total_cost, path

def find_best_solution(tsp_g):
    n = len(tsp_g)
    best_cost = float('inf')
    best_path = None

    for start in range(n):
        cost, path = nearest_neighbour(start, tsp_g)
        if cost < best_cost:
            best_cost = cost
            best_path = path

    return best_cost, best_path
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


tsp_g = np.array(output)

best_cost, best_path = find_best_solution(tsp_g)
print("Best Path:", best_path)
print("Best Cost:", best_cost)

route =[]
route.append("r0")
for i in range (0,len(best_path)-1):
    if(best_path[i] > 0):
        s='n'+str(best_path[i]-1)
    elif(best_path[i]==0):
        continue
    route.append(s)
route.append("r0")
p={"v0":{"path":route}}
json_object = json.dumps(p, indent=4)
with open("level0_output1.json", "w") as outfile:
    outfile.write(json_object)