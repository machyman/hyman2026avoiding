"""Chapter 11 figure: the sub-stage initial-condition pitfall for multi-stage (Erlang-chain) models.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 11 (Section on the SEIR_I / Erlang chain).
Produces figs/ch11_multistage_ic.pdf.

An Erlang-k infectious compartment (I1 -> ... -> Ik -> R) is initialized three ways with the same TOTAL
initial infectious fraction I0 = 1e-3:
  (i)  growth-phase eigenvector distribution  (the correct mid-outbreak initialization),
  (ii) balanced / equal across sub-stages      (a common naive choice),
  (iii) all mass in the first sub-stage         (correct only for a fresh single introduction).
The naive choices inject a transient that biases the early total-infectious trajectory relative to the
eigenvector initialization. Upper panel: total I(t) on a log scale. Lower panel: relative deviation from
the eigenvector trajectory. Baseline SIR_I parameters (sir_i_model.BASE); supercritical regime.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-07-08   Version 1.0
"""
import numpy as np, matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
plt.rcParams.update({'font.family':'serif','font.size':11,'mathtext.fontset':'cm','axes.linewidth':0.8})
B='#1f5fa8'; Rd='#c0392b'; G='#2e7d32'

from sir_i_model import BASE  # Phase 2 (S17): baseline centralized
cS,cI,cR,beta = BASE['c_S'],BASE['c_I'],BASE['c_R'],BASE['beta']
gR,nu = 1/BASE['tau_R'], 1/BASE['tau_m']
k=4; kg=k*gR
def rhs(t,y):
    S=y[0]; I=y[1:1+k]; R=y[1+k]; Itot=I.sum(); C=cS*S+cI*Itot+cR*R
    a=cI*beta*cS*S/C
    dI=np.empty(k); dI[0]=a*Itot-(kg+nu)*I[0]
    for j in range(1,k): dI[j]=kg*I[j-1]-(kg+nu)*I[j]
    return np.concatenate(([nu-a*Itot-nu*S],dI,[kg*I[-1]-nu*R]))

# growth-phase eigenvector of the early-time (S=1) linearization
a0=cI*beta; M=np.zeros((k,k))
for j in range(k):
    M[j,j]=-(kg+nu)
    if j>=1: M[j,j-1]=kg
M[0,:]+=a0
w,V=np.linalg.eig(M); i=np.argmax(w.real); ev=np.abs(V[:,i].real); ev=ev/ev.sum()

I0=1e-3; T=40; t=np.linspace(0,T,1200)
def run(dist):
    y0=np.concatenate(([1-I0],np.array(dist,float)*I0,[0.0]))
    return solve_ivp(rhs,[0,T],y0,dense_output=True,rtol=1e-10,atol=1e-13,max_step=0.25).sol(t)[1:1+k].sum(0)
Iev=run(ev); Ibal=run(np.ones(k)/k); I1=run([1]+[0]*(k-1))

fig,(a1,a2)=plt.subplots(2,1,figsize=(7.2,5.6),sharex=True,gridspec_kw={'height_ratios':[2,1]})
a1.semilogy(t,Iev,color=B,lw=2,ls='-',label='growth-phase distribution (correct)')
a1.semilogy(t,I1,color=G,lw=1.6,ls='-.',label='all in first sub-stage')
a1.semilogy(t,Ibal,color=Rd,lw=1.6,ls='--',label='balanced (equal across sub-stages)')
a1.set_ylabel('Total infectious $\\sum_j I_j(t)$  (log)')
a1.set_title('Same total seed, three sub-stage initializations of an Erlang-$4$ infectious period',fontsize=10.5)
a1.legend(frameon=False,fontsize=8.5,loc='lower right')
a2.axhline(0,color='0.5',lw=0.8)
a2.plot(t,(I1-Iev)/Iev*100,color=G,lw=1.6,ls='-.')
a2.plot(t,(Ibal-Iev)/Iev*100,color=Rd,lw=1.6,ls='--')
a2.set_ylabel('deviation from\ncorrect (\\%)'); a2.set_xlabel('Days'); a2.set_xlim(0,T); a2.set_ylim(-15,32)
a2.text(26,24,'all in first sub-stage',fontsize=8.5,color=G)
a2.text(26,-11,'balanced',fontsize=8.5,color=Rd)
for a in (a1,a2):
    for s in ('top','right'): a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch11_multistage_ic.pdf'); plt.close(fig)
print('stage weights (eigenvector):',np.round(ev,3))
print('max dev balanced %.1f%%  all-in-1 %.1f%%'%(np.max(np.abs((Ibal-Iev)/Iev))*100,np.max(np.abs((I1-Iev)/Iev))*100))
print('ch11_multistage_ic.pdf written')
