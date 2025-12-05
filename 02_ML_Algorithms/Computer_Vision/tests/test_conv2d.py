import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from conv2d import conv2d


def reference_conv(input: np.ndarray, kernel: np.ndarray):
    # naive reference using nested loops
    H, W = input.shape
    KH, KW = kernel.shape
    OH = H - KH + 1
    OW = W - KW + 1
    out = np.zeros((OH, OW), dtype=input.dtype)
    kf = np.flip(np.flip(kernel, axis=0), axis=1)
    for i in range(OH):
        for j in range(OW):
            out[i, j] = np.sum(input[i:i+KH, j:j+KW] * kf)
    return out


def test_conv2d_matches_reference():
    rng = np.random.default_rng(3)
    a = rng.integers(-5, 6, size=(8, 8)).astype(float)
    k = rng.integers(-2, 3, size=(3, 3)).astype(float)
    out1 = conv2d(a, k, padding=0, stride=1)
    out2 = reference_conv(a, k)
    assert np.allclose(out1, out2)
