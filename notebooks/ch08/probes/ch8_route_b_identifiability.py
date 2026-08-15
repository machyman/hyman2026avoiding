# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- Route B synthetic regime (R0 = 2.0).
import numpy as np
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch8_route_b_robustness.py')).read().split('ratios=')[0])
truth=sim(beta_true,I0_true,N_true,120,120,'SIR')
def fitR(data,N_a): return fit(data,N_a,120,120,'SIR','free')

print("CONJECTURE: an incidence-only fit identifies R0 only through the ratio")
print("            k = N_assumed / (rho * N_true)   -- the assumed population")
print("            divided by the EFFECTIVE (ascertained) population.\n")
print("  If true, different (rho, N_a) pairs with the SAME k must give the same R0_hat.\n")
rows=[]
for rho,mult in [(1.0,2.0),(0.5,1.0),(0.25,0.5),(0.1,0.2)]:
    Na=mult*N_true; k=Na/(rho*N_true)
    R=fitR(rho*truth, Na)
    rows.append((rho,mult,k,R))
    print(f"  rho={rho:4.2f}  N_a={mult:4.2f}*N_true   k={k:5.2f}   R0_hat={R:6.4f}")
vals=[r[3] for r in rows]
print(f"\n  spread across identical k: {max(vals)-min(vals):.6f}  -> {'CONFIRMED' if max(vals)-min(vals)<1e-3 else 'REJECTED'}")
print("\n  and the exact-recovery condition k = 1 (N_assumed = rho*N_true):")
for rho in (1.0,0.5,0.23):
    R=fitR(rho*truth, rho*N_true)
    print(f"    rho={rho:4.2f}: assume N_a = rho*N_true -> R0_hat = {R:6.4f}  (truth 2.0)")
