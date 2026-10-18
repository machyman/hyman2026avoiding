"""Chapter 16 (printed Chapter 15) figure: R0 read from an observed growth rate depends on the generation interval.

Companion text: Foundations and Pitfalls in Epidemic Modeling, printed Chapter 15, the influenza worked example and the
pitfall "Generation Time" (RG-12, finding 16.2; RG-198.4). Produces figs/ch16_generation_interval.pdf and prints the
numbers the chapter quotes.

Euler-Lotka: R0 = 1 / M(-r), r the growth rate (the book's sigma), M the moment generating function of the generation-interval density
(Wallinga and Lipsitch 2007). For a gamma interval with mean Tg and shape k, R0 = (1 + r Tg / k)^k; k = 1 is the
exponential interval (R0 = 1 + r Tg); k -> infinity is the fixed interval (R0 = exp(r Tg)), the upper bound for a
given mean. The chapter's kernel K(tau) proportional to tau^2 exp(-tau) is the gamma case k = 3, Tg = 3 days,
calibrated to R0 = 1.3, so its growth rate is r = 1.3^(1/3) - 1. The compartmental reading takes Tg = 1/gamma_R = 5
days with an exponential interval.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-16   Version 1.0
Run under the figure pin (protocols/figure_pin_requirements.txt), SOURCE_DATE_EPOCH=1750000000, MPLBACKEND=pdf.
"""
import os
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 11, 'axes.linewidth': 0.8})
B = '#1f5fa8'; Rd = '#c0392b'; G = '#2e7d32'; Gr = '0.45'

R0_TRUE = 1.3
TG, K_SHAPE, TG_COMP = 3.0, 3, 5.0
r_obs = R0_TRUE ** (1 / K_SHAPE) - 1          # the worked example's growth rate under its own kernel


def gamma_R(r, Tg, k):
    return (1 + r * Tg / k) ** k


readings = [
    ('fixed interval, $T_g = 3$ d', lambda r: np.exp(r * TG), Gr, '-.', 1.5),
    ('gamma, $k = 3$, $T_g = 3$ d (the chapter\'s kernel)', lambda r: gamma_R(r, TG, K_SHAPE), B, '-', 2.2),
    ('exponential, $T_g = 3$ d', lambda r: 1 + r * TG, G, '--', 1.5),
    ('compartmental reading: exponential, $T_g = 5$ d', lambda r: 1 + r * TG_COMP, Rd, ':', 1.8),
]
r = np.linspace(0, 0.3, 301)
fig, ax = plt.subplots(figsize=(6.6, 4.4))
print(f'observed growth rate r = {r_obs:.4f} per day (doubling time {np.log(2) / r_obs:.2f} d)')
for lab, fn, col, ls, lw in readings:
    ax.plot(r, fn(r), color=col, ls=ls, lw=lw, label=lab)
    ax.plot([r_obs], [fn(r_obs)], 'o', color=col, ms=5, zorder=5)
    print(f'  {lab:55s} R0 = {fn(r_obs):.4f};  at r = 0.3: {fn(0.3):.4f}')
ax.axvline(r_obs, color='0.6', lw=0.7)
ax.axhline(R0_TRUE, color='0.6', lw=0.7)
ax.text(r_obs + 0.004, 1.05, r'observed $\sigma = %.3f$/day' % r_obs, fontsize=9)
ax.text(0.235, R0_TRUE - 0.07, r'true $\mathcal{R}_0 = 1.3$', fontsize=9)
ax.set_xlim(0, 0.3); ax.set_ylim(1, 2.75)
ax.set_xlabel(r'observed early growth rate $\sigma$ (per day)')
ax.set_ylabel(r'inferred $\mathcal{R}_0$')
ax.legend(frameon=False, fontsize=8.5, loc='upper left')
fig.tight_layout()
here = os.path.dirname(os.path.abspath(__file__))
fig.savefig(os.path.join(here, '..', 'figs', 'ch16_generation_interval.pdf'))
