**Time Complexity (The "How Fast")**
- **Best Case (Ω)**: Ω(b) where b is branching factor (goal is start's neighbor).
- **Average Case (Θ)**: Θ(number of expanded nodes), depends on heuristic quality.
- **Worst Case (O)**: O(b^d) where d is path length if heuristic is poor.

**Space Complexity (The "How Much Memory")**
- **Auxiliary Space**: O(N) to store open/closed sets, where N is number of reachable cells.
- **Total Space**: grid size + O(N).
- **Common Pitfall**: Using inadmissible heuristic yields non-optimal paths.

**Correctness & Assumptions**
- **Input Constraints**: grid of 0 (free) / 1 (blocked).
- **Preconditions**: start and goal are within bounds and on free cells.
- **Postconditions**: If path exists and heuristic is admissible, returns shortest path.
- **Edge Cases**: No path returns `None`.

**Practical Considerations**
- **Constant Factors**: Heap operations cost log size of open set.
- **Cache Performance**: Use flat arrays for very large grids to improve cache locality.
- **Real-world Data Patterns**: Often obstacles are clustered; consider hierarchical pathfinding.
