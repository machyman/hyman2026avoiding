# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- own R0 = 2.0 synthetic regime.
"""
ch8_central_comparison.py -- Figure 8.x for Chapter 8, section sec:central-comparison.

Replaces the pre-v2_0_0 single-curve figure, which illustrated a claim
(factor-for-factor propagation of an N^c error into R0) that was withdrawn.

The figure now illustrates Proposition 8.2: an incidence-only fit determines
R0 only through k = N_a / (rho * N_true), and how steeply it does so depends on
choices in the fitting procedure. The infected-viewpoint estimate is flat in
every panel because k does not appear in it.

Panels (each varying ONE choice, all else held fixed):
  (a) fitting window      -- early/pre-peak vs through-peak
  (b) seed parameterization -- seed as a count vs as a fraction of N_a
  (c) loss function       -- unweighted least squares vs Poisson weighting

Outputs: figs/ch8_central_comparison.pdf
Evidence base: ch8_route_b_probe.py, _robustness.py, _lossfn_diagnostic.py,
               _ascertainment.py, _identifiability.py
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares

plt.rcParams.update({'text.usetex':True,'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})
B, Rd, G, O = '#1f5fa8', '#c0392b', '#2e7d32', '#e08214'

def despine(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)

# ---------------- model ----------------
N_TRUE, R0_TRUE, TAU_R = 100_000.0, 2.0, 7.0
GAMMA = 1.0 / TAU_R
I0_TRUE = 10.0

def incidence(R0, I0, N, T, n):
    beta = R0 * GAMMA
    def rhs(t, y):
        S, I = y
        inc = beta * S * I / N
        return [-inc, inc - GAMMA * I]
    te = np.linspace(0, T, n + 1)
    sol = solve_ivp(rhs, [0, T], [N - I0, I0], t_eval=te,
                    rtol=1e-9, atol=1e-9, dense_output=True)
    out = np.empty(n)
    for k in range(n):
        ts = np.linspace(te[k], te[k + 1], 15)
        y = sol.sol(ts)
        out[k] = np.trapezoid(beta * y[0] * y[1] / N, ts)
    return out

def fit_R0(data, N_a, T, n, seed='count', loss='ls'):
    """Incidence-only fit of R0 under an assumed population N_a."""
    def resid(p):
        R0 = np.exp(p[0])
        I0 = np.exp(p[1]) if seed == 'count' else (I0_TRUE / N_TRUE) * N_a
        m = incidence(R0, I0, N_a, T, n)
        r = m - data
        return r / np.sqrt(np.maximum(m, 1.0)) if loss == 'poisson' else r
    if seed == 'count':
        out = least_squares(resid, [np.log(1.5), np.log(20.0)], method='lm', xtol=1e-12)
    else:
        out = least_squares(lambda p: resid([p[0], 0.0]), [np.log(1.5)], method='lm', xtol=1e-12)
    return float(np.exp(out.x[0]))

def fit_R0_fixed_seed(data, N_a, T, n, loss='ls'):
    """Incidence-only fit with the seed KNOWN (amplitude is informative)."""
    def resid(p):
        m = incidence(np.exp(p[0]), I0_TRUE, N_a, T, n)
        r = m - data
        return r / np.sqrt(np.maximum(m, 1.0)) if loss == 'poisson' else r
    out = least_squares(resid, [np.log(1.5)], method='lm', xtol=1e-12)
    return float(np.exp(out.x[0]))

# ---------------- data ----------------
T_FULL, N_FULL = 120, 120
truth = incidence(R0_TRUE, I0_TRUE, N_TRUE, T_FULL, N_FULL)
peak = int(np.argmax(truth))
T_EARLY = 30

ks = np.array([1/3, 1/2, 1, 2, 3, 5, 10, 30], dtype=float)

def curve(T, n, seed, loss):
    return np.array([fit_R0(truth[:n], k * N_TRUE, T, n, seed, loss) for k in ks])

series = {
    'a': [(curve(T_EARLY, T_EARLY, 'count', 'ls'),  'early window (pre-peak)',  B,  '-',  'o'),
          (curve(T_FULL,  N_FULL,  'count', 'ls'),  'window through the peak',  Rd, '--', 's')],
    'b': [(curve(T_EARLY, T_EARLY, 'count',    'ls'), 'seed as a count',            B,  '-',  'o'),
          (curve(T_EARLY, T_EARLY, 'fraction', 'ls'), 'seed as a fraction of $N^c_a$', O, '--', 'v')],
    'c': [(np.array([fit_R0_fixed_seed(truth, k*N_TRUE, T_FULL, N_FULL, 'ls')      for k in ks]),
           'unweighted least squares', Rd, '--', 's'),
          (np.array([fit_R0_fixed_seed(truth, k*N_TRUE, T_FULL, N_FULL, 'poisson') for k in ks]),
           'Poisson weighting',        G,  '-.', 'D')],
}
titles = {'a': '(a) fitting window', 'b': '(b) seed parameterization', 'c': '(c) loss function (seed known)'}

fig, axes = plt.subplots(1, 3, figsize=(10.6, 3.5), sharey=True)
for ax, key in zip(axes, ['a', 'b', 'c']):
    for y, lab, c, ls, mk in series[key]:
        ax.semilogx(ks, y, ls, color=c, lw=1.6, marker=mk, ms=4, label=lab)
    # infected viewpoint: exactly flat, k does not enter
    ax.axhline(R0_TRUE, color='0.25', lw=1.8, ls=':',
               label=r'infected viewpoint $\hat\alpha/(\gamma_R+\nu_m)$')
    ax.axhline(1.0, color='0.75', lw=0.9)
    ax.text(ks[0]*1.05, 1.03, 'invasion threshold', fontsize=7, color='0.45')
    ax.set_xscale('log')
    ax.set_xticks([1/3, 1, 3, 10, 30])
    ax.set_xticklabels(['1/3', '1', '3', '10', '30'])
    ax.set_xlabel(r'$k = N^c_a/(\rho N^c_{\mathrm{true}})$')
    ax.set_title(titles[key], fontsize=10)
    ax.set_ylim(0.8, 3.7)
    ax.legend(fontsize=7.2, frameon=False, loc='upper right')
    despine(ax)
axes[0].set_ylabel(r'fitted $\hat{\mathcal{R}}_0$')
fig.tight_layout()
fig.savefig('figs/ch8_central_comparison.pdf', bbox_inches='tight')
print('ch8_central_comparison.pdf written')

# ---------------- worked-example verification (Section sec:worked-example) ----------------
# The worked example has J_obs = 200/day, I_obs = 800, tau_R = 7 -> R0_hat = 1.75.
# Saturation bound: R0_hat cannot fall below 1, so the largest attainable gap is R0 itself.
R0_WE = 1.75
truth_we = incidence(R0_WE, I0_TRUE, N_TRUE, T_FULL, N_FULL)
r_k1  = fit_R0(truth_we, N_TRUE,      T_FULL, N_FULL)
r_k30 = fit_R0(truth_we, 30 * N_TRUE, T_FULL, N_FULL)
print(f'worked example (R0 = {R0_WE}): k=1 -> {r_k1:.3f}, k=30 -> {r_k30:.3f}, '
      f'ratio {r_k1/r_k30:.2f} (saturation bound {R0_WE:.2f})')
