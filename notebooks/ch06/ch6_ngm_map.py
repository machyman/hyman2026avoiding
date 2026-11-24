"""Reading the next-generation matrix: where an entry sits says what it means.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 5 (Section 5.2, Reading the Next-Generation
Matrix). Reproduces (written to figs/):
  ch6_ngm_map.pdf -- COMPUTED: the West Nile virus model of Bergsman, Hyman and Manore (2016) with one mosquito
                 population, a resident and a migratory bird host, and a dead-end human host, at their Table 2
                 baseline (10,000 mosquitoes, 500 birds of each kind) with 500 people added (tolerance 5 bites per
                 day, ILLUSTRATIVE). (a) the next-generation matrix on the states at infection, each entry written
                 as P alpha tau and printed with its value; (b) what the matrix says beyond its spectral radius: the
                 mix of new infections by type in each generation (right eigenvector) and the reproductive value of
                 one infected individual of each type (left eigenvector). The loop shares of R0 (entry
                 elasticities) are printed for Chapter 11.

Every number is computed below and printed. Deterministic; no random stream.
Run with SOURCE_DATE_EPOCH=1750000000 under the book's figure pin. It needs a LaTeX installation (text.usetex).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-26   Version 1.0 (RG-278.1 and .2, Session 275; specimen v0.1 the same day)
         Version 1.1 the same day (the independent check: per-generation label; the calendar-time mix and the
                      factors of the migrant/resident ratio printed)
         Version 1.2 the same day (prints the Chapter 11 case study read beyond R0, RG-278.4; figure unchanged)
         Version 1.3 2026-10-29 (Session 277, staged pass 2, S2a-08): the migrant bird's infectious time is labelled
                      tau_mig, not tau_m, which the chapter reserves for the demographic residence time; numbers
                      unchanged
"""
import os
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 9,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8})
B, Rd, G, O, Gy = '#1f5fa8', '#c0392b', '#2e7d32', '#e08214', '0.55'

# --- Bergsman, Hyman and Manore (2016), Table 2 baseline (days) ---
P = dict(bvb=0.9738, bvm=0.8875, biv=0.468, mu_v=0.0666, nu_v=0.1, sig_v=0.25,
         mu_m=0.0014, gam_m=0.2222, del_m=0.0, sig_m=30.0, mu_b=0.0014, gam_b=0.1, del_b=0.26, sig_b=5.0)
N = dict(v=10000.0, b=500.0, m=500.0, h=500.0)
SIG_H = 5.0                                                  # ILLUSTRATIVE: people tolerate 5 bites per day

# residence times and the chance of reaching the infectious state
tau_E = 1 / (P['nu_v'] + P['mu_v'])                          # time an infected mosquito spends in E_v
tau_v = 1 / P['mu_v']                                        # infectious mosquito lifespan
p_v = P['nu_v'] * tau_E                                      # chance of surviving the EIP
tau_b = 1 / (P['gam_b'] + P['mu_b'] + P['del_b'])
tau_m = 1 / (P['gam_m'] + P['mu_m'] + P['del_m'])


def ngm(Nh=N['h']):
    """K on the states at infection (E_v, I_b, I_m, I_h); K[i, j] = new type-i infections per type-j case."""
    sv, sb, sm, sh = P['sig_v'] * N['v'], P['sig_b'] * N['b'], P['sig_m'] * N['m'], SIG_H * Nh
    tot = sb + sm + sh
    bites = sv * tot / (sv + tot)                            # the Chitnis-Cushing-Hyman total biting rate
    K = np.zeros((4, 4))
    for i, s in ((1, sb), (2, sm), (3, sh)):                 # one mosquito infects: p_v * alpha_{v->i} * tau_v
        K[i, 0] = p_v * P['biv'] * (bites * s / tot / N['v']) * tau_v
    K[0, 1] = P['bvb'] * (bites * sb / tot / N['b']) * tau_b  # one bird infects mosquitoes: alpha_{b->v} * tau_b
    K[0, 2] = P['bvm'] * (bites * sm / tot / N['m']) * tau_m
    return K


def perron(K):
    w, V = np.linalg.eig(K); i = int(np.argmax(w.real)); R = float(w[i].real)
    r = np.abs(V[:, i].real); r = r / r.sum()
    w2, U = np.linalg.eig(K.T); j = int(np.argmax(w2.real)); l = np.abs(U[:, j].real); l = l / (l @ r)
    return R, r, l


K = ngm()
R0, r, l = perron(K)
E = np.outer(l, r) * K / R0                                  # entry elasticities; they sum to 1
K0 = ngm(Nh=0.0)
names = ['mosquitoes', 'resident birds', 'migrant birds', 'people']
print('Residence times (days): tau_E', round(tau_E, 3), 'tau_v', round(tau_v, 3), 'tau_b', round(tau_b, 3),
      'tau_mig', round(tau_m, 3), '; p_v', round(p_v, 4))
print('K =\n', np.round(K, 4))
print(f'R0 {R0:.4f} (without people {perron(K0)[0]:.4f}; Bergsman et al. report 3.46)')
for n_, a_, b_ in zip(names, r, l):
    print(f'  {n_:15s} share of new infections {a_:.4f}; reproductive value {b_:.4f}')
print(f'  loop shares of R0: resident {2 * E[0, 1]:.4f}, migrant {2 * E[0, 2]:.4f}; sum of elasticities {E.sum():.6f}')
print(f'  column sums {np.round(K.sum(0), 4)}')
ratio = l[2] / l[1]
print(f'  one infected migrant is worth {ratio:.1f} infected residents')
print(f'  its factors: bites per bird {P["sig_m"] / P["sig_b"]:.2f} (the assumed feeding preference), per-bite probability'
      f' {P["bvm"] / P["bvb"]:.3f}, infectious time {tau_m / tau_b:.3f}; product'
      f' {P["sig_m"] / P["sig_b"] * P["bvm"] / P["bvb"] * tau_m / tau_b:.2f}')


def realtime_mix(Nh=N['h']):
    """Calendar-time mix of new infections during exponential growth: dominant eigenvector of F - V on
    (E_v, I_v, I_b, I_m, I_h); returns the growth rate and the shares of new infections into E_v, I_b, I_m, I_h."""
    Kq = ngm(Nh)
    # rates per unit time: mosquito infections caused per infectious bird per day, bird infections per I_v per day
    F = np.zeros((5, 5)); Vm = np.zeros((5, 5))
    F[0, 2], F[0, 3] = Kq[0, 1] / tau_b, Kq[0, 2] / tau_m
    for i, k in ((2, 1), (3, 2), (4, 3)):
        F[i, 1] = Kq[k, 0] / (p_v * tau_v)
    Vm[0, 0] = 1 / tau_E; Vm[1, 0] = -P['nu_v']; Vm[1, 1] = 1 / tau_v
    Vm[2, 2], Vm[3, 3], Vm[4, 4] = 1 / tau_b, 1 / tau_m, 1 / tau_b
    w, X = np.linalg.eig(F - Vm); i = int(np.argmax(w.real)); x = np.abs(X[:, i].real)
    new = F @ x; new = new[[0, 2, 3, 4]]
    return float(w[i].real), new / new.sum()


rr, mix_t = realtime_mix()
print(f'  calendar-time growth rate {rr:.4f} per day; mix of new infections during growth (mosquitoes, residents,'
      f' migrants, people): {np.round(mix_t, 4)}')

# --- Chapter 11 case study, sec:two-group-case (essential workers and other adults), read beyond R0 (RG-278.4) ---
# K = beta tau_R* (C^I)^T with the chapter's rounded tau_R* = 1/0.0835 days and beta = 0.040; mixing matrix as printed.
Cw = np.array([[3.6, 3.9], [0.975, 2.025]])
Kw = 0.040 / 0.0835 * Cw.T
Rw, rw, lw = perron(Kw)
Ew = np.outer(lw, rw) * Kw / Rw
print('Chapter 11 case study: K =', np.round(Kw, 4).tolist(), f'R0 {Rw:.4f}')
print(f'  share of each generation\'s new infections: group 1 {rw[0]:.4f}, group 2 {rw[1]:.4f}')
print(f'  reproductive value, group 1 / group 2: {lw[0] / lw[1]:.3f}')
print(f'  entry elasticities: e11 {Ew[0, 0]:.4f}, e12 {Ew[0, 1]:.4f}, e21 {Ew[1, 0]:.4f}, e22 {Ew[1, 1]:.4f};'
      f' column sums (group-1 cases, group-2 cases) {Ew[:, 0].sum():.4f}, {Ew[:, 1].sum():.4f}')
for jj in (0, 1):
    Kc = Kw.copy(); Kc[:, jj] *= 0.9
    print(f'  a 10 percent cut in column {jj + 1} (the transmission of group-{jj + 1} cases): R0 falls'
          f' {100 * (1 - perron(Kc)[0] / Rw):.2f} percent (first order {10 * Ew[:, jj].sum():.2f})')

fig = plt.figure(figsize=(7.4, 3.5))
ax = fig.add_axes([0.0, 0.02, 0.55, 0.92]); ax.set_xlim(-1.5, 4.25); ax.set_ylim(-0.85, 4.75); ax.axis('off')
lab = [r'$E_v$', r'$I_b$', r'$I_m$', r'$I_h$']
sym = {(1, 0): r'$p_v\,\alpha_{v\to b}\,\tau_v$', (2, 0): r'$p_v\,\alpha_{v\to m}\,\tau_v$',
       (3, 0): r'$p_v\,\alpha_{v\to h}\,\tau_v$', (0, 1): r'$\alpha_{b\to v}\,\tau_b$', (0, 2): r'$\alpha_{m\to v}\,\tau_{\mathrm{mig}}$'}
col = {(1, 0): O, (2, 0): O, (3, 0): O, (0, 1): B, (0, 2): B}
for i in range(4):
    for j in range(4):
        y = 3 - i
        fc = col.get((i, j), 'white')
        a = 0.22 if (i, j) in col else 1.0
        ax.add_patch(Rectangle((j, y), 1, 1, facecolor=fc, alpha=a, edgecolor='0.3', lw=0.6))
        if j == 3:
            ax.add_patch(Rectangle((j, y), 1, 1, facecolor='none', edgecolor='0.6', hatch='///', lw=0))
        if (i, j) in sym:
            ax.text(j + 0.5, y + 0.6, sym[(i, j)], ha='center', va='center', fontsize=7.6)
            ax.text(j + 0.5, y + 0.25, f'{K[i, j]:.3g}', ha='center', va='center', fontsize=7.6, color='0.25')
        else:
            ax.text(j + 0.5, y + 0.5, '0', ha='center', va='center', fontsize=8, color='0.5')
    ax.text(-0.12, 3 - i + 0.5, lab[i], ha='right', va='center', fontsize=9)
    ax.text(i + 0.5, 4.12, lab[i], ha='center', va='bottom', fontsize=9)
ax.text(2.0, 4.52, 'caused by one case in', ha='center', va='bottom', fontsize=7.5)
ax.text(-0.72, 2.0, 'new infections in', rotation=90, ha='center', va='center', fontsize=7.5)
ax.text(3.5, -0.32, 'dead-end host:\nzero column', ha='center', va='top', fontsize=7.2, color='0.3')
ax.text(1.0, -0.32, 'zero diagonal: no bird-to-bird or\nmosquito-to-mosquito transmission', ha='center', va='top',
        fontsize=7.2, color='0.3')
ax.set_title(r'(a) The matrix $\mathbf{K}$: entry $=$ $P \cdot \alpha \cdot \tau$', fontsize=9.5, x=0.48, y=1.0)

bx = fig.add_axes([0.66, 0.16, 0.32, 0.70])
y = np.arange(4)[::-1]
bx.barh(y + 0.18, 100 * r, height=0.34, color=O, label=r'share of new infections per generation (\%)')
bx.barh(y - 0.18, 100 * l / l.max(), height=0.34, color=B, label=r'reproductive value (\% of the largest)')
bx.set_yticks(y); bx.set_yticklabels(names, fontsize=8.5)
bx.set_xlim(0, 100); bx.set_xlabel('percent', fontsize=8.5)
for s in ('top', 'right'):
    bx.spines[s].set_visible(False)
bx.legend(frameon=False, fontsize=7.2, loc='lower right', bbox_to_anchor=(1.02, -0.02))
bx.set_title('(b) What the eigenvectors add', fontsize=9.5)
os.makedirs('figs', exist_ok=True)
fig.savefig('figs/ch6_ngm_map.pdf'); plt.close(fig); print('ngm_map ok')
