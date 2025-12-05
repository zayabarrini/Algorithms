**Time Complexity (The "How Fast")**
- **Best/Average/Worst (Ω/Θ/O)**: O(KH * KW * OH * OW) for direct convolution.
- **In Practice**: Use im2col + GEMM or FFT-based methods for large kernels.

**Space Complexity (The "How Much Memory")**
- **Auxiliary Space**: O(1) extra (aside from output) for the direct looped implementation.
- **Total Space**: input + kernel + output.

**Correctness & Assumptions**
- **Input Constraints**: single-channel 2D arrays; for multi-channel or batched inputs wrap or call per-channel.
- **Preconditions**: kernel shapes smaller than input (or use padding).
- **Edge Cases**: non-integer output sizes if stride/padding mis-specified.

**Practical Considerations**
- **Constant Factors**: Python loops are expensive for large maps — prefer vectorized im2col.
- **Cache Performance**: Blocking and data layout matter for CPU performance.
- **Real-world Data Patterns**: Image data tends to be spatially correlated; separable filters can reduce cost.
