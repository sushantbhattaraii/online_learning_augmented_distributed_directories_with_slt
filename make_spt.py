import os
import networkx as nx
from draw_graph import see_graph


def make_spt(G, owner):
    """
    Construct a shortest path tree (SPT) rooted at `owner`.

    Parameters
    ----------
    G : networkx.Graph
        Connected weighted graph.
    owner : int
        Root node of the SPT.

    Returns
    -------
    SPT : networkx.Graph
        Shortest path tree rooted at owner.
    distances : dict
        Shortest-path distance from owner to every node.
    paths : dict
        Shortest path from owner to every node.
    """

    if owner not in G:
        raise ValueError(f"Owner node {owner} is not in the graph.")

    # Compute shortest paths from the owner using Dijkstra's algorithm
    distances, paths = nx.single_source_dijkstra(
        G,
        source=owner,
        weight="weight"
    )

    # Create the shortest path tree
    SPT = nx.Graph()
    SPT.add_nodes_from(G.nodes())

    # For each node, connect it to its predecessor on the shortest path
    for node in G.nodes():
        if node == owner:
            continue

        path = paths[node]
        parent = path[-2]
        # SPT.add_edge(parent, node)
        weight = G[parent][node]["weight"]
        SPT.add_edge(parent, node, weight=weight)

    return SPT, distances, paths


def main():

    # ---------------------------------------------------------
    # Input graph
    # ---------------------------------------------------------
    graphml_file = os.path.join(
        "sample_graphs",
        "12random_diameter54test.edgelist"
    )

    G = nx.read_graphml(graphml_file)

    # Convert node labels from strings to integers
    G = nx.relabel_nodes(G, lambda x: int(x))

    # ---------------------------------------------------------
    # Choose the owner/root
    # ---------------------------------------------------------
    owner = 6

    # ---------------------------------------------------------
    # Make the shortest path tree
    # ---------------------------------------------------------
    SPT, distances, paths = make_spt(G, owner)

    # ---------------------------------------------------------
    # Print results
    # ---------------------------------------------------------
    print("=" * 60)
    print("Shortest Path Tree")
    print("=" * 60)

    print(f"Owner (root): {owner}")
    print(f"Number of nodes in G: {G.number_of_nodes()}")
    print(f"Number of edges in G: {G.number_of_edges()}")
    print(f"Number of nodes in SPT: {SPT.number_of_nodes()}")
    print(f"Number of edges in SPT: {SPT.number_of_edges()}")

    print("\nSPT edges:")
    for u, v in SPT.edges():
        print(f"{u} -- {v}")

    print("\nShortest-path distances from owner:")
    for node in sorted(distances):
        print(f"{owner} -> {node}: {distances[node]}")

    print("\nShortest paths from owner:")
    for node in sorted(paths):
        print(f"{owner} -> {node}: {paths[node]}")

    # ---------------------------------------------------------
    # Verify that SPT is actually a tree
    # ---------------------------------------------------------
    print("\nSPT verification:")
    print(f"Is tree? {nx.is_tree(SPT)}")
    print(f"Expected number of edges: {G.number_of_nodes() - 1}")
    print(f"Actual number of edges: {SPT.number_of_edges()}")

    see_graph(SPT)


if __name__ == "__main__":
    main()