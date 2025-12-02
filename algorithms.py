import heapq
import math

#dijkstra
def dijkstra(G, start, goal):

    distances = {node: math.inf for node in G.nodes()}
    distances[start] = 0

    previous = {node: None for node in G.nodes()}

    pq = [(0, start)]
    visited = set()
    nodes_expanded = 0

    while pq:
        current_dist, city = heapq.heappop(pq)

        if city in visited:
            continue

        visited.add(city)
        nodes_expanded += 1

        if city == goal:
            break

        for neighbor in G.neighbors(city):
            weight = G[city][neighbor]["weight"]
            new_dist = current_dist + weight

            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = city
                heapq.heappush(pq, (new_dist, neighbor))

    if distances[goal] == math.inf:
        return None, math.inf, nodes_expanded

    #reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = previous[node]

    path.reverse()
    return path, distances[goal], nodes_expanded

#second best path
def second_best_path(G, start, goal):

    #first run the shortest path
    p1, dist1, nodes1 = dijkstra(G, start, goal)

    if p1 is None:
        return None, math.inf, None, math.inf, nodes1, 0

    best_alt_path = None
    best_alt_cost = math.inf
    best_nodes2 = 0

    #remove each edge from shortest path and recompute
    for i in range(len(p1) - 1):
        u = p1[i]
        v = p1[i + 1]

        original_weight = G[u][v]["weight"]

        #temporarily remove edge
        G.remove_edge(u, v)

        p2, dist2, nodes2 = dijkstra(G, start, goal)

        #restore edge
        G.add_edge(u, v, weight=original_weight)

        #choose best alternative path
        if p2 is not None and p2 != p1 and dist2 < best_alt_cost:
            best_alt_path = p2
            best_alt_cost = dist2
            best_nodes2 = nodes2

    return p1, dist1, best_alt_path, best_alt_cost, nodes1, best_nodes2
