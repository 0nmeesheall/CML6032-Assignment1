import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from vt import *
from slides_b import ROWS,OUT
# ---------------- 08 : nine-state table ----------------
def s08():
    fig,ax=new_slide('$ ./tabulate_states.sh --all --check-sums',8,tildes=(300,300))
    T(ax,120,H-165,'NINE DISTORTION STATES : GEOMETRY AND RIGID-ION POLARISATION',GREEN,21,'bold')
    panel(ax,120,330,1140,510)
    fs=13; x=155
    hdr=[(0,'z'),(9,'u / pm'),(21,'Ti-O1 UP'),(35,'Ti-O1 DOWN'),(50,'SUM / pm'),(63,'P / (C m-2)'),(79,'STATE')]
    T(ax,x,800,'STATE TABLE',AMBER,14,'bold')
    row(ax,x,765,[(c,t,CYAN) for c,t in hdr],fs=fs,w='bold')
    rule(ax,x,748,1070)
    for i,(z,u,up,dn,p) in enumerate(ROWS):
        y=718-i*42
        col=GREEN if p>0 else (RED if p<0 else MUTE)
        st='UP  (+c)' if p>0 else ('DOWN (-c)' if p<0 else 'PARENT, P = 0')
        row(ax,x,y,[(0,f'{z:.3f}'),(9,f'{u:+.2f}'),(21,f'{up:.1f}'),(35,f'{dn:.1f}'),
                    (50,f'{up+dn:.1f}'),(63,f'{p:+.4f}',col),(79,st,col)],fs=fs)
    panel(ax,1300,330,500,510)
    T(ax,1330,800,'CHECKS',AMBER,14,'bold')
    bullets(ax,1330,762,[
      ('[SUM]','Ti-O1 UP PLUS Ti-O1 DOWN'),
      ('','IS EXACTLY 410.27 pm = LP3'),
      ('','IN EVERY ROW; THE COLUMN'),
      ('','READS 410.2 OR 410.3 ONLY'),
      ('','FROM ONE-DECIMAL ROUNDING'),
      None,
      ('[PAIR]','196.9 pm AND 213.3 pm BELONG'),
      ('','TO z = 0.520, WHERE Ti SITS'),
      ('','8.21 pm ABOVE THE CENTRE AND'),
      ('','SO CLOSER TO THE O1 AT z = 1'),
      None,
      ('[EQUATOR]','Ti-O2 AND Ti-O3 RUN ONLY'),
      ('','199.52 pm TO 199.69 pm OVER'),
      ('','THE WHOLE SCAN, SO THE'),
      ('','DISTORTION IS AXIAL'),
      None,
      ('[LINEAR]','P IS LINEAR IN u ONLY BECAUSE'),
      ('','THE CHARGES ARE FIXED; BORN'),
      ('','CHARGES STEEPEN THE TRUE P(u)'),
    ],dy=25.5,fs=11.5,marker='',headc=CYAN,pad=11)
    T(ax,120,270,'$ ./verify_states.sh',ORANGE,17)
    T(ax,120,232,'[PASS] 9/9 ROWS: SUM RULE OK  |  ANTISYMMETRY P(z) = -P(1 - z) OK  |  ONE CIF WRITTEN PER ROW',GREEN,13)
    T(ax,120,196,'[OPEN]  NO EXPERIMENTAL Ti POSITION WAS ISSUED, SO THE SCAN IS A MODEL SWEEP AND NOT A REFINEMENT',MUTE,13)
    fig.savefig(OUT+'08.png',facecolor=BG); plt.close(fig)
# ---------------- 09 : switching physics ----------------
def s09():
    fig,ax=new_slide('$ ./landau.py --orders 2,4,6 --plot-wells',9,tildes=(300,300))
    T(ax,120,H-165,'WHY A LOOP AND NOT A LINE : DOUBLE WELL, DOMAINS AND Tc',GREEN,21,'bold')
    axp=fig.add_axes([0.065,0.215,0.390,0.545]); axp.set_facecolor(BG)
    for s in axp.spines.values(): s.set_visible(False)
    P=np.linspace(-1.5,1.5,900); YMAX=0.92
    def F(a2,a4=0.5): return np.where(a2*P**2+a4*P**4>YMAX,np.nan,a2*P**2+a4*P**4)
    axp.plot([-1.55,1.55],[0,0],color=BODY,lw=1.2,zorder=1)
    axp.plot([0,0],[-0.78,YMAX],color=BODY,lw=1.2,zorder=1)
    axp.plot(P,F(0.5),color=VIOLET,lw=2.8,zorder=4)
    axp.plot(P,F(0.0),color=AMBER,lw=2.8,zorder=4)
    axp.plot(P,F(-1.0),color=CYAN,lw=3.2,zorder=5)
    tilt=np.where(F(-1.0)-0.24*P>YMAX,np.nan,F(-1.0)-0.24*P)
    axp.plot(P,tilt,color=ORANGE,lw=2.2,ls='--',zorder=4)
    for x in (-1.0,1.0):
        axp.plot([x],[-0.5],'o',ms=9,mfc=CYAN,mec=BG,mew=1.6,zorder=7)
    axp.plot([0],[0],'o',ms=8,mfc=VIOLET,mec=BG,mew=1.6,zorder=7)
    axp.annotate('',xy=(0.0,-0.01),xytext=(0.0,-0.49),
        arrowprops=dict(arrowstyle='<|-|>',color=MUTE,lw=1.5,mutation_scale=12),zorder=6)
    axp.plot([-1.0,0.0],[-0.5,-0.5],color=MUTE,lw=0.9,ls=':',zorder=3)
    axp.text(-0.10,-0.25,'BARRIER',color=MUTE,fontsize=11.5,family='monospace',va='center',ha='right',zorder=7)
    axp.text(-1.0,-0.62,'-Ps',color=CYAN,fontsize=12.5,weight='bold',family='monospace',ha='center',va='top',zorder=7)
    axp.text(1.0,-0.62,'+Ps',color=CYAN,fontsize=12.5,weight='bold',family='monospace',ha='center',va='top',zorder=7)
    axp.set_xlim(-1.56,1.56); axp.set_ylim(-0.80,YMAX+0.04)
    axp.set_xticks([]); axp.set_yticks([])
    axp.set_xlabel('POLARISATION P  (NORMALISED)',color=BODY,fontsize=12,family='monospace',labelpad=6)
    axp.set_ylabel('FREE ENERGY F  (ARBITRARY)',color=BODY,fontsize=12,family='monospace',labelpad=6)
    for i,(cc,lab,ls) in enumerate(((CYAN,'T < Tc : TWO EQUAL MINIMA','-'),(AMBER,'T = Tc : BARRIER GONE','-'),
                                    (VIOLET,'T > Tc : ONE MINIMUM AT P = 0','-'),(ORANGE,'T < Tc, FIELD APPLIED','--'))):
        yl=172-i*31
        ax.plot([140,186],[yl,yl],color=cc,lw=3.0,ls=ls,zorder=6)
        T(ax,200,yl,lab,cc,12)
    panel(ax,960,175,860,685)
    T(ax,990,822,'LANDAU PICTURE AND REAL SWITCHING',AMBER,14,'bold')
    bullets(ax,990,782,[
      ('[1]','F = ALPHA P2 + BETA P4 + GAMMA P6, WITH'),
      ('','ALPHA PROPORTIONAL TO (T - T0)'),
      ('[2]','BETA IS NEGATIVE IN BaTiO3, SO THE TRANSITION IS'),
      ('','FIRST ORDER AND P DROPS DISCONTINUOUSLY AT Tc'),
      ('[3]','GAMMA IS POSITIVE AND KEEPS F BOUNDED BELOW'),
      ('[4]','BELOW Tc = 393 K THE TWO MINIMA ARE EXACTLY THE'),
      ('','z AND (1 - z) Ti SITES OF THE NINE-STATE SCAN'),
      ('[5]','A FIELD ADDS THE TERM -E P, TILTS THE WELLS AND'),
      ('','DESTROYS ONE MINIMUM WHEN E REACHES Ec'),
      ('[6]','ABOVE Tc THE SINGLE MINIMUM AT P = 0 RESTORES'),
      ('','CUBIC m$\\bar{3}$m AND THE LOOP COLLAPSES TO A LINE'),
      ('[7]','PERMITTIVITY ABOVE Tc FOLLOWS CURIE-WEISS,'),
      ('','WHICH IS THE SAME ALPHA PROPORTIONAL TO (T - T0)'),
    ],dy=28,fs=12,marker='',headc=CYAN,pad=5)
    rule(ax,990,410,800)
    bullets(ax,990,380,[
      ('[DOMAINS]','REVERSAL IS NOT HOMOGENEOUS. 180-DEGREE WALLS'),
      ('','NUCLEATE AT DEFECTS AND SWEEP THROUGH THE GRAIN,'),
      ('','SO ONLY A THIN WALL REGION CROSSES THE BARRIER'),
      ('[Ec]','THAT IS WHY MEASURED Ec IS 1e5 TO 1e6 V m-1 AND'),
      ('','NOT THE 1e8 V m-1 A RIGID LATTICE WOULD DEMAND'),
      ('[Pr]','WALL PINNING AND 90-DEGREE DOMAINS KEEP Pr BELOW'),
      ('','Ps IN ANY REAL CERAMIC'),
    ],dy=27,fs=11.5,marker='',headc=RED,pad=11)
    fig.savefig(OUT+'09.png',facecolor=BG); plt.close(fig)
