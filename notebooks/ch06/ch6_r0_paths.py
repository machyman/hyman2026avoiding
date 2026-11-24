"""From entries to stage numbers to the host reproductive number and R0.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 5 (Section 5.3.1, Reading the Next-Generation
Matrix; Figure 5.2, label fig:r0-paths). Reproduces (written to figs/):
  ch6_r0_paths.pdf -- (a) COMPUTED: the next-generation matrix of the dengue model of Chapter 18 on the states at
                 infection (I_h, E_v), each entry written as P alpha tau and printed with its value, the stage
                 numbers R0^{h->v} = a b_v m tau_R* and R0^{v->h} = p_EIP a b_h tau_v^m, from Chapter 18's printed
                 parameters (a 0.5, b_h 0.4, b_v 0.4, m 2, mu_v 0.07, tau_v^E 9 days with the Erlang k = 3 EIP
                 survival, gamma_R 1/7, nu_m 3.4e-5 per day); (b) the host-vector loop: the host reproductive number
                 is the product of the two stage numbers, and R0 = rho(K) its square root; (c) ILLUSTRATIVE entries
                 with the same R0 = 2: a cycle host -> A -> B -> host (the host number is the product of three
                 entries, R0 its cube root), and a Zika-like model with a host-to-host loop (the host number is the
                 path sum K_hh + K_hv K_vh, and R0^2 is not equal to it).

Every printed number is computed below from unrounded inputs and printed (F-275.19). Deterministic; no random
stream. Run with SOURCE_DATE_EPOCH=1750000000 MPLBACKEND=pdf under the book's figure pin
(protocols/figure_pin_requirements.txt). It needs a LaTeX installation (text.usetex).

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-10-28   Version 1.2 (R276.14, Session 276: the infected mosquito's state at infection is E_v, as in
         Figure 5.1; D7 of the independent check). Version 1.1 (RG-281 Phase 1, Session 276: rebuilt to match the Session 275 draft of
                      Figure 5.2 sent to Z. Qu, after the Session 275 stage was lost, F-276.1)
         Version 1.0 (Session 275, lost with the stage)
"""
import os
import numpy as np, matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch

plt.rcParams.update({'text.usetex': True, 'font.family': 'serif', 'font.size': 9,
                     'mathtext.fontset': 'cm', 'axes.linewidth': 0.8,
                     'text.latex.preamble': r'\usepackage{amsmath}'})
B, Rd, O, Gy = '#1f5fa8', '#c0392b', '#e08214', '0.55'
FG, FO, FGy = '#d4e4d1', '#f6e3cb', '#e4e4e4'          # fills: host (green), vector (orange), other type (grey)
RH = r'\mathcal{R}_0^{\text{host}}'


def rho(K):
    return float(max(abs(np.linalg.eigvals(np.asarray(K, float)))))


def host_number(K, hosts):
    """Host reproductive number rho(K11 + K12 (I - K22)^{-1} K21), hosts listed first by index."""
    K = np.asarray(K, float); n = K.shape[0]
    h = list(hosts); o = [i for i in range(n) if i not in h]
    K11, K12, K21, K22 = K[np.ix_(h, h)], K[np.ix_(h, o)], K[np.ix_(o, h)], K[np.ix_(o, o)]
    assert rho(K22) < 1, 'the non-host types sustain transmission alone: no host number (a reservoir)'
    return rho(K11 + K12 @ np.linalg.solve(np.eye(len(o)) - K22, K21))


# --- (a), (b): dengue, Chapter 18 baseline (days) ---
a, b_h, b_v, m, mu_v, tauE, gam_R, nu_m = 0.5, 0.4, 0.4, 2.0, 0.07, 9.0, 1 / 7, 3.4e-5
p_EIP = (1 + mu_v * tauE / 3) ** -3                     # Erlang k = 3 EIP survival, Chapter 18 eq:b-eff
tau_R = 1 / (gam_R + nu_m)                              # tau_R*, time an infected person stays infectious
tau_vm = 1 / mu_v                                       # tau_v^m, infectious mosquito lifespan
R_hv = 1 * a * b_v * m * tau_R                          # one infected person -> mosquitoes (P = 1)
R_vh = p_EIP * a * b_h * tau_vm                         # one infected mosquito -> people (P = p_EIP)
Kd = np.array([[0.0, R_vh], [R_hv, 0.0]])               # order (I_h, E_v); K[i, j]: type i caused by one type j
R0d, Rhd = rho(Kd), host_number(Kd, [0])
print(f'dengue: p_EIP {p_EIP:.6f}; R0^(h->v) {R_hv:.6f}; R0^(v->h) {R_vh:.6f}')
print(f'dengue: R0 = rho(K) {R0d:.6f}; host number {Rhd:.6f} (product {R_hv * R_vh:.6f}); '
      f'herd 1-1/Rhost {100 * (1 - 1 / Rhd):.2f} percent, 1-1/R0 {100 * (1 - 1 / R0d):.2f} percent')

# --- (c) ILLUSTRATIVE: a three-type cycle and a Zika-like model ---
k_hA, k_AB, k_Bh = 4.0, 1.0, 2.0                        # host -> A -> B -> host
Kc = np.array([[0, 0, k_Bh], [k_hA, 0, 0], [0, k_AB, 0]])  # order (host, A, B)
R0c, Rhc = rho(Kc), host_number(Kc, [0])
print(f'cycle: host number {Rhc:.6f}; R0 {R0c:.6f}; cube root of host number {Rhc ** (1 / 3):.6f}')
K_hh, K_hv, K_vh = 0.5, 1.5, 2.0                        # people infect people; vector -> host; host -> vector
Kz = np.array([[K_hh, K_hv], [K_vh, 0.0]])              # order (h, v)
R0z, Rhz = rho(Kz), host_number(Kz, [0])
print(f'Zika-like: host number {Rhz:.6f} (= K_hh + K_hv K_vh = {K_hh + K_hv * K_vh:.6f}); R0 {R0z:.6f}; '
      f'R0^2 {R0z ** 2:.6f}')


def node(ax, xy, text, fc, r=0.42):
    ax.add_patch(Circle(xy, r, facecolor=fc, edgecolor='0.7', lw=0.8, zorder=2))
    ax.text(*xy, text, ha='center', va='center', fontsize=8.5, zorder=3)


def arrow(ax, p, q, color, rad=0.0, shrink=15):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f'arc3,rad={rad}', arrowstyle='-|>', mutation_scale=9,
                                 color=color, lw=1.3, shrinkA=shrink, shrinkB=shrink, zorder=1))


fig = plt.figure(figsize=(7.4, 2.9))

# (a) the dengue matrix
ax = fig.add_axes([0.0, 0.121, 0.33, 0.817]); ax.set_xlim(-1.3, 2.35); ax.set_ylim(-0.95, 3.05); ax.axis('off')
lab = [r'$I_h$', r'$E_v$']
sym = {(0, 1): r'$p_{\mathrm{EIP}}\cdot ab_h\cdot\tau_v^m$', (1, 0): r'$1\cdot ab_v m\cdot\tau_R^*$'}
val = {(0, 1): R_vh, (1, 0): R_hv}
col = {(0, 1): B, (1, 0): O}
for i in range(2):
    for j in range(2):
        y = 1 - i
        ax.add_patch(Rectangle((j, y), 1, 1, facecolor=col.get((i, j), 'white'),
                               alpha=0.22 if (i, j) in col else 1.0, edgecolor='0.3', lw=0.6))
        if (i, j) in sym:
            ax.text(j + 0.5, y + 0.64, sym[(i, j)], ha='center', va='center', fontsize=6.6)
            ax.text(j + 0.5, y + 0.3, f'{val[(i, j)]:.2f}', ha='center', va='center', fontsize=8, color='0.25')
        else:
            ax.text(j + 0.5, y + 0.5, '0', ha='center', va='center', fontsize=8, color='0.5')
    ax.text(-0.12, 1 - i + 0.5, lab[i], ha='right', va='center', fontsize=9)
    ax.text(i + 0.5, 2.12, lab[i], ha='center', va='bottom', fontsize=9)
ax.text(1.0, 2.5, 'caused by one case in', ha='center', va='bottom', fontsize=7.5)
ax.text(-0.72, 1.0, 'new infections in', rotation=90, ha='center', va='center', fontsize=7.5)
ax.text(1.0, -0.12, 'entries $=$ stage numbers\n'
        r'$\mathcal{R}_0^{h\to v}$ and $\mathcal{R}_0^{v\to h}$', ha='center', va='top', fontsize=7.5, color='0.3')
ax.set_title(r'(a) Dengue: $P \cdot \alpha \cdot \tau$', fontsize=9.5, x=0.53, y=1.0)

# (b) the host-vector loop
bx = fig.add_axes([0.35, 0.121, 0.31, 0.817]); bx.set_xlim(0, 4); bx.set_ylim(-1.0, 3.14); bx.set_aspect('equal', adjustable='datalim'); bx.axis('off')
hp, vp = (0.85, 1.35), (3.15, 1.35)
node(bx, hp, 'host', FG, 0.46); node(bx, vp, 'vector', FO, 0.46)
arrow(bx, (hp[0] + 0.2, hp[1] + 0.4), (vp[0] - 0.2, vp[1] + 0.4), O, rad=-0.45, shrink=2)
arrow(bx, (vp[0] - 0.2, vp[1] - 0.4), (hp[0] + 0.2, hp[1] - 0.4), B, rad=-0.45, shrink=2)
bx.text(2.0, 2.4, f'{R_hv:.2f}', ha='center', va='center', fontsize=8.5, color=O)
bx.text(2.0, 0.3, f'{R_vh:.2f}', ha='center', va='center', fontsize=8.5, color=B)
bx.text(2.0, -0.15, rf'around the loop: ${RH} \approx {Rhd:.2f}$', ha='center', va='center', fontsize=8)
bx.text(2.0, -0.68, rf'per step: $\mathcal{{R}}_0 = \rho(\mathbf{{K}}) = \sqrt{{{RH}}} \approx {R0d:.2f}$',
        ha='center', va='center', fontsize=8)
bx.set_title('(b) Two steps per host generation', fontsize=9.5)

# (c) product and path sum
cx = fig.add_axes([0.655, 0.121, 0.345, 0.817]); cx.set_xlim(-0.05, 5.15); cx.set_ylim(-0.95, 3.88)
cx.set_aspect('equal', adjustable='datalim'); cx.axis('off')
P_h, P_A, P_B = (0.55, 1.95), (2.05, 1.95), (1.3, 0.75)
node(cx, P_h, 'host', FG); node(cx, P_A, r'$A$', FGy); node(cx, P_B, r'$B$', FGy)
arrow(cx, P_h, P_A, '0.15'); arrow(cx, P_A, P_B, '0.15'); arrow(cx, P_B, P_h, '0.15')
cx.text(1.3, 2.28, f'{k_hA:g}', ha='center', va='center', fontsize=7.5)
cx.text(1.93, 1.28, f'{k_AB:g}', ha='center', va='center', fontsize=7.5)
cx.text(0.62, 1.28, f'{k_Bh:g}', ha='center', va='center', fontsize=7.5)
cx.text(1.3, -0.28, rf'${RH} = {Rhc:g}$', ha='center', va='center', fontsize=7.5)
cx.text(1.3, -0.62, rf'$\mathcal{{R}}_0 = {Rhc:g}^{{1/3}} = {R0c:g}$', ha='center', va='center', fontsize=7.5)
Q_h, Q_v = (3.75, 1.95), (3.75, 0.62)
node(cx, Q_h, 'host', FG); node(cx, Q_v, 'vector', FO)
arrow(cx, (Q_h[0] + 0.32, Q_h[1] + 0.32), (Q_h[0] - 0.32, Q_h[1] + 0.32), Rd, rad=1.25, shrink=1)
arrow(cx, (Q_h[0] + 0.22, Q_h[1] - 0.38), (Q_v[0] + 0.22, Q_v[1] + 0.38), O, rad=-0.35, shrink=1)
arrow(cx, (Q_v[0] - 0.22, Q_v[1] + 0.38), (Q_h[0] - 0.22, Q_h[1] - 0.38), B, rad=-0.35, shrink=1)
cx.text(4.4, 2.75, f'{K_hh:g}', ha='center', va='center', fontsize=7.5, color=Rd)
cx.text(4.35, 1.28, f'{K_vh:g}', ha='center', va='center', fontsize=7.5, color=O)
cx.text(3.1, 1.28, f'{K_hv:g}', ha='center', va='center', fontsize=7.5, color=B)
cx.text(3.7, -0.28, rf'${RH} = {K_hh:g} + {K_vh:g} \cdot {K_hv:g} = {Rhz:g}$', ha='center', va='center',
        fontsize=7.0)
cx.text(3.7, -0.62, rf'$\mathcal{{R}}_0 = {R0z:g},\ \mathcal{{R}}_0^2 \neq {RH}$', ha='center', va='center',
        fontsize=7.5)
cx.set_title('(c) Product and path sum', fontsize=9.5)

os.makedirs('figs', exist_ok=True)
fig.savefig('figs/ch6_r0_paths.pdf'); plt.close(fig); print('r0_paths ok')
