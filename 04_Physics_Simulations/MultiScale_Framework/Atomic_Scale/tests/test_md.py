import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from molecular_dynamics import velocity_verlet


def test_energy_conservation_small_steps():
    rng = np.random.default_rng(2)
    N = 6
    box = 8.0
    positions = rng.random((N, 2)) * box
    velocities = (rng.random((N, 2)) - 0.5) * 0.1
    traj = velocity_verlet(positions, velocities, box, dt=0.001, steps=200)
    E0 = traj[0][2]
    Efinal = traj[-1][2]
    # energy should not drift too far for small dt and short simulation
    assert abs(Efinal - E0) / (abs(E0) + 1e-12) < 1e-2
