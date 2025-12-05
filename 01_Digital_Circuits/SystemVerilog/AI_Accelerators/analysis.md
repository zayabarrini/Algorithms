**Time Complexity (The "How Fast")**
- **Best/Average/Worst (Ω/Θ/O)**: A systolic array computes an N×N matrix multiply in O(N) pipelined steps with O(N^2) PEs (for a fully-unfolded N×N array). Latency is O(N) across the array; throughput can approach one output per cycle with full pipelining.

**Space Complexity (The "How Much Memory")**
- **Auxiliary Space**: O(N^2) PEs / accumulators when fully unrolled.
- **Total Space**: On-chip storage for partial results, local registers and FIFOs.

**Correctness & Assumptions**
- **Input Constraints**: Inputs must be supplied with correct timing and alignment. Numeric format must be defined (fixed point or floating point) and match across PEs.
- **Preconditions**: Handshake control must ensure no data hazards or pipeline bubbles mis-align inputs.
- **Postconditions**: With correct streaming, each PE computes valid partial sums leading to correct matrix product.
- **Edge Cases**: Overflow, underflow, and fixed-point scaling mistakes are common pitfalls.

**Practical Considerations**
- **Constant Factors**: Choose DATA_W to balance precision with area/timing. Multipliers are area-heavy.
- **Cache Performance**: On FPGA, local register and BRAM layout determines effective data reuse — aim to stream from BRAM tiles.
- **Real-world Data Patterns**: For sparse matrices, zero-skipping and compressed streams significantly reduce work.

**Design notes**
- Use `generate` blocks to scale `DIM`; instantiate PEs with consistent interfaces.
- Add ready signals to avoid data loss when downstream PEs are stalled.
- Pipeline multiply and accumulate steps across registers to meet clock frequency.
