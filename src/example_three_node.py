"""Three-node coherence-gradient chaos experiment.

This script constructs a minimal 3x3 propagator T_infty^(3) intended to model
a small VID-like subgraph, evolves two nearby initial states, and estimates
the coherence-gradient Lyapunov exponent lambda_CG.

It is a deliberately simple toy model illustrating how coherence-gradient
divergence can be realized in a low-dimensional system, as discussed in
the coherence-gradient chaos paper.

Run from the repository root via:

    python -m src.example_three_node
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt

from .cg_model import CGModel


def build_three_node_propagator() -> np.ndarray:
    """Return a 3x3 toy propagator with mild amplification and coupling.

    The structure is chosen phenomenologically so that:

    - spectral radius > 1
    - a generic perturbation grows approximately exponentially
    """
    return np.array(
        [
            [1.02, 0.03, 0.00],
            [0.01, 1.03, 0.02],
            [0.00, 0.02, 1.01],
        ],
        dtype=float,
    )


def main() -> None:
    T = build_three_node_propagator()
    model = CGModel(T)

    dim = T.shape[0]
    psi0 = np.ones(dim)
    delta = 1e-7
    rng = np.random.default_rng(42)
    psi0_prime = psi0 + delta * rng.normal(size=dim)

    n_steps = 200
    _, _, D_n = model.evolve_pair(psi0, psi0_prime, n_steps=n_steps)
    n_all = np.arange(len(D_n))

    lambda_hat, n_fit, logD_fit = model.estimate_lambda_CG(
        psi0=psi0,
        psi0_prime=psi0_prime,
        n_steps=n_steps,
        fit_start=10,
        fit_end=150,
    )

    # Reconstruct fitted line for plotting
    coeffs = np.polyfit(n_fit, logD_fit, deg=1)
    logD_fit_line = np.polyval(coeffs, n_fit)

    print("Three-node toy model diagnostics:")
    print("  spectral radius rho(T_infty) =", model.spectral_radius())
    print("  operator norm ||T_infty||_op =", model.operator_norm())
    print("  estimated lambda_CG ≈", lambda_hat)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(n_all, np.log(D_n), label="log D_n (all)")
    ax.plot(n_fit, logD_fit, "o", markersize=3, label="fit window data")
    ax.plot(n_fit, logD_fit_line, "--", label="linear fit")
    ax.set_xlabel("n (time step)")
    ax.set_ylabel("log D_n")
    ax.set_title("Coherence-gradient chaos: 3-node toy model")
    ax.legend()
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
