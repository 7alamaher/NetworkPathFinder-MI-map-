import heapq
from collections import deque
import math


#Dijkstra
def dijkstra(G, start, goal):
    pq = [(0, start, [start])]
    visited = set()
    nodes_expanded = 0

    while pq:
        dist, city, path = heapq.heappop(pq)

        if city in visited:
            continue
        visited.add(city)
        nodes_expanded += 1

        if city == goal:
            return path, dist, nodes_expanded

        for neighbor in G.neighbors(city):
            weight = G[city][neighbor]['weight']
            heapq.heappush(pq, (dist + weight, neighbor, path + [neighbor]))

    return None, math.inf, nodes_expanded

def second_best_path(G, start, goal):
    # finding the first shortest path
    p1, dist1, _ = dijkstra(G, start, goal)

    if p1 is None:
        return None, float("inf"), None, float("inf")

    best_paths = [(p1, dist1)]

    #now removing each edge and rerunning Dijkstra
    second_path = None
    second_dist = float("inf")

    for i in range(len(p1) - 1):
        u = p1[i]
        v = p1[i + 1]

        weight_backup = G[u][v]["weight"]

        #temporarily removes the edge
        G.remove_edge(u, v)

        p2, dist2, _ = dijkstra(G, start, goal)

        #restores the edge
        G.add_edge(u, v, weight=weight_backup)

        if p2 is not None and p2 != p1 and dist2 < second_dist:
            second_path = p2
            second_dist = dist2

    return p1, dist1, second_path, second_dist
