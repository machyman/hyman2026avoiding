"""Ch 9  Benchmarks, forecasts and rival models; the parametric-bootstrap lab.

Companion text: Foundations and Pitfalls in Epidemic Modeling (hyman2026avoiding), Chapter 9.
Regenerates figs/ch9_benchmark_fits.pdf, figs/ch9_bootstrap_lab.pdf and figs/ch9_forecast_scores.pdf,
and writes every value the text quotes to figs_src/ch9_benchmarks_values.txt.

Data: weekly U.S. mpox cases reported to CDC during the 2022 outbreak, 32 weeks (week 0 is the first
week in the series), as distributed with GrowthPredict (Chowell et al. 2024, Sci. Rep. 14, 1630;
github.com/gchowell/forecasting_growthmodels, file input/Most_Recent_Timeseries_US-CDC.txt, GPL-3.0).
Copied unchanged to data/us_mpox_2022_weekly_cdc.txt.

Models for the expected weekly incidence mu(t) = dC/dt, with C(0) fixed at the first count:
  GGM       dC/dt = r C^p                              (Viboud, Simonsen and Chowell 2016)
  GLM       dC/dt = r C^p (1 - C/K)
  Richards  dC/dt = r C (1 - (C/K)^a)
  SIR       S' = -beta S I/N, I' = beta S I/N - gamma I, incidence beta S I/N; I(0) = y0/beta, S(0) = N - I(0)
Observation model: negative binomial with mean mu and size k (variance mu + mu^2/k), fitted by maximum
likelihood; k is one extra parameter for every model. Model comparison: AICc.
Integration: GGM and Richards in closed form; GLM and SIR by odeint (LSODA). Fits: L-BFGS-B within box bounds from
three starts, each polished by Nelder-Mead; bootstrap refits by L-BFGS-B from the point estimate.
Uncertainty: parametric bootstrap. Resample the calibration window from the fitted negative binomial
(or Poisson, for the lab's contrast), refit, project, add observation noise.
Forecast scores (Bracher, Ray, Gneiting and Reich 2021): MAE and MSE of the median; WIS over the
median and K = 11 central intervals (alpha = 0.02, 0.05, 0.1, ..., 0.9); coverage of the 50% and
95% intervals. Rolling origin: calibration windows ending at weeks 6, 8, ..., 20; horizons 1-4 weeks.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University (code drafted with Claude)
Date:    2026-11-08   Version 1.1 (Session 280, Springer review 3, points 1, 2, 3, 5; AUDIT8 item 8: docstring
                      corrected, unused rk4 removed; rolling() factored out for the guide code. Output unchanged.)
Revised: 2026-11-13   Version 1.2 (round-1 audit, pass-5 L5-05/L5-09: also prints each model's mean WIS and 95%
                      hits at every origin and the ensemble's summed-WIS gap to the GLM, so the per-origin
                      statements of Section 8.8 trace to the values file. No random draws added; scores unchanged.)
"""
import os
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from scipy.optimize import minimize
from scipy.integrate import odeint
from scipy.special import gammaln

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data", "us_mpox_2022_weekly_cdc.txt")
FIGS = os.path.join(ROOT, "figs")
VALS = os.path.join(HERE, "ch9_benchmarks_values.txt")
SEED = 20261108
B_FORECAST = 50       # bootstrap refits per model and origin
B_LAB = 200           # bootstrap refits for the lab
ORIGINS = list(range(6, 21, 2))
H = 4
LAB_ORIGIN = 14       # the lab calibrates through week 14, after the peak
FIG_ORIGIN = 10       # Fig 1 shows fits and forecasts calibrated through week 10, before the peak
ALPHAS = [0.02, 0.05] + [round(0.1 * j, 1) for j in range(1, 10)]

d = np.loadtxt(DATA)
T_ALL, Y_ALL = d[:, 0].astype(int), d[:, 1]
Y0 = Y_ALL[0]


# ---------- models: expected weekly incidence on t = 0..n-1 ----------
def mu_ggm(th, n):
    r, p = np.exp(th[0]), 1 / (1 + np.exp(-th[1]))
    t = np.arange(n)
    if abs(1 - p) < 1e-9:
        C = Y0 * np.exp(r * t)
    else:
        C = (Y0 ** (1 - p) + (1 - p) * r * t) ** (1 / (1 - p))
    return r * C ** p


def mu_glm(th, n):
    r, p, K = np.exp(th[0]), 1 / (1 + np.exp(-th[1])), Y0 + np.exp(th[2])
    f = lambda C, t: r * max(C[0], 1e-12) ** p * (1 - C[0] / K)
    C = odeint(f, [Y0], np.arange(n, dtype=float), rtol=1e-8, atol=1e-8)[:, 0]
    return np.maximum(r * C ** p * (1 - C / K), 1e-9)


def mu_rich(th, n):
    r, a, K = np.exp(th[0]), np.exp(th[1]), Y0 + np.exp(th[2])
    t = np.arange(n)
    C = K / (1 + ((K / Y0) ** a - 1) * np.exp(-r * a * t)) ** (1 / a)
    return np.maximum(r * C * (1 - (C / K) ** a), 1e-9)


def mu_sir(th, n):
    beta, gamma, N = np.exp(th[0]), np.exp(th[1]), Y0 + np.exp(th[2])
    I0 = Y0 / beta
    def f(x, t):
        inc = beta * x[0] * x[1] / N
        return [-inc, inc - gamma * x[1]]
    X = odeint(f, [N - I0, I0], np.arange(n, dtype=float), rtol=1e-8, atol=1e-8)
    return np.maximum(beta * X[:, 0] * X[:, 1] / N, 1e-9)


MODELS = {
    "GGM": (mu_ggm, [np.log(0.8), 0.5]),
    "GLM": (mu_glm, [np.log(0.8), 0.5, np.log(2e4)]),
    "Richards": (mu_rich, [np.log(0.5), np.log(0.5), np.log(2e4)]),
    "SIR": (mu_sir, [np.log(1.0), np.log(0.4), np.log(2e4)]),
}
NAMES = list(MODELS)
# Box bounds on the working parameters (log or logit scale); the last entry is log k for the negative binomial.
# K and N are capped at 10^6 and gamma at 1/52 per week (a one-year infectious period) so that an unidentified
# direction stays finite; a fit that ends on a bound is reported, because it is the diagnostic.
LOGK = (-3.0, 10.0)
BOUNDS = {
    "GGM": [(-5.0, 2.0), (-6.0, 6.0)],
    "GLM": [(-5.0, 2.0), (-6.0, 6.0), (0.0, np.log(1e6))],
    "Richards": [(-5.0, 2.0), (-4.0, 3.0), (0.0, np.log(1e6))],
    "SIR": [(-4.0, 3.0), (np.log(1 / 52), np.log(7.0)), (0.0, np.log(1e6))],
}
PNAMES = {"GGM": ["log r", "logit p"], "GLM": ["log r", "logit p", "log(K - y0)"],
          "Richards": ["log r", "log a", "log(K - y0)"], "SIR": ["log beta", "log gamma", "log(N - y0)"]}


def on_bound(name, x, dist="nb", tol=1e-3):
    b = BOUNDS[name] + ([LOGK] if dist == "nb" else [])
    return [PNAMES[name][i] if i < len(PNAMES[name]) else "log k"
            for i, (lo, hi) in enumerate(b) if x[i] - lo < tol or hi - x[i] < tol]


# ---------- likelihoods and fitting ----------
def nb_ll(y, mu, k):
    return np.sum(gammaln(y + k) - gammaln(k) - gammaln(y + 1) + k * np.log(k / (k + mu)) + y * np.log(mu / (k + mu)))


def pois_ll(y, mu):
    return np.sum(y * np.log(mu) - mu - gammaln(y + 1))


def fit(name, y, dist="nb", start=None):
    f, th0 = MODELS[name]
    n = len(y)
    x0 = np.array(list(start) if start is not None else list(th0) + ([np.log(20.0)] if dist == "nb" else []))

    bnds = BOUNDS[name] + ([LOGK] if dist == "nb" else [])
    lo, hi = np.array([b[0] for b in bnds]), np.array([b[1] for b in bnds])

    def nll(x):
        x = np.clip(x, lo, hi)
        mu = f(x[: len(th0)], n)
        if not np.all(np.isfinite(mu)):
            return 1e12
        v = -(nb_ll(y, mu, np.exp(x[-1])) if dist == "nb" else pois_ll(y, mu))
        return v if np.isfinite(v) else 1e12

    best = None
    x0 = np.clip(x0, lo, hi)
    starts = [x0] if start is not None else [x0, np.clip(x0 + 0.3, lo, hi), np.clip(x0 - 0.3, lo, hi)]
    for s in starts:
        r = minimize(nll, s, method="L-BFGS-B", bounds=bnds)
        if start is None:
            r2 = minimize(nll, r.x, method="Nelder-Mead", options={"maxiter": 3000, "xatol": 1e-6, "fatol": 1e-8})
            r = r2 if r2.fun < r.fun else r
        if best is None or r.fun < best.fun:
            best = r
    return np.clip(best.x, lo, hi), -best.fun


def aicc(ll, k, n):
    return -2 * ll + 2 * k + 2 * k * (k + 1) / max(n - k - 1, 1)


def draw(mu, x, dist, rng):
    if dist == "nb":
        k = np.exp(np.clip(x[-1], -3, 12))
        mu = np.clip(mu, 1e-9, 1e7)
        return rng.negative_binomial(k, k / (k + mu))
    return rng.poisson(np.clip(mu, 1e-9, 1e7))


def bootstrap(name, y, x_hat, dist, B, n_proj, rng):
    """Parametric bootstrap: refit to B resampled windows; return parameter draws and predictive samples."""
    f, th0 = MODELS[name]
    n = len(y)
    mu_hat = f(x_hat[: len(th0)], n)
    params, pred = [], []
    for _ in range(B):
        yb = draw(mu_hat, x_hat, dist, rng).astype(float)
        xb, _ = fit(name, yb, dist, start=x_hat)
        mu_p = f(xb[: len(th0)], n_proj)
        params.append(xb)
        pred.append(draw(mu_p, xb, dist, rng))
    return np.array(params), np.array(pred, dtype=float)


# ---------- scores ----------
def wis(samples, y):
    med = np.median(samples)
    s = 0.5 * abs(y - med)
    for a in ALPHAS:
        lo, hi = np.quantile(samples, [a / 2, 1 - a / 2])
        s += (a / 2) * ((hi - lo) + (2 / a) * max(lo - y, 0) + (2 / a) * max(y - hi, 0))
    return s / (len(ALPHAS) + 0.5)


def covers(samples, y, level):
    lo, hi = np.quantile(samples, [(1 - level) / 2, (1 + level) / 2])
    return float(lo <= y <= hi)


def rolling(dist, H, B, rng, say=print):
    """Rolling-origin forecasts over ORIGINS with horizons 1..H; returns scores, AICc weights, spreads, Fig-1 fits."""
    res = {m: {"ae": [], "se": [], "wis": [], "c50": [], "c95": [], "h": []} for m in NAMES + ["Ensemble"]}
    weights, spread, aic_tab = {}, {}, {}
    fits_at = {}
    for t0 in ORIGINS:
        y = Y_ALL[: t0 + 1]
        n = len(y)
        A, samp = {}, {}
        for m in NAMES:
            x_hat, ll = fit(m, y, dist)
            kpar = len(MODELS[m][1]) + (1 if dist == "nb" else 0)
            ob = on_bound(m, x_hat, dist)
            if ob:
                say(f"  origin {t0}: {m} ends on a bound: {', '.join(ob)}")
            A[m] = aicc(ll, kpar, n)
            _, S = bootstrap(m, y, x_hat, dist, B, t0 + 1 + H, rng)
            samp[m] = S[:, t0 + 1:]
            if t0 == FIG_ORIGIN:
                fits_at[m] = (x_hat, S)
        amin = min(A.values())
        w = {m: np.exp(-0.5 * (A[m] - amin)) for m in NAMES}
        tot = sum(w.values())
        w = {m: w[m] / tot for m in NAMES}
        weights[t0], aic_tab[t0] = w, A
        # ensemble: mixture with B_FORECAST draws allotted by weight
        alloc = rng.multinomial(B, [w[m] for m in NAMES])
        ens = np.vstack([samp[m][rng.integers(0, B, a)] for m, a in zip(NAMES, alloc) if a > 0])
        samp["Ensemble"] = ens
        meds = np.array([np.median(samp[m][:, H - 1]) for m in NAMES[1:]])
        spread[t0] = (meds.min(), meds.max(), np.median(samp["GGM"][:, H - 1]))
        for m in NAMES + ["Ensemble"]:
            for j in range(H):
                tt = t0 + 1 + j
                if tt >= len(Y_ALL):
                    continue
                obs = Y_ALL[tt]
                s = samp[m][:, j]
                med = np.median(s)
                res[m]["ae"].append(abs(med - obs)); res[m]["se"].append((med - obs) ** 2)
                res[m]["wis"].append(wis(s, obs)); res[m]["c50"].append(covers(s, obs, 0.5)); res[m]["c95"].append(covers(s, obs, 0.95)); res[m]["h"].append(j + 1)
    return res, weights, spread, fits_at


def main():
    rng = np.random.default_rng(SEED)
    out = []
    say = lambda s: (out.append(s), print(s))
    say(f"data: {len(Y_ALL)} weeks; peak {int(Y_ALL.max())} cases in week {int(T_ALL[Y_ALL.argmax()])}; total {int(Y_ALL.sum())}")

    # ---- lab (SR3.2): calibration through week LAB_ORIGIN, GLM, Poisson vs negative binomial ----
    y = Y_ALL[: LAB_ORIGIN + 1]
    lab = {}
    for dist in ("pois", "nb"):
        x_hat, ll = fit("GLM", y, dist)
        P, S = bootstrap("GLM", y, x_hat, dist, B_LAB, len(Y_ALL), rng)
        lab[dist] = (x_hat, P, S)
        r, p, K = np.exp(P[:, 0]), 1 / (1 + np.exp(-P[:, 1])), Y0 + np.exp(P[:, 2])
        q = lambda v: np.quantile(v, [0.025, 0.5, 0.975])
        say(f"lab {dist}: point r={np.exp(x_hat[0]):.3f} p={1/(1+np.exp(-x_hat[1])):.3f} K={Y0+np.exp(x_hat[2]):.0f}"
            + (f" k={np.exp(x_hat[-1]):.1f}" if dist == "nb" else ""))
        say(f"lab {dist}: on a bound: {', '.join(on_bound('GLM', x_hat, dist)) or 'none'}")
        say(f"lab {dist}: p 95% [{q(p)[0]:.3f}, {q(p)[2]:.3f}]; K 95% [{q(K)[0]:.0f}, {q(K)[2]:.0f}]; corr(r,p)={np.corrcoef(np.log(r), p)[0,1]:.2f}")
        pk = S[:, LAB_ORIGIN + 1: LAB_ORIGIN + 1 + H]
        cov = np.mean([covers(pk[:, j], Y_ALL[LAB_ORIGIN + 1 + j], 0.95) for j in range(H)])
        say(f"lab {dist}: 95% PI weeks {LAB_ORIGIN+1}-{LAB_ORIGIN+H} covers {int(cov*H)} of {H}; total size 95% [{q(S.sum(1))[0]:.0f}, {q(S.sum(1))[2]:.0f}] (observed {int(Y_ALL.sum())})")

    # ---- rolling-origin forecasts, scores, AICc weights (SR3.1) ----
    res, weights, spread, fits_at = rolling("nb", H, B_FORECAST, rng, say)
    say("scores over origins " + ",".join(map(str, ORIGINS)) + f", horizons 1-{H}:")
    for m in NAMES + ["Ensemble"]:
        R = res[m]
        say(f"  {m}: MAE {np.mean(R['ae']):.0f}  MSE {np.mean(R['se']):.3g}  WIS {np.mean(R['wis']):.0f}  cov50 {np.mean(R['c50']):.2f}  cov95 {np.mean(R['c95']):.2f}  n {len(R['ae'])}")
    for t0 in ORIGINS:
        w = weights[t0]
        say(f"  origin {t0}: AICc weights " + "  ".join(f"{m} {w[m]:.2f}" for m in NAMES)
            + f";  week-{t0+H} medians: GLM/Richards/SIR {spread[t0][0]:.0f} to {spread[t0][1]:.0f}, GGM {spread[t0][2]:.0f} (observed {int(Y_ALL[t0+H]) if t0+H < len(Y_ALL) else 'NA'})")
    # per-origin scores: the origin-10 and week-8 statements of Section 8.8 (no random draws)
    per = [sum(1 for j in range(H) if t0 + 1 + j < len(Y_ALL)) for t0 in ORIGINS]
    idx = np.cumsum([0] + per)
    say("per-origin mean WIS (95% hits/forecasts), horizons 1-4; last: Ensemble minus GLM, WIS summed over the origin:")
    for i, t0 in enumerate(ORIGINS):
        a, b = idx[i], idx[i + 1]
        say(f"  origin {t0}: " + "  ".join(f"{m} {np.mean(res[m]['wis'][a:b]):.0f} ({int(sum(res[m]['c95'][a:b]))}/{per[i]})" for m in NAMES + ["Ensemble"])
            + f";  Ens-GLM {sum(res['Ensemble']['wis'][a:b]) - sum(res['GLM']['wis'][a:b]):+.0f}")
    x_ggm = fits_at["GGM"][0]
    say(f"GGM at origin {FIG_ORIGIN}: r={np.exp(x_ggm[0]):.3f}, p={1/(1+np.exp(-x_ggm[1])):.3f}")
    for t0 in ORIGINS:
        xg = fit("GGM", Y_ALL[: t0 + 1], "nb")[0]
        say(f"GGM at origin {t0}: r={np.exp(xg[0]):.3f}, p={1/(1+np.exp(-xg[1])):.3f}")

    # ---- figures ----
    plt.rcParams.update({"font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    cols = {"GGM": "#1b9e77", "GLM": "#d95f02", "Richards": "#7570b3", "SIR": "#e7298a", "Ensemble": "#333333"}
    # Fig 1: fits and forecasts calibrated through FIG_ORIGIN (week 10)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.plot(T_ALL, Y_ALL, "o", color="0.55", ms=3.5, label="observed", zorder=1)
    ax.axvline(FIG_ORIGIN + 0.5, color="0.7", lw=0.8, ls=":")
    for m in NAMES:
        S = fits_at[m][1]
        tt = np.arange(FIG_ORIGIN + 1, FIG_ORIGIN + 1 + H)
        f, th0 = MODELS[m]
        mu = f(fits_at[m][0][: len(th0)], FIG_ORIGIN + 1 + H)
        ax.plot(np.arange(FIG_ORIGIN + 1 + H), mu, color=cols[m], lw=1.4, label=m)
        lo, hi = np.quantile(S[:, FIG_ORIGIN + 1:], [0.025, 0.975], axis=0)
        ax.fill_between(tt, lo, hi, color=cols[m], alpha=0.15, lw=0)
    ax.set_xlabel("week"); ax.set_ylabel("weekly cases"); ax.set_xlim(-0.5, 20.5)
    ax.set_ylim(0, 1.6 * Y_ALL.max())
    ax.legend(frameon=False, ncol=2, loc="upper left")
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    fig.tight_layout(); fig.savefig(os.path.join(FIGS, "ch9_benchmark_fits.pdf"), metadata={"CreationDate": None})
    plt.close(fig)
    # Fig 2: bootstrap lab
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.9))
    for dist, c, lab_name in (("pois", "#1f78b4", "Poisson"), ("nb", "#e31a1c", "negative binomial")):
        x_hat, P, S = lab[dist]
        axs[0].plot(np.exp(P[:, 0]), 1 / (1 + np.exp(-P[:, 1])), ".", ms=2.5, color=c, alpha=0.5, label=lab_name)
        lo, med, hi = np.quantile(S, [0.025, 0.5, 0.975], axis=0)
        axs[1].fill_between(T_ALL, lo, hi, color=c, alpha=0.18, lw=0)
        axs[1].plot(T_ALL, med, color=c, lw=1.2, label=lab_name)
    axs[0].set_xlabel("$r$"); axs[0].set_ylabel("$p$"); axs[0].legend(frameon=False, markerscale=3)
    axs[1].plot(T_ALL, Y_ALL, "o", color="0.45", ms=2.5)
    axs[1].axvline(LAB_ORIGIN + 0.5, color="0.7", lw=0.8, ls=":")
    axs[1].set_xlabel("week"); axs[1].set_ylabel("weekly cases"); axs[1].set_ylim(0, 1.4 * Y_ALL.max())
    axs[1].xaxis.set_major_locator(MaxNLocator(integer=True))
    for a, l in zip(axs, "ab"):
        a.text(-0.18, 1.02, f"({l})", transform=a.transAxes, fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(FIGS, "ch9_bootstrap_lab.pdf"), metadata={"CreationDate": None})
    plt.close(fig)
    # Fig 3: scores and weights by origin
    fig, axs = plt.subplots(1, 2, figsize=(6.4, 2.9))
    for m in NAMES + ["Ensemble"]:
        per = []
        for t0 in ORIGINS:
            obs = [(t0 + 1 + j) for j in range(H) if t0 + 1 + j < len(Y_ALL)]
            per.append(len(obs))
        w = np.array(res[m]["wis"]); idx = np.cumsum([0] + per)
        axs[0].plot(ORIGINS, [w[idx[i]:idx[i + 1]].mean() for i in range(len(ORIGINS))], "-o", ms=3, color=cols[m],
                    lw=1.6 if m == "Ensemble" else 1.0, label=m)
    axs[0].set_xlabel("last calibration week"); axs[0].set_ylabel("mean WIS, horizons 1-4"); axs[0].set_yscale("log")
    axs[0].legend(frameon=False, fontsize=7)
    bottom = np.zeros(len(ORIGINS))
    for m in NAMES:
        v = np.array([weights[t0][m] for t0 in ORIGINS])
        axs[1].bar(ORIGINS, v, bottom=bottom, width=1.5, color=cols[m], label=m)
        bottom += v
    axs[1].set_xlabel("last calibration week"); axs[1].set_ylabel("AICc weight")
    axs[1].legend(frameon=False, fontsize=7, loc="center left", bbox_to_anchor=(1.0, 0.5))
    for a in axs:
        a.xaxis.set_major_locator(MaxNLocator(integer=True))
    for a, l in zip(axs, "ab"):
        a.text(-0.18, 1.02, f"({l})", transform=a.transAxes, fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(FIGS, "ch9_forecast_scores.pdf"), metadata={"CreationDate": None})
    plt.close(fig)
    with open(VALS, "w") as fh:
        fh.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
