# Reproducibility Notes — Coherence-Gradient Chaos Model

This document links the **model-dependent numerical claims** in

> Valamontes, A., *Chaos as a Coherence–Gradient Phenomenon:  
> A DLSFH–SGCV–MC Analysis* (manuscript)

to specific scripts and parameter choices in this repository.

All experiments are toy-level, finite-dimensional, and explicitly
**model-dependent**. They are designed to support the *structure* of the
coherence-gradient chaos framework, not to model a specific physical system.

---

## A. Mapping Paper Claims to Code

### A.1 Definition of Coherence-Gradient Divergence (Definition 1)

**Paper location:** Definition of coherence-gradient chaos in the main text  
**Objects:** \( D_n(\psi_0, \psi_0') = \|\Psi_n - \Psi_n'\| \),  
coherence-gradient Lyapunov exponent \( \lambda_{\mathrm{CG}} \).

**Code:**

- `src/cg_model.py`
  - `build_three_node_propagator(eta, alpha, beta)`
  - `evolve_linear(T, psi0, n_steps)`
- `tests/test_divergence.py`
  - Constructs two nearby initial conditions `psi0` and `psi0_prime`.
  - Evolves both under the same `T` and measures `D_n`.
  - Performs a linear fit of `log D_n` vs `n` to estimate \( \lambda_{\mathrm{CG}} \).

**Parameters (default in tests):**

- `eta = 0.05`
- `alpha = 0.01`
- `beta = 0.02`
- `n_steps = 200`
- `epsilon = 1e-6` (initial separation)

---

### A.2 Operator-Norm / Spectral-Radius Instability Criterion (Proposition 1)

**Paper location:** Operator-norm criterion & model instability threshold  
**Objects:** \( \|\mathcal{T}_{\infty}^n\|_{\mathrm{op}} > C e^{\lambda n} \),  
spectral radius \( \rho(\mathcal{T}_{\infty}) > 1 \).

**Code:**

- `src/cg_model.py`
  - `build_three_node_propagator(eta, alpha, beta)`
  - `spectral_radius(T)`
- `tests/test_operator_norm.py`
  - Constructs `T` for given `eta, alpha, beta`.
  - Computes `rho = spectral_radius(T)`.
  - Verifies `rho > 1` for `eta > 0`.
  - Optionally scans powers `T**n` and checks the growth of the operator norm.

**Parameters (default in tests):**

- `eta = 0.05`
- `alpha = 0.01`
- `beta = 0.02`
- `n_max = 50` (for norm growth checks)

---

### A.3 Coarse-Grained Lyapunov Matching

**Paper location:** Relation
\( \lambda_{\mathrm{classical}} \approx \langle \lambda_{\mathrm{CG}} \rangle_{\mathrm{coarse}} \).

**Code:**

- `tests/test_lyapunov_coarse.py`
  - Uses the same `T` as in the three-node example.
  - Interprets a scalar observable from the coherence trajectory as a
    “coarse-grained” time series.
  - Computes:
    - A “microscopic” \(\lambda_{\mathrm{CG}}\) from pairwise divergence.
    - An effective “classical” Lyapunov exponent from the observable time series.
  - Compares the two exponents and checks they are of the same order.

**Parameters (default in tests):**

- Same as in A.1, plus:
  - Window sizes for linear fitting.
  - Choice of observable (e.g. norm or a specific component of `Psi_t`).

---

## B. How to Run All Tests

From the repository root:

```bash
pip install -r requirements.txt
pytest -q
