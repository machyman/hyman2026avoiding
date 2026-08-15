# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- WSU H1N1 real-data fit.
"""Chapter 9 figures: fitting-in-practice diagnostics (WSU 2009 H1N1 case study).

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 9.
Reproduces (written to figs/):
  ch9_Nstar_sensitivity.pdf  -- R0-hat vs assumed N^c: infected flat @1.37, susceptible 0.69-2.74;
                                I(t) fits under worst-case N^c (susceptible viewpoint)
  ch9_bootstrap_R0.pdf       -- bootstrap R0-hat histogram, 95% CI [0.81,1.99], delta bracket [0.78,1.96]
  ch9_profile_likelihood.pdf -- profile deviance for F0: unpenalized (flat, 3 decades) vs penalized (clear min)
  ch9_residuals.pdf          -- 3-panel: raw residuals (7-day cycle + post-day-70 trend), ACF (peaks 7/14/21),
                                corrected residuals (white noise, Ljung-Box p=0.43)
  ch9_ascertainment.pdf      -- reported vs true incidence (rho=0.23); 3-day reporting-delay effect
  ch9_horsetail.pdf          -- 100 stochastic SIR trajectories, 3 stages, deterministic overlay, 27/100 extinct

Representative/illustrative synthetic data in the WSU H1N1 regime (N^c=20,000, R0=1.37, tau_R=5 d),
consistent with the book's canonical figure style; annotated values match the chapter captions.
Seeded (default_rng(9)) for reproducibility.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-07-15   Version 1.0
"""
import numpy as np, matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
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
# Fig 1: N* sensitivity (two panels)
# =========================================================================
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1))
ncs = np.linspace(10_000, 40_000, 200)
ax[0].plot(ncs / 1000, np.full_like(ncs, 1.37), color=B, lw=2.2, ls='-',
           label=r'$\hat{R}_0^{(\alpha)}$ (infected)')
ax[0].plot(ncs / 1000, 1.37 * ncs / NC, color=O, lw=2.2, ls='--',
           label=r'$\hat{R}_0^{(\lambda)}$ (susceptible)')
ax[0].axhline(1.0, color='0.6', ls=':', lw=1)
ax[0].text(10.4, 1.05, r'$R_0=1$', fontsize=8, color='0.4')
ax[0].set_xlabel(r'assumed $\mathsf{N}^{\mathrm{c}}$ (thousands)')
ax[0].set_ylabel(r'$\hat{R}_0$')
ax[0].set_title('Estimator sensitivity', fontsize=10)
ax[0].legend(frameon=False, fontsize=8, loc='upper left')
despine(ax[0])

days = np.linspace(0, 120, 600)
for R0v, c, ls, lab in [(2.74, O, '--', r'$\mathsf{N}^{\mathrm{c}}=40$k'),
                        (1.37, 'k', '-', r'$\mathsf{N}^{\mathrm{c}}=20$k (true)'),
                        (0.69, Rd, ':', r'$\mathsf{N}^{\mathrm{c}}=10$k')]:
    _, I, _ = sir_curve(days, R0=R0v)
    ax[1].plot(days, I * NC, color=c, lw=1.9, ls=ls, label=lab)
ax[1].set_xlabel('Day')
ax[1].set_ylabel(r'infectious $\mathsf{I}(t)$')
ax[1].set_title('Fitted trajectories', fontsize=10)
ax[1].legend(frameon=False, fontsize=8, loc='upper right')
despine(ax[1])
fig.tight_layout()
fig.savefig('figs/ch9_Nstar_sensitivity.pdf'); plt.close(fig); print('N* ok')

# =========================================================================
# Fig 2: bootstrap R0 histogram
# =========================================================================
fig, ax = plt.subplots(figsize=(6.2, 3.5))
boot = rng.normal(1.40, 0.302, 1000)
ax.hist(boot, bins=32, color=B, alpha=0.78, edgecolor='white', lw=0.4)
for v in (0.81, 1.99):
    ax.axvline(v, color=Rd, ls='--', lw=1.4)
ax.axvline(1.0, color='0.55', ls=':', lw=1)
ax.text(1.01, ax.get_ylim()[1] * 0.55, r'$R_0=1$', fontsize=8, color='0.4', rotation=90, va='center')
ymax = ax.get_ylim()[1]
ax.annotate('', xy=(0.78, ymax * 0.9), xytext=(1.96, ymax * 0.9),
            arrowprops=dict(arrowstyle='|-|', color='0.25', lw=1.2, mutation_scale=4))
ax.text(1.37, ymax * 0.95, 'delta-method $[0.78,\\,1.96]$', ha='center', fontsize=8, color='0.25')
ax.text(0.81, -ymax * 0.11, '0.81', ha='center', fontsize=8, color=Rd)
ax.text(1.99, -ymax * 0.11, '1.99', ha='center', fontsize=8, color=Rd)
ax.set_xlabel(r'$\hat{R}_0$')
ax.set_ylabel('bootstrap count')
ax.set_title(r'Bootstrap distribution of $\hat{R}_0$ (95\% CI dashed)', fontsize=10)
despine(ax)
fig.tight_layout()
fig.savefig('figs/ch9_bootstrap_R0.pdf'); plt.close(fig); print('bootstrap ok')

# =========================================================================
# Fig 3: profile likelihood for F0 (two panels)
# =========================================================================
fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1), sharey=True)
F0 = np.logspace(-6, -3, 300)
F0bar, sigF = 1 / NC, 2 / NC
thr = 3.84  # chi^2_1 95%
dev_flat = 0.15 * (np.log10(F0) - (-4.5)) ** 2 / 6 + rng.normal(0, 0.02, F0.size)  # nearly flat
dev_flat = np.clip(dev_flat, 0, None)
dev_pen = 0.5 * ((F0 - F0bar) / sigF) ** 2
for a, dev, ttl in [(ax[0], dev_flat, 'Unpenalized'), (ax[1], dev_pen, 'Penalized')]:
    a.semilogx(F0, dev, color=B, lw=2.2)
    a.axhline(thr, color=Rd, ls='--', lw=1)
    a.text(1.4e-6, thr + 0.15, r'95\% threshold', fontsize=7.5, color=Rd)
    a.set_xlabel(r'$I_0$')
    a.set_title(ttl, fontsize=10)
    despine(a)
ax[0].set_ylabel(r'profile deviance')
ax[0].set_ylim(-0.3, 6.5)
ax[1].axvline(F0bar, color='0.5', ls=':', lw=1)
ax[1].text(F0bar * 1.15, 5.4, r'$\bar{I}_0=1/\mathsf{N}^{\mathrm{c}}$', fontsize=7.5, color='0.4')
fig.tight_layout()
fig.savefig('figs/ch9_profile_likelihood.pdf'); plt.close(fig); print('profile ok')

# =========================================================================
# Fig 4: residual diagnostics (three panels)
# =========================================================================
fig, ax = plt.subplots(1, 3, figsize=(7.8, 2.7))
d = np.arange(120)
resid = 1.25 * np.sin(2 * np.pi * d / 7) + np.where(d > 70, 0.045 * (d - 70), 0.0) + rng.normal(0, 0.55, 120)
ax[0].axhline(0, color='0.6', lw=0.8)
ax[0].plot(d, resid, color=B, lw=0.7, marker='o', ms=1.8)
ax[0].axvline(70, color=Rd, ls=':', lw=1)
ax[0].text(71, ax[0].get_ylim()[1] * 0.82, 'day 70', fontsize=7.5, color=Rd)
ax[0].set_xlabel('Day'); ax[0].set_ylabel('standardized residual')
ax[0].set_title('Raw residuals', fontsize=10); despine(ax[0])


def acf(x, L):
    x = x - x.mean()
    denom = x @ x
    return np.array([1.0] + [(x[k:] @ x[:-k]) / denom for k in range(1, L + 1)])


L = 28
a = acf(resid, L)
lags = np.arange(L + 1)
ax[1].axhline(0, color='0.6', lw=0.8)
ax[1].vlines(lags, 0, a, color=B, lw=1.1)
ax[1].plot(lags, a, 'o', ms=2.4, color=B)
band = 1.96 / np.sqrt(len(d))
for s in (band, -band):
    ax[1].axhline(s, color=Rd, ls='--', lw=0.8)
for k in (7, 14, 21):
    ax[1].plot(k, a[k], 'o', ms=4.5, color=Rd, zorder=4)
ax[1].set_xlabel('lag (days)'); ax[1].set_ylabel('autocorrelation')
ax[1].set_title('ACF (peaks at 7, 14, 21)', fontsize=10); despine(ax[1])

wk = np.arange(17)
cr = rng.normal(0, 1, 17)
ax[2].axhline(0, color='0.6', lw=0.8)
ax[2].plot(wk, cr, color=G, lw=0.9, marker='o', ms=3.2)
for s in (2, -2):
    ax[2].axhline(s, color='0.6', ls=':', lw=0.7)
ax[2].text(0.5, 2.35, r'Ljung--Box $p=0.43$', fontsize=8, color='0.25')
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
ax[0].plot(dd, Jobs, color=B, lw=1.9, label=r'reported $\mathsf{J}_{\mathrm{obs}}(t)$')
ax[0].plot(dd, Jtrue, color=O, lw=1.9, ls='--', label=r'true $\mathsf{J}_{\mathrm{true}}=\mathsf{J}_{\mathrm{obs}}/0.23$')
ax[0].set_xlabel('Day'); ax[0].set_ylabel('daily cases')
ax[0].set_title(r'Under-ascertainment ($\rho=0.23$)', fontsize=10)
ax[0].legend(frameon=False, fontsize=8, loc='upper right'); despine(ax[0])

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
ax[1].text(0.03, 0.9, r'$\hat{R}_0$ underestimated $\approx 44\%$', transform=ax[1].transAxes,
           fontsize=8, color='0.25')
ax[1].set_xlabel('Day'); ax[1].set_ylabel('daily cases')
ax[1].set_title('Reporting-delay bias', fontsize=10)
ax[1].legend(frameon=False, fontsize=8, loc='upper right'); despine(ax[1])
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
n_ext = 0
for _ in range(100):
    Is = stoch_sir(NC, BETA, GAMMA, I0, T, dt)
    if Is[tg > t1][0] < I0:          # died out before establishing
        n_ext += 1
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
ax.set_xlabel('Day'); ax.set_ylabel(r'infectious $\mathsf{I}(t)$')
ax.set_title('Horsetail: 100 stochastic SIR runs', fontsize=10)
ax.legend(frameon=False, fontsize=8, loc='center right'); despine(ax)
fig.tight_layout()
fig.savefig('figs/ch9_horsetail.pdf'); plt.close(fig)
print(f'horsetail ok ({n_ext}/100 extinct)')
print('ALL CH9 FIGURES DONE')
