"""Chapter 12 (printed Chapter 11) figure: the herd-immunity boundary in the (f1, f2) plane.

Companion text: Foundations and Pitfalls in Epidemic Modeling, printed Chapter 11, Section "Herd Immunity in
Heterogeneous Populations" and the numerical case study (RG-12, finding 12.2; F-130.2 under RG-2; RG-198.2).
Produces figs/ch12_herd_boundary.pdf and prints the numbers the chapter quotes.

The boundary is the set of coverages (f1, f2) with rho(diag(1 - f1, 1 - f2) K) = 1, where K is the next-generation
matrix. Coverage in group j removes the fraction f_j of that group's susceptibles, so it scales row j of K.
  (a) Symmetric groups of equal size with purely between-group contact, R0 = 2: K = [[0, 2], [2, 0]], so the
      boundary is (1 - f1)(1 - f2) = 1/R0^2. Iso-total lines (f1 + f2)/2 = const.
  (b) The chapter's case study: K = (beta/0.0835) [[3.6, 0.975], [3.9, 2.025]], beta = 0.040, group sizes 0.2 and
      0.8. Iso-total lines 0.2 f1 + 0.8 f2 = const. The bipartite rule (1 - f1)(1 - f2) = 1/R0^2 applied to this
      assortative matrix puts the corner at f1 = 0.82, which leaves rho > 1.
Both panels mark uniform coverage (on the diagonal) and the minimum-total allocation.
After the figure, the script prints the contact-weighted threshold the text quotes (F-200.1, RG-200.1): coverage
f_j = k c_j with c = (7.5, 3) on the case study's K, found by bisection on rho = 1; and, for proportionate mixing,
the closed form F = (1 - 1/R0) <c><c^2>/<c^3>, checked against the spectral radius for the text's illustration
(two equal groups, c2 = 2 c1, R0 = 2). These lines do not touch the figure.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-16   Version 1.0
Revised: 2026-10-16   Version 1.1 (Session 201, RG-200.1): prints the contact-weighted thresholds; figure unchanged
Run under the figure pin (protocols/figure_pin_requirements.txt), SOURCE_DATE_EPOCH=1750000000, MPLBACKEND=pdf.
"""
import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 11, 'axes.linewidth': 0.8})
B = '#1f5fa8'; Rd = '#c0392b'; G = '#2e7d32'; Gr = '0.45'


def rho(K, f1, f2):
    return max(abs(np.linalg.eigvals(np.diag([1 - f1, 1 - f2]) @ K)))


def boundary(K, n=801):
    """For each f1, the smallest f2 with rho <= 1 (NaN if none). Bisection; rho decreases in f2."""
    f1s = np.linspace(0, 1, n); f2s = np.full(n, np.nan)
    for i, f1 in enumerate(f1s):
        if rho(K, f1, 0.0) <= 1:
            f2s[i] = 0.0; continue
        if rho(K, f1, 1.0) > 1:
            continue
        lo, hi = 0.0, 1.0
        for _ in range(60):
            m = 0.5 * (lo + hi)
            lo, hi = (m, hi) if rho(K, f1, m) > 1 else (lo, m)
        f2s[i] = hi
    return f1s, f2s


def uniform(K):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = 0.5 * (lo + hi)
        lo, hi = (m, hi) if rho(K, m, m) > 1 else (lo, m)
    return hi


def min_total(K, w):
    f1s, f2s = boundary(K, 20001)
    ok = ~np.isnan(f2s)
    tot = w[0] * f1s[ok] + w[1] * f2s[ok]
    i = np.argmin(tot)
    return f1s[ok][i], f2s[ok][i], tot[i]


R0a = 2.0
Ka = np.array([[0.0, R0a], [R0a, 0.0]])
wa = (0.5, 0.5)
Kb = 0.040 / 0.0835 * np.array([[3.6, 0.975], [3.9, 2.025]])
wb = (0.2, 0.8)

fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.4))
for ax, K, w, tag in ((axes[0], Ka, wa, 'a'), (axes[1], Kb, wb, 'b')):
    f1s, f2s = boundary(K)
    ok = ~np.isnan(f2s)
    ax.fill_between(f1s[ok], f2s[ok], 1.0, color=B, alpha=0.10, lw=0)
    ax.plot(f1s[ok], f2s[ok], color=B, lw=2)
    # iso-total lines w1 f1 + w2 f2 = c
    for c in np.arange(0.1, 1.0, 0.1):
        x = np.linspace(0, 1, 50); y = (c - w[0] * x) / w[1]
        m = (y >= 0) & (y <= 1)
        ax.plot(x[m], y[m], color=Gr, lw=0.6, ls=':')
    fu = uniform(K)
    m1, m2, mt = min_total(K, w)
    ax.plot([fu], [fu], 'o', color=Rd, ms=7, zorder=5)
    ax.plot([m1], [m2], 's', color=G, ms=7, zorder=5, clip_on=False)
    print(f'panel ({tag}): R0 = {rho(K, 0, 0):.4f}; uniform f = {fu:.4f} (total {fu:.4f}); '
          f'minimum total at f1 = {m1:.4f}, f2 = {m2:.4f}, total {mt:.4f}')
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect('equal')
    ax.set_xlabel('coverage of group 1, $f_1$'); ax.set_ylabel('coverage of group 2, $f_2$')
    ax.text(fu + 0.03, fu + 0.03, f'uniform, total {fu:.3f}', color=Rd, fontsize=9)
    ax.text(0.6, 0.86, r'$\mathcal{R}_e < 1$', color=B, fontsize=11)

axes[0].set_title(r'(a) symmetric groups, between-group contact only, $\mathcal{R}_0 = 2$', fontsize=10)
axes[0].plot([0.75], [0.0], 's', color=G, ms=7, zorder=5, clip_on=False)   # the symmetric twin of the minimum
axes[0].text(0.05, 0.79, 'minimum total 0.375', color=G, fontsize=9)
axes[0].text(0.62, 0.05, 'or here', color=G, fontsize=9)
axes[1].set_title(r'(b) the case study, assortative, $\mathcal{R}_0 = 2.35$', fontsize=10)
m1, m2, mt = min_total(Kb, wb)
axes[1].text(0.50, 0.07, f'minimum total {mt:.3f}', color=G, fontsize=9)
# the bipartite rule misapplied: (1 - f1)(1 - f2) = 1/R0^2 with f2 = 0
R0b = rho(Kb, 0, 0); fbad = 1 - 1 / R0b**2
axes[1].plot([fbad], [0.0], 'o', mfc='white', mec='k', ms=7, zorder=6, clip_on=False)
axes[1].annotate(r'bipartite rule: $\mathcal{R}_e = %.2f$' % rho(Kb, fbad, 0.0), xy=(fbad, 0.0), xytext=(0.18, 0.22),
                 fontsize=9, arrowprops=dict(arrowstyle='->', lw=0.7))
print(f'panel (b): bipartite rule corner f1 = {fbad:.4f} (total {0.2 * fbad:.4f}) leaves R_e = {rho(Kb, fbad, 0.0):.4f}; '
      f'f1 = 1, f2 = 0 leaves R_e = {rho(Kb, 1.0, 0.0):.4f}')
fig.tight_layout()
here = os.path.dirname(os.path.abspath(__file__))
fig.savefig(os.path.join(here, '..', 'figs', 'ch12_herd_boundary.pdf'))


# --- v1.1: the contact-weighted threshold (RG-200.1); printed only, after the figure is saved ---
def contact_weighted(K, c, w):
    """Smallest k with rho(diag(1 - k c) K) <= 1, by bisection; returns (f1, f2, total)."""
    lo, hi = 0.0, 1.0 / max(c)
    assert rho(K, hi * c[0], hi * c[1]) <= 1
    for _ in range(60):
        m = 0.5 * (lo + hi)
        lo, hi = (m, hi) if rho(K, m * c[0], m * c[1]) > 1 else (lo, m)
    return hi * c[0], hi * c[1], w[0] * hi * c[0] + w[1] * hi * c[1]


cw1, cw2, cwt = contact_weighted(Kb, (7.5, 3.0), wb)
print(f'panel (b): contact-weighted f_j = k c_j: f1 = {cw1:.4f}, f2 = {cw2:.4f}, total {cwt:.4f} '
      f'(uniform {uniform(Kb):.4f}, minimum total {min_total(Kb, wb)[2]:.4f})')
c_il, n_il, R0_il = np.array([1.0, 2.0]), np.array([0.5, 0.5]), 2.0
mom = [n_il @ c_il**p for p in (1, 2, 3)]
F_closed = (1 - 1 / R0_il) * mom[0] * mom[1] / mom[2]
K_il = np.outer(c_il * n_il, c_il) / mom[0]          # proportionate mixing: K_jk ~ c_j n_j c_k / <c>
K_il *= R0_il / max(abs(np.linalg.eigvals(K_il)))
f1i, f2i, Fi = contact_weighted(K_il, tuple(c_il), tuple(n_il))
print(f'illustration (c2 = 2 c1, equal groups, R0 = 2, proportionate mixing): uniform {uniform(K_il):.4f}; '
      f'contact-weighted closed form {F_closed:.4f}, spectral radius {Fi:.4f} (f1 = {f1i:.4f}, f2 = {f2i:.4f})')
