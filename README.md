# Coherence-Gradient Chaos Model — Reproducibility Package

This repository contains minimal, self-contained code to explore the
**coherence-gradient chaos** framework introduced in:

> Valamontes, A., *Chaos as a Coherence–Gradient Phenomenon:  
> A DLSFH–SGCV–MC Analysis* (manuscript).

The goal is to provide a concrete numerical playground for the **model-dependent**
results discussed in the paper, including:

- The **linearized ∞–tensor propagator** $\(\mathcal{T}_{\infty}\$.
- The **spectral-radius / operator-norm instability criterion**.
- The **three-node VID chain example**.
- Numerical estimation of the **coherence-gradient Lyapunov exponent** \(\lambda_{\mathrm{CG}}\).
- Simple experiments linking **circulation-like parameters** to divergence rates.

The code is intended to be lightweight and readable, and can be used as a
starting point for more elaborate DLSFH/VID simulations.

---

## 1. Installation

Create and activate a fresh environment (conda or venv recommended), then install
dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

The core dependencies are:

- `numpy` — linear algebra and arrays
- `scipy` — optional, for spectral radius checks (fallbacks provided)
- `matplotlib` — for simple plots
- `networkx` — (optional) for DLSFH/VID graph scaffolding

---

## 2. Repository Structure

```text
chaos_cg_model/
  README.md               # This file
  requirements.txt        # Python dependencies

  src/
    cg_model.py           # Core coherence-gradient model + utilities
    example_three_node.py # Reproduces the 3-node VID chain from the paper
    vid_lattice_demo.py   # Skeleton for DLSFH-like lattice experiments
```

You can add this folder as a GitHub repository directly, or archive it for
Zenodo as-is.

---

## 3. Quickstart: Three-Node VID Chain

To reproduce the **three-node VID chain** described in the paper, run:

```bash
cd chaos_cg_model
python -m src.example_three_node
```

This script will:

1. Construct the 3×3 matrix $\mathcal{T}_{\infty}^{(3)}\$ of the form
   described in the manuscript, with parameters `(eta, alpha, beta)`.
2. Evolve two nearby initial coherence configurations for `N` steps.
3. Compute the distance trajectory
   $\(D_n = \\|\Psi_n - \Psi_n'\\|\$.
4. Estimate $\lambda_{\mathrm{CG}}\)$ via a linear fit of
   `log D_n` vs `n` on a chosen time window.
5. Compare the estimated exponent to the model expectation
   $\log(1+\eta)\$.

The script prints the key quantities to the console and, if `matplotlib` is
available, produces simple diagnostic plots.

---

## 4. Core Concept: Coherence-Gradient Chaos

The numerical model implemented here encodes the following ideas:

- Dynamics on a finite-dimensional coherence vector $\(\Psi_t\)$.
- An effective linear propagator $\(\mathcal{T}_{\infty}\)$ arising from
  linearization of the discrete update rule around a reference configuration.
- A **coherence-gradient Lyapunov exponent** $\(\lambda_{\mathrm{CG}}\)$
  extracted from exponential growth of distances between nearby initial
  coherence states.

The code does **not** attempt to implement full DLSFH/SGCV microphysics; it
focuses instead on the **linearized, model-dependent instability structure**
that underlies the theoretical results in the paper.

---

## 5. Extending the Experiments

Some ideas for extending this package:

- Replace the 3×3 propagator with larger matrices reflecting more detailed
  VID subgraphs of the 20-node DLSFH lattice.
  
- Introduce explicit dependence of $\(\mathcal{T}_{\infty}\)$$ on a discrete
  coherence-gradient field $\(G_{ab}(v)\)$.
  
- Explore the relationship between simple “circulation” parameters in
  `vid_lattice_demo.py` and numerically estimated $\(\lambda_{\mathrm{CG}}\)$.
  
- Scan over parameter spaces (e.g. $\(\eta,\alpha,\beta\))$ to map out
  regions with $\(\rho(\mathcal{T}_{\infty}) > 1\)$ and compare with
  numerically extracted exponents.

---

## 6. Reproducibility Notes

- All scripts use fixed random seeds where randomness is involved.
- The model is **toy-level** and explicitly **model-dependent**; it is meant to
  reflect the mathematical structure of the coherence-gradient chaos framework,
  not to represent a fully realistic physical simulation.
- The code is self-contained and does *not* rely on external data files.

---

## 7. Citation

If you use this package in a publication, please cite the corresponding
manuscript:

> Valamontes, A., *Chaos as a Coherence–Gradient Phenomenon:  
> A DLSFH–SGCV–MC Analysis* (manuscript).
