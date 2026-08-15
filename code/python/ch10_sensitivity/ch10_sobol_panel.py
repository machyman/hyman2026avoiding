#!/usr/bin/env python3
"""ch10_sobol_panel.py -- Ch 10 figure: compact Sobol panel (S_i vs S_Ti) for the
closed-form QOIs, hand-rolled Saltelli Monte Carlo (no new dependency).

QOIs (closed forms; equal-contact-rate case for I*, N* constant by construction):
    R0(p)    = c_I * beta / (gR + nu),          gR = 1/tau_R, nu = 1/tau_m
    Istar(p) = max(0, (nu/(gR+nu)) * (1 - 1/R0))   # long-run prevalence; 0 when
                                                   # the endemic equilibrium does
                                                   # not exist (R0 <= 1)
c_S and c_R enter neither closed form, so their indices are structural zeros --
the variance-based analog of the dummy-parameter check of the PRCC section.

Design: 6 parameters, independent uniform on [p/2, 2p] around the centralized
baseline (sir_i_model.BASE), matching the LHS-PRCC design of the same section.
Estimators on the Saltelli A/B/A_B^i matrices (n_base_samples*(k+2) evaluations
per QOI): first-order S_i per Saltelli et al. (2010), total-order S_Ti per
Jansen (1999). Seeded, deterministic: fixed rng_seed, fixed n_base_samples.

Output: figs/ch10_sobol_panel.pdf  (run from the manuscript root)
Grayscale rendering (print-cost ruling, 2026-08-15): S_i dark gray, S_Ti light
gray with dark edge; distinguishable in pure black-and-white printing.
Also prints the index table (3 decimals) to stdout for the prose values.
"""
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sir_i_model import BASE  # baseline centralized (Phase 2, S17)

plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})

B, Gn, Gy = '#1f5fa8', '#2e7d32', '#888888'   # house palette (ch10_figures.py)

# ---- design constants (dimensionless) --------------------------------------
rng_seed = 2026          # integer seed; fixes the entire sample
n_base_samples = 65536   # Saltelli base-sample count N (2**16)
range_factor = 2.0       # each parameter uniform on [p/range_factor, range_factor*p]

param_names = ['c_S', 'c_I', 'c_R', 'beta', 'tau_R', 'tau_m']
param_tex = [r'$c_S$', r'$c_I$', r'$c_R$', r'$\beta$', r'$\tau_R$', r'$\tau_m$']
k_params = len(param_names)

lo = np.array([BASE[p] / range_factor for p in param_names])
hi = np.array([BASE[p] * range_factor for p in param_names])


def qoi_R0(P):
    """Basic reproduction number; P has columns in param_names order."""
    gR, nu = 1.0 / P[:, 4], 1.0 / P[:, 5]
    return P[:, 1] * P[:, 3] / (gR + nu)


def qoi_Istar(P):
    """Equal-contact endemic prevalence I*/N; 0 where R0 <= 1."""
    gR, nu = 1.0 / P[:, 4], 1.0 / P[:, 5]
    R0 = P[:, 1] * P[:, 3] / (gR + nu)
    return np.where(R0 > 1.0, (nu / (gR + nu)) * (1.0 - 1.0 / R0), 0.0)


def sobol_indices(qoi):
    """Saltelli MC: returns (S_i, S_Ti) arrays of length k_params."""
    rng = np.random.default_rng(rng_seed)
    A = lo + (hi - lo) * rng.random((n_base_samples, k_params))
    Bm = lo + (hi - lo) * rng.random((n_base_samples, k_params))
    fA, fB = qoi(A), qoi(Bm)
    var_total = np.var(np.concatenate([fA, fB]), ddof=1)
    S_first = np.empty(k_params)
    S_total = np.empty(k_params)
    for i in range(k_params):
        ABi = A.copy()
        ABi[:, i] = Bm[:, i]
        fABi = qoi(ABi)
        S_first[i] = np.mean(fB * (fABi - fA)) / var_total          # Saltelli 2010
        S_total[i] = 0.5 * np.mean((fA - fABi) ** 2) / var_total    # Jansen 1999
    return S_first, S_total


results = {}
for label, qoi in [('R0', qoi_R0), ('Istar', qoi_Istar)]:
    S_first, S_total = sobol_indices(qoi)
    results[label] = (S_first, S_total)
    print(f"QOI {label}:  (n_base_samples={n_base_samples}, rng_seed={rng_seed})")
    for name, s1, st in zip(param_names, S_first, S_total):
        print(f"  {name:6s}  S_i = {s1:6.3f}   S_Ti = {st:6.3f}")
    print(f"  sums    S_i = {S_first.sum():6.3f}   S_Ti = {S_total.sum():6.3f}")

# ---- figure ----------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.0), sharey=False)
titles = [r'$\mathcal{R}_0$', r'$I^*$ (equal-contact)']
x = np.arange(k_params)
w = 0.38
for ax, label, title in zip(axes, ['R0', 'Istar'], titles):
    S_first, S_total = results[label]
    ax.bar(x - w / 2, np.maximum(S_first, 0.0), w, color='0.25',
           label=r'$S_i$')
    ax.bar(x + w / 2, np.maximum(S_total, 0.0), w, color='0.72',
           edgecolor='0.25', linewidth=0.6, label=r'$S_{T_i}$')
    ax.set_xticks(x)
    ax.set_xticklabels(param_tex)
    ax.set_title(title, fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.yaxis.grid(True, lw=0.4, alpha=0.5)
    ax.set_axisbelow(True)
axes[0].set_ylabel('variance fraction')
axes[0].legend(frameon=False, loc='upper left')
fig.tight_layout()

out = pathlib.Path('figs/ch10_sobol_panel.pdf')
fig.savefig(out)
print(f"wrote {out}")
