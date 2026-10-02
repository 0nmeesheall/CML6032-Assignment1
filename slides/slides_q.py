"""
QUESTION SLIDES. THE ISSUED BRIEF IS REPRODUCED VERBATIM AS A TWO-PAGE DOCUMENT
VIEW AND THE PART BEING ANSWERED NEXT IS RINGED IN A TERMGREEN BOX.

THESE SLIDES ARE DELIBERATELY OUTSIDE THE SLIDE COUNT: THE FOOTER CARRIES
'[QUESTION]' WHERE AN ANSWER SLIDE CARRIES 'n/15', SO THE FIFTEEN ANSWER SLIDES
KEEP THEIR ORIGINAL NUMBERING.

QUOTED TEXT KEEPS THE BRIEF'S OWN WORDING AND UNITS, INCLUDING THE ANGSTROM IN
ITS CELL-PARAMETER COLUMN. CONVERTING A QUOTATION WOULD MISREPRESENT IT; EVERY
ANSWER SLIDE WORKS IN pm.
"""
from vt import *
from matplotlib.patches import Rectangle

OUT   = '/data/deck/slides/'
INK   = '#17191A'; MUTED = '#6C7276'; DGREEN = '#10763A'
PAPER = '#FFFFFF'; PEDGE2 = '#C9CED1'; BOX = '#3BE04E'
LH    = 22.0                      # IMAGE-SPACE LINE PITCH USED BY THE BRIEF SCAN
def Y(y): return H - y            # IMAGE y (TOP-DOWN) -> AXES y (BOTTOM-UP)

# PAGE FRAMES, IMAGE COORDINATES
P1 = (231, 106, 679, 879)
P2 = (1010, 106, 680, 879)

# ---- THE BRIEF, VERBATIM. (y, text, style) ---------------------------------
# STYLES: t=TITLE  h=BOLD HEAD  b=BODY  m=MUTED BODY  c=MONO
PAGE1 = [
 (158,"ASSIGNMENT 1 (10 marks)",'t'),
 (193,"INSTRUCTIONS: You must submit your assignment as a single-page",'b'),
 (215,"Word or docx file named 'Name_EntryNo_Assignment1.docx'. Record an",'b'),
 (237,"explanation of all three parts of the assignment (Parts A, B) as a",'b'),
 (259,"single video and upload it and share a word file containing:",'b'),
 (281,"\u2022 Link to the recorded video (YouTube video is preferred).",'b'),
 (303,"\u2022 Upload the ppt slides used for the presentation.",'b'),
 (325,"\u2022 Upload the cif files generated for Part B of the assignment.",'b'),
 (390,"Part A (3 marks): Expected duration of video explanation: 5-8 minutes",'h'),
 (422,"Identify the point group of the crystals I gave you in the last class.",'b'),
 (466,"You need to make 2 or 3 ppt slides and explain the morphology of",'b'),
 (488,"the crystals with the help of drawings or photographs or microscopic",'b'),
 (510,"images and explain why you think it belongs to a certain point group.",'b'),
 (554,"Mention the point group and describe why you think it is the most",'b'),
 (576,"probable point group.",'b'),
 (637,"Part B (7 marks):",'h'),
 (661,"Expected duration of video explanation: 5-6 minutes",'m'),
 (685,"A model cif named 'BaTiO3std_P1.cif' is given in the Class materials folder.",'b'),
 (707,"This is a symmetry-reduced version of the crystal structure of BaTiO3, which",'b'),
 (729,"was discussed in the class. Now use this cif as a starting point and vary",'b'),
 (751,"the fractional coordinates of Ti atom to mimic the structural changes upon",'b'),
 (773,"applying an electric field along c-axis. Create a series of such distorted",'b'),
 (795,"crystal structures mimicking the polarization corresponding to a ferroelectric",'b'),
 (817,"hysteresis loop.",'b'),
]
TBL = ["+---+------------+----------------------+-------------------------+",
       "| # | Compound   | Cell parameter, a (\u00c5) | Crystal structural type |",
       "+---+------------+----------------------+-------------------------+",
       "| 1 | NaCl       | 5.640                |                         |",
       "| 2 | CsCl       | 4.120                |                         |",
       "| 3 | CaF2       | 5.463                |                         |",
       "| 4 | ZnS        | 5.406                |                         |",
       "| 5 | CaTe       | 6.356                | Rock salt               |",
       "| 6 | GaP        | 5.448                | Zinc blende             |",
       "| 7 | K2O        | 6.449                | Antifluorite            |",
       "| 8 | CeO2       | 5.4110               | fluorite                |",
       "| 9 | AuZn       | 3.19                 | CsCl structure          |",
       "+---+------------+----------------------+-------------------------+"]
PAGE2 = [
 (153,"Using this cif file as starting point, edit parameters in the cif file, and add",'b'),
 (175,"fractional coordinates of atoms to generate cifs for the following crystal structures:",'b'),
 (197,"Expected duration of video explanation: around 6-8 minutes",'b'),
 (241,"Construct the following crystal structures by editing the sample CIF",'b'),
 (263,"('BaTiO3std_P1.cif') and explain the structures using the 3D models using VESTA.",'b'),
 (285,"Search and obtain the unicell parameters of these structures.",'b'),
] + [(332 + i*20, t, 'c') for i, t in enumerate(TBL)] + [
 (623,"For the visualisation and video explanation of the structures:",'h'),
 (647,"Open the cif files thus generated using the software VESTA.",'b'),
 (669,"https://jp-minerals.org/vesta/en/download.html",'b'),
 (713,"Visualize the unit cells of the crystal structures you generated and make",'b'),
 (735,"diagrams of these crystal structures. Explain the structures and how you",'b'),
 (757,"prepared the cifs in your video presentation.",'b'),
 (779,"Tutorial: https://www.youtube.com/watch?v=7NSi7OOqu00",'b'),
]
STYLE = {'t':(14.5,'bold',INK,'sans-serif'), 'h':(11.0,'bold',INK,'sans-serif'),
         'b':(10.4,'normal',INK,'sans-serif'), 'm':(10.0,'normal',MUTED,'sans-serif'),
         'c':(9.6,'normal',INK,'monospace')}

def qslide(name, target, boxes, lit):
    """boxes: list of (x,y,w,h) IN IMAGE COORDS.  lit: y VALUES TO SET GREEN."""
    fig = plt.figure(figsize=(19.2,10.8), dpi=100); fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis('off')
    ax.add_patch(Rectangle((0,H-38),W,38,color=BAR,zorder=5))
    ax.add_patch(Rectangle((0,0),W,38,color=BAR,zorder=5))
    ax.text(26,H-19,'CML6032@IITD:~/ASSIGNMENT',color=BARTXT,fontsize=12,weight='bold',va='center',zorder=6)
    ax.text(W-26,H-19,'VT100 | Bourne shell',color=BARTXT,fontsize=12,weight='bold',va='center',ha='right',zorder=6)
    ax.text(26,19,'20261005_CML6032_ASSIGNMENT1.docx [PAGE VIEW]',color=BARTXT,fontsize=12,weight='bold',va='center',zorder=6)
    ax.text(W-26,19,f'TARGET: {target}  |  [QUESTION]',color=BARTXT,fontsize=12,weight='bold',va='center',ha='right',zorder=6)
    ax.text(44,H-66,'$ cat 20261005_CML6032_ASSIGNMENT1.docx --layout two-page',color=ORANGE,fontsize=16,va='center')
    for (px,py,pw,ph),content in ((P1,PAGE1),(P2,PAGE2)):
        ax.add_patch(Rectangle((px,Y(py+ph)),pw,ph,fc=PAPER,ec=PEDGE2,lw=1.4,zorder=1))
        for y,txt,st in content:
            fs,wt,col,fam = STYLE[st]
            if y in lit: col,wt = DGREEN,'bold'
            ax.text(px+44,Y(y),txt,color=col,fontsize=fs,weight=wt,family=fam,
                    va='center',zorder=3)
    for (bx,by,bw,bh) in boxes:
        ax.add_patch(Rectangle((bx,Y(by+bh)),bw,bh,fc='none',ec=BOX,lw=3.4,zorder=4))
    fig.savefig(OUT+name, facecolor=BG); plt.close(fig)
    print('  '+name)

def build():
    qslide('01a.png','PART A (3 MARKS)',          [(258,362,630,232)], {390})
    qslide('04a.png','PART B SEGMENT 1 (4 MARKS)',[(258,620,630,218)], {637,661})
    qslide('09a.png','PART B SEGMENT 2 (3 MARKS)',[(1036,132,632,672)], {623})

if __name__ == '__main__':
    build()
