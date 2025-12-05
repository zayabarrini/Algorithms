**Time Complexity (The "How Fast")**
- **Best Case (Ω)**: Ω(n) per update (must touch each parameter once).
- **Average Case (Θ)**: Θ(n) per update.
- **Worst Case (O)**: O(n) per update.
- **In Practice**: Small constant factor overhead from bias-correction and elementwise sqrt.

**Space Complexity (The "How Much Memory")**
- **Auxiliary Space**: O(n) for `m` and O(n) for `v` (two extra arrays same size as params).
- **Total Space**: O(n) parameters + O(n) aux.
- **Common Pitfall**: Forgetting bias-correction increases error early in training.

**Correctness & Assumptions**
- **Input Constraints**: `params` and `grads` must be numpy arrays with matching shapes.
- **Preconditions**: Learning rate > 0; beta1, beta2 in (0,1).
- **Postconditions**: Parameters move in direction of negative gradient with adaptive step size.
- **Edge Cases**: Zero gradients, extremely small v_hat causing division stability handled by `eps`.

**Practical Considerations**
- **Constant Factors**: Per-parameter cost slightly higher than SGD due to extra arrays and sqrt.
- **Cache Performance**: Good when arrays are contiguous; try to use vectorized operations.
- **Real-world Data Patterns**: Adam performs well for sparse gradients and non-stationary objectives.
