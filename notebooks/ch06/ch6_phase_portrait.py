"""Fig 6.2  Phase portrait of the equal-contact-rate SIR_I model.

Companion text: Avoiding Pitfalls in Epidemic Modeling (Hyman, Qu, Xue), Chapter 6.
Reproduces:     Figure 6.2 -- the (S, I) phase portrait in the supercritical regime.
Model:          equal-contact case c_S = c_I = c_R = c (matches Figs 6.1, 6.3),
                for which lambda = beta*c*S*I/(S+I+R) and the endemic susceptible
                fraction is exactly S* = 1/R0, with R0 = c*beta/(gamma_R + nu_m).
                At the canonical baseline R0 = 1.92.  Five trajectories from
                distinct initial conditions spiral into the endemic equilibrium
                (red star) through the damped oscillations of Section 6.

This script was reconstructed (2026-06-22) to close a missing-script gap: the
figure was present in the manuscript but had no generator in figs_src/, and its
caption R0 value (1.86) was inconsistent with the canonical baseline (1.92).
It reuses the shared integrator in sir_i_model.py so the figure regenerates
consistently after any baseline change.

Author:  James M. Hyman, Department of Mathematics, Tulane University
         mhyman@tulane.edu
Date:    2026-06-30   Version 1.2

v1.2 (2026-06-30): added the disease-free equilibrium marker (black dot) at
     (N*, 0) so the figure matches its caption, which identifies the DFE as a
     saddle; widened the right x-limit to frame it.  v1.1 added trajectory
     direction arrows.
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import sys; sys.path.insert(0, 'figs_src')   # run from the repo root, as ch7/ch10 do
import sir_i_model as M

plt.rcParams.update({'font.family': 'serif', 'font.size': 12,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})

# ── Canonical baseline, equal-contact case (c_S = c_I = c_R = c) ───────────────
c    = M.BASE['c_I']           # single contact rate shared by all compartments (value from BASE)
beta = M.BASE['beta']          # per-contact transmission probability (value from BASE)
gR   = 1.0 / M.BASE['tau_R']   # recovery rate 1/12 day^-1  (tau_R = 12 d)
nu   = 1.0 / M.BASE['tau_m']   # demographic turnover 1/7300 day^-1 (tau_m ~ 20 yr)
R0   = c * beta / (gR + nu)    # = 1.917 -> 1.92  (depends only on c_I = c)

eq = M.endemic()               # closed form; S* = 1/R0 is exact in the equal-contact case
Sstar, Istar = eq['S'], eq['I']

# ── Five initial conditions spanning the (S, I) plane ─────────────────────────
ICs = [(0.99, 0.010, 0.000),
       (0.85, 0.001, 0.149),
       (0.60, 0.060, 0.340),
       (0.40, 0.090, 0.510),
       (0.97, 0.020, 0.010)]
cols = ['#1f5fa8', '#c0392b', '#117a3f', '#8e44ad', '#d68910']

fig, ax = plt.subplots(figsize=(6.2, 4.6))
T  = 40000.0                   # ~110 yr: trajectories converge onto the endemic equilibrium
tt = np.linspace(0, T, 60000)
traj = []
for ic, col in zip(ICs, cols):
    sol = solve_ivp(M.rhs, [0, T], ic, args=(c, c, c, beta, gR, nu),
                    dense_output=True, rtol=1e-10, atol=1e-13, max_step=5.0)
    Y = sol.sol(tt)
    traj.append((Y, col, ic))
    ax.plot(Y[0], Y[1], color=col, lw=1.3, alpha=0.9)
    ax.plot(ic[0], ic[1], 'o', color=col, ms=4)                     # starting point
    seg = np.hypot(np.diff(Y[0]), np.diff(Y[1]))
    s   = np.concatenate([[0.0], np.cumsum(seg)])
    i0  = min(int(np.searchsorted(s, 0.15 * s[-1])), len(tt) - 8)
    ax.annotate('', xy=(Y[0][i0 + 6], Y[1][i0 + 6]), xytext=(Y[0][i0], Y[1][i0]),
                arrowprops=dict(arrowstyle='-|>', color=col, lw=1.3, mutation_scale=15))

ax.plot(Sstar, Istar, '*', color='#c0392b', ms=17, mec='k', mew=0.6, zorder=6,
        label=r'endemic equilibrium $(S^*,I^*)$')
ax.plot(1.0, 0.0, 'o', color='k', ms=7, zorder=7,
        label=r'disease-free equilibrium $(N^{\mathrm{c}},0)$')

allS = np.concatenate([Y[0] for Y, _, _ in traj])
allI = np.concatenate([Y[1] for Y, _, _ in traj])
ax.set_xlim(max(allS.min() - 0.03, 0.0), min(allS.max() + 0.05, 1.05))
ax.set_ylim(-0.006, allI.max() * 1.10)

ax.set_xlabel(r'susceptible fraction $S$')
ax.set_ylabel(r'infectious fraction $I$')
ax.set_title(r'$SIR_I$ phase portrait (equal contact, $\mathcal{R}_0 = %.2f$)' % R0)
ax.legend(loc='upper right', frameon=False, fontsize=10)
fig.tight_layout()
fig.savefig('figs/ch6_phase_portrait.pdf', dpi=150, bbox_inches='tight')
plt.close(fig)
maxend = max(np.hypot(Y[0][-1] - Sstar, Y[1][-1] - Istar) for Y, _, _ in traj)
print(f'R0={R0:.4f}  endemic (S*,I*)=({Sstar:.4f},{Istar:.5f})  '
      f'max end-distance to eq={maxend:.2e}  wrote figs/ch6_phase_portrait.pdf')
