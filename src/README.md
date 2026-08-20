# src

Shared Python modules imported by the chapter scripts under
[`../notebooks/`](../notebooks/).

- **`sir_i_model.py`** — the SIR_I integrator and endemic-equilibrium helper used
  across chapters. Force of infection
  λ = β·c_S·c_I·S·I / (c_S S + c_I I + c_R R); R₀ = c_I·β / (γ_R + ν). Canonical
  baseline (N\* = 1): c_S = 20, c_I = 4, c_R = 20, β = 0.040, τ_R = 12, τ_m = 7300.

  Two endemic closed forms are provided and are **not** interchangeable.
  `endemic_general()` solves the model as shipped and is the one to use at the
  canonical baseline, where c_S/c_I = 5. `endemic_equal_contact()` is valid only
  when c_S = c_I = c_R; applying it at the canonical baseline shifts S\* in the
  fourth significant figure. Both are asserted against a long integration by the
  module's `_self_test()`.
