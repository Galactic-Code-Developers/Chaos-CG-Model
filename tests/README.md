# Tests and Reproducibility Notes

This document explains how the numerical statements in the
**"Chaos as a Coherence–Gradient Phenomenon"** paper can be reproduced with
the scripts in this repository.

The code is intentionally minimal and model-dependent. It is not a full
DLSFH/SGCV simulator; instead it provides small, controlled toy systems that
instantiate the *structure* of coherence-gradient chaos:

- linear propagation by a matrix :math:$\mathcal{T}_\infty$,
- exponential growth of the distance :math:$D_n = \|\Psi_n - \Psi_n'\|$,
- operator-norm and spectral diagnostics.


## 1. Operator-norm criterion (||T_infty^n||_op)

**Claim in paper (qualitative)**  
Chaotic regimes correspond to propagators whose iterates exhibit
operator-norm growth of the form

.. math::

    $\|\mathcal{T}_\infty^n\|_{\mathrm{op}} > C e^{\lambda n}$

for some :math:`\lambda > 0`.

**How to test numerically**

1. Open a Python session or Jupyter notebook.
2. Run:

   ```python
   from src.cg_model import CGModel, build_pentagon_circulation_propagator

   T = build_pentagon_circulation_propagator(eta=0.08, damping=0.02)
   model = CGModel(T)

   for n in [1, 2, 5, 10, 20]:
       print(n, model.power_norm(n))
   ```

3. You should see monotone growth in :math:$\|T_\infty^n\|_{\mathrm{op}}$
   with :math:`n`. On a typical machine the growth is close to exponential,
   consistent with an effective :math:`\lambda_{\mathrm{CG}} > 0` for this
   toy model.


## 2. Three-node toy example and distance growth D_n

**Claim in paper (qualitative)**  
A small VID-like subgraph already supports coherence-gradient divergence:
the distance :math:`D_n` between two nearby configurations grows
approximately as :math:`\exp(\lambda_{\mathrm{CG}} n)` over an intermediate
range of :math:`n`.

**Script**

- `src/example_three_node.py`

**How to run**

From the repository root:

```bash
python -m src.example_three_node
```

This will:

- construct a 3x3 propagator $T_infty^(3)$ with mild amplification and
  off-diagonal coupling,
- initialize two nearby states `psi0` and `psi0_prime`,
- evolve them for 200 steps,
- estimate :math:$\lambda_{\mathrm{CG}}$ via a linear fit to
  :math:`\log D_n` on a chosen window,
- print the estimated :math: $\lambda_{\mathrm{CG}}$ and spectral
  diagnostics,
- produce a matplotlib figure of :math:$\log D_n$ and the fitted line.

The numerical value of :math: $\lambda_{\mathrm{CG}}4 depends on the exact
matrix entries, but on a typical CPU it is **positive**, illustrating
coherence-gradient divergence in this minimal model.


## 3. VID-style pentagon and coherence-gradient chaos

**Claim in paper (qualitative)**  
Closed VID loops with sufficient coherence circulation support
coherence-gradient chaos, reflected in a positive
:math: $\lambda_{\mathrm{CG}}$ and operator-norm growth.

**Script**

- `src/vid_lattice_demo.py`

**How to run**

From the repository root:

```bash
python -m src.vid_lattice_demo
```

This will:

- build a directed pentagon graph with unit coherence increments,
- use `build_pentagon_circulation_propagator(eta=0.08, damping=0.02)` to
  construct a 5x5 toy propagator,
- evolve two nearby states and estimate :math: $\lambda_{\mathrm{CG}}$,
- print the number of nodes/edges, spectral radius, operator norm,
  and estimated :math: $\lambda_{\mathrm{CG}}$.

On a typical machine, the estimated :math:`\lambda_{\mathrm{CG}}` is again
**positive**, providing a concrete realization of coherence-gradient
chaos on a single closed loop.


## 4. Jupyter notebook for Zenodo / citation

The `notebooks/chaos_cg_demo.ipynb` notebook provides a self-contained,
executable demonstration of the three-node example and the pentagon VID
example. It is designed to be linked directly from Zenodo as the primary
"reproducibility entry point" for the chaos paper.

Suggested citation text (to include in Zenodo description):

> Numerical experiments for coherence-gradient chaos were performed with
> the `chaos_cg_model` package (Valamontes, 2025), archived at Zenodo
> [DOI to be inserted] and mirrored on GitHub.

