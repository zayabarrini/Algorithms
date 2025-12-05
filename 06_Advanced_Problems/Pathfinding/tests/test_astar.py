import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from astar import astar


def test_astar_simple():
    grid = [[0] * 5 for _ in range(5)]
    grid[2][1] = 1
    grid[2][2] = 1
    grid[2][3] = 1
    path = astar((0, 0), (4, 4), grid)
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (4, 4)
