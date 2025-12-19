def kruskal(edges, num_nodes):
    """
    Implements Kruskal's algorithm to find the Minimum Spanning Tree (MST) of a graph.

    Parameters:
    edges (list of tuples): A list where each tuple represents an edge in the format (weight, node1, node2).
    num_nodes (int): The number of nodes in the graph.

    Returns:
    list of tuples: A list of edges that form the MST.
    """
    # Sort edges based on their weights
    edges.sort(key=lambda x: x[0])

    parent = list(range(num_nodes))
    rank = [0] * num_nodes

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)

        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1

    mst = []
    for weight, node1, node2 in edges:
        if find(node1) != find(node2):
            union(node1, node2)
            mst.append((weight, node1, node2))

    return mst

def dijkstra(graph, start):
    """
    Implements Dijkstra's algorithm to find the shortest paths from a starting node to all other nodes in a weighted graph.

    Parameters:
    graph (dict): A dictionary where keys are node identifiers and values are lists of tuples (neighbor, weight).
    start: The starting node identifier.

    Returns:
    dict: A dictionary with the shortest distance from the start node to each node.
    """
    import heapq

    min_heap = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while min_heap:
        current_distance, current_node = heapq.heappop(min_heap)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(min_heap, (distance, neighbor))

    return distances