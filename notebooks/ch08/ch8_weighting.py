"""Fig 8.x  What the choice of residual weights does to a fit of the baseline outbreak.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 8 (Figure fig:weighting).

(a) Each observation's share of the Fisher information about R0, w_k (dmu_k/dR0)^2
    normalized, under three weightings.  An unweighted fit concentrates its attention on
    the peak; constant-CV weighting spreads it toward the growth phase, which is where the
    identifiability argument locates the cleanest signal.
(b) Actual coverage of nominal 95% intervals against increasing overdispersion, for four
    weighting schemes.

RECONSTRUCTION NOTE (Session 110, 2026-09-14).
--------------------------------------------
The original generator was lost: never pushed to the companion repository, in no archive
(R40.4).  Rewritten from asset-registry row `fig-ch8-weighting`.

The registry recorded that panel (b)'s values are Monte Carlo constants from
`probes/weighting_probe3_negative_binomial.py`, that they are EMBEDDED rather than
recomputed at draw time, and that they MATCH Table tbl:weighting-coverage.  That probe is
itself recorded lost (2026-08-19, D-34.7) and must not be searched for.  But the constants
survive in the book: they are the coverage block of Table tbl:weighting-coverage in
Chapter 8, transcribed below.  The lost probe's output was never only in the probe.

This is NOT byte-identical to the original and will not reproduce
`generator_sha256 a8fd46e1826670c9a6a1763a4246f079eedc055a1654a41f03f6737b96166398`
nor output hash `a23654ba...`.  It restores reproducibility, not byte-provenance.  Do not
overwrite figs/ch8_weighting.pdf without Mac's ruling.

REPAIR NOTE (Session 115, 2026-09-22).  Panel (a) was not reproduced at v2.0; it is now.
The cause and the verification are in the panel (a) block below and in
records/FIGURE_REPRODUCTION_2026-09-22.md.  Both panels now agree with the committed
figure's own plotted data: panel (a) to 0.00000 in share over all 117 plotted points,
panel (b) exactly.  Byte-provenance remains unavailable and is not claimed.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-09-22   Version 2.1 (reconstruction, panel (a) repaired and verified)
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
    "text.usetex": True, "font.family": "serif", "font.size": 12,
    "mathtext.fontset": "cm", "axes.linewidth": 0.8,
})

# ---------------------------------------------------------------------------------
# Panel (b) -- EMBEDDED constants.  Source of truth: Table tbl:weighting-coverage,
# Chapter 8.  150 replicates, common random numbers, Monte Carlo standard error about
# four percentage points; differences smaller than that are not real.  Do not recompute
# these here: the table and the figure must not be able to disagree.
# ---------------------------------------------------------------------------------
KAPPA_LABELS = ["Poisson", r"$\kappa=100$", r"$\kappa=20$", r"$\kappa=5$"]
COVERAGE = {
    r"$w=1$ (unweighted)":                     [65, 61, 69, 61],
    r"$w=1/\mu$ (Poisson)":                    [95, 75, 79, 75],
    r"$w=1/(\mu+\mu^2/\kappa)$ (correct)":     [95, 97, 91, 96],
    r"$w=1/\mu^2$ (constant CV)":              [73, 80, 91, 95],
}
COLORS = ["#c0392b", "#e08a1e", "#1f5fa8", "#2e7d5b"]

# ---------------------------------------------------------------------------------
# Panel (a) -- computed.  39 observations every 3 days, day 3 to day 117.  Reported counts
# peak at day 106.4 (day 105 on the observation grid) and the shaded 20-day peak window,
# truncated on the right by the data, holds 11 of the 39 observations.
# ---------------------------------------------------------------------------------
# STATUS OF THIS PANEL -- REPAIRED AND VERIFIED (Session 115, 2026-09-22).
#   Session 110 reconstructed this panel and could not reproduce it.  The cause was found
#   in Session 115: the reconstruction anchored on Chapter_08_Fitting_v29's caption, which
#   called day 108 the outbreak peak.  Day 108 is where PREVALENCE I(t) peaks once I0 is
#   tuned to put it there; reported counts peak nine days earlier.  Calibrating I0 to a
#   prevalence peak and then fixing the Fisher window on that day put the window on the
#   declining tail.  The caption was corrected at v30 to 'near day 106' and 'eleven of the
#   thirty-nine'.
#   REPAIRED: I0 = 1e-4, recovered rather than calibrated; mu is the model's own force of
#   infection scaled to reported counts per interval, N^c * 3 * lambda with
#   lambda = beta c_S c_I S I / C; the peak window is taken from the computed peak of mu,
#   never from a hard-coded day.
#   VERIFIED against the committed figure, not tuned to it: panel (a) data recovered from
#   figs/ch8_weighting.pdf by vector-path extraction match this script to 0.00000 in share
#   and 0.00000 d in time over all 117 plotted points, and the peak-window shares are
#   78.5 / 58.1 / 23.7 %, which is the figure's own annotation of 79 / 58 / 24.  The
#   parameters came from an independent artifact, the 2026-08-05 predecessor in the CCR
#   upload, used as evidence only; R40.4 stands, it is not a recovery route.
#   Panel (b) is unchanged and was always exact: constants from Table tbl:weighting-coverage.
# ---------------------------------------------------------------------------------
N_OBS, WINDOW_END, PEAK_HALFWIDTH = 39, 117.0, 20.0
OBS_STEP_DAYS = 3.0
I0_RECOVERED = 1.0e-4      # recovered, not calibrated
N_C = 100_000              # reporting population; scales mu and cancels in a normalized share
B = dict(M.BASE)
gR, nu = 1.0 / B["tau_R"], 1.0 / B["tau_m"]
R0_BASE = B["c_I"] * B["beta"] / (gR + nu)

days = WINDOW_END - OBS_STEP_DAYS * np.arange(N_OBS - 1, -1, -1)


def incidence(R0):
    """Expected reported counts per 3-day interval at the observation days."""
    beta = R0 * (gR + nu) / B["c_I"]
    sol = M.simulate(WINDOW_END + 13.0, beta=beta,
                     y0=(1 - I0_RECOVERED, I0_RECOVERED, 0.0))
    S, I, R = sol.sol(days)
    C = B["c_S"] * S + B["c_I"] * I + B["c_R"] * R
    lam = beta * B["c_S"] * B["c_I"] * S * I / C     # the model's own force of infection
    return N_C * OBS_STEP_DAYS * lam                 # reported counts per interval


h = 1e-5
mu = incidence(R0_BASE)
dmu = (incidence(R0_BASE + h) - incidence(R0_BASE - h)) / (2.0 * h)

WEIGHTS = {r"$w=1$": 1.0 / np.ones_like(mu),
           r"$w=1/\mu$": 1.0 / mu,
           r"$w=1/\mu^2$": 1.0 / mu ** 2}

PEAK_DAY = float(days[int(np.argmax(mu))])   # computed from mu, never hard-coded
peak_mask = np.abs(days - PEAK_DAY) <= PEAK_HALFWIDTH
shares, peak_share = {}, {}
for lab, w in WEIGHTS.items():
    info = w * dmu ** 2
    shares[lab] = info / info.sum()
    peak_share[lab] = 100.0 * shares[lab][peak_mask].sum()

print(f"R0 baseline = {R0_BASE:.4f};  {peak_mask.sum()} of {N_OBS} observations in the peak window")
for lab in WEIGHTS:
    print(f"  peak-window Fisher share, {lab:12s}: {peak_share[lab]:5.1f}%")
print("  figure's own annotation: 79 / 58 / 24 %  (recovered from the committed PDF)")

# ---------------------------------------------------------------------------------
fig, (axa, axb) = plt.subplots(1, 2, figsize=(11.0, 4.2))

axa.axvspan(PEAK_DAY - PEAK_HALFWIDTH, WINDOW_END, color="0.85", alpha=0.5, zorder=0)
for (lab, sh), col in zip(shares.items(), COLORS):
    axa.plot(days, 100.0 * sh, "o-", ms=3.2, lw=1.4, color=col,
             label=f"{lab}  ({peak_share[lab]:.0f}\\% in window)")
axa.set_xlabel("day"); axa.set_ylabel(r"share of Fisher information about $\mathcal{R}_0$ (\%)")
axa.set_title(r"(a) which observations the fit listens to", fontsize=11)
axa.legend(frameon=False, fontsize=9); axa.grid(True, lw=0.3, alpha=0.4)

x = np.arange(len(KAPPA_LABELS))
for (lab, cov), col in zip(COVERAGE.items(), COLORS):
    axb.plot(x, cov, "o-", ms=4.5, lw=1.6, color=col, label=lab)
axb.axhline(95, ls="--", lw=1.0, color="0.35")
axb.annotate(r"nominal $95\%$", xy=(0.05, 95.8), fontsize=9, color="0.35")
axb.set_xticks(x); axb.set_xticklabels(KAPPA_LABELS)
axb.set_xlabel("overdispersion"); axb.set_ylabel(r"actual coverage of nominal $95\%$ interval (\%)")
axb.set_ylim(55, 102)
axb.set_title(r"(b) what it does to the interval reported", fontsize=11)
axb.legend(frameon=False, fontsize=9, loc="lower right"); axb.grid(True, lw=0.3, alpha=0.4)

fig.tight_layout()
out = sys.argv[1] if len(sys.argv) > 1 else "figs/ch8_weighting.pdf"
os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
fig.savefig(out)
print(f"wrote {out}")
