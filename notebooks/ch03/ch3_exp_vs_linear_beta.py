# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- illustrative transmission-function forms; no BASE parameters consumed.
"""
ch3_exp_vs_linear_beta.py -- Figure for Chapter 2 (fig:exp-vs-linear-beta).

Compares the exact per-contact transmission probability

    beta = 1 - exp(-rho * tau_c)

with the linear approximation beta ~ rho * tau_c, and marks the region in which
the linear form is within 10 percent of the exact value.

Note on the filename: the output is `figs/ch3_exp_vs_linear_beta.pdf`, a legacy
name from before the chapters were renumbered. The figure now appears in
Chapter 2. The name is retained so the existing \includegraphics reference and
the asset registry stay consistent.

This generator was written to close a reproducibility gap: the PDF existed in
`figs/` with no script behind it, so it could not be regenerated or verified,
and it was invisible to both the integrity check and the registry.

Determinism: no RNG is used. Set SOURCE_DATE_EPOCH before running so the PDF
bytes are reproducible (see figs_src/REPRODUCIBILITY.md).

Output: figs/ch3_exp_vs_linear_beta.pdf
"""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family': 'serif', 'font.size': 10,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})
B, Rd, G, O = '#1f5fa8', '#c0392b', '#2e7d32', '#e08214'

# region where the linear approximation stays within 10% of the exact value
X_VALID = 0.194

x = np.linspace(0, 3, 601)
exact = 1.0 - np.exp(-x)
linear = x

fig, ax = plt.subplots(figsize=(6.4, 4.0))

ax.axvspan(0, X_VALID, color=O, alpha=0.18, lw=0)
ax.axhline(1.0, color='0.6', lw=0.9, ls='-')

ax.plot(x, exact, '-', color=B, lw=1.9,
        label=r'exact: $\beta = 1 - e^{-\rho\tau_c}$')
ax.plot(x, linear, '--', color=Rd, lw=1.7,
        label=r'linear: $\beta \approx \rho\tau_c$')

ax.text(X_VALID / 2, 1.30, 'within 10%', ha='center', fontsize=8, color='#8a5a12')
ax.annotate(r'$\beta = 1$', xy=(2.72, 1.0), xytext=(2.72, 1.06),
            ha='right', fontsize=8, color='0.4')
ax.annotate('linear exceeds unity\n(not a probability)', xy=(1.0, 1.0),
            xytext=(1.30, 0.55), fontsize=8, color=Rd,
            arrowprops=dict(arrowstyle='->', color=Rd, lw=0.8))

ax.set_xlim(0, 3)
ax.set_ylim(0, 1.45)
ax.set_xlabel(r'contact-level transmission dose $\rho\tau_c$')
ax.set_ylabel(r'per-contact transmission probability $\beta$')
ax.legend(frameon=False, fontsize=9, loc='lower right')
for s in ('top', 'right'):
    ax.spines[s].set_visible(False)

fig.tight_layout()
fig.savefig('figs/ch3_exp_vs_linear_beta.pdf', bbox_inches='tight')
print('ch3_exp_vs_linear_beta.pdf written'
      f'  (linear within 10% for rho*tau_c <= {X_VALID})')
