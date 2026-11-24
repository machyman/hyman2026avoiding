"""Chapter 18 figure and numbers: what the human-side ratio zeta_h = J_h/I_h recovers in the dengue case study.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 18 (Dengue), Section 18.3. Reproduces (written to
figs/):
  ch18_zeta_h.pdf -- COMPUTED: the chapter's bipartite model (eq. dengue-model) at its Section 18.3 baseline, with the
                     extrinsic incubation period as three Erlang stages (the k = 3 form the chapter adopts in
                     eq. b-eff), run from 20 infectious people in a city of 200,000 with no infected mosquitoes.
                     (a) human incidence J_h, human prevalence I_h and infectious mosquitoes I_v.
                     (b) what three readings of the ratio report, against the true R0 of eq. dengue-R0: the
                     cycle-aware conversion with the Erlang EIP, the same conversion with a one-stage EIP, and the
                     vector quasi-equilibrium reading R0 = sqrt(zeta_h/(gamma_R + nu_m)).

Every number Section 18.3 quotes from this analysis is computed below and printed: the growth rate and the doubling
time, zeta_h = r + gamma_R + nu_m, the cycle-aware conversion, the one-stage and quasi-equilibrium readings, the ratio
the quasi-equilibrium relation predicts, the weekly ratios of the exercise's outbreak, and the conversion at twice the
vector density. The model is deterministic; no random stream is drawn.

Run with SOURCE_DATE_EPOCH=1750000000 for byte-identical output under the book's pinned environment
(REPRODUCIBILITY.md in the companion repository). It needs a LaTeX installation (text.usetex).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-26   Version 1.0 (RG-277.5, review F-183.1 rows a and e; Session 275)
"""
import math
import os
import numpy as np, matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})
B, Rd, G, O = '#1f5fa8', '#c0392b', '#2e7d32', '#e08214'   # blue, red, green, orange


def despine(ax):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)


# --- Chapter 18, Section 18.3 baseline (days) ---
P = dict(a=0.5, bh=0.4, bv=0.4, mu=0.07, tE=9.0, gR=1 / 7, m=2.0, nm=1 / (80 * 365))
K = 3                                                       # Erlang stages of the EIP (eq. b-eff)


def p_eip(q, k=K):
    return (1 + q['mu'] * q['tE'] / k) ** (-k)


def R0(q, k=K):
    """eq. dengue-R0 with the EIP survival of k Erlang stages."""
    return q['a'] * math.sqrt(q['bh'] * p_eip(q, k) * q['bv'] * q['m'] / (q['mu'] * (q['gR'] + q['nm'])))


def growth_rate(q, k=K):
    """Dominant eigenvalue of the linearized (I_h, E_1..E_k, I_v) system at the disease-free state."""
    kap, g = k / q['tE'], q['gR'] + q['nm']
    n = k + 2
    J = np.zeros((n, n))
    J[0, 0], J[0, n - 1] = -g, q['a'] * q['bh'] * q['m']     # I_v counted per vector, I_h per host
    J[1, 0], J[1, 1] = q['a'] * q['bv'], -(kap + q['mu'])
    for i in range(2, k + 1):
        J[i, i - 1], J[i, i] = kap, -(kap + q['mu'])
    J[n - 1, k], J[n - 1, n - 1] = kap, -q['mu']
    return float(max(np.linalg.eigvals(J).real))


def cycle(r, q, k=K):
    """Cycle-aware conversion: R0^2 = (1 + r/(gamma_R + nu_m)) (1 + r/mu_v) (1 + r/(k/tau_E + mu_v))^k."""
    g = q['gR'] + q['nm']
    return math.sqrt((1 + r / g) * (1 + r / q['mu']) * (1 + r / (k / q['tE'] + q['mu'])) ** k)


q = P
g = q['gR'] + q['nm']
r0, r = R0(q), growth_rate(q)
zeta = r + g
print('Baseline (Section 18.3), EIP as three Erlang stages')
print(f'  p_EIP {p_eip(q):.4f}; R0 {r0:.4f}; growth rate r {r:.5f} per day (doubling {math.log(2) / r:.2f} days)')
print(f'  zeta_h = r + gamma_R + nu_m = {zeta:.4f} per day')
print(f'  cycle-aware conversion (k = 3) {cycle(r, q):.4f}; with a one-stage EIP {cycle(r, q, 1):.4f}')
print(f'  quasi-equilibrium reading sqrt(zeta_h/(gamma_R + nu_m)) {math.sqrt(zeta / g):.4f} ({math.sqrt(zeta / g) / r0:.1%} of R0)')
print(f'  ratio the quasi-equilibrium relation predicts, R0^2 (gamma_R + nu_m) = {r0 ** 2 * g:.4f} per day'
      f' ({r0 ** 2 * g / zeta:.2f} times the outbreak value)')
print(f'  mu_v/gamma_R {q["mu"] / q["gR"]:.3f}')
r1 = growth_rate(q, 1)
print(f'  model as printed (one E_v stage): R0 {R0(q, 1):.4f}; r {r1:.5f}; zeta_h {r1 + g:.4f};'
      f' its own conversion {cycle(r1, q, 1):.4f}; the k = 3 conversion of its r {cycle(r1, q, 3):.4f}')
q2 = dict(q, m=2 * q['m'])
r2 = growth_rate(q2)
print(f'  twice the vector density (m = {q2["m"]:.0f}): R0 {R0(q2):.4f}; r {r2:.5f}; zeta_h {r2 + g:.4f};'
      f' conversion {cycle(r2, q2):.4f}')

# --- the exercise's outbreak: 200,000 people, 20 infectious, vectors uninfected; Erlang EIP ---
Nh = 200_000.0
Nv = q['m'] * Nh
kap = K / q['tE']


def rhs(t, y):
    Sh, Ih, Rh, Sv, E1, E2, E3, Iv, C = y
    lh = q['a'] * q['bh'] * Iv * Sh / Nh
    lv = q['a'] * q['bv'] * Ih * Sv / Nh
    return [q['nm'] * Nh - lh - q['nm'] * Sh, lh - g * Ih, q['gR'] * Ih - q['nm'] * Rh,
            q['mu'] * Nv - lv - q['mu'] * Sv, lv - (kap + q['mu']) * E1, kap * E1 - (kap + q['mu']) * E2,
            kap * E2 - (kap + q['mu']) * E3, kap * E3 - q['mu'] * Iv, lh]


T = 84
tt = np.linspace(0.0, T, T * 24 + 1)
sol = solve_ivp(rhs, (0, T), [Nh - 20, 20, 0, Nv, 0, 0, 0, 0, 0], t_eval=tt, rtol=1e-10, atol=1e-8, method='LSODA')
Sh, Ih, Iv, C = sol.y[0], sol.y[1], sol.y[7], sol.y[8]
Jh = q['a'] * q['bh'] * Iv * Sh / Nh
print('Exercise outbreak (12 weeks; weekly incidence over seven days of the week\'s mean prevalence)')
wk = []
for w in range(12):
    i0, i1 = w * 168, (w + 1) * 168
    Jw = C[i1] - C[i0]
    Im = np.trapezoid(Ih[i0:i1 + 1], tt[i0:i1 + 1]) / 7
    wk.append(Jw / (7 * Im))
    print(f'  week {w + 1:2d}: cases {Jw:7.1f}; mean prevalence {Im:7.1f}; zeta_h {wk[-1]:.4f};'
          f' end-of-week reading {Jw / (7 * Ih[i1]):.4f}; S_h/N_h {Sh[i1] / Nh:.4f}')
print(f'  weeks 4 to 12: zeta_h {min(wk[3:]):.4f} to {max(wk[3:]):.4f}; S_h/N_h at day 84 {Sh[-1] / Nh:.4f}')

ok = tt >= 14.0
z_t = Jh[ok] / Ih[ok]
r_t = z_t - g
conv3 = np.array([cycle(x, q) for x in r_t])
conv1 = np.array([cycle(x, q, 1) for x in r_t])
qss = np.sqrt(z_t / g)
k = np.argmin(abs(tt[ok] - 60.0))
print(f'Figure, day 60: zeta_h {z_t[k]:.4f}; k = 3 {conv3[k]:.4f}; one-stage {conv1[k]:.4f}; quasi-equilibrium {qss[k]:.4f}')

fig, ax = plt.subplots(1, 2, figsize=(7.4, 3.1))
a0 = tt >= 0.5
ax[0].semilogy(tt[a0], Jh[a0], color=B, lw=1.9, label=r'human incidence $J_h$ (per day)')
ax[0].semilogy(tt[a0], Ih[a0], color=Rd, lw=1.9, ls='--', label=r'human prevalence $I_h$')
ax[0].semilogy(tt[a0], Iv[a0], color=G, lw=1.9, ls=':', label=r'infectious mosquitoes $I_v$')
ax[0].set_xlim(0, T); ax[0].set_ylim(1e-1, 1e4)
ax[0].set_xlabel('day'); ax[0].set_ylabel('number')
ax[0].set_title('The outbreak from 20 cases', fontsize=10)
ax[0].legend(frameon=False, fontsize=7.5, loc='upper left')
despine(ax[0])
x = tt[ok]
ax[1].axhline(r0, color='0.45', ls='--', lw=1.1, zorder=3)
ax[1].text(48.0, r0 + 0.13, r'true $\mathcal{R}_0 = %.3f$ (dashed)' % r0, fontsize=7.5, color='0.35', ha='center')
ax[1].plot(x, conv3, color=B, lw=1.9, label=r'cycle-aware, EIP in three stages')
ax[1].plot(x, conv1, color=G, lw=1.9, ls=':', label=r'cycle-aware, EIP in one stage')
ax[1].plot(x, qss, color=O, lw=1.9, ls='--', label=r'quasi-equilibrium: $\sqrt{\zeta_h/(\gamma_R + \nu_m)}$')
for y, c in ((cycle(r, q), B), (cycle(r, q, 1), G), (math.sqrt(zeta / g), O)):
    ax[1].text(T + 1.0, y, '%.3f' % y, fontsize=7.5, color=c, va='center')
ax[1].set_xlim(0, T); ax[1].set_ylim(0, 3.2)
ax[1].set_xlabel('day'); ax[1].set_ylabel(r'reported $\mathcal{R}_0$')
ax[1].set_title(r'What each reading of $\zeta_h$ reports', fontsize=10)
ax[1].legend(frameon=False, fontsize=7.5, loc='lower right')
despine(ax[1])
fig.tight_layout()
os.makedirs('figs', exist_ok=True)
fig.savefig('figs/ch18_zeta_h.pdf'); plt.close(fig); print('zeta_h ok')
