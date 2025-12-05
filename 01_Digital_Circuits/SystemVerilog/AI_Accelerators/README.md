# Systolic Array (AI Accelerators)

This directory contains a clear, educational systolic array skeleton for
matrix multiplication and related accelerator concepts.

Files
- `pe.sv` — Processing Element (PE) that performs multiply-accumulate.
- `systolic_array.sv` — Top-level array built with generate blocks.
- `systolic_array_tb.sv` — Basic testbench to exercise the array.
- `analysis.md` — Complexity, architecture notes and practical considerations.

Notes
- The RTL here is a structural/behavioural skeleton intended for learning and
  to serve as a starting point for synthesis. For production use you will need:
  - Proper handshake (`valid/ready`) with backpressure
  - Pipelining and timing/power optimization
  - Fixed-point format, rounding/saturation, and overflow handling
  - Memory interfaces (DMA/AXI/BRAM) to feed the streams
1. **Systolic Array Algorithm** - Matrix multiplication optimization
2. **Winograd Transformation** - Convolution acceleration
3. **Sparsity Exploitation Algorithms** - Zero-skipping for sparse networks
4. **Attention Mechanism Hardware** - Transformer optimization
5. **Quantization Algorithms** - FP32→INT8/INT4 conversion