# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- illustrative R0 = 3.0 regime.
"""Fig 5.5  Invasion-vs-burden parameter partition (equal-contact point, three classes).

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 5 (Figure 5.5,
fig:invasion-burden-partition, in Chapter_06_SIR_I_Analysis).
At R0 = 3 with equal contact rates c = 8 (illustrative supercritical value), each
parameter is placed by its R0-sensitivity and its I*-sensitivity: c_I, beta are
invasion-facing; tau_R is mixed; tau_m is burden-facing; c_S, c_R are burden-facing
through the endemic level.  The R0 index of c_S and c_R is 0 exactly.  Their I*
indices come from the general endemic prevalence (eq:I-star, via
sir_i_model.endemic_general, all six parameters passed explicitly, so BASE is not
used), evaluated at this point by central differences in log p: +1/R0 and
-gamma_R/((gamma_R+nu_m) R0), about +0.33 and -0.33.  The other four points are the
closed forms of Theorem thm:invasion-burden.  tau_m-parameterized so a baseline
change is one line.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-29   Version 1.3 (Session 277, A1: c_S, c_R from the general model)
"""
import numpy as np, matplotlib.pyplot as plt
import sir_i_model as M
plt.rcParams.update({'text.usetex':True,'font.family':'serif','font.size':12,'mathtext.fontset':'cm','axes.linewidth':0.8})
# --- supercritical setting (equal-contact c=8): tau_R, tau_m fixed; beta calibrated to R0 ---
c, tauR, tauM = 8.0, 12.0, 7300.0
gR, nu = 1/tauR, 1/tauM ; d = gR+nu
R0 = 3.0                         # illustrative value (COVID/SARS/HIV range); partition sharpens as R0 grows
beta = R0*d/c                    # per-contact transmission probability calibrated to R0 (time scales fixed)
# --- c_S, c_R: endemic indices of the GENERAL model (eq:I-star) at the equal-contact point ---
P = dict(c_S=c, c_I=c, c_R=c, beta=beta, tau_R=tauR, tau_m=tauM)
def ups_I(key, h=1e-6):
    """Upsilon(I*, key) = d log I* / d log key for the general model, central difference."""
    up, dn = dict(P), dict(P); up[key] *= np.exp(h); dn[key] *= np.exp(-h)
    return (np.log(M.endemic_general(**up)['I']) - np.log(M.endemic_general(**dn)['I']))/(2*h)
U_cS, U_cR = ups_I('c_S'), ups_I('c_R')
assert abs(U_cS - 1/R0) < 1e-6 and abs(U_cR + gR/(d*R0)) < 1e-6, (U_cS, U_cR)
inv = {'c_I':1.0, r'\beta':1.0, r'\tau_R':gR/d,           r'\tau_m':nu/d,                 'c_S':0.0, 'c_R':0.0}
bur = {'c_I':1/(R0-1), r'\beta':1/(R0-1), r'\tau_R':gR/d*R0/(R0-1),
       r'\tau_m':abs(-1+nu/d*R0/(R0-1)), 'c_S':abs(U_cS), 'c_R':abs(U_cR)}
print(f'R0={R0:.4f}  c_I/beta burden={bur["c_I"]:.3f}  tau_R=({inv[r"\tau_R"]:.3f},{bur[r"\tau_R"]:.3f})  tau_m=({inv[r"\tau_m"]:.4f},{bur[r"\tau_m"]:.3f})')
print(f'c_S=(0,{U_cS:+.4f})  c_R=(0,{U_cR:+.4f})  [general I*, closed forms {1/R0:+.4f}, {-gR/(d*R0):+.4f}]')
fig, ax = plt.subplots(figsize=(6.2,4.6))
# coincident points grouped with combined labels (|U_cS| and |U_cR| differ by 5e-4)
groups = [(['c_I',r'\beta'], '#c0392b', r'$c_I,\ \beta$',  (10,-4)),   # invasion-facing
          ([r'\tau_R'],      '#6c3483', r'$\tau_R$',        (10,-2)),   # mixed
          ([r'\tau_m'],      '#1f5fa8', r'$\tau_m$',        (8,4)),     # burden-facing
          (['c_S','c_R'],    '#1f5fa8', r'$c_S,\ c_R$',     (10,2))]    # burden-facing (endemic level only)
for keys,col,lab,off in groups:
    k = keys[0]
    ax.scatter(inv[k], bur[k], s=70, color=col, zorder=5, edgecolor='white', linewidth=0.8)
    ax.annotate(lab, xy=(inv[k],bur[k]), xytext=off, textcoords='offset points', fontsize=12, color=col)
ax.axhline(0, color='0.85', lw=0.8, zorder=0); ax.axvline(0, color='0.85', lw=0.8, zorder=0)
ax.set_xlabel(r'Invasion sensitivity $\,|\Upsilon^{\mathcal{R}_0}_p|$')
ax.set_ylabel(r'Burden sensitivity $\,|\Upsilon^{i^*}_p|$')
ax.set_xlim(-0.06,1.15); ax.set_ylim(-0.10,1.75)
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch6_invasion_burden.pdf'); print('wrote figs/ch6_invasion_burden.pdf')
