#!/usr/bin/env python3
"""ch10_index_divergence.py -- Ch 10 figure: near-threshold divergence of the
closed-form I* sensitivity indices.

Closed forms (Ch 10, equal-contact-rate case, N* constant by construction):
    S^{I*}_{c_I} = S^{I*}_{beta} = 1/(R0 - 1)
    S^{I*}_{tau_R} = (gR/(gR+nu)) * R0/(R0 - 1)
    S^{I*}_{tau_m} = -(1 - (nu/(gR+nu)) * R0/(R0 - 1))
R0 is swept via the product c_I*beta with the rates gR = 1/tau_R and
nu = 1/tau_m held fixed at the centralized baseline (sir_i_model.BASE), so the
tau_R and tau_m prefactors are the baseline values throughout the sweep.
Deterministic closed-form evaluation; no RNG, no seed.

Output: figs/ch10_index_divergence.pdf  (run from the manuscript root)
"""
import pathlib
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sir_i_model import BASE  # baseline centralized (Phase 2, S17)

plt.rcParams.update({'text.usetex':True,'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})

B, Gn, Gy = '#1f5fa8', '#2e7d32', '#888888'   # house palette (ch10_figures.py)

gR, nu = 1.0 / BASE['tau_R'], 1.0 / BASE['tau_m']
R0_base = BASE['c_I'] * BASE['beta'] / (gR + nu)
f_tauR = gR / (gR + nu)          # ~0.998 at baseline
f_taum = nu / (gR + nu)          # ~0.0016 at baseline

R0 = np.linspace(1.05, 5.0, 600)
S_cI = 1.0 / (R0 - 1.0)
S_tR = f_tauR * R0 / (R0 - 1.0)
S_tm = np.abs(1.0 - f_taum * R0 / (R0 - 1.0))

fig, a = plt.subplots(figsize=(5.4, 3.5))
a.plot(R0, S_cI, color=B, lw=1.6,
       label=r'$S^{I^*}_{c_I}=S^{I^*}_{\beta}=1/(\mathcal{R}_0-1)$')
a.plot(R0, S_tR, color=Gn, lw=1.6, label=r'$S^{I^*}_{\tau_R}$')
a.plot(R0, S_tm, color=Gy, lw=1.4, ls='-.', label=r'$|S^{I^*}_{\tau_m}|$')

a.axvline(R0_base, color='k', lw=0.8, ls='--')
a.annotate(r'baseline $\mathcal{R}_0\approx %.2f$' % R0_base,
           xy=(R0_base + 0.06, 6.55), fontsize=9)
for y in (1.0 / (R0_base - 1.0), f_tauR * R0_base / (R0_base - 1.0), 1.0):
    a.plot([R0_base], [y], 'o', ms=3.5, color='k', zorder=5)

a.set_xlim(1.0, 5.0)
a.set_ylim(0, 8)
a.set_xlabel(r'$\mathcal{R}_0$')
a.set_ylabel(r'sensitivity index magnitude $|S^{I^*}_p|$')
a.legend(frameon=False, fontsize=9, loc='upper right')
fig.tight_layout()
fig.savefig('figs/ch10_index_divergence.pdf')
print('wrote figs/ch10_index_divergence.pdf')
