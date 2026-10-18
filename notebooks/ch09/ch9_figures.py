# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- WSU H1N1 real-data fit.
"""Chapter 9 figures: fitting-in-practice diagnostics (WSU 2009 H1N1 regime, illustrative series).

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 9.
Reproduces (written to figs/):
  ch9_Nstar_sensitivity.pdf  -- COMPUTED (v2.4): R0-hat vs assumed N^c. Infected viewpoint: the plateau estimate,
                                which involves no N^c. Susceptible viewpoint: incidence-only Poisson fits of
                                the single-phase model at each N^c, over days 0-66 and through the peak;
                                the through-peak fits at 10k, 20k and 40k against the reported cases
  ch9_bootstrap_R0.pdf       -- COMPUTED (v2.0): residual bootstrap of the plateau fit of alpha-hat(t_k) = J/I,
                                with and without the literature uncertainty in tau_R; delta-method bracket
  ch9_profile_likelihood.pdf -- COMPUTED (v2.6): profile deviance in the seed i0 = I0/N^c on days 0-20 of the
                                series; left alpha and tau_R free, right with the Table 8.1 penalty on tau_R
  ch9_residuals.pdf          -- COMPUTED (v2.0): standardized residuals of a single-phase Poisson fit to the daily
                                series, their ACF, and weekly residuals after the two-phase fit with a real
                                Ljung-Box p-value
  ch9_ascertainment.pdf      -- reported vs true incidence (rho=0.23); 3-day reporting-delay effect
  ch9_horsetail.pdf          -- 100 stochastic SIR trajectories, 3 stages, deterministic overlay

The chapter's illustrative series (v2.0) is generated here, in the WSU H1N1 regime (N^c = 20,000, R0 = 1.37,
tau_R = 5 d, I0 = 5), with two mechanisms the chapter diagnoses: a weekend reporting cycle (80% of Saturday and
Sunday cases reported on the day, the rest on Monday) and a 15% rise in alpha from day 70 (returning students).
Daily prevalence is a census with Poisson counting noise. These three settings were fixed before the first run and
not tuned to any printed number. Every value annotated on the two computed figures is computed below and printed.

Seeds: default_rng(9) is the v1.0 stream for the unchanged figures (its draws are kept in order, so those PDFs are
byte-identical to v1.0); default_rng(2009) draws the series; default_rng(136) draws the bootstrap.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-07-15   Version 1.0
Revised: 2026-10-05   Version 2.0 (F-130.1: bootstrap and residual figures computed from the series)
Revised: 2026-10-05   Version 2.1 (F-137.1: elasticity of R0 in tau_R is 1, not 0.97; delta bracket moves)
Revised: 2026-10-05   Version 2.2 (RG-139: plateau window days 48 to 66, Stage 2 onset to 10 percent infected,
                      because depletion biases J/I = alpha S low by the fraction already infected)
Revised: 2026-10-11   Version 2.3 (F-168.6, RG-168.1d (c): the delay panel carries no bias figure; Chapter 9
                      derives the bias in its text. F-167.1: the horsetail line counts runs that reached I = 0
                      before the epidemic was established, and those already extinct in Stage 1. No plotted
                      path changes: neither edit draws from or reorders a random stream.)
Revised: 2026-10-11   Version 2.4 (F-168.1, RG-168.1a: the N* figure is computed. v2.3 drew 1.37 * N^c / 20,000,
                      the factor-for-factor propagation Chapter 8 withdrew, and forward runs labelled as fits.
                      Now each point is a fit, as Chapter 8 fits; no random stream is drawn.)
Revised: 2026-10-11   Version 2.5 (RG-174.1d: legibility only. The ascertainment panels' legends move to the
                      upper left, clear of the peaks; the N* right panel draws 40k and 10k in colours the left
                      panel does not use. No data, fit or random stream changes.)
Revised: 2026-10-17   Version 2.6 (RG-219.3 (i), F-218.4: the profile figure is computed. v2.5 drew a formula plus
                      noise on the left and the prior alone on the right. Now each point is a profile fit to the first
                      21 days of the series: the deviance minimized over alpha and tau_R (left) or over alpha and
                      tau_R with the Table 8.1 penalty (tau_R - 5)^2/0.7^2 (right), at each fixed seed I0. tau_R is
                      bounded to [0.05, 200] days and the bound is reported. The v1.0 rng(9) draw this figure made
                      is still taken, unused, so the later figures keep their streams.)
"""
import numpy as np, matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.rcParams.update({'text.usetex':True,'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})
rng = np.random.default_rng(9)
B, Rd, G, O = '#1f5fa8', '#c0392b', '#2e7d32', '#e08214'   # blue, red, green, orange


def despine(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


# --- WSU H1N1 representative outbreak: simple SIR (short campus outbreak, demography negligible) ---
R0_WSU, GAMMA, NC = 1.37, 1 / 5.0, 20_000
BETA = R0_WSU * GAMMA


def sir_rhs(t, y, beta=BETA, gamma=GAMMA):
    S, I = y
    return [-beta * S * I, beta * S * I - gamma * I]


def sir_curve(days, R0=R0_WSU, I0=5):
    beta = R0 * GAMMA
    sol = solve_ivp(sir_rhs, [0, days.max()], [1 - I0 / NC, I0 / NC], args=(beta, GAMMA),
                    dense_output=True, rtol=1e-9, atol=1e-12, max_step=0.5)
    S, I = sol.sol(days)
    inc = beta * S * np.clip(I, 0, None)          # incidence rate (fraction of pop per day)
    return S, np.clip(I, 0, None), inc


# =========================================================================
# The chapter's illustrative series (v2.0) and its fits
# =========================================================================
from scipy.optimize import minimize
from scipy.stats import chi2, norm
rng_data = np.random.default_rng(2009)
NDAYS, T_CHANGE, ALPHA_JUMP, WEEKEND_REPORTED = 119, 70, 1.15, 0.80   # 17 weeks; day 0 is a Monday
dd_obs = np.arange(NDAYS)


def daily_model(alpha1, alpha2, I0, t_change=T_CHANGE, n=NDAYS):
    """Expected new cases in each day k (counts over [k, k+1)) and prevalence I(k), SIR with alpha piecewise."""
    def rhs(t, y, a):
        S, I, C = y
        return [-a * S * I, a * S * I - GAMMA * I, a * S * I]
    y0, out_t, out_y = [1 - I0 / NC, I0 / NC, 0.0], [], []
    for (t0, t1, a) in [(0, t_change, alpha1), (t_change, n, alpha2)]:
        tt = np.arange(t0, t1 + 1)
        s = solve_ivp(rhs, [t0, t1], y0, args=(a,), t_eval=tt, rtol=1e-10, atol=1e-13, max_step=0.5)
        out_t.append(s.t[:-1]); out_y.append(s.y[:, :-1]); y0 = s.y[:, -1]
    out_t.append([n]); out_y.append(np.array(y0)[:, None])
    Y = np.concatenate(out_y, axis=1)
    return NC * np.diff(Y[2]), NC * Y[1][:-1]


ALPHA_TRUE = R0_WSU * GAMMA
mu_true, I_true = daily_model(ALPHA_TRUE, ALPHA_JUMP * ALPHA_TRUE, 5)
cases = rng_data.poisson(mu_true)                                   # true new cases by day
dow = dd_obs % 7                                                      # 0 = Monday ... 5 = Saturday, 6 = Sunday
J_obs = cases.copy()
for k in np.where(dow >= 5)[0]:                                       # weekend: part reported, rest carried
    on_day = rng_data.binomial(cases[k], WEEKEND_REPORTED)
    J_obs[k] = on_day
    nxt = k + (7 - dow[k])                                            # the following Monday
    if nxt < NDAYS:
        J_obs[nxt] += cases[k] - on_day
I_obs = rng_data.poisson(I_true)                                      # daily prevalence census


def pois_nll(mu, y):
    mu = np.maximum(mu, 1e-12)
    return float(np.sum(mu - y * np.log(mu)))


def fit(model, x0, y):
    r = minimize(lambda p: pois_nll(model(np.exp(p)), y), np.log(x0), method='Nelder-Mead',
                 options=dict(xatol=1e-9, fatol=1e-9, maxiter=20000, maxfev=20000))
    return np.exp(r.x), r


def weekly(v):
    return v[:NDAYS - NDAYS % 7].reshape(-1, 7).sum(axis=1)


def acf(x, L):
    x = x - x.mean()
    denom = x @ x
    return np.array([1.0] + [(x[k:] @ x[:-k]) / denom for k in range(1, L + 1)])


def ljung_box(x, h):
    n, r = len(x), acf(x, h)[1:]
    Q = n * (n + 2) * np.sum(r ** 2 / (n - np.arange(1, h + 1)))
    return Q, chi2.sf(Q, h)


def runs_test(x):
    s = np.sign(x[x != 0]); n1, n2 = np.sum(s > 0), np.sum(s < 0)
    runs = 1 + np.sum(s[1:] != s[:-1]); n = n1 + n2
    m = 2 * n1 * n2 / n + 1; v = 2 * n1 * n2 * (2 * n1 * n2 - n) / (n ** 2 * (n - 1))
    z = (runs - m) / np.sqrt(v)
    return runs, m, z, 2 * norm.sf(abs(z))


# single-phase fit to the daily series (alpha, I0 free; tau_R = 5 d and N^c fixed)
one = lambda p: daily_model(p[0], p[0], p[1])[0]
p1, _ = fit(one, [0.27, 5.0], J_obs)
mu1 = one(p1)
res1 = (J_obs - mu1) / np.sqrt(mu1)
s2_1 = np.sum(res1 ** 2) / (NDAYS - 2)
acf1 = acf(res1, 28)
band = 1.96 / np.sqrt(NDAYS)
lb_daily = ljung_box(res1, 14)
runs1 = runs_test(res1)
post = dd_obs >= T_CHANGE

# two-phase fit to the weekly series (alpha1, alpha2, I0 free; change point day 70)
Jw = weekly(J_obs)
two_w = lambda p: weekly(daily_model(p[0], p[1], p[2])[0])
p2, _ = fit(two_w, [0.27, 0.31, 5.0], Jw)
mu2w = two_w(p2)
res2w = (Jw - mu2w) / np.sqrt(mu2w)
lb_weekly = {h: ljung_box(res2w, h) for h in (1, 2, 3, 4, 5, 6)}
LB_H = 4
# weekly aggregation alone (single-phase model, weekly counts): does Pattern B survive?
one_w = lambda p: weekly(daily_model(p[0], p[0], p[1])[0])
p1w, _ = fit(one_w, [0.27, 5.0], Jw)
res1w = (Jw - one_w(p1w)) / np.sqrt(one_w(p1w))
lb_weekly_one = ljung_box(res1w, LB_H)
runs1w = runs_test(res1w)

# plateau estimator and its residual bootstrap (Section "Reporting Confidence Intervals")
# Window (RG-139): from Stage 2 onset (600 cumulative cases, 3% of N^c; day 48 on the expected series) to 10 percent
# infected (day 66), before depletion bends J/I = alpha S(t) down. Fixed here so the printed days are the code's days;
# the rule-derived days are printed below as a check (Session 140, MR-140.3).
PLAT_LO, PLAT_HI = 48, 66
PLAT = (dd_obs >= PLAT_LO) & (dd_obs <= PLAT_HI)
a_k = J_obs[PLAT] / I_obs[PLAT]                                       # alpha-hat(t_k) = J/I
n_p, a_bar, a_med = a_k.size, a_k.mean(), np.median(a_k)
cv_day = a_k.std(ddof=1) / a_bar                                      # day-to-day spread of the values
cv_mean = cv_day / np.sqrt(n_p)                                       # sampling CV of the plateau mean
TAU, CV_TAU, S_TAU = 5.0, 0.14, 1.0                                   # R0 = alpha tau_R, nu_m = 0 (F-137.1)
rng_boot = np.random.default_rng(136)
NB = 1000
idx = rng_boot.integers(0, n_p, (NB, n_p))
boot_data = a_k[idx].mean(axis=1) * TAU                               # resample residuals of the constant fit
tau_draw = rng_boot.normal(TAU, CV_TAU * TAU, NB)
boot_full = a_k[idx].mean(axis=1) * tau_draw                          # same resamples, tau_R drawn independently
L_BLK = 7
st = rng_boot.integers(0, n_p - L_BLK + 1, (NB, int(np.ceil(n_p / L_BLK))))
boot_block = np.array([np.concatenate([a_k[s:s + L_BLK] for s in row])[:n_p].mean() for row in st]) * TAU
ci_data, ci_full, ci_block = (np.percentile(b, [2.5, 97.5]) for b in (boot_data, boot_full, boot_block))
R0_hat = a_bar * TAU
se_rel = np.sqrt(cv_mean ** 2 + (S_TAU * CV_TAU) ** 2)
ci_delta = R0_hat * (1 - 1.96 * se_rel), R0_hat * (1 + 1.96 * se_rel)
ci_delta_data = R0_hat * (1 - 1.96 * cv_mean), R0_hat * (1 + 1.96 * cv_mean)
ci_printed = 1.37 * (1 - 1.96 * 0.22), 1.37 * (1 + 1.96 * 0.22)

print('--- series ---')
print(f'cases {cases.sum()}, reported {J_obs.sum()}; cumulative reported at day 22: {J_obs[:23].sum()}; '
      f'600 reached day {int(np.argmax(np.cumsum(J_obs) >= 600))}; peak reported day {int(np.argmax(J_obs))}; '
      f'peak expected incidence day {int(np.argmax(mu_true))}; peak prevalence day {int(np.argmax(I_true))}')
print('--- single-phase daily fit ---')
print(f'alpha {p1[0]:.4f}, I0 {p1[1]:.2f}, R0 {p1[0]*TAU:.3f}; s^2 {s2_1:.2f}')
print('ACF lags beyond band ' + f'{band:.3f}: ' + ', '.join(f'{k}:{acf1[k]:.2f}' for k in range(1, 29) if abs(acf1[k]) > band))
print(f'ACF at 7, 14, 21: {acf1[7]:.3f} {acf1[14]:.3f} {acf1[21]:.3f}')
print(f'Ljung-Box daily h=14: Q {lb_daily[0]:.1f}, p {lb_daily[1]:.2e}')
print(f'runs test daily: runs {runs1[0]}, expected {runs1[1]:.1f}, z {runs1[2]:.2f}, p {runs1[3]:.2e}')
print(f'mean residual before day 70 {res1[~post].mean():+.2f}, from day 70 {res1[post].mean():+.2f}; '
      f'share positive from day 70 {np.mean(res1[post] > 0):.2f}')
wk_pos = [w for w in range(len(res1w)) if res1w[w] > 0]
print(f'weekly, single-phase: LB h={LB_H} p {lb_weekly_one[1]:.3f}; runs p {runs1w[3]:.3f}; '
      f'weeks (1-based) with positive residual: {[w + 1 for w in wk_pos]}')
print('--- two-phase weekly fit ---')
print(f'alpha1 {p2[0]:.4f}, alpha2 {p2[1]:.4f} (ratio {p2[1]/p2[0]:.3f}), I0 {p2[2]:.2f}; '
      f's^2 {np.sum(res2w**2)/(len(Jw)-3):.2f}; n weeks {len(Jw)}')
print('Ljung-Box weekly: ' + ', '.join(f'h={h}: p {v[1]:.3f}' for h, v in lb_weekly.items()))
print('--- plateau and bootstrap ---')
frac_exp = (np.cumsum(mu_true) + 5) / NC                              # expected cumulative fraction infected
print(f'window check: reported 600 reached day {int(np.argmax(np.cumsum(J_obs) >= 600))} (realized), '
      f'10 percent infected day {int(np.argmax(frac_exp >= 0.10))} (expected)')
print(f'plateau days {PLAT_LO}-{PLAT_HI}: n {n_p}; mean {a_bar:.4f}, median {a_med:.4f}; CV day-to-day {cv_day:.3f}; '
      f'CV of mean {cv_mean:.4f}')
print(f'R0-hat mean x tau {R0_hat:.3f}; median x tau {a_med*TAU:.3f}')
print(f'bootstrap, data only (iid residuals): [{ci_data[0]:.3f}, {ci_data[1]:.3f}]')
print(f'bootstrap, data only (7-day blocks):  [{ci_block[0]:.3f}, {ci_block[1]:.3f}]')
print(f'bootstrap, data + tau_R:              [{ci_full[0]:.3f}, {ci_full[1]:.3f}]')
print(f'delta, CV of mean + tau_R term:       [{ci_delta[0]:.3f}, {ci_delta[1]:.3f}]  (SE/R0 {se_rel:.3f})')
print(f'delta, CV of mean only:               [{ci_delta_data[0]:.3f}, {ci_delta_data[1]:.3f}]')
print(f'delta as printed (CV 0.18):           [{ci_printed[0]:.3f}, {ci_printed[1]:.3f}]')
print(f'share of delta variance from tau_R: {(S_TAU*CV_TAU)**2/se_rel**2:.3f}')
print(f'bootstrap share below R0 = 1: data {np.mean(boot_data < 1):.3f}, data + tau_R {np.mean(boot_full < 1):.3f}')


# =========================================================================
# Fig 1: N* sensitivity (two panels), COMPUTED (v2.4; F-168.1, RG-168.1a)
# An incidence-only fit in the susceptible viewpoint: the single-phase SIR with S(0) = 1 - I0/N^c in units of the
# assumed population, tau_R = 5 d fixed, R0 and the seed count I0 free, Poisson likelihood, as Chapter 8 fits
# (prop:incidence-identifiability). Two windows: days 0-66 (before ten percent are infected, the plateau's end) and
# the whole series (through the peak). The infected-viewpoint estimate is the plateau's a_bar * TAU: no N^c in it.
# =========================================================================
def daily_model_na(R0, I0, Na, n):
    """Expected new cases per day over days 0..n-1, single-phase SIR in units of an assumed population Na."""
    a = R0 * GAMMA
    def rhs(t, y):
        S, I, C = y
        return [-a * S * I, a * S * I - GAMMA * I, a * S * I]
    s = solve_ivp(rhs, [0, n], [1 - I0 / Na, I0 / Na, 0.0], t_eval=np.arange(n + 1), rtol=1e-10, atol=1e-13,
                  max_step=0.5)
    return Na * np.diff(s.y[2])


def fit_na(Na, n, starts):
    """Poisson fit of (R0, I0) at assumed population Na over days 0..n-1; best of several Nelder-Mead starts."""
    y = J_obs[:n]
    def nll(p):
        R0v, I0v = np.exp(p)
        if I0v >= Na:
            return 1e30
        return pois_nll(daily_model_na(R0v, I0v, Na, n), y)
    best = None
    for s0 in starts:
        r = minimize(nll, np.log(s0), method='Nelder-Mead',
                     options=dict(xatol=1e-9, fatol=1e-9, maxiter=20000, maxfev=20000))
        if best is None or r.fun < best.fun:
            best = r
    R0v, I0v = np.exp(best.x)
    mu = daily_model_na(R0v, I0v, Na, n)
    dev = 2 * np.sum(np.where(y > 0, y * np.log(np.maximum(y, 1e-12) / mu), 0.0) - (y - mu))
    return R0v, I0v, dev, mu


N_EARLY = 67                                            # days 0-66
NA_GRID = np.arange(10_000, 40_001, 2_000)
STARTS = [(1.4, 5.0), (1.2, 2.0), (2.0, 1.0), (1.6, 20.0)]
R0_inf = a_bar * TAU                                    # infected viewpoint: no N^c anywhere in it
fits = {}
for win, n in (('early', N_EARLY), ('full', NDAYS)):
    prev = None
    for Na in NA_GRID:
        st = STARTS if prev is None else [prev] + STARTS
        R0v, I0v, dev, mu = fit_na(Na, n, st)
        fits[(win, int(Na))] = (R0v, I0v, dev, mu)
        prev = (R0v, I0v)
print(f'N*: infected-viewpoint plateau R0-hat {R0_inf:.3f} (no N^c)')
for win, n in (('early', N_EARLY), ('full', NDAYS)):
    for Na in (10_000, 20_000, 40_000):
        R0v, I0v, dev, mu = fits[(win, Na)]
        print(f'N* {win} (days 0-{n - 1}), N^c {Na}: R0-hat {R0v:.3f}, I0 {I0v:.2f}, deviance {dev:.1f}, '
              f'fitted cases {mu.sum():.0f} of {J_obs[:n].sum()}')
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1))
x = NA_GRID / 1000
ax[0].plot(x, np.full(x.size, R0_inf), color=B, lw=2.2, ls='-',
           label=r'$\hat{\mathcal{R}}_0^{(\alpha)}$ (infected), no $N^{\mathrm{c}}$')
ax[0].plot(x, [fits[('early', int(v))][0] for v in NA_GRID], color=O, lw=2.0, ls='--',
           label=r'$\hat{\mathcal{R}}_0^{(\lambda)}$, fit to days 0--66')
ax[0].plot(x, [fits[('full', int(v))][0] for v in NA_GRID], color=Rd, lw=2.0, ls=':', marker='o', ms=2.5,
           label=r'$\hat{\mathcal{R}}_0^{(\lambda)}$, fit through the peak')
ax[0].axvline(NC / 1000, color='0.6', ls=':', lw=1)
ax[0].text(NC / 1000 + 0.6, 1.24, r'true $N^{\mathrm{c}}$', fontsize=7.5, color='0.4')
ax[0].set_ylim(1.2, 1.7)
ax[0].set_xlabel(r'assumed $N^{\mathrm{c}}$ (thousands)')
ax[0].set_ylabel(r'$\hat{\mathcal{R}}_0$')
ax[0].set_title('Estimator sensitivity', fontsize=10)
ax[0].legend(frameon=False, fontsize=7.5, loc='upper right')
despine(ax[0])

ax[1].plot(dd_obs, J_obs, 'o', ms=1.8, color='0.6', label='reported cases')
for Na, c, ls, lab in [(40_000, G, '-.', r'$N^{\mathrm{c}}=40$k'),
                       (20_000, 'k', '-', r'$N^{\mathrm{c}}=20$k (true)'),
                       (10_000, '#6a3d9a', ':', r'$N^{\mathrm{c}}=10$k')]:
    ax[1].plot(dd_obs, fits[('full', Na)][3], color=c, lw=1.9, ls=ls, label=lab)
ax[1].set_xlabel('Day')
ax[1].set_ylabel('daily cases')
ax[1].set_title('Fits through the peak', fontsize=10)
ax[1].legend(frameon=False, fontsize=7.5, loc='upper left')
despine(ax[1])
fig.tight_layout()
fig.savefig('figs/ch9_Nstar_sensitivity.pdf'); plt.close(fig); print('N* ok')

# =========================================================================
# Fig 2: bootstrap R0 histogram (computed, v2.0)
# =========================================================================
rng.normal(size=1000)   # v1.0 drew its synthetic histogram here; kept so the later figures' stream is unchanged
fig, ax = plt.subplots(figsize=(6.2, 3.5))
bins = np.linspace(min(boot_full.min(), boot_data.min()), max(boot_full.max(), boot_data.max()), 40)
ax.hist(boot_full, bins=bins, color=B, alpha=0.78, edgecolor='white', lw=0.4,
        label=r'$\hat{\alpha}$ resampled, $\tau_R$ drawn')
ax.hist(boot_data, bins=bins, histtype='step', color=O, lw=1.4, label=r'$\hat{\alpha}$ resampled, $\tau_R=5$ fixed')
for v in ci_full:
    ax.axvline(v, color=Rd, ls='--', lw=1.4)
ax.axvline(1.0, color='0.55', ls=':', lw=1)
ymax = ax.get_ylim()[1]
ax.text(min(1.0, ci_full[0]) - 0.015, ymax * 0.3, r'$\mathcal{R}_0=1$', fontsize=8, color='0.4', rotation=90, va='center', ha='right')
ax.annotate('', xy=(ci_delta[0], ymax * 0.9), xytext=(ci_delta[1], ymax * 0.9),
            arrowprops=dict(arrowstyle='|-|', color='0.25', lw=1.2, mutation_scale=4))
ax.text(R0_hat, ymax * 0.95, 'delta-method $[%.2f,\\,%.2f]$' % ci_delta, ha='center', fontsize=8, color='0.25')
for v in ci_full:
    ax.text(v, -ymax * 0.11, '%.2f' % v, ha='center', fontsize=8, color=Rd)
ax.set_xlabel(r'$\hat{\mathcal{R}}_0$')
ax.set_ylabel('bootstrap count')
ax.set_title(r'Bootstrap distribution of $\hat{\mathcal{R}}_0$ (95\% CI dashed)', fontsize=10)
ax.legend(frameon=False, fontsize=7.5, loc='upper right', bbox_to_anchor=(1.0, 0.84))
despine(ax)
fig.tight_layout()
fig.savefig('figs/ch9_bootstrap_R0.pdf'); plt.close(fig); print('bootstrap ok')

# =========================================================================
# Fig 3: profile deviance in the seed (two panels), COMPUTED (v2.6; RG-219.3 (i), F-218.4)
# The first 21 days of the daily series (Stage 1, before depletion). Model: the chapter's SIR with the infectious
# period tau_R free, seeded with I0 infectious people, Poisson deviance. At each fixed I0 the deviance is minimized
# over (alpha, tau_R), log parameters, Nelder-Mead from four starts; tau_R is bounded to [0.05, 200] days. Right
# panel: the same with the Table 8.1 penalty on tau_R, (tau_R - 5)^2 / 0.7^2 (sigma = CV 0.14 x 5 days, lambda = 1).
# Each curve is shown relative to its own minimum. The design is the guide's (solutions/code/ch08_solutions.py).
# =========================================================================
_ = rng.normal(0, 0.02, 300)            # the v1.0 draw of this figure, kept so rng(9)'s later draws do not move
N_PROF, TAU0, SIG_TAU, TAU_LO, TAU_HI = 21, 5.0, 0.7, 0.05, 200.0


def daily_g(alpha, tau, I0, n):
    """Expected new cases per day over days 0..n-1: the SIR above with infectious period tau, seeded with I0."""
    g = 1 / tau
    def rhs(t, y):
        S, I, C = y
        return [-alpha * S * I, alpha * S * I - g * I, alpha * S * I]
    s = solve_ivp(rhs, [0, n], [1 - I0 / NC, I0 / NC, 0.0], t_eval=np.arange(n + 1), rtol=1e-10, atol=1e-13,
                  max_step=0.5)
    return NC * np.diff(s.y[2])


def deviance(mu, y):
    mu = np.maximum(mu, 1e-12)
    return float(2 * np.sum(np.where(y > 0, y * np.log(np.maximum(y, 1e-12) / mu), 0.0) - (y - mu)))


def profile_point(I0, lam_tau, n=N_PROF):
    """Minimum over (alpha, tau_R) of deviance + lam_tau (tau_R - 5)^2 / 0.7^2 at a fixed seed I0."""
    y = J_obs[:n]
    def obj(p):
        a, tau = np.exp(p)
        if tau > TAU_HI or tau < TAU_LO:
            return 1e30
        return deviance(daily_g(a, tau, I0, n), y) + lam_tau * (tau - TAU0) ** 2 / SIG_TAU ** 2
    best = None
    for s0 in [(0.27, 5.0), (0.5, 2.0), (0.2, 10.0), (1.0, 1.0)]:
        r = minimize(obj, np.log(s0), method='Nelder-Mead', options=dict(xatol=1e-8, fatol=1e-8, maxiter=8000,
                                                                      maxfev=8000))
        if best is None or r.fun < best.fun:
            best = r
    return np.exp(best.x[1]), best.fun


thr = chi2.ppf(0.95, 1)
I0_grid = np.logspace(-1, 3, 49)                       # 0.1 to 1,000 index cases, twelve points per decade
prof, taus = {}, {}
for lam in (0.0, 1.0):
    pts = [profile_point(I0, lam) for I0 in I0_grid]
    taus[lam] = np.array([p[0] for p in pts]); f = np.array([p[1] for p in pts]); prof[lam] = f - f.min()


def crossings(I0s, d):
    """Interpolated seeds (log scale) where the profile crosses the 95% threshold, and the grid points inside it."""
    inside = I0s[d < thr]
    lo = hi = None
    k = int(np.argmin(d))
    for j in range(k, 0, -1):
        if d[j - 1] >= thr > d[j]:
            lo = 10 ** np.interp(thr, [d[j], d[j - 1]], np.log10([I0s[j], I0s[j - 1]])); break
    for j in range(k, len(d) - 1):
        if d[j + 1] >= thr > d[j]:
            hi = 10 ** np.interp(thr, [d[j], d[j + 1]], np.log10([I0s[j], I0s[j + 1]])); break
    return inside, lo, hi


for lam, name in ((0.0, 'tau_R free'), (1.0, 'tau_R penalized')):
    inside, lo, hi = crossings(I0_grid, prof[lam])
    print(f'profile ({name}): grid seeds inside {thr:.2f}: {inside.min():.3g} to {inside.max():.3g} cases;'
          f' crossings {lo if lo is None else round(lo, 2)} to {hi if hi is None else round(hi, 2)};'
          f' argmin {I0_grid[int(np.argmin(prof[lam]))]:.3g}; tau_R at the grid ends {taus[lam][0]:.3g},'
          f' {taus[lam][-1]:.3g} d; points at a tau_R bound: {int(np.sum((taus[lam] < 0.0501) | (taus[lam] > 199.9)))}')
    print('  ' + ', '.join(f'{x:.3g}:{d:.2f}(tau {t:.3g})' for x, d, t in zip(I0_grid, prof[lam], taus[lam])))

fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1), sharey=True)
i0 = I0_grid / NC
for a, lam, ttl in [(ax[0], 0.0, r'$\alpha$ and $\tau_R$ free'), (ax[1], 1.0, r'penalty on $\tau_R$')]:
    a.semilogx(i0, prof[lam], color=B, lw=2.2)
    a.axhline(thr, color=Rd, ls='--', lw=1)
    a.text(i0[0] * 1.3, thr + 0.15, r'95\% threshold', fontsize=7.5, color=Rd)
    a.axvline(5 / NC, color='0.5', ls=':', lw=1)
    a.set_xlabel(r'$i_0$')
    a.set_title(ttl, fontsize=10)
    despine(a)
ax[1].text(5 / NC * 1.5, 5.4, r'$5/N^{\mathrm{c}}$ (true seed)', fontsize=7.5, color='0.4')
ax[0].set_ylabel(r'profile deviance')
ax[0].set_ylim(-0.3, 6.5)
fig.tight_layout()
fig.savefig('figs/ch9_profile_likelihood.pdf'); plt.close(fig); print('profile ok')

# =========================================================================
# Fig 4: residual diagnostics (three panels; computed, v2.0)
# =========================================================================
rng.normal(size=120); rng.normal(size=17)   # v1.0 drew its synthetic residuals here; kept for the stream
fig, ax = plt.subplots(1, 3, figsize=(7.8, 2.7))
ax[0].axhline(0, color='0.6', lw=0.8)
ax[0].plot(dd_obs, res1, color=B, lw=0.7, marker='o', ms=1.8)
ax[0].axvline(T_CHANGE, color=Rd, ls=':', lw=1)
ax[0].text(T_CHANGE + 2, ax[0].get_ylim()[1] * 0.9, 'day %d' % T_CHANGE, fontsize=7.5, color=Rd,
           bbox=dict(fc='white', ec='none', pad=0.6))
ax[0].set_xlabel('Day'); ax[0].set_ylabel('standardized residual')
ax[0].set_title('Raw residuals', fontsize=10); despine(ax[0])

L = 28
lags = np.arange(L + 1)
ax[1].axhline(0, color='0.6', lw=0.8)
ax[1].vlines(lags, 0, acf1, color=B, lw=1.1)
ax[1].plot(lags, acf1, 'o', ms=2.4, color=B)
for s in (band, -band):
    ax[1].axhline(s, color=Rd, ls='--', lw=0.8)
for k in (7, 14, 21):
    ax[1].plot(k, acf1[k], 'o', ms=4.5, color=Rd, zorder=4)
ax[1].set_xlabel('lag (days)'); ax[1].set_ylabel('autocorrelation')
ax[1].set_title('ACF (lags 7, 14, 21 marked)', fontsize=10); despine(ax[1])

wk = np.arange(len(res2w))
ax[2].axhline(0, color='0.6', lw=0.8)
ax[2].plot(wk, res2w, color=G, lw=0.9, marker='o', ms=3.2)
for s in (2, -2):
    ax[2].axhline(s, color='0.6', ls=':', lw=0.7)
ax[2].text(0.5, 2.35, r'Ljung--Box $p=%.2f$' % lb_weekly[LB_H][1], fontsize=8, color='0.25')
ax[2].set_ylim(-3, 3)
ax[2].set_xlabel('week'); ax[2].set_ylabel('standardized residual')
ax[2].set_title('After correction', fontsize=10); despine(ax[2])
fig.tight_layout()
fig.savefig('figs/ch9_residuals.pdf'); plt.close(fig); print('residuals ok')

# =========================================================================
# Fig 5: ascertainment + reporting delay (two panels)
# =========================================================================
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1))
dd = np.linspace(0, 120, 400)
_, _, inc = sir_curve(dd)
Jtrue = inc * NC
Jobs = Jtrue * 0.23
ax[0].plot(dd, Jobs, color=B, lw=1.9, label=r'reported $J_{\mathrm{obs}}(t)$')
ax[0].plot(dd, Jtrue, color=O, lw=1.9, ls='--', label=r'true $J_{\mathrm{true}}=J_{\mathrm{obs}}/0.23$')
ax[0].set_xlabel('Day'); ax[0].set_ylabel('daily cases')
ax[0].set_title(r'Under-ascertainment ($\rho=0.23$)', fontsize=10)
ax[0].legend(frameon=False, fontsize=8, loc='upper left'); despine(ax[0])

# reporting delay: smear the true curve with a gamma-ish 3-day-mean kernel
dt = dd[1] - dd[0]
tau = np.arange(0, 15, dt)
kern = (tau / 3.0) * np.exp(-tau / 3.0 * 2)   # peaked near ~1.5 d, mean ~3 d
kern /= kern.sum()
Jdelay = np.convolve(Jtrue, kern, mode='full')[:dd.size]
ax[1].plot(dd, Jtrue, color=O, lw=1.9, label='true incidence')
ax[1].plot(dd, Jdelay, color=B, lw=1.9, ls='--', label='observed (3-day delay)')
pk_t, pk_d = dd[np.argmax(Jtrue)], dd[np.argmax(Jdelay)]
ax[1].axvline(pk_t, color=O, ls=':', lw=0.8)
ax[1].axvline(pk_d, color=B, ls=':', lw=0.8)
# v2.3 (F-168.6): no bias figure here. The panel's own model (tau_R = 5 d, r = 0.074/d) and the text's derivation
# (r = 0.19/d from T = 1.91 d) give different values; the text carries the derivation.
ax[1].set_xlabel('Day'); ax[1].set_ylabel('daily cases')
ax[1].set_title('Reporting-delay bias', fontsize=10)
ax[1].legend(frameon=False, fontsize=8, loc='upper left'); despine(ax[1])
fig.tight_layout()
fig.savefig('figs/ch9_ascertainment.pdf'); plt.close(fig); print('ascertainment ok')

# =========================================================================
# Fig 6: horsetail plot (100 stochastic SIR trajectories, 3 stages)
# =========================================================================
def stoch_sir(N, beta, gamma, I0, T, dt=0.2):
    steps = int(T / dt)
    S, I = N - I0, I0
    Is = np.empty(steps + 1); Is[0] = I
    for j in range(steps):
        if I <= 0:
            Is[j + 1:] = 0
            return Is
        ni = min(rng.poisson(beta * S * I / N * dt), S)
        nr = min(rng.poisson(gamma * I * dt), I)
        S -= ni; I += ni - nr
        Is[j + 1] = max(I, 0)
    return Is


T, dt, I0 = 140.0, 0.2, 5
tg = np.arange(0, T + dt, dt)
det_S, det_I, _ = sir_curve(tg, I0=I0)
det_I = det_I * NC
# stage boundaries: end of early stochastic phase (det I crosses ~1% of peak growth) and peak
t1 = tg[np.argmax(det_I > det_I.max() * 0.05)]     # Stage 1 -> 2
t2 = tg[np.argmax(det_I)]                            # Stage 2 -> 3 (peak; susceptibles thereafter scarce)

fig, ax = plt.subplots(figsize=(6.6, 3.7))
n_ext, n_ext1 = 0, 0
est = det_I.max() * 0.05                            # the Stage 1 -> 2 threshold above
for _ in range(100):
    Is = stoch_sir(NC, BETA, GAMMA, I0, T, dt)
    if (Is == 0).any() and Is.max() < est:   # went extinct before the epidemic was established (F-167.1)
        n_ext += 1
        n_ext1 += int(Is[tg > t1][0] == 0)   # ... already extinct when Stage 1 ended
    # color each trajectory by stage segments
    for (lo, hi, col) in [(0, t1, Rd), (t1, t2, B), (t2, T + 1, G)]:
        m = (tg >= lo) & (tg <= hi)
        ax.plot(tg[m], Is[m], color=col, lw=0.5, alpha=0.35)
ax.plot(tg, det_I, color='k', lw=1.8, zorder=5, label='deterministic')
for tb in (t1, t2):
    ax.axvline(tb, color='0.55', ls='--', lw=0.9)
ax.text(t1 / 2, ax.get_ylim()[1] * 0.92, 'Stage 1', color=Rd, fontsize=8.5, ha='center')
ax.text((t1 + t2) / 2, ax.get_ylim()[1] * 0.92, 'Stage 2', color=B, fontsize=8.5, ha='center')
ax.text((t2 + T) / 2, ax.get_ylim()[1] * 0.92, 'Stage 3', color=G, fontsize=8.5, ha='center')
ax.set_xlabel('Day'); ax.set_ylabel(r'infectious $I(t)$')
ax.set_title('Horsetail: 100 stochastic SIR runs', fontsize=10)
ax.legend(frameon=False, fontsize=8, loc='center right'); despine(ax)
fig.tight_layout()
fig.savefig('figs/ch9_horsetail.pdf'); plt.close(fig)
print(f'horsetail ok ({n_ext}/100 extinct before the epidemic was established, {n_ext1} of them in Stage 1)')
print('ALL CH9 FIGURES DONE')
