import numpy as np
from vt import *
PS=0.26; EC=0.50; ESAT=3.0; WID=0.45     # Ps C m-2 ; Ec and axis in MV m-1
def _branch(E,sign): return PS*np.tanh((E+sign*EC)/WID)
def draw_loop(ax,fs=13,lw=3.0,annot=True,dark=True):
    fg=BODY if dark else '#1A1A1A'
    gl=GRID if dark else '#C8D0D6'
    ax.set_facecolor(BG if dark else WHITE)
    for s in ax.spines.values(): s.set_visible(False)
    E=np.linspace(-ESAT,ESAT,900)
    Pd=_branch(E,+1)          # descending: field swept + -> -
    Pa=_branch(E,-1)          # ascending:  field swept - -> +
    for x in np.arange(-3,3.1,0.5): ax.plot([x,x],[-0.34,0.34],color=gl,lw=0.6,zorder=0)
    for y in np.arange(-0.3,0.31,0.1): ax.plot([-ESAT,ESAT],[y,y],color=gl,lw=0.6,zorder=0)
    ax.plot([-ESAT,ESAT],[0,0],color=fg,lw=1.4,zorder=1)
    ax.plot([0,0],[-0.34,0.34],color=fg,lw=1.4,zorder=1)
    ax.plot(E,Pd,color=CYAN,lw=lw,zorder=4,solid_capstyle='round')
    ax.plot(E,Pa,color=ORANGE,lw=lw,zorder=4,solid_capstyle='round')
    # direction arrows
    for xa,br,col in ((1.15,+1,CYAN),(-1.15,-1,ORANGE)):
        p0=_branch(xa,br); p1=_branch(xa-0.30*br,br)
        ax.annotate('',xy=(xa-0.30*br,p1),xytext=(xa,p0),
            arrowprops=dict(arrowstyle='-|>',color=col,lw=2.2,mutation_scale=17),zorder=5)
    Pr=_branch(0.,1)
    if annot:
        for x,y,t,c,ha,va in (
            ( EC,0,'+Ec',ORANGE,'left','top'),(-EC,0,'-Ec',CYAN,'right','bottom'),
            (0, Pr,'+Pr',CYAN,'right','top'),(0,-Pr,'-Pr',ORANGE,'left','bottom'),
            (ESAT,  PS,'+Ps',GREEN,'right','bottom'),(-ESAT,-PS,'-Ps',GREEN,'left','top')):
            ax.plot([x],[y],'o',ms=7,mfc=c,mec=BG if dark else WHITE,mew=1.4,zorder=6)
            ax.text(x+(0.22 if ha=='left' else -0.22),y+(0.012 if va=='bottom' else -0.012),
                t,color=c,fontsize=fs,weight='bold',ha=ha,va=va,family='monospace',zorder=6,
                bbox=dict(fc=BG if dark else WHITE,ec='none',pad=1.0,alpha=0.82))
        ax.plot([0,EC],[ -Pr,0],color=DIM,lw=0.9,ls=':',zorder=2)
        ax.plot([-EC,0],[0, Pr],color=DIM,lw=0.9,ls=':',zorder=2)
        ax.plot([-ESAT,ESAT],[PS,PS],color=DIM,lw=0.8,ls='--',zorder=2)
        ax.plot([-ESAT,ESAT],[-PS,-PS],color=DIM,lw=0.8,ls='--',zorder=2)
        ax.text(1.05,0.300,'DESCENDING BRANCH',color=CYAN,fontsize=fs-1,weight='bold',ha='left',va='center',family='monospace',zorder=6)
        ax.text(-1.05,-0.300,'ASCENDING BRANCH',color=ORANGE,fontsize=fs-1,weight='bold',ha='right',va='center',family='monospace',zorder=6)
    ax.set_xticks(np.arange(-3,3.1,1)); ax.set_yticks(np.arange(-0.3,0.31,0.1))
    ax.tick_params(colors=fg,labelsize=fs-2,length=4)
    for lb in ax.get_xticklabels()+ax.get_yticklabels(): lb.set_family('monospace')
    ax.set_xlabel('ELECTRIC FIELD E / (MV m-1)',color=fg,fontsize=fs,family='monospace',labelpad=6)
    ax.set_ylabel('POLARISATION P / (C m-2)',color=fg,fontsize=fs,family='monospace',labelpad=6)
    ax.set_xlim(-ESAT-0.12,ESAT+0.12); ax.set_ylim(-0.345,0.345)
    return Pr
