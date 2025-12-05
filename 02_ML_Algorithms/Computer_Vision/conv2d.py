"""Reference 2D convolution (numpy) — forward only for clarity.

This is a clear, correct, and small implementation intended for learning and
profiling; production code should vectorize using im2col or use optimized
libraries (CuDNN, MKL, etc.).
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def conv2d(input: np.ndarray, kernel: np.ndarray, stride: int = 1, padding: int = 0) -> np.ndarray:
    """Compute 2D convolution for single-channel input and kernel.

    input: (H, W)
    kernel: (KH, KW)
    Returns output (OH, OW).
    """
    assert input.ndim == 2 and kernel.ndim == 2
    H, W = input.shape
    KH, KW = kernel.shape
    # pad input
    if padding > 0:
        padded = np.pad(input, ((padding, padding), (padding, padding)), mode='constant')
    else:
        padded = input

    OH = (H + 2 * padding - KH) // stride + 1
    OW = (W + 2 * padding - KW) // stride + 1
    out = np.zeros((OH, OW), dtype=input.dtype)

    # flip kernel for convolution
    kernel_f = np.flip(np.flip(kernel, axis=0), axis=1)

    for i in range(OH):
        for j in range(OW):
            si = i * stride
            sj = j * stride
            window = padded[si:si+KH, sj:sj+KW]
            out[i, j] = np.sum(window * kernel_f)

    return out


def _naive_conv(input: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    # helper used in tests for clarity
    return conv2d(input, kernel, stride=1, padding=0)


if __name__ == "__main__":
    import numpy as np
    a = np.arange(25).reshape(5,5).astype(float)
    k = np.array([[1,0,-1],[1,0,-1],[1,0,-1]], dtype=float)
    print(conv2d(a, k, padding=1))
