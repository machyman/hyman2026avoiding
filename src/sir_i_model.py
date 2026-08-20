"""Shared SIR_I integrator for the canonical-baseline figures.

Companion text: Avoiding Pitfalls in Epidemic Modeling (Hyman, Qu, Xue).
Used by:        ch6_phase_portrait.py, ch7_figures.py, ch10_figures.py.
Model:          force of infection lam = beta*c_S*c_I*S*I/(c_S S + c_I I + c_R R);
                R0 = c_I*beta/(gamma_R + nu_m).  Parameterized by tau_m so every
                figure regenerates consistently after a baseline change -- the
                safeguard against the missing-script problem.
Canonical baseline (N*=1): c_S=20, c_I=4, c_R=20, beta=0.040, tau_R=12, tau_m=7300.
Two closed forms are provided and are NOT interchangeable: endemic_general() solves
rhs() as shipped; endemic_equal_contact() is valid only for c_S = c_I = c_R.  Both
are asserted against a long integration by _self_test().  See DECISIONS.md F-27.2.

Author:  James M. Hyman, Department of Mathematics, Tulane University
         mhyman@tulane.edu
Date:    2026-08-16   Version 1.2
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

def endemic_equal_contact(c_I=None, tau_m=None, **kw):
    """Endemic equilibrium of the EQUAL-CONTACT model (c_S = c_I = c_R).

    Returns dict(R0, S=1/R0, I, R); the DFE if R0 <= 1.

    Valid ONLY when the caller integrates rhs() with c_S = c_I = c_R.  It is NOT
    the equilibrium of the general model with distinct contact rates -- for that,
    use endemic_general().  At the canonical baseline (c_S/c_I = 5) the two differ
    in the 4th significant figure of S*, which is enough to change a printed
    3-decimal figure annotation.  See DECISIONS.md F-27.2.
    """
    p = {**BASE, **kw}
    if c_I is not None: p['c_I'] = c_I
    if tau_m is not None: p['tau_m'] = tau_m
    gR, nu = 1/p['tau_R'], 1/p['tau_m']; d = gR+nu; R0 = p['c_I']*p['beta']/d
    if R0 <= 1: return dict(R0=R0, S=1.0, I=0.0, R=0.0)
    S = 1/R0; I = (nu/d)*(1-1/R0)
    return dict(R0=R0, S=S, I=I, R=1-S-I)


def endemic_general(c_I=None, tau_m=None, **kw):
    """Endemic equilibrium of the GENERAL model with distinct c_S, c_I, c_R.

    Returns dict(R0, S, I, R); the DFE if R0 <= 1.  This is the equilibrium of
    rhs() as shipped, and it is what the book's closed form (eq:I-star) states:

        I* = c_S nu (R0-1) / [c_S (gR+nu)(R0-1) + c_I nu + c_R gR]
        S* = (c_I nu + c_R gR) / [ same denominator ]
        R* = (gR/nu) I*                                     (N* = 1)

    It reduces to endemic_equal_contact() when c_S = c_I = c_R.  Use this whenever
    the caller integrates rhs() with the BASE contact rates.
    """
    p = {**BASE, **kw}
    if c_I is not None: p['c_I'] = c_I
    if tau_m is not None: p['tau_m'] = tau_m
    gR, nu = 1/p['tau_R'], 1/p['tau_m']; d = gR+nu
    cS, cI, cR = p['c_S'], p['c_I'], p['c_R']
    R0 = cI*p['beta']/d
    if R0 <= 1: return dict(R0=R0, S=1.0, I=0.0, R=0.0)
    den = cS*(R0-1)*d + cI*nu + cR*gR
    I = cS*nu*(R0-1)/den
    S = (cI*nu + cR*gR)/den
    return dict(R0=R0, S=S, I=I, R=(gR/nu)*I)

def _self_test(T=4.0e6, tol=1e-6):
    """Assert each closed form against a long integration of rhs().

    A closed form that is never checked against the model it claims to solve is
    indistinguishable from a correct one.  F-27.2 arose exactly that way, so this
    gate is permanent and runs on `python3 sir_i_model.py`.
    """
    gR, nu = 1/BASE['tau_R'], 1/BASE['tau_m']
    checks = [
        ("general",       endemic_general(),
         (BASE['c_S'], BASE['c_I'], BASE['c_R'])),
        ("equal-contact", endemic_equal_contact(),
         (BASE['c_I'], BASE['c_I'], BASE['c_I'])),
    ]
    for name, e, (cS, cI, cR) in checks:
        sol = solve_ivp(rhs, [0, T], [e['S']*1.05, e['I']*1.05, e['R']*0.95],
                        args=(cS, cI, cR, BASE['beta'], gR, nu),
                        rtol=1e-11, atol=1e-14, method='Radau')
        S, I, R = sol.y[:, -1]
        for lbl, closed, num in (('S', e['S'], S), ('I', e['I'], I), ('R', e['R'], R)):
            rel = abs(closed-num)/abs(num)
            assert rel < tol, f"{name} {lbl}*: closed {closed!r} vs numerical {num!r} (rel {rel:.2e})"
        print(f"  {name:<14} S*={e['S']:.9f} I*={e['I']:.9f} R*={e['R']:.9f}  OK vs integration")
    print("  self-test PASS")


if __name__ == "__main__":
    print("baseline endemic equilibria (N*=1):")
    _self_test()
