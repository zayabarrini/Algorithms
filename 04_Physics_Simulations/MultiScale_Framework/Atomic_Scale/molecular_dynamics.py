"""Minimal velocity-Verlet molecular dynamics with Lennard-Jones potential.

This example is intentionally small: it demonstrates the integrator, force
calculation, and energy monitoring for a handful of particles in 2D.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple


def lj_force(positions: np.ndarray, box: float, epsilon: float = 1.0, sigma: float = 1.0) -> np.ndarray:
    """Compute pairwise Lennard-Jones forces with periodic boundaries.

    positions: (N,2)
    returns forces array shape (N,2)
    """
    N = positions.shape[0]
    forces = np.zeros_like(positions)
    for i in range(N):
        for j in range(i + 1, N):
            # minimum image
            dx = positions[i] - positions[j]
            dx -= box * np.rint(dx / box)
            r2 = dx.dot(dx)
            if r2 == 0:
                continue
            inv_r2 = 1.0 / r2
            inv_r6 = inv_r2 ** 3
            f_scalar = 24 * epsilon * inv_r2 * inv_r6 * (2 * inv_r6 - 1)
            f = f_scalar * dx
            forces[i] += f
            forces[j] -= f
    return forces


def potential_energy(positions: np.ndarray, box: float, epsilon: float = 1.0, sigma: float = 1.0) -> float:
    N = positions.shape[0]
    U = 0.0
    for i in range(N):
        for j in range(i + 1, N):
            dx = positions[i] - positions[j]
            dx -= box * np.rint(dx / box)
            r2 = dx.dot(dx)
            if r2 == 0:
                continue
            inv_r6 = (1.0 / r2) ** 3
            U += 4 * epsilon * (inv_r6 ** 2 - inv_r6)
    return float(U)


def velocity_verlet(positions: np.ndarray, velocities: np.ndarray, box: float, dt: float, steps: int):
    forces = lj_force(positions, box)
    traj = []
    for _ in range(steps):
        positions = (positions + velocities * dt + 0.5 * forces * dt * dt) % box
        new_forces = lj_force(positions, box)
        velocities = velocities + 0.5 * (forces + new_forces) * dt
        forces = new_forces
        Ekin = 0.5 * np.sum(velocities ** 2)
        Epot = potential_energy(positions, box)
        traj.append((positions.copy(), velocities.copy(), Ekin + Epot))
    return traj


def _example_run():
    rng = np.random.default_rng(1)
    N = 8
    box = 10.0
    positions = rng.random((N, 2)) * box
    velocities = (rng.random((N, 2)) - 0.5) * 0.1
    traj = velocity_verlet(positions, velocities, box, dt=0.001, steps=100)
    print("Initial E:", traj[0][2], "Final E:", traj[-1][2])


if __name__ == "__main__":
    _example_run()
