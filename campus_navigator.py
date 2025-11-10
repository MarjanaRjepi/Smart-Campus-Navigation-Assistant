from collections import deque
import heapq

# Grid codes:
# 0 = free path
# 1 = restricted area (blocked)
# 2 = crowded path (extra cost)

# Example campus map (5x5)
campus_map = [
    [0, 0, 2, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 2, 0, 0],
    [0, 1, 0, 0, 2],
    [0, 0, 0, 0, 0]
]

start = (0, 0)  # starting point (entrance)
goals = [(2, 4), (4, 2)]  # destinations (library and cafeteria)

def neighbors(pos, grid):
    """Return all valid neighbor cells (no out-of-bounds, no restricted areas)."""
    x, y = pos
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in moves:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] != 1:
            yield (nx, ny)

def manhattan(a, b):
    """Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def bfs_search(grid, start, goals):
    """Breadth-First Search to find a path visiting all goals."""
    queue = deque([(start, [], set())])
    visited = set()
    while queue:
        pos, path, visited_goals = queue.popleft()
        if (pos, tuple(sorted(visited_goals))) in visited:
            continue
        visited.add((pos, tuple(sorted(visited_goals))))

        new_path = path + [pos]
        if pos in goals:
            visited_goals = visited_goals | {pos}
            if len(visited_goals) == len(goals):
                return new_path  # all goals visited

        for n in neighbors(pos, grid):
            queue.append((n, new_path, visited_goals))
    return None

def a_star_search(grid, start, goals):
    """A* search that uses Manhattan distance + crowd penalty as heuristic."""
    open_heap = []
    heapq.heappush(open_heap, (0, start, [], set()))
    visited = set()

    while open_heap:
        cost, pos, path, visited_goals = heapq.heappop(open_heap)
        if (pos, tuple(sorted(visited_goals))) in visited:
            continue
        visited.add((pos, tuple(sorted(visited_goals))))

        new_path = path + [pos]
        if pos in goals:
            visited_goals = visited_goals | {pos}
            if len(visited_goals) == len(goals):
                return new_path  # done

        for n in neighbors(pos, grid):
            crowd_penalty = 2 if grid[n[0]][n[1]] == 2 else 1
            g = cost + crowd_penalty
            remaining = [g for g in goals if g not in visited_goals]
            h = min(manhattan(n, g) for g in remaining) if remaining else 0
            heapq.heappush(open_heap, (g + h, n, new_path, visited_goals))
    return None

if __name__ == "__main__":
    print("Campus Map (0=free, 1=restricted, 2=crowded):")
    for row in campus_map:
        print(row)
    print("\nStarting BFS and A*...\n")

    bfs_path = bfs_search(campus_map, start, goals)
    print("BFS Path:", bfs_path)
    print("Steps:", len(bfs_path) if bfs_path else "No path found")

    a_star_path = a_star_search(campus_map, start, goals)
    print("\nA* Path:", a_star_path)
    print("Steps:", len(a_star_path) if a_star_path else "No path found")