"""Chapter 10 figures: sensitivity tornado, invasion/burden schematic, and PRCC.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 10.
Reproduces (written to figs/):
  ch10_tornado_R0_Istar.pdf          -- tornado of |S^q_p| for R0 and I* (closed-form indices)
  ch10_invasion_burden_schematic.pdf -- invasion- vs burden-facing parameter schematic
  ch10_prcc_R0_Istar.pdf             -- LHS-PRCC for R0 and I*
Closed-form indices at the canonical baseline: S^{R0} over (c_I, beta, tau_R, tau_m) =
(1, 1, 0.998, 0.0016); S^{I*}_{tau_R} = 2.087, S^{I*}_{c_I} = S^{I*}_{beta} = 1.090,
S^{I*}_{tau_m} = -0.997.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-06-22   Version 1.1
"""
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({'font.family':'serif','font.size':10,'mathtext.fontset':'cm','axes.linewidth':0.8})
cI,cS,cR,beta,tauR,taum=8.,10.,10.,0.02,12.,7300.
gR=1/tauR; nu=1/taum; g=gR+nu; R0=cI*beta/g
# closed-form indices at NEW baseline
SR0={'$c_I$':1.0,'$\\beta$':1.0,'$\\tau_R$':gR/g,'$\\tau_m$':nu/g,'$c_S$':0.0,'$c_R$':0.0}
SIs={'$\\tau_R$':(gR/g)*(R0/(R0-1)),'$c_I$':1/(R0-1),'$\\beta$':1/(R0-1),
     '$\\tau_m$':-(1-(nu/g)*(R0/(R0-1))),'$c_S$':0.0,'$c_R$':0.0}
B,Rd,Gn,Gy='#1f5fa8','#c0392b','#2e7d32','#888888'

# ---- Fig 1: tornado (two panels) ----
fig,ax=plt.subplots(1,2,figsize=(9.4,3.6))
for a,(D,ttl) in zip(ax,[(SR0,'Sensitivity of $\\mathcal{R}_0$'),(SIs,'Sensitivity of $I^*$')]):
    items=sorted(D.items(),key=lambda kv:abs(kv[1]))
    names=[k for k,_ in items]; vals=[v for _,v in items]
    cols=[Rd if v<0 else B for v in vals]
    a.barh(range(len(vals)),vals,color=cols,height=0.6,edgecolor='k',linewidth=0.5)
    a.set_yticks(range(len(names))); a.set_yticklabels(names)
    a.axvline(0,color='k',lw=0.8); a.set_title(ttl,fontsize=10); a.set_xlabel('normalized sensitivity $S$')
    for i,v in enumerate(vals):
        a.text(v+(0.04 if v>=0 else -0.04),i,f'{v:+.2f}',va='center',ha='left' if v>=0 else 'right',fontsize=7.5)
    for s in('top','right'):a.spines[s].set_visible(False)
ax[0].set_xlim(-0.3,1.3); ax[1].set_xlim(-1.6,2.5)
fig.tight_layout(); fig.savefig('figs/ch10_tornado_R0_Istar.pdf'); plt.close(fig); print('tornado ok')

# ---- Fig 2: invasion-burden schematic (scatter at (S_R0, S_I*)) ----
pts={'$c_I$':(SR0['$c_I$'],SIs['$c_I$'],B),'$\\beta$':(SR0['$\\beta$'],SIs['$\\beta$'],B),
     '$\\tau_R$':(SR0['$\\tau_R$'],SIs['$\\tau_R$'],Gn),'$\\tau_m$':(SR0['$\\tau_m$'],SIs['$\\tau_m$'],'#e8820c'),
     '$c_S$':(0,0.02,Gy),'$c_R$':(0,-0.02,Gy)}
fig,a=plt.subplots(figsize=(6.0,5.2))
a.axhspan(-0.5,0.5,alpha=0.04,color='gray'); a.axvspan(-0.5,0.5,alpha=0.04,color='gray')
a.axhline(0,color='k',lw=0.6); a.axvline(0,color='k',lw=0.6)
for lab,(x,y,c) in pts.items():
    a.scatter([x],[y],s=90,color=c,edgecolor='k',linewidth=0.6,zorder=3)
    a.annotate(lab,(x,y),xytext=(8,6),textcoords='offset points',fontsize=11)
a.set_xlabel('normalized sensitivity of $\\mathcal{R}_0$ (invasion)')
a.set_ylabel('normalized sensitivity of $I^*$ (burden)')
a.text(1.05,0.15,'invasion',color=B,fontsize=9); a.text(0.06,-1.0,'burden',color='#e8820c',fontsize=9)
a.text(1.02,2.0,'mixed',color=Gn,fontsize=9)
a.set_xlim(-0.4,1.4); a.set_ylim(-1.4,2.4)
for s in('top','right'):a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch10_invasion_burden_schematic.pdf'); plt.close(fig); print('schematic ok')

# ---- Fig 3: PRCC (LHS n=5000, uniform +/-20% around new baseline) ----
rng=np.random.default_rng(11); n=5000
base={'cI':cI,'cS':cS,'cR':cR,'beta':beta,'tauR':tauR,'taum':taum}
order=['cI','beta','tauR','taum','cS','cR']
def lhs(n,k):
    u=(np.argsort(rng.random((n,k)),axis=0)+rng.random((n,k)))/n
    return u
U=lhs(n,len(order)); X=np.zeros_like(U)
for j,p in enumerate(order): X[:,j]=base[p]*(0.8+0.4*U[:,j])  # +/-20%
gg=1/X[:,2]+1/X[:,3]; R0s=X[:,0]*X[:,1]/gg; Is=1.0*(1/X[:,3])/gg*(1-1/R0s)
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
for a,(pr,ttl) in zip(ax,[(pr_R0,'PRCC for $\\mathcal{R}_0$'),(pr_I,'PRCC for $I^*$')]):
    o=np.argsort(np.abs(pr)); v=pr[o]; nm=[labels[i] for i in o]
    a.barh(range(len(v)),v,color=[Rd if x<0 else B for x in v],height=0.6,edgecolor='k',linewidth=0.5)
    a.set_yticks(range(len(nm))); a.set_yticklabels(nm); a.axvline(0,color='k',lw=0.8)
    a.set_title(ttl,fontsize=10); a.set_xlabel('PRCC'); a.set_xlim(-1.1,1.1)
    for s in('top','right'):a.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch10_prcc_R0_Istar.pdf'); plt.close(fig); print('prcc ok')
print(f"check: SR0_tauR={SR0['$\\tau_R$']:.3f} SR0_taum={SR0['$\\tau_m$']:.4f} SIs_taum={SIs['$\\tau_m$']:.3f} SIs_cI={SIs['$c_I$']:.3f}")
print(f"PRCC R0 (cI,b,tauR,taum)=({pr_R0[0]:+.2f},{pr_R0[1]:+.2f},{pr_R0[2]:+.2f},{pr_R0[3]:+.2f})")
print(f"PRCC I* (cI,b,tauR,taum)=({pr_I[0]:+.2f},{pr_I[1]:+.2f},{pr_I[2]:+.2f},{pr_I[3]:+.2f})")
