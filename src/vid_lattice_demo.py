"""VID lattice demo.

This module provides a minimal demonstration of coherence transport on a
small directed pentagon graph that mimics a subgraph of the 20-node DLSFH
lattice. It shows how:

- a graph can be endowed with simple "coherence increments" G(e),
- a toy propagator T_infty can be constructed, and
- the CGModel class can be used to study stability and distance growth.

Run from the repository root:

    python -m src.vid_lattice_demo
"""

from __future__ import annotations

import numpy as np
import networkx as nx

from .cg_model import CGModel, build_pentagon_circulation_propagator


def build_pentagon_graph() -> nx.DiGraph:
    """Build a directed pentagon graph with unit coherence increments."""
    G = nx.DiGraph()
    nodes = list(range(5))
    G.add_nodes_from(nodes)
    for i in nodes:
        j = (i + 1) % len(nodes)
        G.add_edge(i, j, G_increment=1.0)
    return G


def main() -> None:
    # Build graph and associated propagator
    G = build_pentagon_graph()
    T = build_pentagon_circulation_propagator(eta=0.08, damping=0.02)
    model = CGModel(T)

    dim = T.shape[0]
    psi0 = np.ones(dim)
    delta = 1e-7
    rng = np.random.default_rng(7)
    psi0_prime = psi0 + delta * rng.normal(size=dim)

    lambda_hat, n_fit, logD_fit = model.estimate_lambda_CG(
        psi0=psi0,
        psi0_prime=psi0_prime,
        n_steps=200,
        fit_start=10,
        fit_end=150,
    )

    print("VID pentagon demo diagnostics:")
    print("  number of nodes =", G.number_of_nodes())
    print("  number of edges =", G.number_of_edges())
    print("  spectral radius rho(T_infty) =", model.spectral_radius())
    print("  operator norm ||T_infty||_op =", model.operator_norm())
    print("  estimated lambda_CG ≈", lambda_hat)


if __name__ == "__main__":
    main()
