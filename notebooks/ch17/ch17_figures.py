"""Chapter 17 figure and numbers: what the infected-viewpoint ratio recovers in the COVID-19 case study.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 17 (Integrated Case Studies: Introduction and
COVID-19). Reproduces (written to figs/):
  ch17_alpha_hat.pdf -- COMPUTED: the chapter's SEIAR_I model (eq. covid-model-v2) at its Section 17.4 baseline,
                        run from a small seed. (a) symptomatic onsets J_obs = p gamma_E E, symptomatic prevalence I
                        and total prevalence I + A. (b) what three conversions of the case-count ratio report,
                        against the true R0 of eq. covid-R0: the SIR_I reading R0 = alpha_hat/(gamma_R + nu_m), the
                        relation that carries the latent period, (1 + r tau_E)(1 + r tau_R), and symptomatic onsets
                        divided by total prevalence, times tau_R.

Every number Chapter 17 quotes from this analysis is computed below and printed: the growth rate and the ratio
alpha_hat = J_obs/I = r + gamma_R + mu_d + nu_m; the three conversions and the p = 1 control; the track terms; the
exact sensitivity of R0 to tau_R and the delta-method bracket at the chapter's printed indices; the Monte Carlo
interval on the delta method's ranges; the final sizes of the scenarios; and the asymptomatic infectious period at
which the asymptomatic share of R0 falls to one half.

The model is the chapter's, with its stated assumption that the two tracks share the infectious period tau_R. No
random stream is drawn except default_rng(178) for the Monte Carlo interval (Latin hypercube, n = 200,000).

Run with SOURCE_DATE_EPOCH=1750000000 for byte-identical output under the book's pinned environment
(REPRODUCIBILITY.md in the companion repository). It needs a LaTeX installation (text.usetex).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-11   Version 1.0 (RG-178.1 rows a, c, d, e and f; Session 179)
Revised: 2026-10-11   Version 1.1 (independent check: the right panel's labels print three decimals; the
                      Monte Carlo comment states the standard deviations the code uses; figs/ is created)
"""
import os
import numpy as np, matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.stats import norm, qmc
plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})
B, Rd, G, O = '#1f5fa8', '#c0392b', '#2e7d32', '#e08214'   # blue, red, green, orange


def despine(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


# --- Chapter 17, Section 17.4 baseline (days) ---
BASE = dict(tauE=4.0, tauR=7.0, tauA=7.0, cI=5.0, cA=10.0, bI=0.05, bA=0.05, p=0.6, mud=7e-4, num=1 / (80 * 365))


def tracks(q):
    """The symptomatic and asymptomatic terms of eq. covid-R0, latent factor included."""
    gE = 1 / q['tauE']
    f = gE / (gE + q['num'])
    return (f * q['p'] * q['cI'] * q['bI'] / (1 / q['tauR'] + q['mud'] + q['num']),
            f * (1 - q['p']) * q['cA'] * q['bA'] / (1 / q['tauA'] + q['num']))


def R0(q):
    return sum(tracks(q))


def growth_rate(q, latent=True):
    """Dominant eigenvalue of the linearized (E, I, A) system at the disease-free state (S = 1)."""
    gE, gR, gA, mud, nu, p = 1 / q['tauE'], 1 / q['tauR'], 1 / q['tauA'], q['mud'], q['num'], q['p']
    kI, kA = q['cI'] * q['bI'], q['cA'] * q['bA']
    if latent:
        J = np.array([[-(gE + nu), kI, kA], [p * gE, -(gR + mud + nu), 0.0], [(1 - p) * gE, 0.0, -(gA + nu)]])
    else:                                   # SIAR_I: infection enters I or A directly
        J = np.array([[p * kI - (gR + mud + nu), p * kA], [(1 - p) * kI, (1 - p) * kA - (gA + nu)]])
    return float(max(np.linalg.eigvals(J).real))


q = BASE
r0, (tI, tA) = R0(q), tracks(q)
gR, gE = 1 / q['tauR'], 1 / q['tauE']
r = growth_rate(q)
ahat = r + gR + q['mud'] + q['num']
sir = ahat / (gR + q['num'])            # the SIR_I reading of the ratio
lat = (1 + r * q['tauE']) * (1 + r * q['tauR'])
# symptomatic onsets over total prevalence in the growth phase, from the dominant eigenvector
w, V = np.linalg.eig(np.array([[-(gE + q['num']), q['cI'] * q['bI'], q['cA'] * q['bA']],
                               [q['p'] * gE, -(gR + q['mud'] + q['num']), 0.0],
                               [(1 - q['p']) * gE, 0.0, -(gR + q['num'])]]))
E_, I_, A_ = np.abs(V[:, int(np.argmax(w.real))].real)
mism = q['p'] * gE * E_ / (I_ + A_) * q['tauR']
print('Baseline (Section 17.4)')
print(f'  R0 {r0:.4f}; symptomatic term {tI:.4f}, asymptomatic term {tA:.4f}; asymptomatic share {tA / r0:.4f}')
a1 = q['cI'] * q['bI'] / (gR + q['mud'] + q['num']); a2 = q['cA'] * q['bA'] / (gR + q['num'])
print(f'  per-track quotients {a1:.4f}, {a2:.4f}; bracket terms {q["p"] * a1:.4f} + {(1 - q["p"]) * a2:.4f}'
      f' = {q["p"] * a1 + (1 - q["p"]) * a2:.4f}; latent factor {gE / (gE + q["num"]):.6f}')
print(f'  S_p = (p/R0)(q_I - q_A): p/R0 {q["p"] / r0:.4f}; q_I - q_A {a1 - a2:.4f}; S_p {q["p"] / r0 * (a1 - a2) * gE / (gE + q["num"]):.4f};'
      f' S_cI = S_bI {tI / r0:.4f}; S_cA = S_bA {tA / r0:.4f}; S_cA/S_cI {tA / tI:.3f}')
print(f'  growth rate r {r:.5f} per day; alpha_hat = J_obs/I = r + gamma_R + mu_d + nu_m = {ahat:.4f}')
print(f'  SIR_I reading alpha_hat/(gamma_R + nu_m) {sir:.4f} ({sir / r0:.1%}); 1 + r/(gamma_R + nu_m) {1 + r / (gR + q["num"]):.4f}')
print(f'  latent-aware conversion (1 + r tau_E)(1 + r tau_R) {lat:.4f} ({lat / r0:.1%})')
print(f'  symptomatic onsets over total prevalence, times tau_R {mism:.4f} ({mism / r0:.1%})')
q1 = dict(q, p=1.0)
q1['cI'] = r0 / (gE / (gE + q['num']) / (gR + q['mud'] + q['num'])) / q['bI']
r1 = growth_rate(q1)
print(f'  control p = 1 at the same R0: SIR_I reading {(r1 + gR + q["mud"] + q["num"]) / (gR + q["num"]) / R0(q1):.1%}; '
      f'latent-aware {(1 + r1 * q["tauE"]) * (1 + r1 * q["tauR"]) / R0(q1):.1%}')
rs = growth_rate(q, latent=False)
r0s = R0(q) * (gE + q['num']) / gE
print(f'  SIAR_I (no latent stage): SIR_I reading {(rs + gR + q["mud"] + q["num"]) / (gR + q["num"]) / r0s:.1%}')

# --- sensitivity of R0 to tau_R, and the delta method at the chapter's printed indices (l. 213 to 222) ---
S_tauR = (tI * gR / (gR + q['mud'] + q['num']) + tA * gR / (gR + q['num'])) / r0
terms = [round(round(S_tauR, 3) ** 2 * 0.10 ** 2, 4), 0.0029, 0.0029, 0.0073, 0.0073, 0.0013]
Vd = sum(terms); sd = np.sqrt(Vd)
print(f'Delta method: S_tauR exact {S_tauR:.4f}; terms {terms}; V {Vd:.4f}; relative SD {sd:.4f};'
      f' interval at 2.45 [{2.45 * (1 - 1.96 * sd):.3f}, {2.45 * (1 + 1.96 * sd):.3f}];'
      f' shares tau_R {terms[0] / Vd:.1%}, c_A {terms[3] / Vd:.1%}, beta_A {terms[4] / Vd:.1%},'
      f' rest {(terms[1] + terms[2] + terms[5]) / Vd:.1%}')
print(f'  the same bracket at the exact R0 {r0:.3f}: [{r0 * (1 - 1.96 * sd):.3f}, {r0 * (1 + 1.96 * sd):.3f}]; 1.96 SD {1.96 * sd:.4f}')
print(f'  S_tauR split if tau_A is restored: tau_R {tI * gR / (gR + q["mud"] + q["num"]) / r0:.3f},'
      f' tau_A {tA * gR / (gR + q["num"]) / r0:.3f}')

# --- Monte Carlo interval on the delta method's ranges, with its standard deviations: each 95% half-width over 2
#     (tau_R 0.10, c_I and beta_I 0.125, c_A and beta_A 0.15, relative), p's 0.10 over 1.96 (0.051, absolute) ---
U = qmc.LatinHypercube(d=6, rng=np.random.default_rng(178)).random(200_000)
Z = norm.ppf(U)
tauR_s = 7 * (1 + 0.10 * Z[:, 0]); cI_s = 5 * (1 + 0.125 * Z[:, 1]); bI_s = 0.05 * (1 + 0.125 * Z[:, 2])
cA_s = 10 * (1 + 0.15 * Z[:, 3]); bA_s = 0.05 * (1 + 0.15 * Z[:, 4]); p_s = 0.6 + 0.051 * Z[:, 5]
f = gE / (gE + q['num'])
Rs = f * (p_s * cI_s * bI_s / (1 / tauR_s + q['mud'] + q['num']) + (1 - p_s) * cA_s * bA_s / (1 / tauR_s + q['num']))
print(f'Monte Carlo (n = 200,000, seed 178): 95% interval [{np.percentile(Rs, 2.5):.3f}, {np.percentile(Rs, 97.5):.3f}];'
      f' median {np.median(Rs):.3f}')

# --- final sizes, closed population: z = 1 - exp(-R0 z) ---
print('Final sizes (closed population, nu_m = 0):')
for lab, ch in (('baseline', {}), ('masking', dict(bI=0.025, bA=0.025)), ('isolation', dict(cI=1.25)),
                ('combined', dict(bI=0.025, bA=0.025, cI=1.25, cA=5.0))):
    RR = R0(dict(q, num=0.0, **ch))
    z = brentq(lambda x: x - (1 - np.exp(-RR * x)), 1e-9, 1.0) if RR > 1 else 0.0
    print(f'  {lab:<10s} R0 {RR:.4f}  final size {z:.4f}')

# --- the asymptomatic infectious period at which the asymptomatic share is one half (F-117.4) ---
tA_half = brentq(lambda x: (lambda tt: tt[1] / sum(tt) - 0.5)(tracks(dict(q, tauA=x))), 1.0, 14.0)
print(f'Asymptomatic share falls to one half at tau_A = {tA_half:.2f} days ({tA_half / q["tauR"]:.3f} tau_R)')

# --- the figure: the chapter's model from a small seed (normalized; S(0) = 1) ---
def rhs(t, y):
    S, E, I, A = y
    lam = q['cI'] * q['bI'] * I + q['cA'] * q['bA'] * A
    return [q['num'] - lam * S - q['num'] * S, lam * S - (gE + q['num']) * E,
            q['p'] * gE * E - (gR + q['mud'] + q['num']) * I, (1 - q['p']) * gE * E - (gR + q['num']) * A]


T = 80.0
tt = np.linspace(0.0, T, 1601)
sol = solve_ivp(rhs, (0, T), [1 - 1e-6, 1e-6, 0.0, 0.0], t_eval=tt, rtol=1e-10, atol=1e-16, method='LSODA')
S_, E_t, I_t, A_t = sol.y
J = q['p'] * gE * E_t
ok = tt >= 2.0
ah = J[ok] / I_t[ok]
rt = np.gradient(np.log(I_t[ok]), tt[ok])
conv_sir = ah / (gR + q['num'])                             # the SIR_I reading of the ratio
conv_lat = (1 + rt * q['tauE']) * (1 + rt * q['tauR'])
conv_mis = J[ok] / (I_t[ok] + A_t[ok]) * q['tauR']
k = np.argmin(abs(tt[ok] - 60.0))
print(f'Figure, day 60: alpha_hat {ah[k]:.4f}; SIR_I {conv_sir[k]:.4f}; latent-aware {conv_lat[k]:.4f};'
      f' mismatched {conv_mis[k]:.4f}; S {S_[ok][k]:.6f}')

fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1))
a0 = tt >= 0.5
ax[0].semilogy(tt[a0], J[a0], color=B, lw=1.9, label=r'symptomatic onsets $J_{\rm obs}$ (per day)')
ax[0].semilogy(tt[a0], I_t[a0], color=Rd, lw=1.9, ls='--', label=r'symptomatic prevalence $i$')
ax[0].semilogy(tt[a0], (I_t + A_t)[a0], color=G, lw=1.9, ls=':', label=r'total prevalence $i + A$')
ax[0].set_xlim(0, T); ax[0].set_ylim(1e-8, 1e-2)
ax[0].set_xlabel('day'); ax[0].set_ylabel('fraction of the population')
ax[0].set_title('The model from a small seed', fontsize=10)
ax[0].legend(frameon=False, fontsize=7.5, loc='upper left')
despine(ax[0])
x = tt[ok]
ax[1].axhline(r0, color='0.45', ls='--', lw=1.1, zorder=3)
ax[1].text(40.0, r0 + 0.13, r'true $\mathcal{R}_0 = %.3f$ (dashed)' % r0, fontsize=7.5, color='0.35', ha='center')
ax[1].plot(x, conv_lat, color=B, lw=1.9, label=r'$(1 + r\tau_E)(1 + r\tau_R)$')
ax[1].plot(x, conv_sir, color=O, lw=1.9, ls='--', label=r'SIR reading: $\hat\alpha/(\gamma_R + \nu_m)$')
ax[1].plot(x, conv_mis, color=Rd, lw=1.9, ls=':', label=r'onsets $\div$ total prevalence, $\times\,\tau_R$')
for y, c in ((lat, B), (sir, O), (mism, Rd)):
    ax[1].text(T + 1.0, y, '%.3f' % y, fontsize=7.5, color=c, va='center')
ax[1].set_xlim(0, T); ax[1].set_ylim(0, 3.2)
ax[1].set_xlabel('day'); ax[1].set_ylabel(r'reported $\mathcal{R}_0$')
ax[1].set_title(r'What each conversion reports', fontsize=10)
ax[1].legend(frameon=False, fontsize=7.5, loc='lower right')
despine(ax[1])
fig.tight_layout()
os.makedirs('figs', exist_ok=True)
fig.savefig('figs/ch17_alpha_hat.pdf'); plt.close(fig); print('alpha_hat ok')
