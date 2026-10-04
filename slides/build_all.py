import sys,os; sys.path.insert(0,'/data/deck')
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from vt import *
import slides_a            # SLIDES 01 TO 04 RENDER AT IMPORT
import slides_q            # QUESTION SLIDES 01a, 04a, 09a
import slides_notice       # NOTICE SLIDE 02a, ADDED AFTER EVALUATION
import slides_b as B, slides_c as C, slides_d as D
from hyst import draw_loop
R='/data/repo'
os.makedirs(R+'/figures',exist_ok=True); os.makedirs(R+'/renders',exist_ok=True)
slides_q.build()
slides_notice.build()
for f in (B.s05,B.s06,B.s07,C.s08,C.s09,D.s10,D.s11,D.s12,D.s13,D.s14,D.s15): f()
# ---- standalone hysteresis figure, dark and light ----
for tag,dark,fc in (('dark',True,BG),('light',False,WHITE)):
    fig=plt.figure(figsize=(10.0,6.8),dpi=200); fig.patch.set_facecolor(fc)
    ax=fig.add_axes([0.105,0.285,0.865,0.625]); draw_loop(ax,fs=12,dark=dark)
    tc=GREEN if dark else '#0B6B3A'; mc=MUTE if dark else '#5A6670'
    ax.set_title('BaTiO3 FERROELECTRIC HYSTERESIS LOOP : TWO BRANCHES, P = 0 AT PLUS AND MINUS Ec',
                 color=tc,fontsize=12.5,weight='bold',family='monospace',pad=12)
    for i,t in enumerate([
      '[MODEL] TANH SWITCHING MODEL DRAWN TO SCALE FROM Ps = 0.26 C m-2, Pr = 0.21 C m-2 AND Ec = 0.5 MV m-1; NOT MEASURED DATA',
      '[Ti] THE RIGID-ION Ti-ONLY SUM OF THIS ASSIGNMENT GIVES ONLY 0.0805 C m-2, SO THE MEASURED Ps IS USED FOR THE LOOP HEIGHT',
      '[Ec] REAL CERAMIC Ec IS 1e5 TO 1e6 V m-1 BECAUSE 180-DEGREE DOMAIN WALLS SWEEP; HOMOGENEOUS REVERSAL WOULD NEED ABOUT 1e8 V m-1']):
        fig.text(0.105,0.168-i*0.038,t,color=mc,fontsize=7.6,family='monospace',va='center')
    fig.text(0.105,0.030,'NISHEAL MICHAEL KALEY  |  ENTRY NO 2025CYS7090  |  CML6032 ASSIGNMENT 1  |  PART B SEGMENT 1',
             color=mc,fontsize=7.6,family='monospace',va='center')
    fig.savefig(f'{R}/figures/hysteresis_loop_{tag}.png',facecolor=fc)
    fig.savefig(f'{R}/figures/hysteresis_loop_{tag}.pdf',facecolor=fc)
    plt.close(fig)
# ---- nine prototype renders ----
for ph in D.PH:
    basis,a,radii,cols=D.PH[ph]
    fig=plt.figure(figsize=(5.4,5.4),dpi=200); fig.patch.set_facecolor(WHITE)
    axs=fig.add_axes([0.02,0.145,0.96,0.80])
    draw_structure(axs,basis,a,radii,cols,scale=0.40)
    x0,x1=axs.get_xlim(); y0,y1=axs.get_ylim()
    triad(axs,x0+0.26,y0+0.24,L=0.30,fs=9)
    axs.text((x0+x1)/2,y1-0.02,ph,color='#111111',fontsize=15,weight='bold',
             family='monospace',ha='center',va='top')
    axs.text(x1-0.03,y0+0.05,f'LP = {a:.1f} pm',color='#333333',fontsize=10,
             family='monospace',ha='right',va='bottom')
    st=D.PHSTATE[ph]
    for i,(el_,c) in enumerate(cols.items()):
        fig.text(0.07,0.105-i*0.038,f'{el_}({st[el_]}, SPIN UNASSIGNED)   r = {radii[el_]} pm',
                 color=c,fontsize=9,weight='bold',family='monospace',va='center')
        fig.patches.append(plt.Circle((0.045,0.105-i*0.038),0.013,transform=fig.transFigure,
                                      fc=c,ec='#333333',lw=0.6))
    fig.savefig(f'{R}/renders/{ph}.png',facecolor=WHITE); plt.close(fig)
print('BUILT')
