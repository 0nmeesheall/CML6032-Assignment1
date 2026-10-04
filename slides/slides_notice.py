# NOTICE SLIDE 02a, ADDED 4 OCTOBER 2026 AFTER EVALUATION. IT SITS JUST BEFORE THE FIRST
# CORRECTED SLIDE (03), CARRIES '[NOTICE]' INSTEAD OF A NUMBER, AND REPRODUCES THE
# INSTRUCTOR'S FEEDBACK AS RECEIVED: THE SCREENSHOT IS PASTED UNEDITED.
import sys,os; sys.path.insert(0,'/data/deck')
from vt import *
from PIL import Image
HERE=os.path.dirname(os.path.abspath(__file__))
OUT='/data/deck/slides/'
SHOT=os.path.join(HERE,'notice','feedback_whatsapp_20261004.png')
def build():
    fig,ax=new_slide('$ cat NOTICE_POST_EVALUATION.txt','[NOTICE]')
    T(ax,1800,H-95,'[ADDED 4 OCT 2026, AFTER EVALUATION]',RED,13,'bold',ha='right')
    T(ax,120,H-158,'NOTICE: PART A CORRECTED AFTER EVALUATION',GREEN,23,'bold')
    T(ax,1800,H-158,'[NOT FOR EXTRA MARKS]',AMBER,19,'bold',ha='right')
    # ---- LEFT: THE FEEDBACK AS RECEIVED, PIXEL FOR PIXEL AFTER ONE LANCZOS RESIZE
    panel(ax,120,130,1060,760)
    T(ax,650,862,'THE FEEDBACK AS RECEIVED: WHATSAPP, 4 OCT 2026, 3:11 TO 3:23 PM',CYAN,14,'bold','center')
    src=Image.open(SHOT).convert('RGB'); bw=1020; bh=int(round(bw*src.height/src.width))
    im=np.asarray(src.resize((bw,bh),Image.LANCZOS))
    x0=140; y0=178+(662-bh)//2
    a=fig.add_axes([x0/W,y0/H,bw/W,bh/H]); a.imshow(im,interpolation='none',aspect='auto'); a.axis('off')
    ax.add_patch(Rectangle((x0-3,y0-3),bw+6,bh+6,fc='none',ec=PEDGE,lw=1.4,zorder=3))
    T(ax,650,152,'SCREENSHOT PASTED UNEDITED  |  THE LAST MESSAGE (GREEN) IS MY REPLY',AMBER,12.5,'bold','center')
    # ---- RIGHT: WHAT CHANGED AND WHAT DID NOT
    panel(ax,1205,130,595,760)
    T(ax,1502,862,'WHAT CHANGED, AND WHAT DID NOT',CYAN,14,'bold','center')
    ITEMS=[('[1]',['EVALUATED AS COMMIT 1bebbc3 (2 OCT 2026):','PART A THERE, AND IN ITS VIDEO, SAYS m$\\bar{3}$m.'],BODY),
           ('[2]',['FEEDBACK: "IT\'S DONE WELL", BUT THE POINT','GROUP IS NOT CORRECT.'],BODY),
           ('[3]',['CLUE: NO 3 OR $\\bar{3}$ SYMMETRY IN THE CRYSTAL','AS A WHOLE; I HAD READ $\\bar{3}$ OFF THE CORNERS.'],BODY),
           ('[4]',['CORRECTED ON THE NEXT TWO SLIDES (03, 04)','AND IN ITEM [1] OF SLIDE 15: mmm (D2h).'],GREEN),
           ('[5]',["THE CORRECTION USES THE INSTRUCTOR'S CLUE,",'SO IT IS NOT INDEPENDENT WORK.'],BODY),
           ('[6]',['FOR THE RECORD ONLY: NO EXTRA MARKS ARE','ASKED FOR, TO BE FAIR TO THE CLASS.'],AMBER),
           ('[7]',['UNCHANGED: SLIDES 02, 05 TO 14, PART B AND','EVERY CIF FILE; 01 GAINED ONLY THE DATES.'],BODY)]
    y=812; fs=12
    for mk,lines,c in ITEMS:
        T(ax,1230,y,mk,AMBER,fs,'bold')
        for k,l in enumerate(lines): T(ax,1230+cw(fs,4),y-k*28,l,c,fs,'bold' if c!=BODY else 'normal')
        y-=28*len(lines)+22
    rule(ax,1230,y+6,545,c='#2B3942')
    T(ax,1230,y-22,'THE EVALUATED VERSION, KEPT AS IT WAS:',MUTE,11)
    T(ax,1230,y-46,'github.com/0nmeesheall/CML6032-Assignment1',CYAN,11)
    T(ax,1230,y-68,'    /tree/1bebbc3',CYAN,11)
    T(ax,120,92,'$ ./diff_since_evaluation.sh --slides',ORANGE,17)
    T(ax,120,56,'[NOTICE] CHANGED AFTER EVALUATION: 01 (DATES ONLY), 02a (THIS NOTICE), 03, 04 AND 15  |  '
               'UNCHANGED: 02, 05 TO 14, PART B AND THE CIF FILES',BODY,12.5)
    fig.savefig(OUT+'02a.png',facecolor=BG); plt.close(fig)
if __name__=='__main__': build()
