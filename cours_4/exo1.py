import collections


def shortest_paths(adj, start):
    dist={start: 0}
    queue=collections.deque([start])
    while queue:
        node = queue.popleft()
        queue.extend(adj[node] - dist.keys())
        for neighbor in adj[node]-dist.keys():
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
    return dist
    
print(shortest_paths({0: {1, 2}, 1: {3, 4}, 2: {5,6}, 3: set(),4: set(),5: set(),6: set()}, 0))
