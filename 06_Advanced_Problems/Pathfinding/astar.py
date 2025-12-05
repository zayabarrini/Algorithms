"""A* pathfinding on a 2D grid.

Grid cells: 0 free, 1 blocked.
"""
from __future__ import annotations

import heapq
from typing import List, Tuple, Dict, Optional


Point = Tuple[int, int]


def heuristic(a: Point, b: Point) -> float:
    # Manhattan distance
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(pt: Point, grid: List[List[int]]) -> List[Point]:
    x, y = pt
    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    res = []
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0
    for dx, dy in deltas:
        nx, ny = x + dx, y + dy
        if 0 <= nx < h and 0 <= ny < w and grid[nx][ny] == 0:
            res.append((nx, ny))
    return res


def reconstruct(came_from: Dict[Point, Point], current: Point) -> List[Point]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def astar(start: Point, goal: Point, grid: List[List[int]]) -> Optional[List[Point]]:
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from: Dict[Point, Point] = {}
    gscore: Dict[Point, float] = {start: 0}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct(came_from, current)

        for nb in neighbors(current, grid):
            tentative_g = gscore[current] + 1
            if tentative_g < gscore.get(nb, float('inf')):
                came_from[nb] = current
                gscore[nb] = tentative_g
                f = tentative_g + heuristic(nb, goal)
                heapq.heappush(open_set, (f, tentative_g, nb))

    return None


if __name__ == "__main__":
    grid = [[0] * 5 for _ in range(5)]
    grid[2][1] = 1
    grid[2][2] = 1
    grid[2][3] = 1
    p = astar((0, 0), (4, 4), grid)
    print(p)
