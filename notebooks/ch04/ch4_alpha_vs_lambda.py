"""Fig 4.2  The two forces over time: alpha nearly flat while lambda grows.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 4 (Figure fig:alpha-vs-lambda).

In the Chapter 7 Scenario 1 baseline outbreak, the force FROM infection, alpha = c_I beta P_S, stays nearly flat across
the early-growth window, while the force OF infection, lambda = c_S beta P_I, grows with the infectious fraction. Here
P_S = c_S S / C and P_I = c_I I / C are the contact-weighted proportions of Chapter 4, with
C = c_S S + c_I I + c_R R: the quantities the chapter defines, its caption names and the committed figure plots.

REPAIR NOTE (Session 169, 2026-10-11; F-168.4, RG-168.1c).
---------------------------------------------------------
Version 2.0 (the Session 110 reconstruction) plotted c_S beta I and c_I beta S, the unweighted fractions. At t = 0 its
lambda was C / c_I = 4.996 times the chapter's, which is the "about five times larger" floor Session 115 found (D2), and
its alpha drifted 4.9% where the chapter's drifts 3.1%. Regenerated from v2.0, lambda would have crossed alpha near the
peak; in the committed figure it stays below alpha throughout. This version computes the chapter's quantities and
reproduces the committed figure's data (see the verification in reviews/S169_VERIFY/). The annotation is computed and
its percent sign escaped: the committed figure prints "alpha changes by 3" with no unit (F-168.5), most likely because
an unescaped % began a TeX comment. Byte provenance of the lost original remains unavailable and is not claimed.

Window: the early-growth window is S >= 0.95, the phase before five percent of the population has been infected.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-11   Version 3.0 (repair: the chapter's P_S and P_I; computed annotation)
"""
import os
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sir_i_model as M

plt.rcParams.update({
    "text.usetex": True, "font.family": "serif", "font.size": 10,
    "mathtext.fontset": "cm", "axes.linewidth": 0.8,
})

# --- Chapter 7 Scenario 1 baseline -------------------------------------------------
B = dict(M.BASE)
c_S, c_I, c_R, beta = B["c_S"], B["c_I"], B["c_R"], B["beta"]
T_END = 130.0
sol = M.simulate(160.0)                      # the shared integrator, dense output
t = np.linspace(0.0, T_END, 4001)
S, I, R = sol.sol(t)
C = c_S * S + c_I * I + c_R * R              # total contact rate (Chapter 4)
P_S, P_I = c_S * S / C, c_I * I / C          # contact-weighted proportions
alpha = c_I * beta * P_S                     # force FROM infection
lam = c_S * beta * P_I                       # force OF infection

# --- early-growth window and the annotated numbers ---------------------------------
GROW_S_MIN = 0.95
k_end = int(np.argmax(S < GROW_S_MIN))       # first grid point past the window
t_end = float(np.interp(GROW_S_MIN, S[k_end::-1], t[k_end::-1]))
alpha_end, lam_end = np.interp(t_end, t, alpha), np.interp(t_end, t, lam)
alpha_change = 100.0 * (1.0 - alpha_end / alpha[0])
lam_fold = lam_end / lam[0]
t_peak = float(t[np.argmax(I)])

print(f"early-growth window 0-{t_end:.2f} d (S >= {GROW_S_MIN}); peak of I at t = {t_peak:.2f} d")
print(f"alpha = c_I beta P_S: {alpha[0]:.5f} -> {alpha_end:.5f}  ({alpha_change:.2f}% change)")
print(f"lambda = c_S beta P_I: {lam[0]:.4e} -> {lam_end:.4e}  ({lam_fold:.2f}-fold)")
print(f"lambda stays below alpha on [0, {T_END:.0f}]: {bool((lam < alpha).all())}; max lambda {lam.max():.4f}")

# --- figure ----------------------------------------------------------------------
BLUE, RED = "#1f5fa8", "#c0392b"
fig, ax = plt.subplots(figsize=(7.2, 4.3))
ax.axvspan(0.0, t_end, color="0.9", zorder=0)
ax.semilogy(t, alpha, color=BLUE, lw=2.2,
            label=r"$\alpha(t)=c_I\beta P_S$\quad force \emph{from} infection")
ax.semilogy(t, lam, color=RED, lw=2.2, ls="--",
            label=r"$\lambda(t)=c_S\beta P_I$\quad force \emph{of} infection")
ax.set_xlim(0.0, T_END)
ax.set_ylim(1e-4, 0.4)
ax.axvline(t_peak, color="0.55", ls=":", lw=1.0)
ax.text(t_peak - 2.5, 3e-3, "epidemic peak", rotation=90, ha="center", va="center", fontsize=8, color="0.45")
ax.text(t_end / 2.0, 1.6e-4, "early-growth window\n" + r"($S \ge %.2f$)" % GROW_S_MIN,
        ha="center", va="center", fontsize=8, color="0.45")
ax.text(0.61, 0.135,
        "Across the early-growth window:\n"
        + r"$\alpha$ changes by %.1f\%%" % alpha_change + "\n"
        + r"$\lambda$ grows %.1f-fold" % lam_fold,
        transform=ax.transAxes, fontsize=8, va="center", ha="left",
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="0.75", lw=0.7))
ax.set_xlabel("Days")
ax.set_ylabel(r"force (day$^{-1}$), log scale")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.annotate("", xy=(1.009, 0.0), xytext=(1.0, 0.0), xycoords="axes fraction",
            arrowprops=dict(arrowstyle="-|>", color="0.2", lw=1.5))
ax.legend(loc="upper right", frameon=False, fontsize=9)
fig.tight_layout()

out = sys.argv[1] if len(sys.argv) > 1 else "figs/ch4_alpha_vs_lambda.pdf"
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
fig.savefig(out)
print(f"wrote {out}")
