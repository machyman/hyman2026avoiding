"""Chapter 7 figures: SIR_I scenario trajectories and dynamic reproductive number.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 7.
Reproduces (written to figs/):
  ch7_scenario1_trajectory.pdf  -- baseline outbreak S/I/R over 1000 d (R0 ~ 1.92);
                                    distinct line styles for B&W + labeled S*, R* reference lines
  ch7_scenario1_long.pdf        -- recurrent dynamics over ~110 yr; the one-infectious-individual
                                    level (N*=1e5) is marked and the sub-threshold curve is faded
  ch7_scenario2.pdf             -- Scenario 1 vs 2 as two stacked LINEAR panels (outbreak vs die-out),
                                    shared time axis
  ch7_Re_over_time.pdf          -- effective reproductive number R_e(t)
All time axes carry a right-pointing arrowhead (Chapter 7 figure convention).
Reuses the shared integrator in sir_i_model.py; run from the repository root.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-07-08   Version 1.2
"""
import numpy as np, matplotlib.pyplot as plt, sys; sys.path.insert(0, 'figs_src')
from sir_i_model import simulate, endemic, BASE  # Phase 2 (S17): BASE imported for scenario labels
plt.rcParams.update({'font.family':'serif','font.size':11,'mathtext.fontset':'cm','axes.linewidth':0.8})
B='#1f5fa8'; Rd='#c0392b'; G='#2e7d32'
e=endemic(); Ss,Is,Rs=e['S'],e['I'],e['R']

def time_arrow(ax):
    """Right-pointing arrowhead at the right end of the x-axis: a time-direction cue."""
    ax.plot(1,0,marker='>',ms=8,color='0.2',transform=ax.transAxes,clip_on=False,zorder=5)

# 1) scenario1_trajectory: linear S/I/R, 1000 d; distinct line styles (B&W) + labeled reference lines
sol=simulate(1000); t=np.linspace(0,1000,4000); S,I,R=sol.sol(t)
fig,ax=plt.subplots(figsize=(7.2,4.0))
ax.plot(t,S,color=B,lw=2,ls='-',label='$S(t)$')
ax.plot(t,I,color=Rd,lw=2,ls='--',label='$I(t)$')
ax.plot(t,R,color=G,lw=2,ls='-.',label='$R(t)$')
ax.axhline(Ss,color='0.55',ls=':',lw=1); ax.axhline(Rs,color='0.55',ls=':',lw=1)
ax.text(995,Ss,'$S^*\\approx%.2f$'%Ss,fontsize=9,color='0.35',va='bottom',ha='right')
ax.text(995,Rs,'$R^*\\approx%.2f$'%Rs,fontsize=9,color='0.35',va='top',ha='right')
ax.set_xlabel('Days'); ax.set_ylabel('population fraction'); ax.set_xlim(0,1000); ax.set_ylim(-0.03,1.02)
ax.legend(frameon=False,ncol=3,loc='upper center')
for s in('top','right'):ax.spines[s].set_visible(False)
time_arrow(ax)
fig.tight_layout(); fig.savefig('figs/ch7_scenario1_trajectory.pdf'); plt.close(fig); print('1 ok')

# 2) recurrent: I on log with one-individual fade-out level + S linear, over 110 yr
sol=simulate(40150,n=70000); t=np.linspace(0,40150,24000); S,I,R=sol.sol(t); yr=t/365
Ione=1e-5   # one infectious individual for a representative population N^c=1e5
Iclip=np.clip(I,1e-9,None)
fig,(a1,a2)=plt.subplots(2,1,figsize=(7.2,5.6),sharex=True)
a1.semilogy(yr,Iclip,color='0.75',lw=1.0,zorder=1)                    # faded deterministic continuation
a1.semilogy(yr,np.where(I>=Ione,Iclip,np.nan),color=Rd,lw=1.2,zorder=2)  # physically >= 1 individual
a1.axhline(Ione,color='0.45',ls='-',lw=1.0)
a1.text(108,Ione*1.5,'one infectious individual  ($\\mathsf{N}^{\\mathrm{c}}{=}10^{5}$)',fontsize=8.5,color='0.35',ha='right',va='bottom')
a1.axhline(Is,color='0.4',ls='--',lw=1)
a1.text(2,Is*1.7,'$I^*\\approx%.4f$'%Is,fontsize=9,color='0.3')
a1.set_ylabel('Infectious $I(t)$  (log)'); a1.set_ylim(1e-8,0.3)
a1.set_title('Recurrent epidemics damping to a low endemic level',fontsize=11)
a2.plot(yr,S,color=B,lw=1.1); a2.axhline(Ss,color='0.4',ls='--',lw=1)
a2.text(2,Ss+0.03,'$S^*\\approx%.3f$'%Ss,fontsize=9,color='0.3')
a2.set_ylabel('Susceptible $S(t)$'); a2.set_xlabel('Years'); a2.set_xlim(0,110); a2.set_ylim(0.15,1.0)
for a in(a1,a2):
    for s in('top','right'):a.spines[s].set_visible(False)
time_arrow(a2)
fig.tight_layout(); fig.savefig('figs/ch7_scenario1_long.pdf'); plt.close(fig); print('2 ok')

# 3) scenario2: Scenario 1 vs 2 as two stacked LINEAR panels, shared time axis (outbreak vs die-out)
t=np.linspace(0,600,3000); c2=BASE['c_I']/2; I1=simulate(600).sol(t)[1]; I2=simulate(600,c_I=c2).sol(t)[1]
fig,(a1,a2)=plt.subplots(2,1,figsize=(7.2,5.4),sharex=True)
a1.plot(t,I1,color=B,lw=2)
ipk=int(np.argmax(I1))
a1.annotate('peak $\\approx%.2f$ (day %d)'%(I1[ipk],round(t[ipk])),xy=(t[ipk],I1[ipk]),
            xytext=(t[ipk]+80,I1[ipk]*0.85),fontsize=9,color='0.25',
            arrowprops=dict(arrowstyle='->',color='0.5',lw=0.8))
a1.set_ylabel('Infectious $I(t)$'); a1.set_ylim(0,0.17)
a1.set_title(f'Scenario 1:  $c_I={BASE["c_I"]:g}$, $\\mathcal{{R}}_0\\approx{endemic()["R0"]:.2f}$  (supercritical outbreak)',fontsize=10.5)
a2.plot(t,I2,color=Rd,lw=2)
for th in (200,400):a2.axvline(th,color='0.85',ls=':',lw=0.9)
a2.text(300,I2.max()*0.72,'halves $\\approx$ every 200 d',fontsize=9,color='0.3',ha='center')
a2.set_ylabel('Infectious $I(t)$'); a2.set_xlabel('Days'); a2.set_xlim(0,600); a2.set_ylim(0,0.00108)
a2.set_title(f'Scenario 2:  $c_I={c2:g}$, $\\mathcal{{R}}_0\\approx{endemic(c_I=c2)["R0"]:.2f}$  (subcritical die-out)',fontsize=10.5)
for a in(a1,a2):
    for s in('top','right'):a.spines[s].set_visible(False)
time_arrow(a2)
fig.tight_layout(); fig.savefig('figs/ch7_scenario2.pdf'); plt.close(fig); print('3 ok')

# (equivalence figure removed in v160; the machine-precision agreement is stated in the text, Section 7.5.1)
cS,cI,cR,beta=BASE['c_S'],BASE['c_I'],BASE['c_R'],BASE['beta']; gR,nu=1/BASE['tau_R'],1/BASE['tau_m']   # baseline for the R_e computation (Phase 2: centralized)

# 5) Re(t): (a) first 600 d with I(t) overlaid, (b) ~110 yr long-term (Zhuolin Set 2)
fig,(axS,axL)=plt.subplots(1,2,figsize=(9.8,4.0))
sol=simulate(600); t=np.linspace(0,600,3000); S,I,R=sol.sol(t)
C=cS*S+cI*I+cR*R; PS=cS*S/C; R0=cI*beta/(gR+nu); Re=R0*PS
axS.plot(t,Re,color=Rd,lw=2); axS.axhline(1,color='0.4',ls='--',lw=1)
tpk=t[np.argmin(np.abs(Re[:1000]-1))]; axS.axvline(tpk,color='0.7',ls=':',lw=1)
axS.text(tpk+8,1.62,'peak\n($\\mathcal{R}_e=1$)',fontsize=9)
axS.set_xlabel('Days'); axS.set_ylabel('Effective reproductive number $\\mathcal{R}_e(t)$',color=Rd)
axS.set_xlim(0,600); axS.set_ylim(0,2.05); axS.tick_params(axis='y',labelcolor=Rd)
axI=axS.twinx(); axI.plot(t,I,color='0.45',lw=1.4)
axI.set_ylabel('Infectious $I(t)$',color='0.45'); axI.tick_params(axis='y',labelcolor='0.45')
axI.set_ylim(0,I.max()*1.18); axS.spines['top'].set_visible(False); axI.spines['top'].set_visible(False)
axS.set_title('(a) First 600 days',fontsize=10,loc='left')
solL=simulate(40150,n=70000); tL=np.linspace(0,40150,24000); SL,IL,RL=solL.sol(tL); yr=tL/365
CL=cS*SL+cI*IL+cR*RL; ReL=R0*(cS*SL/CL)
axL.plot(yr,ReL,color=Rd,lw=0.9); axL.axhline(1,color='0.4',ls='--',lw=1)
axL.set_xlabel('Years'); axL.set_ylabel('$\\mathcal{R}_e(t)$'); axL.set_xlim(0,110); axL.set_ylim(0,2.05)
for s in('top','right'):axL.spines[s].set_visible(False)
axL.set_title('(b) Over $\\sim$110 years',fontsize=10,loc='left')
fig.tight_layout(); fig.savefig('figs/ch7_Re_over_time.pdf'); plt.close(fig); print('5 ok')
