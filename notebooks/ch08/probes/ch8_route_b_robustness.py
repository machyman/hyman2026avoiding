# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- Route B synthetic regime (R0 = 2.0).
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares
rng = np.random.default_rng(8)

N_true=100_000.0; R0_true=2.0; tau_R=7.0; gamma=1/tau_R
beta_true=R0_true*gamma; I0_true=10.0; sigma=1/3.0   # SEIR latent 3 d

def sim(beta,I0,N,T,n,model='SIR',E0frac=0.0):
    if model=='SIR':
        y0=[N-I0,I0]
        def rhs(t,y):
            S,I=y; inc=beta*S*I/N; return [-inc,inc-gamma*I]
        idx_inc=lambda sol,ts: beta*sol.sol(ts)[0]*sol.sol(ts)[1]/N
    else:  # SEIR
        E0=I0; y0=[N-I0-E0,E0,I0]
        def rhs(t,y):
            S,E,I=y; inc=beta*S*I/N; return [-inc,inc-sigma*E,sigma*E-gamma*I]
        idx_inc=lambda sol,ts: beta*sol.sol(ts)[0]*sol.sol(ts)[2]/N
    te=np.linspace(0,T,n+1)
    sol=solve_ivp(rhs,[0,T],y0,t_eval=te,rtol=1e-9,atol=1e-9,dense_output=True)
    inc=np.array([np.trapezoid(idx_inc(sol,np.linspace(te[k],te[k+1],15)),
                               np.linspace(te[k],te[k+1],15)) for k in range(n)])
    return inc

def fit(data,N_a,T,n,model='SIR',seed_mode='free',noise=False):
    """seed_mode: 'free' (I0 estimated), 'fixed_count' (I0 known), 'fixed_frac' (i0=I0/N known)"""
    def resid(p):
        R0=np.exp(p[0])
        if seed_mode=='free':        I0=np.exp(p[1])
        elif seed_mode=='fixed_count': I0=I0_true
        else:                          I0=(I0_true/N_true)*N_a     # fixed FRACTION
        m=sim(R0*gamma,I0,N_a,T,n,model)
        if noise: return (m-data)/np.sqrt(np.maximum(m,1.0))        # Poisson-ish weighting
        return m-data
    p0=[np.log(1.5),np.log(20.0)] if seed_mode=='free' else [np.log(1.5)]
    if seed_mode!='free':
        f=lambda p: resid([p[0],0.0]); out=least_squares(f,[p0[0]],method='lm',xtol=1e-12)
    else:
        out=least_squares(resid,p0,method='lm',xtol=1e-12)
    return float(np.exp(out.x[0]))

ratios=[1/3,1,3,10,30]
print("robustness of the two regimes (true R0 = 2.0)\n")
for model in ['SIR','SEIR']:
    truth=sim(beta_true,I0_true,N_true,120,120,model)
    peak=int(np.argmax(truth))
    for seed_mode in ['free','fixed_count','fixed_frac']:
        row_e=[];row_p=[]
        for r in ratios:
            row_e.append(fit(truth[:30],N_true*r,30,30,model,seed_mode))
            row_p.append(fit(truth,N_true*r,120,120,model,seed_mode))
        print(f"  {model:4s} seed={seed_mode:11s} peak d{peak}")
        print(f"     early  : "+"  ".join(f"{r:>5.3g}x->{v:5.3f}" for r,v in zip(ratios,row_e)))
        print(f"     to-peak: "+"  ".join(f"{r:>5.3g}x->{v:5.3f}" for r,v in zip(ratios,row_p)))
