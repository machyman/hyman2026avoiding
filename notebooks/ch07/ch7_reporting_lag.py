# BASELINE NOTE (Phase 2, Session 17): intentionally independent of sir_i_model.BASE -- self-contained synthetic curve.
"""Chapter 7 figure: mis-identifying the epidemic start shifts the whole timeline.

Companion text: Avoiding Pitfalls in Epidemic Modeling, Chapter 7 (Natural Initial Conditions).
Produces figs/ch7_reporting_lag.pdf.

A single early-growth infectious curve I(t) (illustrative exponential growth, doubling time three days,
seeded at one infectious individual) is plotted on a LINEAR axis under three assumptions about when the
epidemic began, relative to the first reported case at day 0:
  Run 1  the first reported case is taken to be the first infection (epidemic starts at day 0);
  Run 2  a five-day reporting delay: the first case was infected five days before it was reported;
  Run 3  the first reported case is actually the fifth case, treated as if it were the first, so the
         epidemic began ln(5)/sigma ~ 7 days earlier.
The curve has the same shape in all three; only its position on the time axis moves.

Author:  James M. Hyman, mhyman@tulane.edu, Tulane University
Date:    2026-07-08   Version 2.0
"""
import numpy as np, matplotlib.pyplot as plt
plt.rcParams.update({'text.usetex':True,'font.family':'serif','font.size':11,'mathtext.fontset':'cm','axes.linewidth':0.8})
B='#1f5fa8'; Rd='#c0392b'; G='#2e7d32'

sig=np.log(2)/3.0                 # illustrative early-growth rate: doubling time 3 days
Icap=300.0                        # draw each run's identical rise from I=1 up to Icap
tau=np.linspace(0,np.log(Icap)/sig,700)
Iepi=np.exp(sig*tau)              # one epidemic curve, time since that run's start
shift2=5.0                        # reporting delay (days)
shift3=np.log(5.0)/sig            # time from the 1st case to the 5th case

fig,ax=plt.subplots(figsize=(7.2,4.3))
ax.axvline(0,color='0.5',ls=':',lw=1.0)
ax.plot(tau-0.0,   Iepi,color=B, lw=2.0,ls='-',  label='first report taken as the start')
ax.plot(tau-shift2,Iepi,color=Rd,lw=1.8,ls='--', label='5-day reporting delay')
ax.plot(tau-shift3,Iepi,color=G, lw=1.8,ls='-.', label='first report is the 5th case')
ax.set_xlim(-9,25.5); ax.set_ylim(0,Icap*1.06)
ax.set_xlabel('days  (day 0 = first reported case)'); ax.set_ylabel('infectious individuals  $I(t)$')
ax.set_title('Mis-identifying the start shifts the whole timeline',fontsize=11)
ax.text(0.4,Icap*1.0,'first\nreported\ncase',fontsize=8.5,color='0.35',va='top')
# shift indicator between Run 1 and Run 3 at a mid-height
yA=205.0; xR1=np.log(yA)/sig; xR3=xR1-shift3
ax.annotate('',xy=(xR1,yA),xytext=(xR3,yA),arrowprops=dict(arrowstyle='<->',color='0.4',lw=1.0))
ax.text((xR1+xR3)/2,yA+10,'same curve,\nshifted earlier',fontsize=8.5,color='0.35',ha='center',va='bottom')
ax.legend(frameon=False,fontsize=8.5,loc='upper left')
for s in ('top','right'): ax.spines[s].set_visible(False)
fig.tight_layout(); fig.savefig('figs/ch7_reporting_lag.pdf'); plt.close(fig)
print(f'sigma={sig:.4f}/day (doubling 3 d); shift2={shift2:.1f} d, shift3=ln(5)/sig={shift3:.2f} d')
print(f'each run rises identically from I=1 to I={Icap:.0f} over {np.log(Icap)/sig:.1f} days')
print('ch7_reporting_lag.pdf written')
