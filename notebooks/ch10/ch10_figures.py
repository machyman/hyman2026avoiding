"""Chapter 10 figures: sensitivity tornado, invasion/burden schematic, and PRCC.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 10.
Reproduces (written to figs/):
  ch10_tornado_R0_Istar.pdf          -- tornado of |S^q_p| for R0 and I* (closed-form indices)
  ch10_invasion_burden_schematic.pdf -- invasion- vs burden-facing parameter schematic
  ch10_prcc_R0_Istar.pdf             -- LHS-PRCC for R0 and I*
Closed-form indices are evaluated at the canonical baseline (sir_i_model.BASE)
and printed by the runtime check line; the docstring intentionally carries no
copied numbers.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-06-22   Version 1.1
Revised: 2026-10-11   Version 1.2 (F-168.2, RG-168.1b: the PRCC sample is uniform on [p/2, 2p], the factor-of-2
                      design the caption states and the Sobol panel uses, in place of +/-20%; I* is 0 where
                      R0 <= 1, as in the Sobol panel. The tornado and schematic are unchanged.)
Revised: 2026-10-17   Version 1.3 (F-221.1, RG-222.1 (ii): I* is the general-contact closed form (eq. 5.21) of the
                      model the book integrates, not the equal-contact form. The I* tornado and the schematic take
                      the general indices, in which c_S and c_R are about +0.52 and -0.52 at the baseline; the PRCC
                      sample is unchanged (same seed and draws) and I* is evaluated with the general form.)
Revised: 2026-10-17   Version 1.4 (F-223.2, RG-225.4: the schematic's labels only. c_I and beta share one point and
                      one label; the class words sit clear of the markers. No data, index or random stream changes.)
"""
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({'text.usetex':True,'font.family':'serif','font.size':10,'mathtext.fontset':'cm','axes.linewidth':0.8})
from sir_i_model import BASE  # Phase 2 (S17): baseline centralized
cI,cS,cR,beta,tauR,taum=BASE['c_I'],BASE['c_S'],BASE['c_R'],BASE['beta'],BASE['tau_R'],BASE['tau_m']
gR=1/tauR; nu=1/taum; g=gR+nu; R0=cI*beta/g
# closed-form indices at NEW baseline
SR0={'$c_I$':1.0,'$\\beta$':1.0,'$\\tau_R$':gR/g,'$\\tau_m$':nu/g,'$c_S$':0.0,'$c_R$':0.0}
# I* indices of the general-contact closed form (eq. 5.21), v1.3: I* = c_S nu A/g / D with A = c_I beta - g and
# D = c_S A + c_I nu + c_R gR (log-derivatives; the equal-contact values differ by at most 0.001 for c_I, beta,
# tau_R and tau_m, and are 0 for c_S and c_R)
A=cI*beta-g; D=cS*A+cI*nu+cR*gR
SIs={'$\\tau_R$':gR/A+gR/g+gR*(cR-cS)/D,'$c_I$':cI*beta/A-(cS*cI*beta+cI*nu)/D,'$\\beta$':cI*beta/A-cS*cI*beta/D,
     '$\\tau_m$':-(1-nu/A-nu/g-nu*(cI-cS)/D),'$c_S$':1-cS*A/D,'$c_R$':-cR*gR/D}
B,Rd,Gn,Gy='#1f5fa8','#c0392b','#2e7d32','#888888'

# ---- Fig 1: tornado (two panels) ----
fig,ax=plt.subplots(1,2,figsize=(9.4,3.6))
for a,(D,ttl) in zip(ax,[(SR0,'Sensitivity of $\\mathcal{R}_0$'),(SIs,'Sensitivity of $i^*$')]):
    items=sorted(D.items(),key=lambda kv:abs(kv[1]))
    names=[k for k,_ in items]; vals=[v for _,v in items]
    cols=[Rd if v<0 else B for v in vals]
    a.barh(range(len(vals)),vals,color=cols,height=0.6,edgecolor='k',linewidth=0.5)
    a.set_yticks(range(len(names))); a.set_yticklabels(names)
    a.axvline(0,color='k',lw=0.8); a.set_title(ttl,fontsize=10); a.set_xlabel('normalized sensitivity $\\Upsilon$')
    for i,v in enumerate(vals):
        a.text(v+(0.04 if v>=0 else -0.04),i,f'{v:+.2f}',va='center',ha='left' if v>=0 else 'right',fontsize=7.5)
    for s in('top','right'):a.spines[s].set_visible(False)
ax[0].set_xlim(-0.3,1.3); ax[1].set_xlim(-1.6,2.5)
fig.tight_layout(); fig.savefig('figs/ch10_tornado_R0_Istar.pdf'); plt.close(fig); print('tornado ok')

# ---- Fig 2: invasion-burden schematic (scatter at (S_R0, S_I*)) ----
pts={'$c_I$':(SR0['$c_I$'],SIs['$c_I$'],B),'$\\beta$':(SR0['$\\beta$'],SIs['$\\beta$'],B),
     '$\\tau_R$':(SR0['$\\tau_R$'],SIs['$\\tau_R$'],Gn),'$\\tau_m$':(SR0['$\\tau_m$'],SIs['$\\tau_m$'],'#e8820c'),
     '$c_S$':(0,SIs['$c_S$'],Gy),'$c_R$':(0,SIs['$c_R$'],Gy)}
fig,a=plt.subplots(figsize=(6.0,5.2))
a.axhspan(-0.5,0.5,alpha=0.04,color='gray'); a.axvspan(-0.5,0.5,alpha=0.04,color='gray')
a.axhline(0,color='k',lw=0.6); a.axvline(0,color='k',lw=0.6)
for lab,(x,y,c) in pts.items():
    a.scatter([x],[y],s=90,color=c,edgecolor='k',linewidth=0.6,zorder=3)
    if lab=='$\\beta$': continue   # v1.4: same point as c_I; one label for both
    a.annotate('$c_I$, $\\beta$' if lab=='$c_I$' else lab,(x,y),xytext=(8,6),textcoords='offset points',fontsize=11)
a.set_xlabel('normalized sensitivity of $\\mathcal{R}_0$ (invasion)')
a.set_ylabel('normalized sensitivity of $i^*$ (burden)')
a.text(1.05,0.15,'invasion',color=B,fontsize=9); a.text(0.12,-1.25,'burden',color='#e8820c',fontsize=9)
a.text(1.12,1.85,'mixed',color=Gn,fontsize=9)
a.set_xlim(-0.4,1.4); a.set_ylim(-1.4,2.4)
for s in('top','right'):a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch10_invasion_burden_schematic.pdf'); plt.close(fig); print('schematic ok')

# ---- Fig 3: PRCC (LHS n=5000, each parameter uniform on [p/2, 2p]: the factor-of-2 design of the caption) ----
rng=np.random.default_rng(11); n=5000
base={'cI':cI,'cS':cS,'cR':cR,'beta':beta,'tauR':tauR,'taum':taum}
order=['cI','beta','tauR','taum','cS','cR']
def lhs(n,k):
    u=(np.argsort(rng.random((n,k)),axis=0)+rng.random((n,k)))/n
    return u
U=lhs(n,len(order)); X=np.zeros_like(U)
for j,p in enumerate(order): X[:,j]=base[p]*(0.5+1.5*U[:,j])  # uniform on [p/2, 2p] (v1.2; was +/-20%)
gg=1/X[:,2]+1/X[:,3]; R0s=X[:,0]*X[:,1]/gg
Is=X[:,4]*(1/X[:,3])*(R0s-1)/(X[:,4]*gg*(R0s-1)+X[:,0]/X[:,3]+X[:,5]/X[:,2])   # general I*, eq. 5.21 (v1.3)
Is=np.where(R0s>1,Is,0.0)   # no endemic equilibrium where R0 <= 1 (v1.2; the Sobol panel's convention)
print(f'PRCC sample: share with R0 <= 1 = {np.mean(R0s<=1):.3f}')
def prcc(X,y):
    from numpy import argsort
    R=np.apply_along_axis(lambda c:argsort(argsort(c)),0,X).astype(float)
    ry=argsort(argsort(y)).astype(float); out=[]
    for i in range(X.shape[1]):
        idx=[k for k in range(X.shape[1]) if k!=i]; Z=np.column_stack([np.ones(len(ry)),R[:,idx]])
        bi=np.linalg.lstsq(Z,R[:,i],rcond=None)[0]; ei=R[:,i]-Z@bi
        by=np.linalg.lstsq(Z,ry,rcond=None)[0]; ey=ry-Z@by
        out.append(np.corrcoef(ei,ey)[0,1])
    return np.array(out)
pr_R0=prcc(X,R0s); pr_I=prcc(X,Is)
labels=['$c_I$','$\\beta$','$\\tau_R$','$\\tau_m$','$c_S$','$c_R$']
fig,ax=plt.subplots(1,2,figsize=(9.4,3.6))
for a,(pr,ttl) in zip(ax,[(pr_R0,'PRCC for $\\mathcal{R}_0$'),(pr_I,'PRCC for $i^*$')]):
    o=np.argsort(np.abs(pr)); v=pr[o]; nm=[labels[i] for i in o]
    a.barh(range(len(v)),v,color=[Rd if x<0 else B for x in v],height=0.6,edgecolor='k',linewidth=0.5)
    a.set_yticks(range(len(nm))); a.set_yticklabels(nm); a.axvline(0,color='k',lw=0.8)
    a.set_title(ttl,fontsize=10); a.set_xlabel('PRCC'); a.set_xlim(-1.1,1.1)
    for s in('top','right'):a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch10_prcc_R0_Istar.pdf'); plt.close(fig); print('prcc ok')
print(f"check: SR0_tauR={SR0['$\\tau_R$']:.3f} SR0_taum={SR0['$\\tau_m$']:.4f} SIs_taum={SIs['$\\tau_m$']:.3f} SIs_cI={SIs['$c_I$']:.3f}")
print(f"PRCC R0 (cI,b,tauR,taum)=({pr_R0[0]:+.2f},{pr_R0[1]:+.2f},{pr_R0[2]:+.2f},{pr_R0[3]:+.2f})")
print(f"PRCC I* (cI,b,tauR,taum)=({pr_I[0]:+.2f},{pr_I[1]:+.2f},{pr_I[2]:+.2f},{pr_I[3]:+.2f})")
print(f"PRCC I* (cS,cR)=({pr_I[4]:+.3f},{pr_I[5]:+.3f}); PRCC R0 (cS,cR)=({pr_R0[4]:+.3f},{pr_R0[5]:+.3f})")
print('general I* indices: ' + ', '.join(f"{k} {v:+.4f}" for k, v in SIs.items()))
