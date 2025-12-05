"""Adam optimizer (reference implementation)

Provides a small, well-documented implementation of the Adam update rule
suitable for educational use and small experiments.
"""
from __future__ import annotations

import numpy as np
from typing import Dict, Tuple


class Adam:
    def __init__(self, lr: float = 1e-3, beta1: float = 0.9, beta2: float = 0.999, eps: float = 1e-8):
        self.lr = float(lr)
        self.beta1 = float(beta1)
        self.beta2 = float(beta2)
        self.eps = float(eps)
        self.m: Dict[int, np.ndarray] = {}
        self.v: Dict[int, np.ndarray] = {}
        self.t = 0

    def step(self, params: Dict[int, np.ndarray], grads: Dict[int, np.ndarray]) -> Dict[int, np.ndarray]:
        """Apply one Adam update step.

        params/grads are dicts mapping an identifier to numpy arrays (this simple
        API avoids requiring a specific neural-net framework).
        Returns the updated params dict.
        """
        self.t += 1
        updated = {}
        for k, p in params.items():
            g = grads[k]
            if k not in self.m:
                self.m[k] = np.zeros_like(p)
                self.v[k] = np.zeros_like(p)

            self.m[k] = self.beta1 * self.m[k] + (1 - self.beta1) * g
            self.v[k] = self.beta2 * self.v[k] + (1 - self.beta2) * (g * g)

            m_hat = self.m[k] / (1 - self.beta1 ** self.t)
            v_hat = self.v[k] / (1 - self.beta2 ** self.t)

            step = self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
            updated[k] = p - step

        return updated


def _example_quadratic_minimize() -> Tuple[float, float]:
    """Simple demo: minimize f(x)=(x-3)^2 starting at x=0 using Adam.
    Returns (x_final, f(x_final))."""
    adam = Adam(lr=0.1)
    x = np.array([0.0])
    for _ in range(200):
        grad = 2 * (x - 3)
        params = {0: x}
        grads = {0: grad}
        x = adam.step(params, grads)[0]
    return float(x), float(((x - 3) ** 2)[0])


if __name__ == "__main__":
    x_final, fval = _example_quadratic_minimize()
    print("x_final=", x_final, "fval=", fval)
