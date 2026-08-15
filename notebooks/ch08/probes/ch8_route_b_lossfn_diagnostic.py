# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- Route B synthetic regime (R0 = 2.0).
import numpy as np
import os
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ch8_route_b_robustness.py')).read().split('ratios=')[0])
truth=sim(beta_true,I0_true,N_true,120,120,'SIR')
print("multistart diagnostic: SIR, fixed_count seed, through-peak, N_a = 3x true")
Na=3*N_true
def sse(R0, weighted):
    m=sim(R0*gamma,I0_true,Na,120,120,'SIR')
    r=(m-truth)/np.sqrt(np.maximum(m,1.0)) if weighted else (m-truth)
    return float((r**2).sum())
for weighted in (False,True):
    grid=np.linspace(1.05,3.0,40)
    vals=[sse(R,weighted) for R in grid]
    best=grid[int(np.argmin(vals))]
    print(f"  weighted={weighted}:  grid-search minimum at R0_hat = {best:.3f}")
    # show the profile shape near the minimum
    near=[(round(float(R),2),round(sse(R,weighted),1)) for R in np.linspace(max(1.05,best-0.5),best+0.5,6)]
    print(f"     profile: {near}")
print("\n  -> if the two loss functions disagree, the 'factor' is procedure-dependent, not intrinsic.")
