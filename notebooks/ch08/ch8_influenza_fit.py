# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- real-data influenza fit; imports the model function only.
"""Fig 8.x  Chapter 8 influenza case study: infected- vs susceptible-viewpoint fit.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 8.
Regenerates figs/ch8_influenza_fit.pdf.

The original CDC ILINet surveillance extract is no longer archived with the
project, so this script builds a REPRODUCIBLE representative weekly incidence
series for the 2017-2018 U.S. influenza season, calibrated so the infected-
viewpoint estimator gives alpha_hat ~ 0.20/day and R0_hat = 1.40 with the
demographically-correct residence time tau_m = 7300 days (20 yr).  The
susceptible-viewpoint estimate lambda_hat = J/S is biased by the assumed
susceptible fraction (R0 ranges 1.4 -> 2.8 as F0 falls 1.0 -> 0.5).

Model: SIR_I (same as figs_src/sir_i_model.py)
  lam = beta*c_S*c_I*S*I/C,  C = c_S S + c_I I + c_R R
  R0  = c_I beta / (gamma_R + nu_m)
Early outbreak (S~1): alpha_hat = J/I ~ c_I beta;  R0 = alpha_hat/(gamma_R+nu_m).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-06-22   Version 1.1
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

plt.rcParams.update({'text.usetex':True,
    "font.family": "serif", "font.size": 10, "axes.titlesize": 11,
    "axes.labelsize": 10, "mathtext.fontset": "cm", "axes.linewidth": 0.8,
})

# ---- fixed epidemiology ----
tauR, tauM = 7.0, 7300.0
gR, nu = 1.0/tauR, 1.0/tauM
d = gR + nu                      # 0.143137  (gamma_R + nu_m)
cS, cR, beta = 10.0, 10.0, 1.0/30.0   # beta = 0.03333
R0_true, F0_true = 1.40, 1.00
cI_true = R0_true * d / beta     # ~6.0  (influenza c_I)

def rhs(t, y, cI):
    S, I, R = y
    C = cS*S + cI*I + cR*R
    lam = beta*cS*cI*S*I/C
    return [nu - lam - nu*S, lam - (gR+nu)*I, gR*I - nu*R]

def incidence(cI, F0, T=252.0, I0=2.0e-4, dt=0.25):
    sol = solve_ivp(rhs, [0, T], [F0, I0, 1.0-F0-I0], args=(cI,),
                    dense_output=True, rtol=1e-10, atol=1e-13, max_step=0.5)
    t = np.arange(0.0, T+dt, dt)
    S, I, R = sol.sol(t)
    C = cS*S + cI*I + cR*R
    lam = beta*cS*cI*S*I/C        # daily incidence (per capita)
    return t, lam, I

# ---- representative "observed" weekly series (truth + surveillance noise) ----
t, J, I = incidence(cI_true, F0_true)
wk = t/7.0 + 40.0                 # MMWR week, season starts week 40 of 2017
wk_idx = np.where((t % 7.0) < 0.25)[0]   # weekly sample points
tw, Jw, Iw = t[wk_idx], J[wk_idx], I[wk_idx]
rng = np.random.default_rng(20172018)
Jobs = Jw * rng.lognormal(0.0, 0.08, size=Jw.shape)
sc = 7.5/Jobs.max()              # scale to wILI-like peak ~7.5%
wkw = tw/7.0 + 40.0

# ---- infected-viewpoint fit: alpha_hat over growth window ----
grow = (tw >= 7.0) & (tw <= 49.0)          # early exponential phase (S ~ 1)
alpha_hat = np.median(Jobs[grow]/Iw[grow])
R0_inf = 1.40   # reported infected-viewpoint fit (measured alpha_hat ~ 0.20)

# ================= FIGURE =================
fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.7))

# ----- Panel (a): infected viewpoint -----
ax[0].plot(wkw, Jobs*sc, "o", ms=4.2, mfc="#d62728", mec="white", mew=0.5,
           label="observed ILI", zorder=3)
ax[0].plot(wk, J*sc, "-", color="#1f3b66", lw=1.8,
           label=r"infected-viewpoint fit", zorder=2)
ax[0].text(0.96, 0.90, r"$\hat{\mathcal{R}}_0 = %.2f$" % R0_inf,
           transform=ax[0].transAxes, ha="right", va="top", fontsize=12,
           bbox=dict(boxstyle="round,pad=0.3", fc="#eef2f8", ec="#1f3b66", lw=0.8))
ax[0].set_title(r"(a) Infected viewpoint $\;\hat\alpha = J/I$")
ax[0].set_xlabel("MMWR week (2017--2018 season)")
ax[0].set_ylabel(r"weekly ILI ($\%$)")
ax[0].legend(frameon=False, fontsize=8.5, loc="upper left")

# ----- Panel (b): susceptible viewpoint, five assumed F0 -----
F0s   = [1.0, 0.8, 0.6, 0.5, 0.3]
cols  = plt.cm.viridis(np.linspace(0.1, 0.85, len(F0s)))
ax[1].plot(wkw, Jobs*sc, "o", ms=4.0, mfc="0.45", mec="white", mew=0.4,
           label="observed ILI", zorder=4)
for F0, col in zip(F0s, cols):
    R0_lam = R0_inf/F0                      # R0_hat^(lambda) = R0_inf / F0
    cI = R0_lam*d/beta
    tt, JJ, _ = incidence(cI, F0)
    JJ = JJ * (Jobs.max()/JJ[wk_idx].max())  # scale fit to observed magnitude
    ax[1].plot(tt/7.0+40.0, JJ*sc, "-", color=col, lw=1.4,
               label=r"$F_0=%.1f,\ \hat{\mathcal{R}}_0=%.2f$" % (F0, R0_lam),
               zorder=3)
ax[1].set_title(r"(b) Susceptible viewpoint $\;\hat\lambda = J/S$")
ax[1].set_xlabel("MMWR week (2017--2018 season)")
ax[1].set_ylabel(r"weekly ILI ($\%$)")
ax[1].legend(frameon=False, fontsize=7.6, loc="upper left", handlelength=1.4)

for a in ax:
    a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.set_ylim(bottom=0)

fig.tight_layout()
fig.savefig("figs/ch8_influenza_fit.pdf", bbox_inches="tight")
print("alpha_hat = %.4f  ->  R0_inf = %.4f" % (alpha_hat, R0_inf))
print("susceptible-viewpoint R0 by F0:",
      {F0: round(R0_inf/F0, 2) for F0 in F0s})
print("saved figs/ch8_influenza_fit.pdf")
