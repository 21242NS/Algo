def topological_sort(adj: dict) -> list:
    visited = set()
    order = []
    def dfs(u):
        visited.add(u)
        for v in adj[u]:
            if v not in visited:
                dfs(v)
        order.append(u)    
    for node in adj:
        if node not in visited:
            dfs(node)
    return order[::-1]   
print(topological_sort({ 1: {2}, 0: {1}, 2: {3}, 3: set() }))