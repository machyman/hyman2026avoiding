# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- parameter sweep over its own grid, not the BASE point.
"""Fig 6.1  Transcritical bifurcation diagram, scaled (residence-time-independent).

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 6 (Figure 6.1).
y-axis = 1 - 1/R0  (= 1 - S*/N* in the equal-contact case); actual prevalence
I*/N* = (1 - 1/R0) * nu_m/(gamma_R + nu_m), so the scaled form is tau_m-independent.
The DFE is stable for R0 < 1 and exchanges stability with the endemic branch at R0 = 1.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-06-30   Version 1.2
"""
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({'text.usetex':True,'font.family':'serif','font.size':12,'mathtext.fontset':'cm','axes.linewidth':0.8})
fig, ax = plt.subplots(figsize=(6.2,4.0))
ax.plot([0,1],[0,0], color='#1f5fa8', lw=2.6, label='DFE (stable)')
ax.plot([1,3],[0,0], color='#1f5fa8', lw=2.6, ls=(0,(5,3)), label='DFE (unstable)')
R = np.linspace(1,3,400)
ax.plot(R, 1-1/R, color='#c0392b', lw=2.6, marker='o', markevery=45, ms=5, mfc='white', mec='#c0392b', label='EE (stable)')
ax.plot(1,0,'o', color='black', ms=7, zorder=6)
ax.annotate('transcritical\nthreshold', xy=(1,0), xytext=(1.42,0.07), fontsize=10,
            arrowprops=dict(arrowstyle='->', lw=1.0, color='black'))
ax.set_xlabel(r'Basic reproductive number $\mathcal{R}_0$')
ax.set_ylabel(r'$1 - 1/\mathcal{R}_0 = 1 - S^{*}/N^{*}$')
ax.set_xlim(0,3); ax.set_ylim(-0.04,0.72)
ax.legend(loc='upper left', frameon=False, fontsize=10.5)
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch6_bifurcation.pdf'); print('wrote figs/ch6_bifurcation.pdf')
