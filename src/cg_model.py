"""Core coherence-gradient chaos model.

This module implements a minimal, *model-dependent* linear coherence-gradient
evolution scheme consistent with the discussion in the paper
"Chaos as a Coherence–Gradient Phenomenon: A DLSFH–SGCV–MC Analysis".

The main object is :class:`CGModel`, which wraps a propagator matrix
:math:`\mathcal{T}_\infty` and provides:

- evolution of two nearby coherence configurations
- numerical estimation of a coherence-gradient Lyapunov exponent
  :math:`\lambda_{\mathrm{CG}}`
- basic spectral diagnostics (spectral radius and operator norms)

This code is intentionally simple and phenomenological: it is **not** a full
DLSFH / SGCV microphysical simulator, but rather a linearized toy model that
allows referees and readers to reproduce the statements about
"operator-norm growth" and "coherence-gradient divergence" in a controlled,
transparent setting.
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass
from typing import Tuple


@dataclass
class CGModel:
    """Minimal coherence-gradient evolution model.

    Parameters
    ----------
    T_infty : np.ndarray
        Square propagator matrix implementing
        :math:`\Psi_{t+1} = \mathcal{T}_\infty \Psi_t`.
    """

    T_infty: np.ndarray

    # ------------------------------------------------------------
    #  Basic consistency checks
    # ------------------------------------------------------------
    def __post_init__(self) -> None:
        self.T_infty = np.array(self.T_infty, dtype=float)
        if self.T_infty.ndim != 2 or self.T_infty.shape[0] != self.T_infty.shape[1]:
            raise ValueError("T_infty must be a square 2D array")

    # ------------------------------------------------------------
    #  Time evolution
    # ------------------------------------------------------------
    def evolve(self, psi0: np.ndarray, n_steps: int) -> np.ndarray:
        """Evolve a single coherence configuration for ``n_steps``.

        Returns an array of shape (n_steps + 1, dim).
        """
        psi = np.array(psi0, dtype=float)
        if psi.ndim != 1 or psi.shape[0] != self.T_infty.shape[0]:
            raise ValueError("psi0 must be a 1D array compatible with T_infty")

        traj = [psi.copy()]
        for _ in range(n_steps):
            psi = self.T_infty @ psi
            traj.append(psi.copy())
        return np.vstack(traj)

    def evolve_pair(
        self,
        psi0: np.ndarray,
        psi0_prime: np.ndarray,
        n_steps: int,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Evolve two nearby configurations and return their distance trajectory.

        Returns
        -------
        psi_traj : ndarray
            Trajectory of psi0, shape (n_steps + 1, dim).
        psi_traj_prime : ndarray
            Trajectory of psi0_prime, same shape.
        D_n : ndarray
            Distance :math:`D_n = \|\Psi_n - \Psi_n'\|` at each step, shape (n_steps + 1,).
        """
        psi_traj = self.evolve(psi0, n_steps)
        psi_traj_prime = self.evolve(psi0_prime, n_steps)
        D_n = np.linalg.norm(psi_traj - psi_traj_prime, axis=1)
        return psi_traj, psi_traj_prime, D_n

    # ------------------------------------------------------------
    #  Lambda_CG estimation
    # ------------------------------------------------------------
    def estimate_lambda_CG(
        self,
        psi0: np.ndarray,
        psi0_prime: np.ndarray,
        n_steps: int = 200,
        fit_start: int = 10,
        fit_end: int = 150,
    ) -> Tuple[float, np.ndarray, np.ndarray]:
        """Estimate a coherence-gradient Lyapunov exponent.

        The estimate is obtained by fitting a straight line to
        :math:`\log D_n` over the window ``[fit_start, fit_end]``,
        where :math:`D_n = \|\Psi_n - \Psi_n'\|`.

        Returns
        -------
        lambda_hat : float
            Slope of the best-fit line (estimate of :math:`\lambda_{\mathrm{CG}}`).
        n_fit : ndarray
            Indices used in the fit.
        logD_fit : ndarray
            Corresponding :math:`\log D_n` values.
        """
        _, _, D_n = self.evolve_pair(psi0, psi0_prime, n_steps=n_steps)
        n_all = np.arange(len(D_n))

        fit_start = max(fit_start, 0)
        fit_end = min(fit_end, len(D_n) - 1)
        if fit_end <= fit_start + 1:
            raise ValueError("Fit window too small.")

        n_fit = n_all[fit_start:fit_end]
        logD_fit = np.log(D_n[fit_start:fit_end])

        slope, intercept = np.polyfit(n_fit, logD_fit, deg=1)
        lambda_hat = float(slope)
        return lambda_hat, n_fit, logD_fit

    # ------------------------------------------------------------
    #  Spectral diagnostics
    # ------------------------------------------------------------
    def spectral_radius(self) -> float:
        """Return the spectral radius rho(T_infty)."""
        eigvals = np.linalg.eigvals(self.T_infty)
        return float(np.max(np.abs(eigvals)))

    def operator_norm(self) -> float:
        """Return the operator 2-norm ||T_infty||_op (largest singular value)."""
        svals = np.linalg.svd(self.T_infty, compute_uv=False)
        return float(np.max(svals))

    def power_norm(self, n: int) -> float:
        """Return ||T_infty^n||_op (2-norm) for integer n >= 1."""
        if n < 1:
            raise ValueError("n must be >= 1")
        Tn = np.linalg.matrix_power(self.T_infty, n)
        svals = np.linalg.svd(Tn, compute_uv=False)
        return float(np.max(svals))


# ------------------------------------------------------------------------
# Helper: simple 5-node circulation + damping matrix for use in demos
# ------------------------------------------------------------------------
def build_pentagon_circulation_propagator(
    eta: float = 0.08,
    damping: float = 0.02,
) -> np.ndarray:
    """Construct a 5x5 toy propagator with circulation and damping.

    This is the matrix used in the VID pentagon demonstration and in some of
    the numerical experiments described in TESTS.md. It should be understood
    as a schematic analogue of a coherence-transport operator on a single
    closed loop of the DLSFH graph.
    """
    n = 5
    I = np.eye(n)
    A = np.zeros((n, n))
    for i in range(n):
        j = (i + 1) % n
        A[j, i] = 1.0  # directed cycle i -> j

    T = (1.0 - damping) * I + eta * A
    return T


def main() -> None:
    """Small self-test: print diagnostics for the default pentagon propagator."""
    T = build_pentagon_circulation_propagator()
    model = CGModel(T)

    dim = T.shape[0]
    psi0 = np.ones(dim)
    delta = 1e-6
    psi0_prime = psi0 + delta * np.random.default_rng(123).normal(size=dim)

    lambda_hat, n_fit, logD_fit = model.estimate_lambda_CG(
        psi0=psi0,
        psi0_prime=psi0_prime,
        n_steps=200,
        fit_start=10,
        fit_end=150,
    )

    print("Diagnostics for default pentagon propagator:")
    print("  spectral radius rho(T_infty) =", model.spectral_radius())
    print("  operator norm ||T_infty||_op =", model.operator_norm())
    print("  estimated lambda_CG ≈", lambda_hat)


if __name__ == "__main__":
    main()
