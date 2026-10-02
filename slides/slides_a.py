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

# =====================================================================================
# PART A, REBUILT FROM THE CLASS PHOTOGRAPHS (part_a_photos/picture1-5.jpg).
# EVERY NUMBER ON SLIDES 02-04 COMES FROM part_a_photos/measure.json, WRITTEN BY
# part_a_photos/measure_edges.py (LSD EDGE FIT ON THE FULL-RESOLUTION PHOTOS).
# =====================================================================================
import json
from PIL import Image
PA='/data/repo/part_a_photos/'
MJ=json.load(open(PA+'measure.json'))
SM=MJ['_summary']
SCL=3072/900
CEN=[(115,105),(760,155),(190,410),(665,415),(230,688),(600,700),(318,925),(518,942),(335,1112),(458,1125)]
ISO={3:(445,600),4:(463,662),5:(430,715)}
_IMG={}
def photo(i):
    if i not in _IMG: _IMG[i]=np.asarray(Image.open(PA+f'picture{i}.jpg').convert('RGB')).astype(np.float32)
    return _IMG[i]
def stretch(a,lo=0.8,hi=99.6):
    l,h=np.percentile(a,lo),np.percentile(a,hi)
    return np.clip((a-l)/(h-l),0,1)
def crop(i,cx,cy,w,h,dx=0,dy=0):
    X,Y=int(cx*SCL)+dx,int(cy*SCL)+dy
    return photo(i)[Y-h//2:Y+h//2,X-w//2:X+w//2]
def imax(fig,x,y,w,h,edge=PEDGE,lw=1.4):
    a=fig.add_axes([x/W,y/H,w/W,h/H]); a.set_xticks([]); a.set_yticks([])
    for s in a.spines.values(): s.set_color(edge); s.set_linewidth(lw)
    return a
def tagbox(a,x,y,s,c=CYAN,fs=10.5):
    a.text(x,y,s,color=c,fontsize=fs,weight='bold',ha='center',va='center',family='monospace',
           bbox=dict(boxstyle='square,pad=0.18',fc='#05080CCC',ec=c,lw=1.0),zorder=6)

# ---------------- 02 THE CRYSTALS AS PHOTOGRAPHED ----------------
fig,ax=new_slide('$ ls ./part_a/photos && cat observation.log',2)
T(ax,120,H-158,'PART A: THE CRYSTALS ISSUED IN CLASS, AS PHOTOGRAPHED',GREEN,23,'bold')
T(ax,1800,H-158,'[5 PHOTOS | 11 CRYSTALS | NO SCALE BAR]',AMBER,17,'bold',ha='right')
# --- left: picture 1 with labels
panel(ax,120,130,500,760)
T(ax,370,862,'PICTURE 1: 10 CRYSTALS, C1 TO C10',CYAN,14,'bold','center')
a=imax(fig,140,192,460,613)
import cv2
p1=np.asarray(Image.open(PA+'picture1.jpg').convert('RGB').resize((900,1200),Image.LANCZOS)).astype(np.float32)
p1=p1/cv2.GaussianBlur(p1,(0,0),45); p1=np.clip(p1/np.percentile(p1,96)*0.94,0,1)   # FLAT-FIELD THE PAPER
a.imshow(p1,extent=(0,900,1200,0)); a.set_xlim(0,900); a.set_ylim(1200,0)
SIDE=[1,-1,1,-1,1,-1,-1,1,-1,1]       # LABEL LEFT OR RIGHT OF EACH CRYSTAL
for k,(x,y) in enumerate(CEN):
    tagbox(a,x+SIDE[k]*80,y,f'C{k+1}',fs=10.5)
T(ax,370,162,'PICTURE 2 IS THE SAME LAYOUT, RETAKEN',MUTE,11.5,ha='center')
# --- middle: views A-C and detail crops
panel(ax,650,130,560,760)
T(ax,930,862,'ONE CRYSTAL ALONE: VIEWS A, B, C',CYAN,14,'bold','center')
T(ax,930,834,'(PICTURES 3, 4, 5; TURNED BETWEEN SHOTS)',MUTE,11,ha='center')
for j,(i,lab) in enumerate([(3,'A: FROSTED FACE'),(4,'B: SMOOTH FACE'),(5,'C: TURNED OVER')]):
    x0=672+j*178
    a=imax(fig,x0,500,160,300)
    a.imshow(stretch(crop(i,*ISO[i],320,600,dy=20)))
    T(ax,x0+80,478,lab,BODY,11,'bold','center')
T(ax,930,436,'DETAILS FROM PICTURE 1',CYAN,14,'bold','center')
for j,(k,l1,l2) in enumerate([(3,'C3: TOP + SIDE','FACE, SQUARE'),(6,'C6: FROSTED','CENTRE'),
                              (1,'C1: BANDS IN','THE BODY'),(10,'C10: CRACK','ALONG A FACE')]):
    x0=668+j*134
    a=imax(fig,x0,262,124,124)
    a.imshow(stretch(crop(1,*CEN[k-1],340,340)))
    T(ax,x0+62,240,l1,BODY,10,'bold','center'); T(ax,x0+62,218,l2,BODY,10,'bold','center')
T(ax,930,170,'LIGHT FROM THE RIGHT: THE DARK BAND ON THE',MUTE,10.5,ha='center')
T(ax,930,150,'LEFT OF EACH CRYSTAL IS ITS SHADOW',MUTE,10.5,ha='center')
# --- right: observation log
panel(ax,1240,130,560,760)
T(ax,1265,862,'OBSERVATION LOG',AMBER,15,'bold')
bullets(ax,1265,822,[
 ('[COUNT]','10 IN PICTURES 1-2, PLUS ONE CRYSTAL'),('','ALONE IN 3 POSES (PICTURES 3-5)'),
 ('[COLOUR]','COLOURLESS. THE SLIGHT WARM CAST IS'),('','ALSO IN THE SHADOWS, SO IT IS LIGHTING'),
 ('[LUSTRE]','VITREOUS AND TRANSLUCENT; FROSTED'),('','FACE CENTRES ON C5, C6, C10, VIEW A'),
 ('[HABIT]','BLOCKY BOXES; PLAN L/W 1.0 TO 2.0'),
 ('[FACES]','FLAT, IN PARALLEL OPPOSITE PAIRS;'),('','STRAIGHT EDGES; FLAT, BLUNT ENDS'),
 ('[ANGLES]','EVERY CLEAN CORNER LOOKS SQUARE'),
 ('[ABSENT]','NO PYRAMID, DOME OR CORNER FACET'),('','RESOLVED ON ANY OF THE 11 CRYSTALS'),
 ('[DEFECTS]','ROUNDED EDGES, CHIPPED ENDS AND'),('','CRACKS RUNNING PARALLEL TO A FACE'),
 ('[SCALE]','NO SCALE OBJECT: SIZES AS RATIOS'),
],dy=37,fs=12.5,marker='',headc=CYAN,pad=10)
panel(ax,1262,160,516,96,fill='#07160F',edge=GREEN,lw=1.4,r=6)
T(ax,1280,231,'READ-OUT: ONE GEOMETRY ONLY. SIX FLAT FACES',GREEN,12.5,'bold')
T(ax,1280,203,'IN THREE PARALLEL PAIRS, MEETING SQUARE,',GREEN,12.5,'bold')
T(ax,1280,175,'WHATEVER THE LENGTH OF THE CRYSTAL',GREEN,12.5,'bold')
T(ax,120,92,'$ ./measure_angles.py --photos 1,4 --edges lsd',ORANGE,17)
T(ax,120,56,'[STATUS] 11 OUTLINES PASSED TO THE EDGE FIT ON SLIDE 03',BODY,13)
fig.savefig(OUT+'02.png',facecolor=BG); plt.close(fig)

# ---------------- 03 MEASURED ANGLES AND THE IDEALISED HABIT ----------------
def seg_overlay(a,name,i,cx,cy,r):
    rec=MJ[name]; segs=rec['segs']
    a.imshow(stretch(crop(i,cx,cy,2*r,2*r)),extent=(0,2*r,2*r,0))
    a.set_xlim(0,2*r); a.set_ylim(2*r,0)
    for sid in rec['prism']:
        x1,y1,x2,y2=segs[sid]; a.plot([x1,x2],[y1,y2],color=CYAN,lw=3.0,solid_capstyle='round')
    for nm,e in rec['ends'].items():
        col=GREEN if e['clean'] else RED; P=[]
        for sid in e['ids']:
            x1,y1,x2,y2=segs[sid]; a.plot([x1,x2],[y1,y2],color=col,lw=3.0,solid_capstyle='round')
            P+= [(x1,y1),(x2,y2)]
        P=np.array(P).mean(0); c=np.array([r,r]); v=P-c; v=v/np.linalg.norm(v)
        q=np.clip(P+v*48,30,2*r-30)
        a.text(q[0],q[1],f"{e['corner']:.1f}",color=col,fontsize=11,weight='bold',ha='center',va='center',
               family='monospace',bbox=dict(boxstyle='square,pad=0.15',fc='#05080CDD',ec=col,lw=1.0))
fig,ax=new_slide('$ ./measure_angles.py --photos 1,4 --edges lsd --report',3)
T(ax,120,H-158,'MORPHOLOGY: ONE ANGLE, MANY SHAPES',GREEN,23,'bold')
T(ax,1800,H-158,'[STENO 1669, TESTED ON THESE CRYSTALS]',AMBER,17,'bold',ha='right')
# --- left: four fitted crops
panel(ax,120,130,580,760)
T(ax,410,862,'EDGES FITTED BY LINE-SEGMENT DETECTION',CYAN,14,'bold','center')
T(ax,410,836,'CYAN: PRISM EDGES | GREEN: CLEAN END | RED: CHIPPED END',MUTE,10.5,ha='center')
for j,(name,i,lab) in enumerate([('C4',1,'C4'),('C6',1,'C6'),('C7',1,'C7'),('PIC4',4,'VIEW B')]):
    x0=145+(j%2)*275; y0=560-(j//2)*335
    if name=='PIC4': cx,cy=ISO[4]; r=250
    else: cx,cy=CEN[int(name[1:])-1]; r=190
    a=imax(fig,x0,y0,255,255); seg_overlay(a,name,i,cx,cy,r)
    tagbox(a,2*r*0.12,2*r*0.09,lab,c=AMBER,fs=10.5)
for (x0,y0,t1,t2) in [(272,550,'RIGHT END SQUARE,','LEFT END ROUNDED'),(547,550,'BOTH ENDS SQUARE',''),
                      (272,215,'SQUARE CORNER',''),(547,215,'BOTTOM END SQUARE,','TOP END ROUGH')]:
    T(ax,x0,y0-10,t1,BODY,10.5,'bold','center')
    if t2: T(ax,x0,y0-31,t2,BODY,10.5,'bold','center')
# --- middle: angle and aspect plots
panel(ax,725,130,600,760)
T(ax,1025,862,'CORNER ANGLE PER CRYSTAL',CYAN,14,'bold','center')
names=[f'C{k}' for k in range(1,11)]+['PIC4']; labs=names[:-1]+['B']
def darkax(x,y,w,h):
    a=fig.add_axes([x/W,y/H,w/W,h/H]); a.set_facecolor('#08131F')
    for s in a.spines.values(): s.set_color(PEDGE)
    a.tick_params(colors=BODY,labelsize=10)
    for t in a.get_xticklabels()+a.get_yticklabels(): t.set_family('monospace')
    return a
a=darkax(800,585,500,235)
a.axhspan(SM['clean_min'],SM['clean_max'],color=GREEN,alpha=0.10)
a.axhline(90,color=AMBER,lw=1.4,ls='--')
for k,nm in enumerate(names):
    rec=MJ.get(nm,{})
    for e in rec.get('ends',{}).values():
        if e['clean']: a.plot(k,e['corner'],'o',ms=8,mfc=GREEN,mec='#04140A')
        else: a.plot(k,e['corner'],'x',ms=9,mew=2.4,color=RED)
    if 'ends' not in rec: a.text(k,72,'N/M',color=MUTE,fontsize=8.5,ha='center',family='monospace')
a.set_xticks(range(len(labs))); a.set_xticklabels(labs,family='monospace',fontsize=9.5)
a.set_ylim(66,94); a.set_xlim(-0.6,len(labs)-0.4); a.set_yticks([70,75,80,85,90])
a.set_ylabel('DEGREES',color=BODY,fontsize=10,family='monospace')
T(ax,1025,530,f"CLEAN: {SM['clean_n']} CORNERS, {SM['clean_min']:.1f} TO {SM['clean_max']:.1f}, MEAN {SM['clean_mean']:.1f}",GREEN,11.5,'bold','center')
T(ax,1025,507,f"CHIPPED: {len(SM['oblique'])} ENDS, {min(SM['oblique']):.1f} TO {max(SM['oblique']):.1f}, NEVER IN PARALLEL PAIRS",RED,11.5,'bold','center')
T(ax,1025,466,'PLAN-VIEW LENGTH / WIDTH',CYAN,14,'bold','center')
a=darkax(800,232,500,205)
asp=[MJ[nm]['aspect'] if 'aspect' in MJ.get(nm,{}) else np.nan for nm in names]
a.bar(range(len(labs)),[0 if np.isnan(v) else v-0.9 for v in asp],bottom=0.9,color=CYAN,alpha=0.85,width=0.62)
for k,v in enumerate(asp):
    if not np.isnan(v): a.text(k,v+0.04,f'{v:.2f}',color=BODY,fontsize=8,ha='center',family='monospace')
for k,v in enumerate(asp):
    if np.isnan(v): a.text(k,1.06,'N/M',color=MUTE,fontsize=8.5,ha='center',family='monospace')
a.set_xticks(range(len(labs))); a.set_xticklabels(labs,family='monospace',fontsize=9.5)
a.set_ylim(0.9,2.2); a.set_xlim(-0.6,len(labs)-0.4); a.set_yticks([1.0,1.5,2.0])
T(ax,1025,180,f"L/W {min(SM['aspect']):.2f} TO {max(SM['aspect']):.2f} IN ONE BATCH: SHAPE VARIES",AMBER,11.5,'bold','center')
T(ax,1025,157,'2-FOLD, THE ANGLE DOES NOT',AMBER,11.5,'bold','center')
# --- right: idealised habit
panel(ax,1350,130,450,760)
T(ax,1575,862,'IDEALISED HABIT: CUBE {100}',CYAN,14,'bold','center')
def box(hx,hy,hz):
    V=lambda sx,sy,sz:np.array([sx*hx,sy*hy,sz*hz])
    F=[]
    for s in (1,-1):
        F.append(('x',[V(s,-1,-1),V(s,1,-1),V(s,1,1),V(s,-1,1)]))
        F.append(('y',[V(-1,s,-1),V(1,s,-1),V(1,s,1),V(-1,s,1)]))
        F.append(('z',[V(-1,-1,s),V(1,-1,s),V(1,1,s),V(-1,1,s)]))
    return F
def drawbox(a,F,az=212,el=22,lab=True,ext=None,lfs=10.5):
    a.set_facecolor(PANEL); a.axis('off')
    e1,e2,n=rot(az,el); cam=-n; vis=[]
    for kind,P in F:
        P=np.array(P); c=P.mean(0); nn=c/np.linalg.norm(c) if kind else c
        nn=np.zeros(3); nn['xyz'.index(kind)]=np.sign(c['xyz'.index(kind)])
        if np.dot(nn,cam)<=0.02: continue
        xy,_=proj(P,az,el); sh=abs(np.dot(nn,cam))
        al=0.30+0.55*sh
        a.add_patch(Polygon(xy,closed=True,fc='#4FC3D9',ec='#0A1420',lw=1.4,alpha=al,zorder=2))
        fcol=tuple(al*np.array([0x4F,0xC3,0xD9])/255+(1-al)*np.array([0x0C,0x1E,0x33])/255)
        vis.append((kind,np.sign(c['xyz'.index(kind)]),proj(c,az,el)[0][0],fcol))
    if lab:
        L={('x',1):'(100)',('y',1):'(010)',('z',1):'(001)',('x',-1):'($\\bar{1}$00)',('y',-1):'(0$\\bar{1}$0)'}
        for kind,s,cxy,fcol in vis:
            if (kind,s) in L: a.text(cxy[0],cxy[1],L[(kind,s)],color='#04101A',fontsize=lfs,weight='bold',
                                     ha='center',va='center',family='monospace',zorder=4,
                                     bbox=dict(boxstyle='square,pad=0.12',fc=fcol,ec='none'))
    allp=np.vstack([np.array(P) for _,P in F]); xy,_=proj(allp,az,el)
    a.set_aspect('equal')
    pad=0.35 if ext is None else ext
    a.set_xlim(xy[:,0].min()-pad,xy[:,0].max()+pad); a.set_ylim(xy[:,1].min()-pad,xy[:,1].max()+pad)
    return az,el
a=fig.add_axes([1380/W,560/H,390/W,270/H]); az,el=drawbox(a,box(1,1,1),ext=0.55)
for d,c,mk in [((0,0,1),AMBER,'s'),((1,1,1),GREEN,'^'),((0,1,1),'#FF7CA8','D')]:
    d=np.array(d,float); d=d/np.linalg.norm(d)*(1.62 if mk=='s' else (1.75 if mk=='^' else 1.62))
    P,_=proj(np.vstack([-d,d]),az,el)
    a.plot(P[:,0],P[:,1],color=c,lw=1.6,ls='--',zorder=3)
    a.plot(P[1,0],P[1,1],mk,ms=9,mfc=c,mec='#04140A',zorder=5)
T(ax,1575,538,'AMBER 4-FOLD: FACE TO FACE',AMBER,10.5,'bold','center')
T(ax,1575,516,'GREEN 3-FOLD: CORNER TO CORNER',GREEN,10.5,'bold','center')
T(ax,1575,494,'PINK 2-FOLD: EDGE TO EDGE',"#FF7CA8",10.5,'bold','center')
a=fig.add_axes([1380/W,300/H,390/W,170/H]); drawbox(a,box(1.9,0.95,0.95),az=222,el=20,ext=0.3,lfs=9.5)
bullets(ax,1372,268,[
 'SAME 6 FACES, SAME 90-DEGREE ANGLES;',
 'ONLY THE CENTRAL DISTANCES DIFFER,',
 'AS IN C4, C7 AND VIEW B',
 None,
 'FORM: CUBE {100}, 6 FACES = ALL SEEN',
],dy=25,fs=11,marker='',lc=BODY)
T(ax,120,92,'$ ./measure_angles.py --summary',ORANGE,17)
T(ax,120,56,f"[RESULT] {SM['clean_n']} CLEAN CORNERS = 90 READ WITH ABOUT 2.4 DEGREES OF EDGE NOISE (A FOLDED SCATTER READS LOW) | "
           "OPPOSITE EDGES PARALLEL WITHIN 1 TO 7 DEGREES",BODY,12)
fig.savefig(OUT+'03.png',facecolor=BG); plt.close(fig)

# ---------------- 04 POINT GROUP ----------------
def sproj(v):
    v=np.array(v,float); v=v/np.linalg.norm(v)
    if v[2]<0: v=-v
    return np.array([v[0],v[1]])/(1+v[2])
def stereo_m3m(a):
    a.set_facecolor(PANEL); a.set_aspect('equal'); a.set_xlim(-1.22,1.22); a.set_ylim(-1.22,1.22); a.axis('off')
    th=np.linspace(0,2*np.pi,400); a.plot(np.cos(th),np.sin(th),color=PEDGE,lw=2.6)
    MPC='#2C8FB8'
    for ang in (0,45,90,135):
        r=np.radians(ang); a.plot([-np.cos(r),np.cos(r)],[-np.sin(r),np.sin(r)],color=MPC,lw=1.5)
    for nrm in [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1)]:
        nrm=np.array(nrm,float); nrm/=np.linalg.norm(nrm)
        u=np.cross(nrm,[0,0,1.]) if abs(nrm[2])<0.99 else np.array([1.,0,0]); u/=np.linalg.norm(u); w=np.cross(nrm,u)
        pts=[]
        for t in np.linspace(0,np.pi,200):
            v=np.cos(t)*u+np.sin(t)*w
            if v[2]<0: v=-v
            pts.append(sproj(v))
        pts=np.array(pts); a.plot(pts[:,0],pts[:,1],color=MPC,lw=1.5)
    def sq(p,s=0.07,c='#7FE3F2'):
        a.add_patch(Polygon([[p[0]-s,p[1]-s],[p[0]+s,p[1]-s],[p[0]+s,p[1]+s],[p[0]-s,p[1]+s]],fc='none',ec=c,lw=2.0,zorder=5))
    def tri(p,s=0.075,c=GREEN):
        a.add_patch(Polygon([[p[0],p[1]+s],[p[0]-s*0.87,p[1]-s*0.5],[p[0]+s*0.87,p[1]-s*0.5]],fc=c,ec='#07131F',lw=0.8,zorder=5))
    def lens(p,ang,s=0.07,c='#FF7CA8'):
        r=np.radians(ang); u=np.array([np.cos(r),np.sin(r)]); v=np.array([-u[1],u[0]])
        a.add_patch(Polygon([p-s*u,p+0.55*s*v,p+s*u,p-0.55*s*v],fc=c,ec='#07131F',lw=0.8,zorder=5))
    for v in [(0,0,1),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]: sq(sproj(v))
    for v in [(1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1)]: tri(sproj(v))
    for v in [(1,1,0),(-1,1,0),(-1,-1,0),(1,-1,0)]:
        p=sproj(v); lens(p,np.degrees(np.arctan2(p[1],p[0]))+90)
    for v in [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1)]:
        p=sproj(v); lens(p,np.degrees(np.arctan2(p[1],p[0]))+90)
    for v in [(0,0,1),(1,0,0),(-1,0,0),(0,1,0),(0,-1,0)]:
        p=sproj(v); a.add_patch(Circle(p,0.042,fc=AMBER,ec='#07131F',lw=0.6,zorder=7))
        a.add_patch(Circle(p,0.105,fc='none',ec=AMBER,lw=1.6,zorder=7))
    for p,t,dx,dy in [((0,0),'(001)',0.0,-0.19),((0,-1),'(100)',0.27,-0.09),((1,0),'(010)',-0.02,0.18)]:
        p=np.array(p,float); a.text(p[0]+dx,p[1]+dy,t,color=AMBER,fontsize=10,weight='bold',ha='center',va='center',family='monospace',zorder=8,
                                    bbox=dict(boxstyle='square,pad=0.1',fc=PANEL,ec='none'))
fig,ax=new_slide('$ ./assign_point_group.sh --form cube --rule holohedry',4)
T(ax,120,H-158,'POINT GROUP: OPERATIONS, EXCLUSIONS AND VERDICT',GREEN,23,'bold')
T(ax,1800,H-158,'[MOST PROBABLE: m$\\bar{3}$m (Oh, CLASS 32)]',AMBER,19,'bold',ha='right')
panel(ax,120,130,560,760)
T(ax,400,862,'STEREOGRAM: m$\\bar{3}$m WITH THE OBSERVED POLES',CYAN,14,'bold','center')
a=fig.add_axes([175/W,445/H,450/W,400/H]); stereo_m3m(a)
bullets(ax,140,428,[
 ('AMBER','THE 6 OBSERVED FACE POLES {100}'),
 ('SQUARE','4-FOLD  |  TRIANGLE 3-FOLD  |  LENS 2-FOLD'),
 ('LINES','9 MP: PRIMITIVE + 4 DIAMETERS + 4 ARCS'),
],dy=27,fs=11,marker='',headc=AMBER,pad=7)
T(ax,140,334,'OPERATION INVENTORY (48), MAPPED ONTO THE CRYSTAL',AMBER,12.5,'bold')
bullets(ax,140,302,[
 ('3 4-FOLD','FACE CENTRE TO FACE CENTRE, EACH'),('','WITH A COINCIDENT 2-FOLD AND $\\bar{4}$'),
 ('4 3-FOLD','CORNER TO CORNER, EACH WITH $\\bar{3}$'),
 ('6 2-FOLD','EDGE MIDPOINT TO EDGE MIDPOINT'),
 ('9 MP','3 PARALLEL TO FACES + 6 THROUGH EDGES'),
 ('CENTRE i','EVERY FACE HAS A PARALLEL PARTNER'),
],dy=27,fs=11,marker='[>]',headc=CYAN,pad=9)
panel(ax,705,130,1095,760)
T(ax,730,862,'EXCLUSION CHAIN: WHAT EACH CANDIDATE NEEDS AGAINST WHAT THE PHOTOS SHOW',AMBER,13.5,'bold')
x=730; fs=11.5
row(ax,x,826,[(0,'CANDIDATE',CYAN),(15,'NEEDS',CYAN),(50,'PHOTOS SHOW',CYAN),(91,'RESULT',CYAN)],fs=fs,w='bold')
rule(ax,x,810,1050)
CH=[('1, $\\bar{1}$','SOME CORNER (IA) AWAY FROM 90','11 CLEAN CORNERS, 86 TO 90','EXCLUDED',RED),
    ('2, m, 2/m','BOTH ENDS TILTED AND PARALLEL','NONE: THE 6 TILTED ENDS ARE','EXCLUDED',RED),
    ('','(AN OBLIQUE PINACOID)','CHIPPED AND NEVER PARALLEL','',RED),
    ('HEX, TRIGONAL','60, 120 OR RHOMB CORNERS','RIGHT ANGLES ONLY','EXCLUDED',RED),
    ('mmm, 4/mmm','A FIXED LONG AXIS WITH ITS OWN','L/W WANDERS 1.0 TO 2.0;','RUNNER-UP',AMBER),
    ('','FACE TYPE (2 OR 3 FORMS)','NO FACE TYPE TIED TO ONE AXIS','',AMBER),
    ('23, m$\\bar{3}$','STRIATED FACES OR {hk0} FACETS','NONE RESOLVED','NOT INDICATED',MUTE),
    ('432, $\\bar{4}$3m','TWISTED ETCH PITS, {111} FACETS','NO FACETS BEYOND THE CUBE','NOT INDICATED',MUTE),
    ('m$\\bar{3}$m','ONE FORM, CUBE {100}: 3 SQUARE','EXACTLY THIS, IN ALL 11','MOST PROBABLE',GREEN),
    ('','PAIRS OF FACES AT 90','','',GREEN)]
for k,(c1,c2,c3,c4,cc) in enumerate(CH):
    y=785-k*29
    row(ax,x,y,[(0,c1,GREEN if c1 else BODY),(15,c2),(50,c3),(91,c4,cc)],fs=fs,w='bold' if c4 else 'normal')
rule(ax,x,488,1050,c='#2B3942')
T(ax,x,460,'VERDICT: m$\\bar{3}$m',GREEN,21,'bold')
T(ax,1050,460,'FULL SYMBOL 4/m $\\bar{3}$ 2/m  |  Oh  |  HOLOHEDRAL CUBIC  |  48 OPERATIONS',BODY,12.5)
bullets(ax,x,420,[
 ('WHY:','THE CUBE {100} ALONE REPRODUCES EVERY FACE AND EVERY ANGLE SEEN; A BOX NEEDS 2 OR 3 FORMS'),
 ('','FOR THE SAME FACES, AND NOTHING MEASURED TIES THE ELONGATION OR A FACE TYPE TO ONE AXIS'),
 ('HOLOHEDRY:','THE CUBE LOOKS THE SAME IN ALL 5 CUBIC CLASSES, SO THE FULL CLASS IS TAKEN, AS IS STANDARD'),
 ('LIMIT:','A TETRAGONAL OR ORTHORHOMBIC BOX HAS THE SAME 90-DEGREE ANGLES, SO FORM ALONE CANNOT'),
 ('','EXCLUDE IT; CENTRE i COMES FROM PARALLEL FACE PAIRS ONLY (NO PIEZO OR PYRO TEST)'),
 ('RANKING:','m$\\bar{3}$m, THEN 4/mmm AND mmm (SAME ANGLES, MORE FORMS); ALL LOWER SYSTEMS FAIL ON ANGLES'),
 ('TEST:','CROSSED POLARISERS (LCD SCREEN + POLARISING FILTER), CLEAR CRYSTAL ON EACH'),
 ('','OF ITS 3 FACE TYPES, TURNED: CUBIC STAYS DARK ON ALL 3; 4/mmm IS DARK ON ONE ONLY;'),
 ('','mmm ON NONE (A BIREFRINGENT VIEW GOES DARK EVERY 90 DEGREES, BRIGHT BETWEEN)'),
],dy=31,fs=11.5,marker='[>]',headc=CYAN,pad=11)
T(ax,120,92,'$ ./assign_point_group.sh --report',ORANGE,17)
T(ax,120,56,'[RESULT] MOST PROBABLE POINT GROUP m$\\bar{3}$m; RUNNER-UP 4/mmm, THEN mmm; DECIDED BY ONE CROSSED-POLARISER CHECK',GREEN,12.5)
fig.savefig(OUT+'04.png',facecolor=BG); plt.close(fig)
print('A OK')
