from heapq import heappush, heappop
import math 


def a_star(start, goal, is_blocked):
    dirs = [
        (1, 0), (-1, 0), (0, 1), (0, -1),
        (1, 1), (-1, 1), (1, -1), (-1, -1)
    ]

    def heuristic(a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)

    open_set = []
    heappush(open_set, (heuristic(start, goal), start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heappop(open_set)

        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        cx, cy = current

        for dx, dy in dirs:
            nx, ny = cx + dx, cy + dy

            if dx != 0 and dy != 0:
                if is_blocked(cx + dx, cy) or is_blocked(cx, cy + dy):
                    continue

            if is_blocked(nx, ny):
                continue

            cost = math.sqrt(2) if dx != 0 and dy != 0 else 1
            tentative_g = g_score[current] + cost

            if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                g_score[(nx, ny)] = tentative_g
                came_from[(nx, ny)] = current

                f = tentative_g + heuristic((nx, ny), goal)
                heappush(open_set, (f, (nx, ny)))

    return None

def get_nearest_walkable(goal, is_blocked):
    from collections import deque
    
    visited = set()
    q = deque([goal])
    visited.add(goal)
    dirs = [(1,0),(-1,0),(0,1),(0,-1)]
    while q:
        x, y = q.popleft()

        if not is_blocked(x, y):
            return (x, y)

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                q.append((nx, ny))

    return None


def heuristic(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)