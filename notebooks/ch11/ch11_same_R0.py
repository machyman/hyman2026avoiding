"""Chapter 11 (printed Chapter 10) figure: the same R0, different dynamics.

Companion text: Foundations and Pitfalls in Epidemic Modeling, printed Chapter 10, Section "A Common Pattern"
(RG-12 finding 11.3; RG-198.1). Produces figs/ch11_same_R0.pdf and prints the numbers the chapter quotes.

(a) SIR, SEIR (mean latent period 5 days) and SIR with an Erlang-4 infectious period, each with the baseline R0. The
    transmission factor beta of each variant is rescaled so its R0 equals the SIR value exactly. Exposed individuals
    keep the susceptible contact rate c_S; every infectious sub-stage has c_I. Seed: infectious fraction 1e-3 in the
    first infectious stage. Shown: total infectious fraction over 400 days. Printed: peak day, peak height and the
    fraction ever infected by day 400.
(b) SIRS with mean immunity 1 year and 5 years against SIR (permanent immunity), same R0 and seed, over 10 years on a
    log scale, with each model's endemic prevalence (solved from the equilibrium equations) as a thin line.
Baseline from sir_i_model.BASE (c_S = 20, c_I = 4, c_R = 20, beta = 0.040, tau_R = 12 d, tau_m = 7300 d);
force from infection alpha = c_I beta P_S, P_S = c_S S / (sum of contact-weighted compartments).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-16   Version 1.0
Run under the figure pin (protocols/figure_pin_requirements.txt), SOURCE_DATE_EPOCH=1750000000, MPLBACKEND=pdf.
"""
import os, sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
from sir_i_model import BASE

plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 11, 'axes.linewidth': 0.8})
B = '#1f5fa8'; Rd = '#c0392b'; G = '#2e7d32'; Gr = '0.35'

cS, cI, cR, beta0 = BASE['c_S'], BASE['c_I'], BASE['c_R'], BASE['beta']
gR, nu = 1 / BASE['tau_R'], 1 / BASE['tau_m']
tauE, k = 5.0, 4
gE, kg = 1 / tauE, k * gR
R0 = cI * beta0 / (gR + nu)
beta_seir = R0 * (gR + nu) * (gE + nu) / (cI * gE)                 # R0 = cI b/(gR+nu) * gE/(gE+nu)
beta_erl = R0 / (cI * (1 - (kg / (kg + nu)) ** k) / nu)            # R0 = cI b * expected infectious time
I0 = 1e-3


def run_sir(T, om=0.0, beta=beta0, n=4001):
    def f(t, y):
        S, I, R, J = y
        a = cI * beta * cS * S / (cS * S + cI * I + cR * R)
        return [nu - a * I + om * R - nu * S, a * I - (gR + nu) * I, gR * I - (om + nu) * R, a * I]
    t = np.linspace(0, T, n)
    s = solve_ivp(f, [0, T], [1 - I0, I0, 0, 0], t_eval=t, rtol=1e-10, atol=1e-14, method='LSODA')
    return t, s.y[1], s.y[3]


def run_seir(T, n=4001):
    def f(t, y):
        S, E, I, R, J = y
        a = cI * beta_seir * cS * S / (cS * S + cS * E + cI * I + cR * R)
        return [nu - a * I - nu * S, a * I - (gE + nu) * E, gE * E - (gR + nu) * I, gR * I - nu * R, a * I]
    t = np.linspace(0, T, n)
    s = solve_ivp(f, [0, T], [1 - I0, 0, I0, 0, 0], t_eval=t, rtol=1e-10, atol=1e-14, method='LSODA')
    return t, s.y[2], s.y[4]


def run_erlang(T, n=4001):
    def f(t, y):
        S = y[0]; I = y[1:1 + k]; R = y[1 + k]; It = I.sum()
        a = cI * beta_erl * cS * S / (cS * S + cI * It + cR * R)
        dI = np.empty(k); dI[0] = a * It - (kg + nu) * I[0]
        for j in range(1, k):
            dI[j] = kg * I[j - 1] - (kg + nu) * I[j]
        return np.concatenate(([nu - a * It - nu * S], dI, [kg * I[-1] - nu * R, a * It]))
    t = np.linspace(0, T, n)
    y0 = np.concatenate(([1 - I0], [I0] + [0] * (k - 1), [0, 0]))
    s = solve_ivp(f, [0, T], y0, t_eval=t, rtol=1e-10, atol=1e-14, method='LSODA')
    return t, s.y[1:1 + k].sum(0), s.y[-1]


def endemic(om):
    def g(I):
        R = gR * I / (om + nu); S = 1 - I - R
        return cI * beta0 * cS * S / (cS * S + cI * I + cR * R) - (gR + nu)
    return brentq(g, 1e-12, 0.5)


fig, (a1, a2) = plt.subplots(1, 2, figsize=(10.0, 4.2))
T1 = 400.0
print(f'R0 = {R0:.4f} for all three; beta: SIR {beta0:.5f}, SEIR {beta_seir:.5f}, Erlang-{k} {beta_erl:.5f}')
for lab, fn, col, ls in (('SIR', run_sir, B, '-'), ('SEIR, latent period 5 d', run_seir, Rd, '--'),
                         (f'SIR, Erlang-{k} infectious period', run_erlang, G, '-.')):
    t, I, J = fn(T1)
    i = np.argmax(I)
    a1.plot(t, I, color=col, ls=ls, lw=1.8, label=lab)
    print(f'  {lab:34s} peak day {t[i]:6.1f}, peak {I[i]:.4f}, ever infected by day {T1:.0f}: {J[-1] + I0:.4f}')
a1.set_xlim(0, T1); a1.set_ylim(0, None)
a1.set_xlabel('Days'); a1.set_ylabel(r'infectious fraction $i(t)$')
a1.set_title(r'(a) three models, the same $\mathcal{R}_0 = %.2f$' % R0, fontsize=10)
a1.legend(frameon=False, fontsize=8.5)

T2 = 3650.0
for lab, om, col, ls in (('SIR (permanent immunity)', 0.0, B, '-'), ('SIRS, immunity 5 years', 1 / 1825, G, '-.'),
                         ('SIRS, immunity 1 year', 1 / 365, Rd, '--')):
    t, I, J = run_sir(T2, om=om, n=8001)
    Ie = endemic(om)
    a2.semilogy(t / 365, I, color=col, ls=ls, lw=1.6, label=lab)
    a2.axhline(Ie, color=col, lw=0.6, ls=':')
    print(f'  {lab:34s} endemic prevalence {Ie:.5f}')
a2.set_xlim(0, T2 / 365); a2.set_ylim(1e-6, 0.3)
a2.set_xlabel('Years'); a2.set_ylabel(r'infectious fraction $i(t)$ (log)')
a2.set_title(r'(b) the same threshold, different endemic levels', fontsize=10)
a2.legend(frameon=False, fontsize=8.5, loc='lower right')
fig.tight_layout()
fig.savefig(os.path.join(here, '..', 'figs', 'ch11_same_R0.pdf'))
