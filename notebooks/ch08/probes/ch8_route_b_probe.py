# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- Route B synthetic regime (R0 = 2.0).
"""
ch8_route_b_probe.py -- numerical probe for the Chapter 8 central claim (Route B).

Question: does an incidence-only fit of R0 depend on the modeler's ASSUMED
susceptible population N^c, and in which regime?

Findings (2026-07-22, seed-free deterministic):
  * EARLY-ONLY data (pre-peak): R0_hat is essentially INDEPENDENT of assumed N^c
    (2.079 -> 1.982 across a 150x range; <4% variation). A free seed I0 absorbs
    the amplitude and the growth rate fixes R0. The book's current early-outbreak
    framing of the claim is therefore backwards.
  * THROUGH-PEAK data: strong dependence (3.580 -> 1.018 across the same range).
    Mechanism is susceptible depletion: assuming N^c too large under-reads
    depletion and pulls R0_hat toward 1.
  * Magnitude: factor-3 error in N^c gives a factor-1.5 error in R0_hat (not
    factor-3); factor-30 gives factor-1.96 (not factor-30). The bias SATURATES,
    because R0_hat cannot fall below 1 and still produce an epidemic.
  * alpha-hat = J_obs/I_obs contains no N^c, so it is exactly invariant by
    construction, and correctly tracks R_e(t) = R0*s(t) as the epidemic proceeds.

Basis for the replacement of fig:central-comparison.
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

# ---- truth ----
N_true = 100_000.0
R0_true, tau_R = 2.0, 7.0
gamma = 1/tau_R
beta_true = R0_true*gamma
I0_true = 10.0

def sim(beta, I0, N, T, n):
    """frequency-dependent SIR in counts; returns daily incidence counts."""
    def rhs(t, y):
        S, I = y
        inc = beta*S*I/N
        return [-inc, inc - gamma*I]
    t_eval = np.linspace(0, T, n+1)
    sol = solve_ivp(rhs, [0,T], [N-I0, I0], t_eval=t_eval, rtol=1e-9, atol=1e-9, dense_output=True)
    S, I = sol.y
    # daily incidence = integral of beta S I / N over each day
    inc = np.array([np.trapezoid(beta*sol.sol(np.linspace(t_eval[k],t_eval[k+1],21))[0]
                                 *sol.sol(np.linspace(t_eval[k],t_eval[k+1],21))[1]/N,
                                 np.linspace(t_eval[k],t_eval[k+1],21)) for k in range(n)])
    return inc, S, I

# ---- generate truth data ----
T_full, n_full = 120, 120
inc_true, S_true, I_true = sim(beta_true, I0_true, N_true, T_full, n_full)
peak_day = int(np.argmax(inc_true))
print(f"truth: R0={R0_true}, N={N_true:,.0f}, peak day {peak_day}, peak inc {inc_true[peak_day]:,.0f}")
print(f"       cumulative by peak = {inc_true[:peak_day].sum():,.0f} "
      f"({inc_true[:peak_day].sum()/N_true:.3f} of N)")

def fit_R0(data, N_assumed, T, n, free_I0=True):
    """incidence-only least squares for (R0, I0) under an ASSUMED N."""
    def resid(p):
        R0 = np.exp(p[0]); I0 = np.exp(p[1]) if free_I0 else I0_true
        m,_,_ = sim(R0*gamma, I0, N_assumed, T, n)
        return m - data
    p0 = [np.log(1.5), np.log(20.0)]
    out = least_squares(resid, p0, method='lm', xtol=1e-12, ftol=1e-12)
    return np.exp(out.x[0])

ratios = np.array([1/5, 1/3, 1/2, 1, 2, 3, 5, 10, 30])
for label, T, n in [("EARLY ONLY (through day 30, pre-peak)", 30, 30),
                    ("THROUGH PEAK (day 120, full epidemic)", T_full, n_full)]:
    d = inc_true[:n]
    print(f"\n=== {label} ===")
    print("  N_assumed/N_true    R0_hat     rel.error")
    for r in ratios:
        Rh = fit_R0(d, N_true*r, T, n)
        print(f"    {r:>8.3g}          {Rh:6.3f}     {(Rh/R0_true-1)*100:+7.1f}%")
