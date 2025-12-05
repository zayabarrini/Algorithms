import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from adam import Adam


def test_adam_converges_quadratic():
    adam = Adam(lr=0.1)
    x = np.array([0.0])
    for _ in range(300):
        grad = 2 * (x - 3)
        params = {0: x}
        grads = {0: grad}
        x = adam.step(params, grads)[0]

    assert abs(float(x) - 3.0) < 1e-3
