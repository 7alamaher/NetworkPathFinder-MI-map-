import heapq
import math


#dijkstra algorithm
def dijkstra(G, start, goal):
    #initialize distance table and previous-node table
    distances = {node: math.inf for node in G.nodes()}
    distances[start] = 0

    previous = {node: None for node in G.nodes()}

    #priority queue of (distance, node)
    pq = [(0, start)]
    visited = set()
    nodes_expanded = 0

    #main dijkstra loop
    while pq:
        current_dist, city = heapq.heappop(pq)

        if city in visited:
            continue
        visited.add(city)
        nodes_expanded += 1

        #shortest path found
        if city == goal:
            break

        #explore neighbors
        for neighbor in G.neighbors(city):
            weight = G[city][neighbor]["weight"]
            new_distance = current_dist + weight

            # Check if we found a better path
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous[neighbor] = city
                heapq.heappush(pq, (new_distance, neighbor))

    #reconstruct shortest path
    if distances[goal] == math.inf:
        return None, math.inf, nodes_expanded

    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = previous[node]

    path.reverse()
    return path, distances[goal], nodes_expanded


#second shortest path
def second_best_path(G, start, goal):

    #compute shortest path first
    p1, dist1, _ = dijkstra(G, start, goal)

    if p1 is None:
        #if there is no path at all
        return None, math.inf, None, math.inf

    best_second_path = None
    best_second_cost = math.inf

    #remove each edge from shortest path & recompute
    for i in range(len(p1) - 1):
        u = p1[i]
        v = p1[i + 1]

        #backup weight
        original_weight = G[u][v]["weight"]

        #remove the edge temporarily
        G.remove_edge(u, v)

        #compute alternate path
        p2, dist2, _ = dijkstra(G, start, goal)

        #restore edge
        G.add_edge(u, v, weight=original_weight)

        #keep the best valid alternative
        if p2 is not None and p2 != p1 and dist2 < best_second_cost:
            best_second_path = p2
            best_second_cost = dist2

    return p1, dist1, best_second_path, best_second_cost
