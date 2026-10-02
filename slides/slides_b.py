import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from vt import *
from hyst import draw_loop
OUT='/data/deck/slides/'
A1,C1=399.04,410.27
ROWS=[(0.520,+8.21,196.9,213.3,+0.0805),(0.515,+6.15,199.0,211.3,+0.0604),
      (0.510,+4.10,201.0,209.2,+0.0402),(0.505,+2.05,203.1,207.2,+0.0201),
      (0.500, 0.00,205.1,205.1, 0.0000),(0.495,-2.05,207.2,203.1,-0.0201),
      (0.490,-4.10,209.2,201.0,-0.0402),(0.485,-6.15,211.3,199.0,-0.0604),
      (0.480,-8.21,213.3,196.9,-0.0805)]
# ---------------- 05 : method ----------------
def s05():
    fig,ax=new_slide('$ cd ../part_b1_batio3 && cat model.txt',5)
    T(ax,120,H-165,'PART B SEGMENT 1 (4 MARKS) : FERROELECTRIC DISTORTION OF BaTiO3',GREEN,22,'bold')
    panel(ax,120,400,840,480); panel(ax,1000,400,800,480)
    T(ax,150,840,'[1] CELL AND BASIS AS ISSUED',AMBER,14,'bold')
    bullets(ax,150,798,[
      ('CELL:','TETRAGONAL P  |  LP1 = LP2 = 399.04 pm  |  LP3 = 410.27 pm'),
      ('RATIO:','LP3 / LP1 = 1.0282     VOLUME = 6.5325e7 pm3'),
      ('CLASS:','m$\\bar{3}$m (Pm$\\bar{3}$m) ABOVE Tc  ->  4mm (P4mm, No 99) BELOW Tc'),
    ],dy=32,fs=12.5)
    T(ax,150,676,'BASIS, FRACTIONAL COORDINATES:',AMBER,13,'bold')
    for i,(lab,crd) in enumerate([('Ba(+2, SPIN UNASSIGNED)','0, 0, 0'),
        ('Ti(+4, SPIN UNASSIGNED)','1/2, 1/2, z   <- SCANNED'),
        ('O1(-2, SPIN UNASSIGNED)','1/2, 1/2, 0   APICAL, ALONG c'),
        ('O2(-2, SPIN UNASSIGNED)','1/2, 0, 1/2   EQUATORIAL'),
        ('O3(-2, SPIN UNASSIGNED)','0, 1/2, 1/2   EQUATORIAL')]):
        y=636-i*34
        T(ax,172,y,lab,CYAN,12.5,'bold'); T(ax,172+cw(12.5,26),y,crd,BODY,12.5)
    T(ax,1030,840,'[2] RIGID-ION POLARISATION MODEL',AMBER,14,'bold')
    bullets(ax,1030,798,[
      ('SCAN:','z = 0.480 -> 0.520, STEP 0.005, NINE STATES'),
      ('OFFSET:','u = (z - 1/2) x LP3'),
      ('SUM:','P = (1/V) SUM q u = 4e u / V   (Ti ONLY)'),
      None,
      ('WORKED:','z = 0.520  ->  u = +8.21 pm'),
      ('','P = 4(1.602e-19)(8.21e-12) / 6.5325e-29'),
      ('','P = +0.0805 C m-2'),
    ],dy=31,fs=12.5)
    bullets(ax,1030,540,[
      ('[MODEL]','ONLY Ti MOVES; Ba AND O STAY ON PARENT SITES'),
      ('[NOTE]','THE TRUE SOFT MODE ALSO SHIFTS O AGAINST Ba,'),
      ('','SO MEASURED Ps = 0.26 C m-2 EXCEEDS THIS SUM'),
      ('[SIGN]','POSITIVE u GIVES P ALONG +c; z AND (1 - z)'),
      ('','ARE THE TWO SWITCHED STATES OF EQUAL ENERGY'),
    ],dy=30,fs=12,marker='',headc=RED,pad=10)
    T(ax,120,340,'$ ls cif_batio3/',ORANGE,17)
    T(ax,120,298,'BaTiO3_P1_z0480.cif  z0485  z0490  z0495  z0500  z0505  z0510  z0515  z0520   '
                 '[9 FILES, ONE PER STATE]',BODY,13)
    T(ax,120,230,'[CHECK] THE ISSUED RATIO 1.0282 IS LARGER THAN THE LITERATURE 300 K TETRAGONALITY 1.011,',MUTE,12.5)
    T(ax,120,202,'        SO THE ISSUED CELL IS AN EXAGGERATED TETRAGONAL AND THE TREND, NOT THE MAGNITUDE, IS THE RESULT',MUTE,12.5)
    fig.savefig(OUT+'05.png',facecolor=BG); plt.close(fig)
# ---------------- 06 : hysteresis ----------------
def s06():
    fig,ax=new_slide('$ ./plot_hysteresis.sh --branches 2 --zero-at-Ec',6,tildes=(300,300))
    T(ax,120,H-165,'FERROELECTRIC HYSTERESIS : CORRECTED TWO-BRANCH LOOP',GREEN,22,'bold')
    axp=fig.add_axes([0.058,0.175,0.505,0.575]); draw_loop(axp,fs=11.5)
    panel(ax,1140,175,680,685)
    T(ax,1170,822,'WHY THE LOOP IS DOUBLE VALUED',AMBER,14,'bold')
    bullets(ax,1170,782,[
      ('[>]','ABOVE Ec THE FIELD DRIVES Ti THROUGH THE'),
      ('','CENTRE OF THE OCTAHEDRON TO THE OPPOSITE WELL'),
      ('[>]','THE SWITCHED STATE IS RETAINED AT E = 0,'),
      ('','WHICH FIXES THE REMANENT Pr'),
      ('[>]','P VANISHES ONLY WHEN THE REVERSE FIELD'),
      ('','REACHES THE COERCIVE VALUE Ec'),
    ],dy=28,fs=12,marker='',pad=4)
    rule(ax,1170,592,620)
    bullets(ax,1170,560,[
      ('[NOTE]','P = 0 SITS AT E = -Ec ON THE DESCENDING BRANCH'),
      ('','AND AT E = +Ec ON THE ASCENDING BRANCH; A SINGLE'),
      ('','S CURVE THROUGH THE ORIGIN IS NOT A LOOP'),
      ('[MODEL]','SHAPE IS A TANH SWITCHING MODEL, NOT MEASURED DATA'),
      ('[Ti]','THE Ti-ONLY SUM GIVES ONLY 0.0805 C m-2;'),
      ('','THE PLOT USES THE MEASURED Ps = 0.26 C m-2'),
      ('[Ec]','REAL CERAMIC Ec IS 1e5 TO 1e6 V m-1, WHILE'),
      ('','HOMOGENEOUS REVERSAL WOULD NEED ABOUT 1e8 V m-1'),
      ('','DOMAIN-WALL MOTION CLOSES THAT GAP'),
    ],dy=27,fs=11.5,marker='',mc=RED,headc=RED,pad=9)
    T(ax,640,108,'Ps = 0.26 C m-2   |   Pr = 0.21 C m-2   |   Ec = 0.5 MV m-1   |   Tc = 393 K',CYAN,13,'bold',ha='center')
    fig.savefig(OUT+'06.png',facecolor=BG); plt.close(fig)
# ---------------- perovskite panel ----------------
BA,TI,OX='#3FA64B','#2E6FD6','#D0342C'
OCT_E=[(0,2),(0,3),(0,4),(0,5),(1,2),(1,3),(1,4),(1,5),(2,4),(4,3),(3,5),(5,2)]
def perov(ax,z,exag=6.0,az=24,el=15):
    ax.set_facecolor(WHITE); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    M=np.diag([1.,1.,C1/A1]); zz=0.5+(z-0.5)*exag
    ba=[np.array([i,j,k],float) for i in (0,1) for j in (0,1) for k in (0,1)]
    ox=[np.array(p) for p in ([.5,.5,0.],[.5,.5,1.],[.5,0.,.5],[.5,1.,.5],[0.,.5,.5],[1.,.5,.5])]
    ti=np.array([.5,.5,zz]); mid=np.array([.5,.5,.5])
    def pj(p): return proj(np.atleast_2d(p)@M,az,el)
    cxy,_=proj(cube_pts()@M,az,el)
    for i,j in CELL_E: ax.plot(*zip(cxy[i],cxy[j]),color='#9AA3A8',lw=1.3,zorder=1,solid_capstyle='round')
    oxy,odep=pj(np.array(ox)); bxy,bdep=pj(np.array(ba))
    txy,tdep=pj(ti); txy=txy[0]; mxy=pj(mid)[0][0]
    for i,j in OCT_E: ax.plot(*zip(oxy[i],oxy[j]),color='#7FC6D8',lw=1.5,zorder=2,alpha=0.95)
    for k in range(6): ax.plot(*zip(txy,oxy[k]),color='#55606B',lw=1.5,zorder=3)
    ax.plot([mxy[0]],[mxy[1]],'+',color='#55606B',ms=9,mew=1.4,zorder=3)
    if abs(z-0.5)>1e-9:
        ax.annotate('',xy=txy,xytext=mxy,arrowprops=dict(arrowstyle='-|>',color='#E07A00',lw=2.4,
            mutation_scale=15,shrinkA=0,shrinkB=0),zorder=9)
    items=[('Ba',bxy[k],bdep[k]) for k in range(8)]+[('O',oxy[k],odep[k]) for k in range(6)]+[('Ti',txy,tdep[0])]
    rad={'Ba':0.108,'O':0.078,'Ti':0.060}; col={'Ba':BA,'O':OX,'Ti':TI}
    for sp,p,d in sorted(items,key=lambda t:-t[2]): sphere(ax,p,rad[sp],col[sp],10)
    ax.set_aspect('equal')
    xs=np.r_[bxy[:,0],oxy[:,0],cxy[:,0]]; ys=np.r_[bxy[:,1],oxy[:,1],cxy[:,1]]
    p=0.17
    ax.set_xlim(xs.min()-p,xs.max()+p); ax.set_ylim(ys.min()-p,ys.max()+p)
# ---------------- 07 : displacement series ----------------
def s07():
    fig,ax=new_slide('$ ./build_series.sh --z 0.480:0.520:0.010 --exaggerate 6',7,tildes=(300,300))
    T(ax,120,H-165,'Ti DISPLACEMENT SERIES ALONG c  (FIVE OF THE NINE STATES)',GREEN,21,'bold')
    sel=[0.480,0.490,0.500,0.510,0.520]
    d={r[0]:r for r in ROWS}
    for i,z in enumerate(sel):
        x0=0.036+i*0.1935
        a=fig.add_axes([x0,0.40,0.175,0.345]); perov(a,z)
        r=d[z]
        xc=(x0+0.0875)*W
        T(ax,xc,0.375*H,f'z = {z:.3f}',CYAN,14,'bold',ha='center')
        T(ax,xc,0.345*H,f'u = {r[1]:+.2f} pm',AMBER,13,'bold',ha='center')
        T(ax,xc,0.316*H,f'Ti-O1 UP   {r[2]:.1f} pm',BODY,12,ha='center')
        T(ax,xc,0.290*H,f'Ti-O1 DOWN {r[3]:.1f} pm',BODY,12,ha='center')
        T(ax,xc,0.260*H,f'P = {r[4]:+.4f} C m-2',GREEN if r[4]>0 else (RED if r[4]<0 else MUTE),12.5,'bold',ha='center')
    T(ax,120,215,'KEY:',AMBER,13,'bold')
    for i,(lab,c) in enumerate([('Ba(+2, SPIN UNASSIGNED)',BA),('Ti(+4, SPIN UNASSIGNED)',TI),('O(-2, SPIN UNASSIGNED)',OX)]):
        x=190+i*330
        ax.add_patch(Circle((x,217),11,fc=c,ec='#2A2A2A',lw=0.8,zorder=6))
        T(ax,x+22,215,lab,BODY,12.5)
    T(ax,1185,215,'GREY STICKS = SIX Ti-O CONTACTS | AMBER ARROW = Ti OFFSET',MUTE,11.5)
    rule(ax,120,185,1680,c='#2B3942',lw=1)
    bullets(ax,120,155,[
      ('[EXAGGERATED]','THE PLOTTED Ti OFFSET IS SCALED BY 6 FOR VISIBILITY; THE TRUE EXTREME OFFSET IS ONLY 8.21 pm IN A 410.27 pm REPEAT'),
      ('[SYMMETRY]','z = 0.500 IS THE CENTROSYMMETRIC PARENT, SO P = 0; ANY z NOT EQUAL TO 0.500 REMOVES THE INVERSION CENTRE AND POLARISES THE CELL'),
      ('[PAIRING]','z AND (1 - z) ARE THE TWO SWITCHED STATES, EQUAL IN ENERGY AND OPPOSITE IN P'),
    ],dy=29,fs=12,marker='',mc=CYAN,headc=CYAN,pad=15)
    fig.savefig(OUT+'07.png',facecolor=BG); plt.close(fig)
