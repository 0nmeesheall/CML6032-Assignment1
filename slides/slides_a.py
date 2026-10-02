import sys; sys.path.insert(0,'/data/deck')
from vt import *
import numpy as np
OUT='/data/deck/slides/'
def ax_in(fig,x,y,w,h):
    a=fig.add_axes([x/W,y/H,w/W,h/H]); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_visible(False)
    return a
def wpanel(ax,fig,x,y,w,h,title,caption,tc=CYAN):
    panel(ax,x,y,w,h,PANEL,PEDGE,1.8,10)
    T(ax,x+w/2,y+h-26,title,tc,14,'bold','center')
    T(ax,x+w/2,y+20,caption,AMBER,13,'bold','center')
    return ax_in(fig,x+16,y+46,w-32,h-84)

# ---------------- 01 TITLE ----------------
fig,ax=new_slide('$ cat title.txt',1,tildes=(250,760))
T(ax,150,H-200,'20261005 CML6032 ASSIGNMENT 1',GREEN,30,'bold')
T(ax,150,H-258,'MATERIALS CHEMISTRY : STRUCTURAL ANALYSIS',AMBER,21)
T(ax,150,H-312,'CRYSTAL MORPHOLOGY, PEROVSKITE HYSTERESIS AND NINE BINARY PROTOTYPES',CYAN,19)
T(ax,150,H-396,'NISHEAL MICHAEL KALEY',GREEN,20)
T(ax,150,H-444,'ENTRY NO 2025CYS7090  |  IIT DELHI',GREEN,17)
T(ax,150,H-488,'10 OCTOBER 2026',GREEN,17)
T(ax,150,H-566,'$ ./init_pipeline.sh',ORANGE,21)
for i,l in enumerate(['MODULES INITIALIZED: [PART A: MORPHOLOGY AND POINT GROUPS]',
                      '                     [PART B SEGMENT 1: FERROELECTRIC DISTORTION SERIES]',
                      '                     [PART B SEGMENT 2: NINE BINARY PROTOTYPES]']):
    T(ax,150,H-612-i*32,l,BODY,15)
T(ax,150,H-724,'$ ./set_notation.sh --house',ORANGE,21)
T(ax,150,H-770,'UNITS pm ONLY  |  RATIOS NOT PER-100  |  STATE TUPLES ON ALL IONS  |  NO GREEK GLYPHS',BODY,15)
T(ax,150,H-804,'MIRROR PLANES AS MP  |  OVERHEAD BARS ON ROTOINVERSION AXES AND SPACE GROUPS, e.g. '
               '$\\bar{3}$m AND Fm$\\bar{3}$m',BODY,15)
fig.savefig(OUT+'01.png',facecolor=BG); plt.close(fig)

# ---------------- 02 PART A METHOD ----------------
fig,ax=new_slide('$ cd ./part_a_morphology && cat README.txt',2)
panel(ax,120,210,1680,700)
T(ax,160,860,'[MODULE 1 : PART A (3 MARKS)]',CYAN,17,'bold')
T(ax,160,812,'CRYSTAL MORPHOLOGY AND MOST PROBABLE POINT GROUPS',GREEN,25,'bold')
ax.plot([160,1760],[778,778],color=PEDGE,lw=1.5)
T(ax,160,736,'OBJECTIVE AND PROTOCOL:',AMBER,16,'bold')
bullets(ax,160,692,[
 ('SPECIMEN 1: ','[IDENTITY AS ISSUED IN CLASS] - CUBO-OCTAHEDRAL HABIT'),
 ('SPECIMEN 2: ','[IDENTITY AS ISSUED IN CLASS] - HEXAGONAL PRISMATIC HABIT'),
 ('PROTOCOL: ','INVENTORY THE MACROSCOPIC OPERATIONS, BUILD THE STEREOGRAM, THEN EXCLUDE EVERY LOWER CLASS'),
 ('STENO 1669: ','FACE AREAS VARY WITH GROWTH RATE, INTERFACIAL ANGLES DO NOT'),
 ('LIMIT: ','EXTERNAL FORM FIXES THE CLASS ONLY UP TO THE HOLOHEDRY OF THE LATTICE,'),
 ('','          SO THE ANSWER IS THE MOST PROBABLE POINT GROUP AND NOT A PROOF'),
 ('NOT TESTED: ','PYROELECTRIC, PIEZOELECTRIC AND OPTICAL-ACTIVITY MEASUREMENTS WERE NOT MADE,'),
 ('','             SO CENTROSYMMETRY IS INFERRED FROM FORM EQUIVALENCE ONLY'),
 ],dy=44,fs=15)
T(ax,120,150,'$ ./analyze_morphology.sh --all',ORANGE,21)
T(ax,120,104,'[STATUS: READY] 2 SPECIMENS QUEUED | 48 AND 24 OPERATION INVENTORIES PENDING',BODY,15)
fig.savefig(OUT+'02.png',facecolor=BG); plt.close(fig)

# ---------------- habit + stereogram helpers ----------------
def cubo_faces(t=0.70):
    V=[];
    for s in [(1,1,1),(1,1,-1),(1,-1,1),(1,-1,-1),(-1,1,1),(-1,1,-1),(-1,-1,1),(-1,-1,-1)]:
        hexf=[(t,1-t,0),(1-t,t,0),(0,t,1-t),(0,1-t,t),(1-t,0,t),(t,0,1-t)]
        V.append(('hex',[np.array([p[0]*s[0],p[1]*s[1],p[2]*s[2]]) for p in hexf]))
    for ax_i in range(3):
        for sg in (1,-1):
            sq=[]
            for d in [(1-t,0),(0,1-t),(-(1-t),0),(0,-(1-t))]:
                p=np.zeros(3); p[ax_i]=sg*t
                o=[i for i in range(3) if i!=ax_i]
                p[o[0]],p[o[1]]=d[0],d[1]; sq.append(p)
            V.append(('sq',sq))
    return V
def hexbipy():
    F=[]; R=1.0; zt=0.62; ap=1.5
    top=[np.array([R*np.cos(np.radians(60*i)),R*np.sin(np.radians(60*i)),zt]) for i in range(6)]
    bot=[np.array([p[0],p[1],-zt]) for p in top]
    for i in range(6):
        j=(i+1)%6
        F.append(('pr',[top[i],top[j],bot[j],bot[i]]))
        F.append(('cap',[top[i],top[j],np.array([0,0,ap])]))
        F.append(('cap',[bot[i],bot[j],np.array([0,0,-ap])]))
    return F
def draw_poly(a,F,az=26,el=18,cols={'hex':'#E8A33D','sq':'#4FC3D9','pr':'#4FC3D9','cap':'#E8A33D'}):
    a.set_facecolor(PANEL)
    e1,e2,n=rot(az,el); cam=-n
    out=[]
    for kind,P in F:
        P=np.array(P); c=P.mean(0)
        v1,v2=P[1]-P[0],P[2]-P[0]; nn=np.cross(v1,v2); nn/=np.linalg.norm(nn)
        if np.dot(nn,c)<0: nn=-nn
        if np.dot(nn,cam)<=0.02: continue
        xy,_=proj(P,az,el); out.append((np.dot(c,cam),xy,kind,abs(np.dot(nn,cam))))
    out.sort(key=lambda r:r[0])
    for d,xy,kind,sh in out:
        col=cols[kind]
        a.add_patch(Polygon(xy,closed=True,fc=col,ec='#0A1420',lw=1.3,alpha=0.42+0.5*sh,zorder=2))
    allp=np.vstack([np.array(P) for _,P in F]); xy,_=proj(allp,az,el)
    a.set_aspect('equal'); a.set_xlim(xy[:,0].min()-0.25,xy[:,0].max()+0.25)
    a.set_ylim(xy[:,1].min()-0.25,xy[:,1].max()+0.25)
def stereo(a,kind):
    a.set_facecolor(PANEL); a.set_aspect('equal'); a.set_xlim(-1.28,1.28); a.set_ylim(-1.28,1.28)
    th=np.linspace(0,2*np.pi,400)
    a.plot(np.cos(th),np.sin(th),color=PEDGE,lw=2.4)
    def sq(p,c=AMBER,s=0.075):
        a.add_patch(Polygon([[p[0]-s,p[1]],[p[0],p[1]+s],[p[0]+s,p[1]],[p[0],p[1]-s]],fc=c,ec='#07131F',lw=0.8,zorder=5))
    def tri(p,c=GREEN,s=0.08):
        a.add_patch(Polygon([[p[0],p[1]+s],[p[0]-s*0.88,p[1]-s*0.5],[p[0]+s*0.88,p[1]-s*0.5]],fc=c,ec='#07131F',lw=0.8,zorder=5))
    def lens(p,c='#FF7CA8',s=0.075):
        a.add_patch(Polygon([[p[0]-s,p[1]],[p[0],p[1]+s*0.62],[p[0]+s,p[1]],[p[0],p[1]-s*0.62]],fc=c,ec='#07131F',lw=0.8,zorder=5))
    if kind=='m-3m':
        for ang in (0,45,90,135):
            r=np.radians(ang); a.plot([-np.cos(r),np.cos(r)],[-np.sin(r),np.sin(r)],color='#2C6E8F',lw=1.6)
        sq((0,0))
        for ang in (0,90,180,270):
            r=np.radians(ang); sq((np.cos(r),np.sin(r)))
        for ang in (45,135,225,315):
            r=np.radians(ang); tri((0.366*np.sqrt(2)*np.cos(r)/1.0*0.73,0.366*np.sqrt(2)*np.sin(r)*0.73))
        for ang in (45,135,225,315):
            r=np.radians(ang); lens((np.cos(r),np.sin(r)))
        for ang in (0,90,180,270):
            r=np.radians(ang); lens((0.414*np.cos(r),0.414*np.sin(r)))
        a.text(0,-1.19,'3 4-FOLD | 4 3-FOLD | 6 2-FOLD | 9 MP | CENTRE i',color=BODY,fontsize=10.5,ha='center')
    else:
        for ang in range(0,180,30):
            r=np.radians(ang); a.plot([-np.cos(r),np.cos(r)],[-np.sin(r),np.sin(r)],color='#2C6E8F',lw=1.6)
        a.add_patch(Polygon([[0.085*np.cos(np.radians(60*i)),0.085*np.sin(np.radians(60*i))] for i in range(6)],
                    fc=AMBER,ec='#07131F',lw=0.8,zorder=5))
        for ang in range(0,360,30):
            r=np.radians(ang); lens((np.cos(r),np.sin(r)))
        a.text(0,-1.19,'1 6-FOLD | 6 2-FOLD | 7 MP | CENTRE i',color=BODY,fontsize=10.5,ha='center')
    a.axis('off')

# ---------------- 03 SPECIMEN 1 ----------------
fig,ax=new_slide('$ ./analyze_morphology.sh -s 1 -h cubo-octahedral',3)
T(ax,120,H-158,'SPECIMEN 1: CUBO-OCTAHEDRAL HABIT',GREEN,23,'bold')
T(ax,880,H-158,'[MOST PROBABLE: m$\\bar{3}$m (Oh, CLASS 32)]',AMBER,19,'bold')
panel(ax,120,150,700,740)
T(ax,470,852,'HABIT: {111} OCTAHEDRON + {100} CUBE',CYAN,14,'bold',ha='center')
a1=ax_in(fig,150,520,640,320); draw_poly(a1,cubo_faces()); a1.axis('off')
T(ax,470,492,'STEREOGRAM: m$\\bar{3}$m',CYAN,14,'bold',ha='center')
a2=ax_in(fig,290,180,360,300); stereo(a2,'m-3m')
x0=870
T(ax,x0,852,'1. FORMS',AMBER,16,'bold')
bullets(ax,x0,812,['OCTAHEDRON {111} DOMINANT, TRUNCATED AT ITS 6 VERTICES BY CUBE {100}',
 '{100}/{111} INTERFACIAL ANGLE: MEASURED [___] DEGREES, IDEAL 54.74'],dy=36,fs=14)
T(ax,x0,718,'2. OPERATION INVENTORY (48 TOTAL)',AMBER,16,'bold')
bullets(ax,x0,678,['3 4-FOLD ALONG <100>, EACH WITH A COINCIDENT 2-FOLD AND A $\\bar{4}$',
 '4 3-FOLD ALONG <111>, EACH WITH A COINCIDENT $\\bar{3}$ (S6)',
 '6 2-FOLD ALONG <110>',
 '9 MP: 3 PERPENDICULAR TO <100> PLUS 6 DIAGONAL',
 'INVERSION CENTRE PRESENT'],dy=36,fs=14)
T(ax,x0,476,'3. EXCLUSIONS AND VERDICT',AMBER,16,'bold')
bullets(ax,x0,436,['4 NON-COPLANAR 3-FOLD FIX THE CUBIC SYSTEM',
 'm$\\bar{3}$ EXCLUDED BY SQUARE UNSTRIATED {100} AND THE 6 DIAGONAL MP.',
 '    FACE COUNT ALONE CANNOT EXCLUDE IT: {111} IS ALSO A FORM IN m$\\bar{3}$',
 '432 EXCLUDED BY THE OBSERVED MP',
 '$\\bar{4}$3m EXCLUDED BY EQUAL DEVELOPMENT OF ALL 8 {111} FACES'],dy=36,fs=14)
T(ax,x0,250,'VERDICT: m$\\bar{3}$m',GREEN,20,'bold')
T(ax,x0,214,'FULL SYMBOL 4/m $\\bar{3}$ 2/m, HOLOHEDRAL CUBIC',BODY,14)
T(ax,x0,170,'[NOTE] HOLOHEDRY IS THE CEILING OF THE METHOD, NOT A CENTROSYMMETRY PROOF',DIM,12.5)
fig.savefig(OUT+'03.png',facecolor=BG); plt.close(fig)

# ---------------- 04 SPECIMEN 2 ----------------
fig,ax=new_slide('$ ./analyze_morphology.sh -s 2 -h hex-prism-bipyramid',4)
T(ax,120,H-158,'SPECIMEN 2: HEXAGONAL PRISMATIC HABIT',GREEN,23,'bold')
T(ax,960,H-158,'[MOST PROBABLE: 6/mmm (D6h, CLASS 27)]',AMBER,19,'bold')
panel(ax,120,150,700,740)
T(ax,470,852,'HABIT: {10$\\bar{1}$0} PRISM + {10$\\bar{1}$1} BIPYRAMID',CYAN,14,'bold',ha='center')
a1=ax_in(fig,150,520,640,320); draw_poly(a1,hexbipy()); a1.axis('off')
T(ax,470,492,'STEREOGRAM: 6/mmm',CYAN,14,'bold',ha='center')
a2=ax_in(fig,290,180,360,300); stereo(a2,'6/mmm')
x0=870
T(ax,x0,852,'1. FORMS',AMBER,16,'bold')
bullets(ax,x0,812,['PRISM {10$\\bar{1}$0}: 6 VERTICAL FACES, 120-DEGREE EDGES',
 'BIPYRAMID {10$\\bar{1}$1} CAPS, EQUALLY DEVELOPED ABOVE AND BELOW'],dy=36,fs=14)
T(ax,x0,718,'2. OPERATION INVENTORY (24 TOTAL)',AMBER,16,'bold')
bullets(ax,x0,678,['1 6-FOLD ALONG [0001] WITH COINCIDENT 3-FOLD, 2-FOLD, $\\bar{6}$ (S3) AND S6',
 '6 BASAL 2-FOLD: 3 PERPENDICULAR TO PRISM FACES, 3 TO PRISM EDGES',
 '7 MP: 1 BASAL PLUS 6 VERTICAL',
 'INVERSION CENTRE PRESENT'],dy=36,fs=14)
T(ax,x0,512,'3. EXCLUSIONS AND VERDICT',AMBER,16,'bold')
bullets(ax,x0,472,['6mm EXCLUDED: IDENTICAL CAPS DEMAND THE BASAL MP',
 '6/m EXCLUDED BY THE 6 BASAL DIADS',
 '6 AND 622 EXCLUDED BY MP PLUS INVERSION CENTRE',
 '$\\bar{6}$m2 AND THE TRIGONAL MIMICS $\\bar{3}$m, 32, 3m EXCLUDED:',
 '    6 EQUAL CAP FACES, NOT 3 PLUS 3 ALTERNATING'],dy=36,fs=14)
T(ax,x0,268,'VERDICT: 6/mmm',GREEN,20,'bold')
T(ax,x0,232,'FULL SYMBOL 6/m 2/m 2/m, HOLOHEDRAL HEXAGONAL',BODY,14)
T(ax,x0,186,'[NOTE] A TRIGONAL CRYSTAL CAN MIMIC THIS HABIT, SO CAP-FACE EQUIVALENCE',DIM,12.5)
T(ax,x0,160,'       IS THE DECIDING OBSERVATION',DIM,12.5)
fig.savefig(OUT+'04.png',facecolor=BG); plt.close(fig)
print('A OK')
