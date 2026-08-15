"""Shared SIR_I integrator for the canonical-baseline figures.

Companion text: Avoiding Pitfalls in Epidemic Modeling (Hyman, Qu, Xue).
Used by:        ch6_phase_portrait.py, ch7_figures.py, ch10_figures.py.
Model:          force of infection lam = beta*c_S*c_I*S*I/(c_S S + c_I I + c_R R);
                R0 = c_I*beta/(gamma_R + nu_m).  Parameterized by tau_m so every
                figure regenerates consistently after a baseline change -- the
                safeguard against the missing-script problem.
Canonical baseline (N*=1): c_S=10, c_I=8, c_R=10, beta=0.02, tau_R=12, tau_m=7300.

Author:  James M. Hyman, Department of Mathematics, Tulane University
         mhyman@tulane.edu
Date:    2026-06-22   Version 1.1
"""
import numpy as np
from scipy.integrate import solve_ivp

# canonical baseline (N*=1)
BASE = dict(c_S=20.0, c_I=4.0, c_R=20.0, beta=0.040, tau_R=12.0, tau_m=7300.0)

def rhs(t, y, c_S, c_I, c_R, beta, gR, nu):
    """SIR_I RHS d/dt[S,I,R]; force lam = beta*c_S*c_I*S*I/(c_S S+c_I I+c_R R)."""
    S, I, R = y
    C = c_S*S + c_I*I + c_R*R
    lam = beta*c_S*c_I*S*I/C
    return [nu - lam - nu*S, lam - (gR+nu)*I, gR*I - nu*R]

def simulate(T, c_I=None, tau_m=None, y0=(0.999, 0.001, 0.0), n=20000, **kw):
    """Integrate to time T from y0; returns the dense solve_ivp solution object."""
    p = {**BASE, **kw}
    if c_I is not None: p['c_I'] = c_I
    if tau_m is not None: p['tau_m'] = tau_m
    gR, nu = 1/p['tau_R'], 1/p['tau_m']
    sol = solve_ivp(rhs, [0, T], list(y0),
                    args=(p['c_S'], p['c_I'], p['c_R'], p['beta'], gR, nu),
                    dense_output=True, rtol=1e-9, atol=1e-12, max_step=T/n)
    return sol

def endemic(c_I=None, tau_m=None, **kw):
    """Closed-form endemic equilibrium: dict(R0, S=1/R0, I, R); DFE if R0<=1."""
    p = {**BASE, **kw}
    if c_I is not None: p['c_I'] = c_I
    if tau_m is not None: p['tau_m'] = tau_m
    gR, nu = 1/p['tau_R'], 1/p['tau_m']; d = gR+nu; R0 = p['c_I']*p['beta']/d
    if R0 <= 1: return dict(R0=R0, S=1.0, I=0.0, R=0.0)
    S = 1/R0; I = (nu/d)*(1-1/R0)
    return dict(R0=R0, S=S, I=I, R=1-S-I)

if __name__ == "__main__":
    e = endemic(); print("baseline endemic:", {k: round(v,5) for k,v in e.items()})
