import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Polygon, FancyArrow
plt.rcParams['font.family']='monospace'
plt.rcParams['font.monospace']=['DejaVu Sans Mono']
plt.rcParams['axes.unicode_minus']=False
# OVERHEAD BAR NOTATION. THE COMBINING MACRON U+0304 AND OVERLINE U+0305 BOTH LAND
# ON THE WRONG GLYPH IN MATPLOTLIB, WHICH DOES NOT DO COMPLEX SHAPING, SO BARS ARE
# WRITTEN AS MATHTEXT $\bar{n}$ AND MATHTEXT IS POINTED AT THE SAME MONO FACE.
plt.rcParams['mathtext.fontset']='custom'
plt.rcParams['mathtext.rm']='DejaVu Sans Mono'
plt.rcParams['mathtext.it']='DejaVu Sans Mono'
plt.rcParams['mathtext.bf']='DejaVu Sans Mono:bold'
plt.rcParams['mathtext.default']='regular'
W,H=1920.,1080.
BG='#05080C'; BAR='#24E06E'; BARTXT='#04140A'; ORANGE='#FFB03A'; GREEN='#36F08C'
CYAN='#58D3E8'; BODY='#C9D2D8'; DIM='#38464D'; PANEL='#0C1E33'; PEDGE='#3FC7DE'
MUTE='#8C9AA4'; AMBER='#FFC857'; RED='#E8392F'; WHITE='#FFFFFF'; GRID='#14314F'; VIOLET='#B99BE8'
def new_slide(cmd, page, total=15, tildes=(300,780)):
    # page MAY BE AN int (NUMBERED ANSWER SLIDE) OR A str SUCH AS '[QUESTION]',
    # WHICH IS PRINTED VERBATIM SO QUESTION SLIDES STAY OUT OF THE COUNT.
    fig=plt.figure(figsize=(19.2,10.8),dpi=100); fig.patch.set_facecolor(BG)
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis('off')
    ax.add_patch(Rectangle((0,H-30),W,30,color=BAR,zorder=5))
    ax.add_patch(Rectangle((0,0),W,30,color=BAR,zorder=5))
    ax.text(22,H-15,'CML6032@IITD:~/ASSIGNMENT',color=BARTXT,fontsize=11,weight='bold',va='center',zorder=6)
    ax.text(W-22,H-15,'VT100 | Bourne shell',color=BARTXT,fontsize=11,weight='bold',va='center',ha='right',zorder=6)
    ax.text(22,15,'assignment1.tex',color=BARTXT,fontsize=11,weight='bold',va='center',zorder=6)
    ax.text(W/2,15,'[READ ONLY]',color=BARTXT,fontsize=11,weight='bold',va='center',ha='center',zorder=6)
    tag = page if isinstance(page,str) else f'{page}/{total}'
    ax.text(W-22,15,tag,color=BARTXT,fontsize=11,weight='bold',va='center',ha='right',zorder=6)
    for y in range(int(tildes[0]),int(tildes[1]),30): ax.text(60,y,'~',color=DIM,fontsize=12,va='center')
    if cmd: ax.text(120,H-95,cmd,color=ORANGE,fontsize=21,va='center')
    return fig,ax
def T(ax,x,y,s,c=BODY,fs=13,w='normal',ha='left',va='center',fam='monospace',z=4):
    return ax.text(x,y,s,color=c,fontsize=fs,weight=w,ha=ha,va=va,family=fam,zorder=z)
def panel(ax,x,y,w,h,fill=PANEL,edge=PEDGE,lw=1.8,r=10):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle=f'round,pad=0,rounding_size={r}',
        fc=fill,ec=edge,lw=lw,zorder=1)); return None
CW=0.602*100/72.0          # DejaVu Sans Mono advance, px per pt of fontsize
def cw(fs,n=1): return n*fs*CW
def bullets(ax,x,y0,lines,dy=34,fs=13,marker='[>]',mc=AMBER,lc=BODY,headc=CYAN,gap=1,pad=None):
    """lines: str | (head,rest) | None (half-space). Label column auto-sized."""
    y=y0
    mw=cw(fs,len(marker)+gap)
    if pad is None:
        heads=[l[0] for l in lines if isinstance(l,tuple)]
        pad=(max(len(h) for h in heads)+2) if heads else 0
    for ln in lines:
        if ln is None: y-=dy*0.45; continue
        if marker: T(ax,x,y,marker,mc,fs,'bold')
        if isinstance(ln,tuple):
            head,rest=ln
            T(ax,x+mw,y,head,headc,fs,'bold')
            T(ax,x+mw+cw(fs,pad),y,rest,lc,fs)
        else:
            T(ax,x+mw,y,ln,lc,fs)
        y-=dy
    return y
def row(ax,x,y,cells,fs=12,c=BODY,w='normal'):
    """cells: list of (col_in_chars, text) or (col, text, colour)"""
    for cell in cells:
        col,txt=cell[0],cell[1]; col_c=cell[2] if len(cell)>2 else c
        T(ax,x+cw(fs,col),y,str(txt),col_c,fs,w)
def rule(ax,x,y,w_,c=PEDGE,lw=1.2,z=3): ax.plot([x,x+w_],[y,y],color=c,lw=lw,zorder=z)
# ---------- 3D projection ----------
def rot(az=24,el=16):
    a,e=np.radians(az),np.radians(el)
    e1=np.array([np.cos(a),-np.sin(a),0.])
    e2=np.array([np.sin(a)*np.sin(e),np.cos(a)*np.sin(e),np.cos(e)])
    n=np.array([np.sin(a)*np.cos(e),np.cos(a)*np.cos(e),-np.sin(e)])
    return e1,e2,n
def proj(P,az=24,el=16):
    e1,e2,n=rot(az,el); P=np.atleast_2d(P)
    return np.c_[P@e1,P@e2], P@n
CELL_E=[(0,1),(0,2),(0,4),(1,3),(1,5),(2,3),(2,6),(3,7),(4,5),(4,6),(5,7),(6,7)]
def cube_pts(): return np.array([[i,j,k] for i in (0,1) for j in (0,1) for k in (0,1)],float)
def sphere(ax,c,r,col,z):
    ax.add_patch(Circle(c,r,fc=col,ec='#2A2A2A',lw=0.7,zorder=z))
    ax.add_patch(Circle((c[0]-0.33*r,c[1]+0.33*r),0.34*r,fc='white',ec='none',alpha=0.55,zorder=z+0.01))
def draw_structure(ax,basis,a_pm,radii,colors,az=24,el=16,bonds=True,scale=0.8,bond_cut=1.28,cdim=None):
    ax.set_facecolor(WHITE)
    for s in ax.spines.values(): s.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    cdim=cdim or (1.,1.,1.)
    M=np.diag(cdim)
    at=[]
    for sp,x,y,z in basis:
        for dx in ([0,1] if abs(x)<1e-6 else [0]):
            for dy in ([0,1] if abs(y)<1e-6 else [0]):
                for dz in ([0,1] if abs(z)<1e-6 else [0]):
                    at.append((sp,np.array([x+dx,y+dy,z+dz])))
    P=np.array([p for _,p in at])@M
    xy,dep=proj(P,az,el)
    cp=cube_pts()@M; cxy,_=proj(cp,az,el)
    for i,j in CELL_E: ax.plot(*zip(cxy[i],cxy[j]),color='#3A4248',lw=1.1,zorder=2.6,solid_capstyle='round')
    if bonds:
        D=np.linalg.norm(P[:,None,:]-P[None,:,:],axis=-1)
        un=[(i,j) for i in range(len(at)) for j in range(i+1,len(at)) if at[i][0]!=at[j][0]]
        if un:
            dmin=min(D[i,j] for i,j in un)
            for i,j in un:
                if D[i,j]<=dmin*bond_cut:
                    m=(xy[i]+xy[j])/2
                    ax.plot(*zip(xy[i],m),color=colors[at[i][0]],lw=4.2,zorder=2,solid_capstyle='round')
                    ax.plot(*zip(m,xy[j]),color=colors[at[j][0]],lw=4.2,zorder=2,solid_capstyle='round')
    order=np.argsort(dep)[::-1]
    for k in order:
        sp=at[k][0]; r=radii[sp]/a_pm*scale
        sphere(ax,xy[k],r,colors[sp],3+float(dep[k])*0.0+3)
    ax.set_aspect('equal'); ax.autoscale_view()
    xs,ys=xy[:,0],xy[:,1]; pad=0.42
    ax.set_xlim(min(xs.min(),cxy[:,0].min())-pad,max(xs.max(),cxy[:,0].max())+pad)
    ax.set_ylim(min(ys.min(),cxy[:,1].min())-pad,max(ys.max(),cxy[:,1].max())+pad)
def triad(ax,ox,oy,L=0.33,az=24,el=16,fs=8):
    V={'a':(np.array([1.,0,0]),'#D0342C'),'b':(np.array([0,1.,0]),'#2FA84F'),'c':(np.array([0,0,1.]),'#2F5FD0')}
    for lab,(v,c) in V.items():
        d,_=proj(v*L,az,el); d=d[0]
        ax.annotate('',xy=(ox+d[0],oy+d[1]),xytext=(ox,oy),arrowprops=dict(arrowstyle='-|>',color=c,lw=1.5,mutation_scale=9),zorder=6)
        ax.text(ox+d[0]*1.33,oy+d[1]*1.33,lab,color='#222222',fontsize=fs,ha='center',va='center',zorder=6)
    ax.add_patch(Circle((ox,oy),0.028,fc='#DDDDDD',ec='#555555',lw=0.6,zorder=6))
