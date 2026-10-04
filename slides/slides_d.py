import numpy as np, matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from vt import *
from slides_b import OUT
FCC=[(0.,0.,0.),(0.,.5,.5),(.5,0.,.5),(.5,.5,0.)]
OCT=[(.5,0.,0.),(0.,.5,0.),(0.,0.,.5),(.5,.5,.5)]
TET=[(.25,.25,.25),(.75,.75,.25),(.75,.25,.75),(.25,.75,.75)]
TET8=[(.25,.25,.25),(.75,.25,.25),(.25,.75,.25),(.25,.25,.75),
      (.75,.75,.25),(.75,.25,.75),(.25,.75,.75),(.75,.75,.75)]
def rocksalt(c,a): return [(c,*p) for p in FCC]+[(a,*p) for p in OCT]
def cscl(c,a): return [(c,0.,0.,0.),(a,.5,.5,.5)]
def fluorite(c,a): return [(c,*p) for p in FCC]+[(a,*p) for p in TET8]
def antifluor(c,a): return [(a,*p) for p in FCC]+[(c,*p) for p in TET8]
def blende(c,a): return [(c,*p) for p in FCC]+[(a,*p) for p in TET]
PH={
 'NaCl':(rocksalt('Na','Cl'),564.0,{'Na':102,'Cl':181},{'Na':'#A05AE8','Cl':'#2F9E2F'}),
 'CaTe':(rocksalt('Ca','Te'),635.6,{'Ca':100,'Te':221},{'Ca':'#3F9E22','Te':'#B06A2A'}),
 'CsCl':(cscl('Cs','Cl'),412.0,{'Cs':174,'Cl':181},{'Cs':'#6B2FA0','Cl':'#2F9E2F'}),
 'AuZn':(cscl('Au','Zn'),319.0,{'Au':144,'Zn':134},{'Au':'#C79A00','Zn':'#6E7B8B'}),
 'CaF2':(fluorite('Ca','F'),546.3,{'Ca':112,'F':131},{'Ca':'#3F9E22','F':'#C9A227'}),
 'CeO2':(fluorite('Ce','O'),541.1,{'Ce':97,'O':138},{'Ce':'#8D7BC0','O':'#D0342C'}),
 'K2O':(antifluor('K','O'),644.9,{'K':137,'O':142},{'K':'#7A52C9','O':'#D0342C'}),
 'ZnS':(blende('Zn','S'),540.6,{'Zn':122,'S':105},{'Zn':'#6E7B8B','S':'#D4A017'}),
 'GaP':(blende('Ga','P'),544.8,{'Ga':126,'P':107},{'Ga':'#2E6FD6','P':'#E07B39'}),
}
def struct(fig,rect,ph,scale=0.40,az=24,el=16):
    basis,a,radii,cols=PH[ph]
    axs=fig.add_axes(rect)
    draw_structure(axs,basis,a,radii,cols,az=az,el=el,scale=scale)
    x0,x1=axs.get_xlim(); y0,y1=axs.get_ylim()
    triad(axs,x0+0.26,y0+0.24,L=0.30,az=az,el=el,fs=9)
    axs.text(x1-0.04,y1-0.06,f'LP = {a:.1f} pm',color='#222222',fontsize=10.5,
             family='monospace',ha='right',va='top',zorder=8)
    return axs
PHSTATE={'NaCl':{'Na':'+1','Cl':'-1'},'CaTe':{'Ca':'+2','Te':'-2'},
         'CsCl':{'Cs':'+1','Cl':'-1'},'AuZn':{'Au':'0','Zn':'0'},
         'CaF2':{'Ca':'+2','F':'-1'},'CeO2':{'Ce':'+4','O':'-2'},
         'K2O':{'K':'+1','O':'-2'},'ZnS':{'Zn':'+2','S':'-2'},'GaP':{'Ga':'+3','P':'-3'}}
def legend_col(ax,xc,y0,ph,fs=11.5,dy=25,tuples=True):
    cols=PH[ph][3]; st=PHSTATE[ph]
    for i,(el_,c) in enumerate(cols.items()):
        lab=f'{el_}({st[el_]}, SPIN UNASSIGNED)' if tuples else el_
        x=xc-cw(fs,len(lab)+2)/2.0
        ax.add_patch(Circle((x,y0-i*dy+1),8,fc=c,ec='#20303A',lw=0.8,zorder=6))
        T(ax,x+17,y0-i*dy,lab,c,fs,'bold')
# ---------------- 10 : master table ----------------
MT=[('NaCl','ROCK SALT','Fm$\\bar{3}$m','564.0','Na4 Cl4','282.0','6:6'),
    ('CaTe','ROCK SALT','Fm$\\bar{3}$m','635.6','Ca4 Te4','317.8','6:6'),
    ('CsCl','CAESIUM CHLORIDE','Pm$\\bar{3}$m','412.0','Cs1 Cl1','356.8','8:8'),
    ('AuZn','CAESIUM CHLORIDE B2','Pm$\\bar{3}$m','319.0','Au1 Zn1','276.3','8:8'),
    ('CaF2','FLUORITE','Fm$\\bar{3}$m','546.3','Ca4 F8','236.6','8:4'),
    ('CeO2','FLUORITE','Fm$\\bar{3}$m','541.1','Ce4 O8','234.3','8:4'),
    ('K2O','ANTIFLUORITE','Fm$\\bar{3}$m','644.9','K8 O4','279.2','4:8'),
    ('ZnS','ZINC BLENDE','F$\\bar{4}$3m','540.6','Zn4 S4','234.1','4:4'),
    ('GaP','ZINC BLENDE','F$\\bar{4}$3m','544.8','Ga4 P4','235.9','4:4')]
def s10():
    fig,ax=new_slide('$ cd ../part_b2_prototypes && ./summary.sh',10,tildes=(300,300))
    T(ax,120,H-165,'PART B SEGMENT 2 (3 MARKS) : NINE BINARY CUBIC PROTOTYPES',GREEN,21,'bold')
    panel(ax,120,420,1150,420)
    x=155; fs=12.5
    T(ax,x,805,'MASTER TABLE',AMBER,14,'bold')
    row(ax,x,772,[(0,'PHASE',CYAN),(8,'PROTOTYPE',CYAN),(30,'PARENT SG',CYAN),(43,'LP / pm',CYAN),
                  (54,'ATOMS PER CELL',CYAN),(71,'NEAREST UNLIKE / pm',CYAN),(94,'CN',CYAN)],fs=fs,w='bold')
    rule(ax,x,756,1080)
    for i,r in enumerate(MT):
        y=730-i*34
        row(ax,x,y,[(0,r[0],GREEN),(8,r[1]),(30,r[2],VIOLET),(43,r[3]),(54,r[4]),(71,r[5]),(94,r[6],AMBER)],fs=fs)
    panel(ax,1310,420,490,420)
    T(ax,1340,805,'RADIUS-RATIO WINDOWS',AMBER,14,'bold')
    bullets(ax,1340,768,[
      ('TETRAHEDRAL','0.225 TO 0.414, CN 4'),
      ('OCTAHEDRAL','0.414 TO 0.732, CN 6'),
      ('CUBIC','ABOVE 0.732, CN 8'),
    ],dy=30,fs=12,marker='',headc=CYAN,pad=13)
    rule(ax,1340,660,430,c='#2B3942')
    bullets(ax,1340,630,[
      ('[TWO SIDED]','EACH WINDOW HAS A LOWER AND'),
      ('','AN UPPER BOUND; QUOTING ONLY'),
      ('','ONE EDGE IS NOT A PREDICTION'),
      ('[IONIC ONLY]','THE RULE ASSUMES HARD CHARGED'),
      ('','SPHERES, SO IT IS SILENT ON'),
      ('','COVALENT OR METALLIC BONDING'),
      ('[RATIO FORM]','QUOTED AS A PLAIN RATIO, FOR'),
      ('','EXAMPLE 0.5635, NOT PER 100'),
    ],dy=26,fs=11.5,marker='',headc=RED,pad=13)
    T(ax,120,360,'$ head -3 cif_prototypes/NaCl.cif',ORANGE,17)
    T(ax,120,322,"data_NaCl   _symmetry_space_group_name_H-M 'P 1'   _cell_length_a 5.6400",BODY,12.5)
    bullets(ax,120,278,[
      ('[P1]','EVERY FILE IS WRITTEN IN P1 WITH ALL ATOMS LISTED, SO THE CIF ITSELF MAKES NO SYMMETRY CLAIM;'),
      ('','THE PARENT SG COLUMN IS THE IDEALISED SYMMETRY OF THE PROTOTYPE, NOT A REFINED RESULT'),
      ('[SOURCE]','LATTICE PARAMETERS ARE THE ROOM-TEMPERATURE LITERATURE VALUES SUPPLIED WITH THE ASSIGNMENT'),
    ],dy=28,fs=12,marker='',headc=CYAN,pad=10)
    fig.savefig(OUT+'10.png',facecolor=BG); plt.close(fig)
# ---------------- 11 : rock salt ----------------
WD,HT,YB=0.2224,0.395,0.385
def family(page,cmd,title,phases,left,right,azel=None,verdict=None,scale=0.40):
    fig,ax=new_slide(cmd,page,tildes=(300,300))
    T(ax,120,H-165,title,GREEN,21,'bold')
    n=len(phases); gap=WD+0.022; x0=(1.0-(n*WD+(n-1)*0.022))/2.0
    for i,ph in enumerate(phases):
        az,el=(azel or {}).get(ph,(24,16))
        struct(fig,[x0+i*gap,YB,WD,HT],ph,scale=scale,az=az,el=el)
        xc=(x0+i*gap+WD/2)*W
        T(ax,xc,400,ph,GREEN,15,'bold',ha='center')
        legend_col(ax,xc,371,ph,fs=11)
    panel(ax,120,100,860,220)
    T(ax,150,292,left[0],AMBER,13,'bold')
    y=bullets(ax,150,259,left[1],dy=28,fs=12,marker='',headc=CYAN,pad=left[2])
    if verdict: T(ax,150,y+2,verdict,GREEN,12)
    panel(ax,1020,100,780,220)
    T(ax,1050,292,right[0],AMBER,13,'bold')
    bullets(ax,1050,259,right[1],dy=24,fs=11.5,marker='',headc=CYAN,pad=right[2])
    fig.savefig(OUT+f'{page:02d}.png',facecolor=BG); plt.close(fig)
def s11():
    family(11,'$ ./inspect.sh --family rock-salt','ROCK SALT TYPE : NaCl AND CaTe  (Fm$\\bar{3}$m, CN 6:6)',
      ('NaCl','CaTe'),
      ('GEOMETRY AND RADIUS CHECK',[
        ('NaCl','NEAREST UNLIKE = LP/2 = 282.0 pm   SUM 102 + 181 = 283 pm   DIFF -1.0 pm'),
        ('CaTe','NEAREST UNLIKE = LP/2 = 317.8 pm   SUM 100 + 221 = 321 pm   DIFF -3.2 pm'),
        ('RATIOS','Na+/Cl- = 0.5635 AND Ca2+/Te2- = 0.4525, BOTH INSIDE 0.414 TO 0.732'),
      ],8),
      ('READING THE PAIR',[
        ('[>]','TWO INTERPENETRATING fcc ARRAYS OFFSET BY LP/2 ALONG'),
        ('','ONE AXIS, FOUR FORMULA UNITS PER CELL, CN 6:6'),
        ('[>]','CaTe HAS THE LARGER LP ONLY BECAUSE Te2- AT 221 pm IS'),
        ('','FAR LARGER THAN Cl- AT 181 pm; THE TWO CATIONS DIFFER'),
        ('','BY ONLY 2 pm, SO THE ANION SETS THE CELL SIZE'),
        ('[>]','Fm$\\bar{3}$m IS CENTROSYMMETRIC, SO NEITHER PHASE CAN BE'),
        ('','PIEZOELECTRIC OR FERROELECTRIC'),
      ],4),
      verdict='SO THE OCTAHEDRAL WINDOW PREDICTS THE OBSERVED CN 6 FOR BOTH PHASES')

def s12():
    family(12,'$ ./inspect.sh --family cscl','CAESIUM CHLORIDE TYPE : CsCl AND AuZn  (Pm$\\bar{3}$m, CN 8:8)',
      ('CsCl','AuZn'),
      ('GEOMETRY AND RADIUS CHECK',[
        ('FORMULA','NEAREST UNLIKE = LP x 3^0.5 / 2'),
        ('CsCl','356.8 pm   SUM 174 + 181 = 355 pm   DIFF +1.8 pm   RATIO 0.9613'),
        ('AuZn','276.3 pm   SUM 144 + 134 = 278 pm   DIFF -1.7 pm   RATIO 0.9306'),
      ],9),
      ('READING THE PAIR',[
        ('[>]','SIMPLE CUBIC ARRAY OF ONE SPECIES WITH THE OTHER AT'),
        ('','THE BODY CENTRE; ONE FORMULA UNIT PER CELL'),
        ('[>]','THIS IS NOT BODY-CENTRED CUBIC: THE CENTRE CARRIES A'),
        ('','DIFFERENT ATOM, SO THE LATTICE STAYS PRIMITIVE CUBIC'),
        ('[METALLIC]','AuZn IS A B2 INTERMETALLIC. THE 144 pm AND 134 pm'),
        ('','RADII ARE METALLIC, THE SUM MATCHES WELL, BUT THE'),
        ('','RADIUS-RATIO RULE ITSELF DOES NOT APPLY TO A METAL'),
      ],11),
      verdict='SO THE CUBIC WINDOW IS SATISFIED BY CsCl, WHILE AuZn MATCHES ONLY ON SIZE')
def s13():
    family(13,'$ ./inspect.sh --family fluorite','FLUORITE AND ANTIFLUORITE : CaF2, CeO2 AND K2O  (Fm$\\bar{3}$m)',
      ('CaF2','CeO2','K2O'),
      ('GEOMETRY AND RADIUS CHECK',[
        ('FORMULA','NEAREST UNLIKE = LP x 3^0.5 / 4'),
        ('CaF2','236.6 pm   SUM 112 + 131 = 243 pm   DIFF -6.4 pm   CN 8:4'),
        ('CeO2','234.3 pm   SUM  97 + 138 = 235 pm   DIFF -0.7 pm   CN 8:4'),
        ('K2O','279.2 pm   SUM 137 + 142 = 279 pm   DIFF +0.2 pm   CN 4:8'),
      ],9),
      ('WHERE THE RULE BREAKS',[
        ('[CaF2]','RATIO 0.8550 IS IN THE CUBIC WINDOW AND CN 8 FOLLOWS'),
        ('[CeO2]','RATIO 0.7029 SITS JUST BELOW THE 0.732 EDGE, SO THE'),
        ('','WINDOW WOULD PREDICT CN 6 YET CN 8 IS OBSERVED'),
        ('[K2O]','RATIO 0.9648 WOULD PREDICT CN 8 FOR K+, BUT THE 2:1'),
        ('','STOICHIOMETRY FORCES K+ INTO CN 4 AND O2- INTO CN 8'),
        ('[LESSON]','STOICHIOMETRY AND THE ANION ARRAY OVERRIDE THE RATIO'),
        ('','WHENEVER THE TWO DISAGREE'),
      ],9),
      verdict='SO THE CATION AND ANION ROLES SIMPLY EXCHANGE BETWEEN FLUORITE AND ANTIFLUORITE')
def s14():
    family(14,'$ ./inspect.sh --family zinc-blende','ZINC BLENDE TYPE : ZnS AND GaP  (F$\\bar{4}$3m, CN 4:4)',
      ('ZnS','GaP'),
      ('GEOMETRY AND RADIUS CHECK',[
        ('FORMULA','NEAREST UNLIKE = LP x 3^0.5 / 4; COVALENT RADII USED THROUGHOUT'),
        ('ZnS','234.1 pm   SUM 122 + 105 = 227 pm   DIFF +7.1 pm   RATIO 0.3261'),
        ('GaP','235.9 pm   SUM 126 + 107 = 233 pm   DIFF +2.9 pm'),
      ],9),
      ('READING THE PAIR',[
        ('[>]','fcc ARRAY OF ONE SPECIES WITH THE OTHER IN HALF THE'),
        ('','TETRAHEDRAL HOLES, FOUR FORMULA UNITS PER CELL'),
        ('[COVALENT]','GaP IS A III-V SEMICONDUCTOR AND ZnS IS STRONGLY'),
        ('','COVALENT, SO COVALENT RADII ARE THE CORRECT CHECK'),
        ('','AND THE IONIC RATIO RULE CARRIES NO WEIGHT FOR GaP'),
        ('[POLAR]','F$\\bar{4}$3m HAS NO INVERSION CENTRE, SO BOTH PHASES ARE'),
        ('','PIEZOELECTRIC, UNLIKE THE ROCK SALT PAIR'),
      ],11),
      verdict='SO THE TETRAHEDRAL HOLE FILLING, NOT THE IONIC RATIO, IS THE REAL CONSTRAINT')

VER=[('NaCl','0.5635','OCTAHEDRAL','6','6','AGREES','G'),
     ('CaTe','0.4525','OCTAHEDRAL','6','6','AGREES','G'),
     ('CsCl','0.9613','CUBIC','8','8','AGREES','G'),
     ('AuZn','0.9306','NOT VALID','-','8','METALLIC BONDING','A'),
     ('CaF2','0.8550','CUBIC','8','8','AGREES','G'),
     ('CeO2','0.7029','OCTAHEDRAL','6','8','FAILS, NEAR 0.732 EDGE','R'),
     ('K2O','0.9648','CUBIC','8','4','FAILS, STOICHIOMETRY','R'),
     ('ZnS','0.3261','TETRAHEDRAL','4','4','AGREES','G'),
     ('GaP','0.8492','NOT VALID','-','4','COVALENT BONDING','A')]
def s15():
    fig,ax=new_slide('$ ./verify_all.sh && ./manifest.sh',15,tildes=(300,300))
    T(ax,120,H-165,'VERIFICATION, MANIFEST AND WHAT IS STILL MISSING',GREEN,21,'bold')
    CM={'G':GREEN,'A':AMBER,'R':RED}
    panel(ax,120,300,1040,540); x=155; fs=12.5
    T(ax,x,805,'RADIUS-RATIO RULE AGAINST OBSERVED COORDINATION',AMBER,14,'bold')
    row(ax,x,770,[(0,'PHASE',CYAN),(9,'RATIO',CYAN),(18,'WINDOW',CYAN),(32,'PRED CN',CYAN),
                  (42,'OBS CN',CYAN),(51,'VERDICT',CYAN)],fs=fs,w='bold')
    rule(ax,x,753,980)
    for i,(ph,r,w_,pc,oc,vd,cl) in enumerate(VER):
        y=727-i*42; c=CM[cl]
        row(ax,x,y,[(0,ph,GREEN),(9,r),(18,w_),(32,pc),(42,oc),(51,vd,c)],fs=fs)
    rule(ax,x,372,980,c='#2B3942')
    T(ax,x,348,'5 AGREE  |  2 FAIL  |  2 OUTSIDE THE SCOPE OF THE RULE',CYAN,12.5,'bold')
    T(ax,x,322,'[NOTE] IONIC RADII USED FOR THE SIX IONIC PHASES AND ZnS; AuZn METALLIC, GaP COVALENT, SO NO WINDOW APPLIES',MUTE,11)
    panel(ax,1200,540,600,300)
    T(ax,1230,805,'DELIVERABLE MANIFEST',AMBER,14,'bold')
    bullets(ax,1230,770,[
      ('cif_prototypes/','9 FILES, P1, ONE PHASE EACH'),
      ('cif_batio3/','9 FILES, z = 0.480 TO 0.520'),
      ('renders/','9 PNG + 5 BaTiO3 FRAMES'),
      ('figures/','hysteresis_loop.png AND .pdf'),
      ('slides/','15 ANSWER, 3 QUESTION, 1 NOTICE PNG'),
      ('docx','ONE PAGE, AS THE BRIEF ASKS'),
      ('docs/ video/','PAGES PLAYER, MP4, BUILDER'),
      ('README.md','METHOD, SOURCES AND CHECKS'),
      ('part_a_photos/','5 PHOTOS, EDGE FIT, OVERLAYS'),
    ],dy=25,fs=11.5,marker='',headc=CYAN,pad=17)
    panel(ax,1200,300,600,222)
    T(ax,1230,487,'STILL OUTSTANDING',AMBER,14,'bold')
    bullets(ax,1230,452,[
      ('[1]','PART A CORRECTED AFTER EVALUATION:'),
      ('','m$\\bar{3}$m TO mmm, NO 3 OR $\\bar{3}$ AXIS;'),
      ('','POLARISER CHECK STILL NOT RUN'),
      ('[2]','VIDEO IS SELF-HOSTED AT'),
      ('','docs/index.html, NOT YOUTUBE'),
    ],dy=26,fs=11.5,marker='',headc=RED,pad=5)
    T(ax,120,270,'$ ./verify_all.sh --summary',ORANGE,17)
    T(ax,120,232,'[PASS] 18 CIF PARSE OK  |  9 RADIUS SUMS WITHIN 10 pm  |  9 CN VALUES MATCH THE PROTOTYPE  |  BaTiO3 SUM RULE OK',GREEN,12.5)
    T(ax,120,196,'[OPEN] THE POLARISER CHECK NEEDS THE CRYSTALS; EVERY NUMBER ON THESE SLIDES IS REPRODUCIBLE FROM THE CIF SET AND part_a_photos/',MUTE,12.5)
    # STATUTORY NOTE ON THE RUNNING TIME, ADDED 2026-10-05 AT THE AUTHOR'S REQUEST. ONE SENTENCE,
    # WRAPPED AT THE CLAUSE SO IT KEEPS THE 12.5 pt OF THE [PASS] AND [OPEN] LINES ABOVE IT.
    T(ax,120,150,'$ cat STATUTORY_NOTE.txt',ORANGE,17)
    T(ax,120,112,"BY RPwD 2016 I'M ENTITLED TO A COMPENSATORY TIME OF 1.34 MINUTES PER MINUTE,",AMBER,12.5)
    T(ax,120,76,"HENCE THE EXCESS TIME CONSIDERS MY PROPENSITY TOWARDS DETAIL WHEN I'M VERY INTERESTED IN A PROJECT; AS WAS THIS.",AMBER,12.5)
    fig.savefig(OUT+'15.png',facecolor=BG); plt.close(fig)
