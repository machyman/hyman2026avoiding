# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- real-data influenza fit; imports the model function only.
"""Fig 8.x  Chapter 8 influenza case study: infected- vs susceptible-viewpoint fit.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 8.
Regenerates figs/ch8_influenza_fit.pdf.

The original CDC ILINet surveillance extract is no longer archived with the
project, so this script builds a REPRODUCIBLE representative weekly incidence
series for the 2017-2018 U.S. influenza season, calibrated so the infected-
viewpoint estimator gives alpha_hat ~ 0.20/day with the demographically-correct
residence time tau_m = 7300 days (20 yr).  The season's population is partly
immune: the truth has F0 = 0.8 and R0 = 1.75, so R_e(0) = R0 P_S(0) ~ 1.40, and
alpha_hat/(gamma_R + nu_m) estimates R_e, not R0.  The susceptible-viewpoint
estimate lambda_hat = J/S depends on the assumed susceptible fraction, and its
R0 conversion is R_e_hat/F0.  Every value the text quotes (alpha_hat, R_e_hat and
its interval, lambda_hat and R0_hat^(lambda)) is computed below and printed.
Prevalence is the reconstruction model's own I(t); no convolution is done.

Model: SIR_I (same as figs_src/sir_i_model.py)
  lam = beta*c_S*c_I*S*I/C,  C = c_S S + c_I I + c_R R
  R0  = c_I beta / (gamma_R + nu_m)
Early outbreak: alpha_hat = J/I ~ c_I beta P_S;  alpha_hat/(gamma_R+nu_m) = R0 P_S = R_e.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-06-22   Version 1.1
Revised: 2026-10-29   Version 1.2 (S277 review, R3-04, R3-05: the truth is a partly immune population,
                      F0 = 0.8 and R0 = 1.75, so R_e(0) ~ 1.40; beta = 1/24 keeps c_I ~ 6.  Panel (a) is
                      labelled R_e_hat, computed from the series, not hard-coded.  The interval and lambda_hat
                      are computed and printed.  Panel (b) curves are forward runs scaled to the observed peak.)
Revised: 2026-10-29   Version 1.3 (Session 277, staged pass 2): review fixes S3-02.  The panel (a) curve is the
                      generating trajectory (R0 = 1.75, F0 = 0.8), not a fit, and its legend now says so.  A
                      forward run at R_e_hat needs an F0, so no fitted trajectory is drawn.
Revised: 2026-10-31   Version 1.4 (Session 278 figure pin, U3b-04): the series is the stated season, week 40
                      of 2017 through week 20 of 2018, 33 weekly counts at t = 0, 7, ..., 224 d (T = 224 d; was
                      T = 252 d, 37 points, weeks 40-76).  The axis ticks read MMWR weeks 40...52, 1...20.  Same
                      seed; the first 33 draws, the growth window (days 7-49), the peak and every printed value
                      are unchanged.
Revised: 2026-11-17   Version 1.5 (round 1: the legend reads synthetic series (C1A-R006); the interval is a
                      percentile bootstrap of the median, 20,000 resamples, seed 1 (G1A-R020).  Round 2, B3
                      (G2A-R005): with n = 7 that interval is the 2nd and 6th of the sorted weekly values,
                      [1.3054, 1.4066].  Under the series' independent weekly noise it covers the median with
                      probability 1 - 2(1 + 7)/2^7 = 0.875, not 0.95; dependent real weekly values would make
                      it too narrow.  Comments and print lines only; every printed value is unchanged.)
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
cS, cR, beta = 10.0, 10.0, 1.0/24.0   # beta = 0.04167
R0_true, F0_true = 1.75, 0.80          # partly immune population: R_e(0) = R0 P_S(0) ~ 1.40
cI_true = R0_true * d / beta     # ~6.0  (influenza c_I)

def rhs(t, y, cI):
    S, I, R = y
    C = cS*S + cI*I + cR*R
    lam = beta*cS*cI*S*I/C
    return [nu - lam - nu*S, lam - (gR+nu)*I, gR*I - nu*R]

SEASON_T = 224.0                  # week 40 of 2017 (t = 0) through week 20 of 2018 (t = 224): 33 weekly counts

def incidence(cI, F0, T=SEASON_T, I0=2.0e-4, dt=0.25):
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
assert Jobs.size == 33, Jobs.size  # k = 1, ..., 33

def mmwr_ticks(a):
    """Label the continuous season week (40 ... 72) as MMWR weeks 40...52, 1...20 (2017 has 52 weeks)."""
    pos = np.arange(40, 73, 4)
    a.set_xticks(pos)
    a.set_xticklabels([str(int(w)) if w <= 52 else str(int(w - 52)) for w in pos])
    a.set_xlim(39, 73)

# ---- infected-viewpoint fit: alpha_hat over growth window ----
grow = (tw >= 7.0) & (tw <= 49.0)          # early exponential phase (S ~ 1)
I_init = 2.0e-4                            # the seed used by incidence()
PS0 = cS*F0_true/(cS*F0_true + cI_true*I_init + cR*(1.0-F0_true-I_init))
Re_weekly = Jobs[grow]/Iw[grow]/d          # weekly alpha_hat/(gamma_R+nu_m) over the window
n_w = Re_weekly.size
alpha_hat = np.median(Jobs[grow]/Iw[grow])
Re_hat = alpha_hat/d                       # infected-viewpoint estimate: R_e, not R0 (P_S < 1)
sd_w = Re_weekly.std(ddof=1)
se_w = sd_w/np.sqrt(n_w)
boot = np.random.default_rng(1)           # percentile bootstrap of the median, 20,000 resamples; with n = 7 it
                                          # returns the 2nd and 6th order statistics, which cover the median with
                                          # probability 0.875 under independent weekly noise (not 0.95)
Re_boot = [np.median(boot.choice(Re_weekly, n_w)) for _ in range(20000)]
Re_lo, Re_hi = np.percentile(Re_boot, [2.5, 97.5])
def lam_hat(F0):                           # median over the window of J_obs/S with S = F0 assumed
    return np.median(Jobs[grow]/F0)
def R0_lam_hat(F0):                        # median over the window of eq (R0-from-lambda-hat)
    return np.median(Jobs[grow]/(F0*Iw[grow]*d))

# ================= FIGURE =================
fig, ax = plt.subplots(1, 2, figsize=(9.4, 3.7))

# ----- Panel (a): infected viewpoint -----
ax[0].plot(wkw, Jobs*sc, "o", ms=4.2, mfc="#d62728", mec="white", mew=0.5,
           label="synthetic series", zorder=3)
ax[0].plot(wk, J*sc, "-", color="#1f3b66", lw=1.8,
           label=r"generating trajectory", zorder=2)
ax[0].text(0.96, 0.90, r"$\hat{\mathcal{R}}_e = %.2f$" % Re_hat,
           transform=ax[0].transAxes, ha="right", va="top", fontsize=12,
           bbox=dict(boxstyle="round,pad=0.3", fc="#eef2f8", ec="#1f3b66", lw=0.8))
ax[0].set_title(r"(a) Infected viewpoint $\;\hat\alpha = j/i$")
ax[0].set_xlabel("MMWR week (2017--2018 season)")
ax[0].set_ylabel(r"weekly incidence, ILI scale ($\%$)")
ax[0].legend(frameon=False, fontsize=8.5, loc="upper left")

# ----- Panel (b): susceptible viewpoint, five assumed F0 -----
F0s   = [1.0, 0.8, 0.6, 0.5, 0.3]
cols  = plt.cm.viridis(np.linspace(0.1, 0.85, len(F0s)))
ax[1].plot(wkw, Jobs*sc, "o", ms=4.0, mfc="0.45", mec="white", mew=0.4,
           label="synthetic series", zorder=4)
for F0, col in zip(F0s, cols):
    R0_lam = R0_lam_hat(F0)                 # R0_hat^(lambda) = Re_hat / F0
    cI = R0_lam*d/beta
    tt, JJ, _ = incidence(cI, F0)
    JJ = JJ * (Jobs.max()/JJ[wk_idx].max())  # forward run scaled to the observed peak (not a fit)
    ax[1].plot(tt/7.0+40.0, JJ*sc, "-", color=col, lw=1.4,
               label=r"$F_0=%.1f,\ \hat{\mathcal{R}}_0=%.2f$" % (F0, R0_lam),
               zorder=3)
ax[1].set_title(r"(b) Susceptible viewpoint $\;\hat\lambda = j/s$")
ax[1].set_xlabel("MMWR week (2017--2018 season)")
ax[1].set_ylabel(r"weekly incidence, ILI scale ($\%$)")
ax[1].legend(frameon=False, fontsize=7.6, loc="upper left", handlelength=1.4)

for a in ax:
    mmwr_ticks(a)
    a.spines["top"].set_visible(False); a.spines["right"].set_visible(False)
    a.set_ylim(bottom=0)

fig.tight_layout()
fig.savefig("figs/ch8_influenza_fit.pdf", bbox_inches="tight")
print("truth: R0 = %.2f, F0 = %.2f, c_I = %.4f, beta = %.5f, P_S(0) = %.5f, R_e(0) = %.4f"
      % (R0_true, F0_true, cI_true, beta, PS0, R0_true*PS0))
print("gamma_R + nu_m = %.6f" % d)
print("weekly counts: %d (t = %g ... %g d, MMWR week 40 of 2017 ... week %d of 2018)" % (Jobs.size, tw[0], tw[-1], int(wkw[-1] - 52)))
print("weekly alpha_hat/(gamma_R+nu_m), days 7-49:", np.round(Re_weekly, 3))
print("n = %d, median %.4f, mean %.4f, sd %.4f, SE %.4f" % (n_w, np.median(Re_weekly), Re_weekly.mean(), sd_w, se_w))
print("alpha_hat = %.4f /day  ->  R_e_hat = %.4f" % (alpha_hat, Re_hat))
print("interval (bootstrap of the median): [%.4f, %.4f]" % (Re_lo, Re_hi))
print("= 2nd and %dth of the %d sorted weekly values: [%.4f, %.4f]" % (n_w - 1, n_w, np.sort(Re_weekly)[1], np.sort(Re_weekly)[-2]))
print("coverage of the median under independent weekly noise: 1 - 2(1 + %d)/2^%d = %.4f"
      % (n_w, n_w, 1 - 2*(1 + n_w)/2**n_w))
for F0 in (0.8, 0.5):
    print("F0 = %.1f: lambda_hat = %.3e /day, R0_hat^(lambda) = %.4f, R_e_hat/F0 = %.4f"
          % (F0, lam_hat(F0), R0_lam_hat(F0), Re_hat/F0))
print("susceptible-viewpoint R0 by F0 (panel b):",
      {F0: round(R0_lam_hat(F0), 2) for F0 in F0s})
print("saved figs/ch8_influenza_fit.pdf")
