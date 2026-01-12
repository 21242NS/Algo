from collections import deque
snakes = {17: 13, 52: 29, 57: 40, 62: 22, 88: 18, 95: 51, 97: 79}
ladders = {3: 21, 8: 30, 28: 84, 58: 77, 75: 86, 80: 100, 90: 91} 

def minimum_turns(snakes, ladders):
    teleport = {**snakes, **ladders}

    # BFS
    queue = deque([(1, 0)])      
    visited = {1: None}          

    while queue:
        square, turns = queue.popleft()
        if square == 100:
            path = []
            cur = square
            while cur is not None:
                path.append(cur)
                cur = visited[cur]
            return turns, path[::-1]
        for move in range(1, 7):
            nxt = square + move
            if nxt > 100:
                continue
            if nxt in teleport:
                nxt = teleport[nxt]
            if nxt not in visited:
                visited[nxt] = square
                queue.append((nxt, turns + 1))

    return None
turns, path = minimum_turns(snakes, ladders)
print("Minimum turns:", turns)
print("Path:", path)