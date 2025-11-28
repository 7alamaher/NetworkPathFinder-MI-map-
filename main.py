import json
import networkx as nx
from GUI import create_gui


def build_graph(json_path="graph_data.json"):
    with open(json_path) as f:
        data = json.load(f)

    G = nx.Graph()

    # add cities with (lat, long) positions
    for city, info in data["Cities"].items():
        G.add_node(city, pos=(info["lat"], info["long"]))

    # add weighted edges
    for city, neighbors in data["Distances"].items():
        for neighbor, dist in neighbors.items():
            G.add_edge(city, neighbor, weight=dist)

    return G


if __name__ == "__main__":
    G = build_graph()
    create_gui(G)
