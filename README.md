# Coherence-Gradient Chaos Model — Reproducibility Package

This repository contains minimal, self-contained code to explore the
**coherence-gradient chaos** framework introduced in:

> Valamontes, A., *Chaos as a Coherence–Gradient Phenomenon:  
> A DLSFH–SGCV–MC Analysis* (manuscript).

The goal is to provide a concrete numerical playground for the **model-dependent**
results discussed in the paper, including:

- The **linearized ∞–tensor propagator** $\mathcal{T}_{\infty}$.
- The **spectral-radius / operator-norm instability criterion**.
- The **three-node VID chain example**.
- Numerical estimation of the **coherence-gradient Lyapunov exponent** $\lambda_{\mathrm{CG}}$.
- Simple experiments linking **VID-like circulation parameters** to divergence rates.

The code is intentionally lightweight and readable, intended as a starting point
for more elaborate DLSFH/VID simulations.

---

## 1. Installation

Create and activate a fresh environment (conda or venv recommended), then install
dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

Core dependencies:

- `numpy` — core linear algebra  
- `scipy` — optional (spectral radius, stability checks)  
- `matplotlib` — plotting  
- `networkx` — optional lattice/graph tooling  

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

  tests/
    test_divergence.py
    test_operator_norm.py
    test_lyapunov_coarse.py

  notebooks/
    chaos_three_vertex.ipynb
    vid_circulation_instability.ipynb
```

All scripts correspond directly to sections of the manuscript (see Appendix A).

---

## 3. Quickstart: Three-Node VID Chain

To reproduce the **three-node VID chain** analyzed in the paper:

```bash
cd chaos_cg_model
python -m src.example_three_node
```

This script:

1. Constructs the 3×3 propagator $\mathcal{T}_{\infty}^{(3)}$  
   using parameters `(eta, alpha, beta)`.
2. Evolves two nearby coherence configurations for `N` steps.
3. Computes the distance trajectory  
   $D_n = \| \Psi_n - \Psi'_n \|$.
4. Fits $\lambda_{\mathrm{CG}}$ from a linear regression of `log(D_n)` vs `n`.
5. Compares against the model expectation  
   $\log(1+\eta)$.

If `matplotlib` is installed, diagnostic plots are also generated.

---

## 4. Core Concept: Coherence-Gradient Chaos

The numerical model implements these ideas:

- Evolution of a discrete coherence field represented by  
  $\Psi_t \in \mathbb{R}^N$.
- A linearized update rule  
  $\Psi_{t+1} = \mathcal{T}_{\infty} \Psi_t$.
- A coherence-gradient Lyapunov exponent $\lambda_{\mathrm{CG}}$ defined by  
  exponential growth of distances between nearby states.
- Instability driven by **anisotropies** in a coherence-gradient field.
- Theoretical linkage to **VID loop circulation**.

The code does **not** attempt full DLSFH or SGCV physics — it reproduces only
the mathematical instability structure used in the manuscript.

---

## 5. Extending the Experiments

Several natural directions for extending this package:

- Replace the 3×3 matrix with larger propagators modeling full VID subgraphs.
- Examine how “circulation parameters’’ in `vid_lattice_demo.py` influence  
  $\lambda_{\mathrm{CG}}$.
- Introduce explicit dependence of $\mathcal{T}_{\infty}$ 
  - on a discrete coherence-gradient field $G_{ab}(v)$.
- Perform parameter scans over $(\eta,\alpha,\beta)$ to map regions where  
  $\rho(\mathcal{T}_{\infty}) > 1$.
- Compare operator-norm growth with numerically extracted Lyapunov exponents.

These experiments mirror the interpretive structure of the manuscript.

---

## 6. Reproducibility Notes

- All randomness uses fixed seeds.  
- No external data files required.  
- Every experiment runs in **< 1.5 seconds** on a modern laptop.  
- Each numerical claim in the paper corresponds to a test or notebook:

| Manuscript Section | Numerical Validation |
|-------------------|----------------------|
| Definition 1 (Divergence) | `tests/test_divergence.py` |
| Proposition 1 (Operator Norm) | `tests/test_operator_norm.py` |
| VID Circulation Instability | `notebooks/vid_circulation_instability.ipynb` |
| Three-Node Example | `src/example_three_node.py` |
| Coarse-Grained Lyapunov Matching | `tests/test_lyapunov_coarse.py` |

See **`TESTS.md`** for details.

---

## 7. Citation

If you use this package, please cite:

> Valamontes, A., *Chaos as a Coherence–Gradient Phenomenon:  
> A DLSFH–SGCV–MC Analysis* (manuscript).

