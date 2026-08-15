# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- Route B synthetic regime (R0 = 2.0).
import numpy as np
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch8_route_b_robustness.py')).read().split('ratios=')[0])
rng=np.random.default_rng(23)
truth=sim(beta_true,I0_true,N_true,120,120,'SIR')
peak=int(np.argmax(truth))
I_path=None
# rebuild prevalence path for alpha-hat
from scipy.integrate import solve_ivp
def paths(beta,I0,N,T,n):
    def rhs(t,y):
        S,I=y; inc=beta*S*I/N; return [-inc,inc-gamma*I]
    te=np.linspace(0,T,n+1)
    s=solve_ivp(rhs,[0,T],[N-I0,I0],t_eval=te,rtol=1e-10,atol=1e-10,dense_output=True)
    return s.y[0],s.y[1]
S_p,I_p=paths(beta_true,I0_true,N_true,120,120)
I_mid=0.5*(I_p[:120]+I_p[1:121])

print("=== (1) does rho cancel in alpha-hat ? ===")
for rJ,rI,lab in [(0.23,0.23,'matched   rho_J=rho_I=0.23'),
                  (0.23,0.46,'mismatched rho_J=0.23, rho_I=0.46'),
                  (0.10,0.60,'mismatched rho_J=0.10, rho_I=0.60')]:
    a=(rJ*truth)/(rI*I_mid); R=a/gamma
    print(f"  {lab:36s} R_e-hat at day 0 = {R[0]:5.3f}   (truth 2.0; predicted bias factor rho_J/rho_I = {rJ/rI:.3f})")

print("\n=== (2) DEGENERACY TEST: is ignoring rho the same as over-assuming N^c by 1/rho ? ===")
def fitR(data,N_a,T,n): return fit(data,N_a,T,n,'SIR','free')
for rho in (0.5,0.23):
    a=fitR(rho*truth, N_true, 120,120)          # observed rho*J, assume correct N
    b=fitR(truth,     N_true/rho, 120,120)      # true J, assume N too large by 1/rho
    print(f"  rho={rho}:  ignore-rho fit R0_hat = {a:5.3f}   |   over-assume N^c by {1/rho:.2f}x -> {b:5.3f}   (difference {abs(a-b):.4f})")

print("\n=== (3) magnitude of the ascertainment-induced R0 bias (through-peak, incidence only) ===")
for rho in (1.0,0.5,0.23,0.10):
    R=fitR(rho*truth, N_true, 120,120)
    print(f"  rho={rho:4.2f} ignored:  R0_hat = {R:5.3f}  ({(R/2.0-1)*100:+6.1f}% vs truth)")
print("\n=== (4) early-phase, same test ===")
for rho in (1.0,0.5,0.23):
    R=fitR(rho*truth[:30], N_true, 30,30)
    print(f"  rho={rho:4.2f} ignored:  R0_hat = {R:5.3f}  ({(R/2.0-1)*100:+6.1f}%)")
