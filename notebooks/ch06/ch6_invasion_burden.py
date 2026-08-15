# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- illustrative R0 = 3.0 regime.
"""Fig 6.3  Invasion-vs-burden parameter partition (equal-contact case).

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 6 (Figure 6.3).
At R0 = 3 (illustrative supercritical value), each parameter is placed by its R0-sensitivity
(invasion-facing) and its I*-sensitivity (burden-facing): c_I, beta are purely
invasion-facing; tau_m is burden-facing; c_S, c_R are passive.  tau_m-parameterized
so a baseline change is one line.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-06-30   Version 1.2
"""
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','font.size':12,'mathtext.fontset':'cm','axes.linewidth':0.8})
# --- supercritical setting (equal-contact c=8): tau_R, tau_m fixed; beta calibrated to R0 ---
c, tauR, tauM = 8.0, 12.0, 7300.0
gR, nu = 1/tauR, 1/tauM ; d = gR+nu
R0 = 3.0                         # illustrative value (COVID/SARS/HIV range); partition sharpens as R0 grows
beta = R0*d/c                    # per-contact transmission probability calibrated to R0 (time scales fixed)
inv = {'c_I':1.0, r'\beta':1.0, r'\tau_R':gR/d,           r'\tau_m':nu/d,                 'c_S':0.0, 'c_R':0.0}
bur = {'c_I':1/(R0-1), r'\beta':1/(R0-1), r'\tau_R':gR/d*R0/(R0-1),
       r'\tau_m':abs(-1+nu/d*R0/(R0-1)), 'c_S':0.0, 'c_R':0.0}
print(f'R0={R0:.4f}  c_I/beta burden={bur["c_I"]:.3f}  tau_R=({inv[r"\tau_R"]:.3f},{bur[r"\tau_R"]:.3f})  tau_m=({inv[r"\tau_m"]:.4f},{bur[r"\tau_m"]:.3f})')
fig, ax = plt.subplots(figsize=(6.2,4.6))
# coincident points grouped with combined labels
groups = [(['c_I',r'\beta'], '#c0392b', r'$c_I,\ \beta$',  (10,-4)),   # invasion-facing
          ([r'\tau_R'],      '#6c3483', r'$\tau_R$',        (10,-2)),   # mixed
          ([r'\tau_m'],      '#1f5fa8', r'$\tau_m$',        (8,4)),     # burden-facing
          (['c_S','c_R'],    '#7f8c8d', r'$c_S,\ c_R$',     (10,2))]    # passive
for keys,col,lab,off in groups:
    k = keys[0]
    ax.scatter(inv[k], bur[k], s=70, color=col, zorder=5, edgecolor='white', linewidth=0.8)
    ax.annotate(lab, xy=(inv[k],bur[k]), xytext=off, textcoords='offset points', fontsize=12, color=col)
ax.axhline(0, color='0.85', lw=0.8, zorder=0); ax.axvline(0, color='0.85', lw=0.8, zorder=0)
ax.set_xlabel(r'Invasion sensitivity $\,|S^{\mathcal{R}_0}_p|$')
ax.set_ylabel(r'Burden sensitivity $\,|S^{I^*}_p|$')
ax.set_xlim(-0.06,1.15); ax.set_ylim(-0.10,1.75)
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch6_invasion_burden.pdf'); print('wrote figs/ch6_invasion_burden.pdf')
