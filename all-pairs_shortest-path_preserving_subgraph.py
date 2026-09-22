import networkx as nx
import os
from draw_graph import see_graph


def make_distance_preserving_graph(G):
    """
    Build a subgraph of G that preserves one chosen shortest path
    and the shortest-path distance for every pair of vertices.

    Assumes positive edge weights stored under 'weight'.
    """

    H = nx.Graph()

    # Keep all vertices
    H.add_nodes_from(G.nodes())

    # Compute one shortest path for every pair
    for source in G.nodes():

        paths = nx.single_source_dijkstra_path(
            G,
            source=source,
            weight="weight"
        )

        # Add every edge from every shortest path
        for target, path in paths.items():

            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]

                # Copy the original edge weight
                weight = G[u][v]["weight"]

                H.add_edge(u, v, weight=weight)

    return H

def load_graph(network_file_name):
    graphml_file = os.path.join('sample_graphs', str(network_file_name))
    G_example = nx.read_graphml(graphml_file)
    G_example = nx.relabel_nodes(G_example, lambda x: int(x))
    return G_example


network_file_name = '12random_diameter54test.edgelist'
G = load_graph(network_file_name)
G_sub = make_distance_preserving_graph(G)

see_graph(G_sub)