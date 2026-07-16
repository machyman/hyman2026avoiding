# src

Shared Python modules imported by the chapter scripts under
[`../notebooks/`](../notebooks/).

- **`sir_i_model.py`** — the SIR_I integrator and endemic-equilibrium helper used
  across chapters. Force of infection
  λ = β·c_S·c_I·S·I / (c_S S + c_I I + c_R R); R₀ = c_I·β / (γ_R + ν). Canonical
  baseline (N\* = 1): c_S = 10, c_I = 8, c_R = 10, β = 0.02, τ_R = 12, τ_m = 7300.
