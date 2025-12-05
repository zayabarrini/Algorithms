**Time Complexity (The "How Fast")**
- **Best/Average/Worst (Ω/Θ/O)**: O(N^2) per force evaluation due to pairwise interactions.
- **In Practice**: Use neighbor lists or cell lists to reduce to O(N) or O(N log N).

**Space Complexity (The "How Much Memory")**
- **Auxiliary Space**: O(N) for forces and velocities.
- **Total Space**: O(N) positions + auxiliaries.

**Correctness & Assumptions**
- **Input Constraints**: positions as (N,2) numpy array; periodic cubic box scalar `box`.
- **Preconditions**: dt small enough for stable integration.
- **Postconditions**: Returns trajectory steps with energy values.
- **Edge Cases**: Overlapping particles (r=0) are ignored to avoid division by zero.

**Practical Considerations**
- **Constant Factors**: LJ uses few arithmetic ops per pair but pair count dominates.
- **Cache Performance**: Use contiguous arrays and vectorized loops where possible.
- **Real-world Data Patterns**: For dense systems, neighbor lists are essential.
