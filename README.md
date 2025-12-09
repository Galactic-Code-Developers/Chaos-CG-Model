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

To reproduce the **three-node VID chain** described in the paper, run:

```bash
cd chaos_cg_model
python -m src.example_three_node
```

This script will:

1. Construct the 3×3 matrix $\mathcal{T}_{\infty}^{(3)}$ with parameters `(eta, alpha, beta)`.
2. Evolve two nearby initial coherence configurations for `N` steps.
3. Compute the divergence trajectory  
   $D_n = \lVert \Psi_n - \Psi_n' \rVert$.
4. Estimate $\lambda_{\mathrm{CG}}$ via a linear regression of `log(D_n)` vs `n`.
5. Compare the measured value to the model prediction  
   $\log(1+\eta)$.

If `matplotlib` is installed, the script also produces diagnostic plots.

---

## 4. Core Concept: Coherence-Gradient Chaos

The numerical model implemented here encodes the following theoretical structure:

- A discrete **coherence vector** $\Psi_t$ evolving over time.
- An effective **linear propagator** $\mathcal{T}_{\infty}$ derived from  
  a linearization of the coherence update rule around a reference configuration.
- A **coherence-gradient Lyapunov exponent** $\lambda_{\mathrm{CG}}$ extracted  
  from exponential separation of nearby initial states.
- A connection between **VID loop circulation** and instability growth rates.

The code is **model-dependent** and **toy-level**, designed specifically to match
the mathematical framework of the accompanying manuscript.

---

## 5. Extending the Experiments

Several natural extensions include:

- Replace the 3×3 matrix with higher-dimensional propagators corresponding to
  more realistic VID subgraphs of the 20-node DLSFH lattice.
- Explore how simple “circulation” parameters defined in  
  `vid_lattice_demo.py` influence $\lambda_{\mathrm{CG}}$.
- **Introduce explicit dependence of $\mathcal{T}_{\infty}$ on a discrete coherence-gradient field $G_{ab}(v)$.**
- Perform parameter-space scans over $(\eta,\alpha,\beta)$ to map regions where  
  $\rho(\mathcal{T}_{\infty}) > 1$.
- Compare operator-norm growth with numerically extracted Lyapunov exponents.

All such experiments are suitable for inclusion in a Zenodo archive.

---

## 6. Reproducibility Notes

The design philosophy for this package:

- All scripts use **fixed random seeds** where random choices occur.
- No external datasets are required.
- Experiments complete in **under 1.5 seconds** on a 2024 laptop.
- Results correspond to each subsection of **Appendix A** in the manuscript:
  - A.1 Divergence experiment  
  - A.2 Three-node VID growth  
  - A.3 Operator-norm criterion  
  - A.4 Circulation instability  
  - A.5 Coarse-grained Lyapunov comparison  

The manuscript cross-references these reproducibility points.

---

## 7. TESTS.md Mapping

See `TESTS.md` for a detailed mapping between numerical claims and code files.

Example excerpts:

- **Definition 1 (Divergence):**  
  Verified by `tests/test_divergence.py`.

- **Proposition 1 (Operator-Norm Criterion):**  
  Verified by `tests/test_operator_norm.py`.

- **VID Circulation Instability:**  
  Demonstrated in `notebooks/vid_circulation_instability.ipynb`.

- **Three-Node Exponential Growth:**  
  Reproduced in `src/example_three_node.py`.

---

## 8. Citation

If you use this package in a publication, please cite:

> Valamontes, A., *Chaos as a Coherence–Gradient Phenomenon:  
> A DLSFH–SGCV–MC Analysis* (manuscript).

