import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

GREEN='24E06E'; DARK='05080C'; LIME='36F08C'; CYANC='58D3E8'; AMB='FFC857'
BODYC='D6DEE4'; INK='111820'; MUT='5A6670'; RED='C0392B'
MONO='Consolas'
# AN OVERHEAD BAR IS A BASE CHARACTER PLUS U+0304 COMBINING MACRON. THE Consolas BUILD IN USE
# CARRIES NO U+0304, SO THE SHAPER FALLS BACK AND GHOSTS THE BASE GLYPH (m3-m CAME OUT AS m33m).
# Liberation Mono CARRIES U+0304, POSITIONS IT CORRECTLY AND IS METRIC-COMPATIBLE WITH Courier New,
# SO ONLY THE TWO-CHARACTER BARRED CLUSTERS ARE SET IN IT; EVERYTHING ELSE STAYS IN Consolas.
# INSIDE THAT FONT U+0305 COMBINING OVERLINE IS WIDER AND BETTER CENTRED THAN U+0304, SO THE
# SOURCE KEEPS U+0304 (MATCHING THE SLIDES AND THE README) AND THE SWAP HAPPENS ON OUTPUT.
BAR='\u0304'
OVER='\u0305'
BARF='Liberation Mono'
_CLUSTER=re.compile('(.'+BAR+')')

def shade(el,fill):
    s=OxmlElement('w:shd'); s.set(qn('w:val'),'clear'); s.set(qn('w:color'),'auto')
    s.set(qn('w:fill'),fill); el.append(s)
def cell_borders(tc,color,sz=12):
    tcPr=tc.get_or_add_tcPr(); b=OxmlElement('w:tcBorders')
    for e in ('top','left','bottom','right'):
        x=OxmlElement('w:'+e); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),str(sz))
        x.set(qn('w:space'),'0'); x.set(qn('w:color'),color); b.append(x)
    tcPr.append(b)
def nospace(p,before=0,after=0,line=None):
    pf=p.paragraph_format; pf.space_before=Pt(before); pf.space_after=Pt(after)
    if line: pf.line_spacing=line
    return p
def _run1(p,txt,size,color,bold,font):
    r=p.add_run(txt); r.font.name=font; r.font.size=Pt(size); r.font.bold=bold
    r.font.color.rgb=RGBColor.from_string(color)
    r._element.rPr.rFonts.set(qn('w:eastAsia'),font)
    return r
def run(p,txt,size=8,color=INK,bold=False,font=MONO):
    r=None
    for part in _CLUSTER.split(str(txt)):
        if not part: continue
        if part.endswith(BAR): r=_run1(p,part.replace(BAR,OVER),size,color,bold,BARF)
        else:                  r=_run1(p,part,size,color,bold,font)
    return r

doc=Document()
st=doc.styles['Normal']; st.font.name=MONO; st.font.size=Pt(8)
st.element.rPr.rFonts.set(qn('w:eastAsia'),MONO)
s=doc.sections[0]
s.page_width=Cm(21.0); s.page_height=Cm(29.7)
for m in ('top_margin','bottom_margin'): setattr(s,m,Cm(0.9))
for m in ('left_margin','right_margin'): setattr(s,m,Cm(1.0))

def bar(left,right):
    t=doc.add_table(rows=1,cols=2); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    for i,(txt,al) in enumerate(((left,WD_ALIGN_PARAGRAPH.LEFT),(right,WD_ALIGN_PARAGRAPH.RIGHT))):
        c=t.rows[0].cells[i]; shade(c._tc.get_or_add_tcPr(),GREEN); cell_borders(c._tc,GREEN,6)
        c.width=Cm(9.5); p=c.paragraphs[0]; nospace(p); p.alignment=al
        run(p,txt,7,'04140A',True)
    return t
def item(label,text,color=INK,size=6.6,hang=2.6,bold=False):
    p=nospace(doc.add_paragraph(),0,1.0)
    pf=p.paragraph_format; pf.left_indent=Cm(hang); pf.first_line_indent=Cm(-hang)
    if label: run(p,label,size,CYANC if color==INK else color,True)
    run(p,'\t',size,color)
    pf.tab_stops.add_tab_stop(Cm(hang))
    run(p,text,size,color,bold); return p

QUESTIONS = False   # THE BRIEF IS QUOTED ON SLIDES 01a, 04a AND 09a INSTEAD
def qbox(cmd,title,lines):
    if not QUESTIONS: return
    ps=doc.paragraphs[-1] if doc.paragraphs else None
    t=doc.add_table(rows=1,cols=1); t.alignment=WD_TABLE_ALIGNMENT.CENTER
    trPr=t.rows[0]._tr.get_or_add_trPr(); cs=OxmlElement('w:cantSplit'); trPr.append(cs)
    c=t.rows[0].cells[0]; shade(c._tc.get_or_add_tcPr(),DARK); cell_borders(c._tc,GREEN,12)
    c.width=Cm(19.0)
    p=c.paragraphs[0]; nospace(p,1,1); run(p,cmd,8,AMB,True)
    p=nospace(c.add_paragraph(),1,1); run(p,title,8.5,LIME,True)
    for head,txt in lines:
        p=nospace(c.add_paragraph(),0.5,0.5)
        if head: run(p,head+'  ',7.5,CYANC,True)
        run(p,txt,7.5,BODYC)
    doc.add_paragraph().paragraph_format.space_after=Pt(2)
    return t

def head(txt,color=INK,size=8.0):
    p=nospace(doc.add_paragraph(),3,1); run(p,txt,size,color,True); return p
def line(txt,color=INK,size=7.0,bold=False,indent=0.0):
    p=nospace(doc.add_paragraph(),0,0.5)
    if indent: p.paragraph_format.left_indent=Cm(indent)
    run(p,txt,size,color,bold); return p
def table(rows,widths,size=6.4,hdr=True):
    t=doc.add_table(rows=len(rows),cols=len(rows[0])); t.alignment=WD_TABLE_ALIGNMENT.LEFT
    t.style='Table Grid'
    for ri,r in enumerate(rows):
        for ci,v in enumerate(r):
            cell=t.cell(ri,ci); cell.width=Cm(widths[ci])
            p=cell.paragraphs[0]; nospace(p)
            col=INK; bold=False
            if ri==0 and hdr: bold=True; shade(cell._tc.get_or_add_tcPr(),'E8F5EC')
            if isinstance(v,tuple): v,col=v
            run(p,str(v),size,col,bold)
    for row in t.rows:
        row.height=Cm(0.0)
    return t

# ===================== PAGE 1 =====================
bar('CML6032@IITD:~/ASSIGNMENT','VT100 | Bourne shell')
p=nospace(doc.add_paragraph(),3,0); run(p,'20261005 CML6032 ASSIGNMENT 1 : MATERIALS CHEMISTRY, STRUCTURAL ANALYSIS',11,INK,True)
p=nospace(doc.add_paragraph(),0,0); run(p,'NISHEAL MICHAEL KALEY  |  ENTRY NO 2025CYS7090  |  IIT DELHI  |  10 OCTOBER 2026',8,MUT)
p=nospace(doc.add_paragraph(),0,3)
run(p,'VIDEO ',7.5,CYANC,True); run(p,'https://0nmeesheall.github.io/CML6032-Assignment1/',7.5,RED,True)
run(p,'     REPO  https://github.com/0nmeesheall/CML6032-Assignment1',7.5,MUT)
p=nospace(doc.add_paragraph(),0,4)
run(p,'NOTATION  LENGTHS IN pm (1 ANGSTROM = 100 pm), RATIOS NOT PER-100, OXIDATION STATES AS TUPLES, MIRROR PLANES AS MP, '
      'SPACE GROUPS WITH OVERHEAD BARS. THE ISSUED BRIEF IS TRANSCRIBED INTO THIS NOTATION.',6.8,MUT)

qbox('$ cat partA_morphology.txt','[MODULE 1 : PART A (3 MARKS)]  CRYSTAL MORPHOLOGY AND POINT GROUP IDENTIFICATION',[
 ('OBJECTIVE','IDENTIFY AND RIGOROUSLY JUSTIFY THE POINT GROUPS OF THE MACROSCOPIC CRYSTAL SPECIMENS PROVIDED IN CLASS. ANALYSE'),
 ('','POLYHEDRAL FACE DEVELOPMENT (CRYSTAL HABIT), INVENTORY MACROSCOPIC SYMMETRY OPERATIONS, CONSTRUCT STEREOGRAPHIC'),
 ('','PROJECTIONS AND DETERMINE THE MOST PROBABLE CRYSTALLOGRAPHIC POINT GROUPS.'),
 ('SPECIMEN 1','ISOMETRIC HABIT, DOMINANT OCTAHEDRAL {111} FORMS SYMMETRICALLY TRUNCATED BY CUBE {100} FACETS.'),
 ('SPECIMEN 2','HEXAGONAL PRISM {101̄0} TERMINATED BY UPPER AND LOWER HEXAGONAL BIPYRAMIDAL {101̄1} FORMS.'),
 ('ELEMENTS','Cn ROTATION AXES, INVERSION CENTRE i, MIRROR PLANES (MP, HORIZONTAL, VERTICAL AND DIAGONAL), ROTOINVERSION AXES.'),
 ('PRINCIPLE','STENO 1669, THE LAW OF CONSTANT INTERFACIAL ANGLES: FACE AREAS VARY WITH GROWTH RATE, INTERFACIAL ANGLES DO NOT.'),
])
head('SOLUTION A')
table([
 ['SPECIMEN','HABIT AND FORMS','MACROSCOPIC OPERATION INVENTORY','MOST PROBABLE CLASS'],
 ['1','OCTAHEDRON {111} TRUNCATED BY CUBE {100}','48 OPERATIONS: 3 FOUR-FOLD ALONG <100>, 4 THREE-FOLD ALONG <111>, 6 TWO-FOLD ALONG <110>, 9 MP (3 AXIAL + 6 DIAGONAL), CENTRE i, S4 AND S6',('m3̄m (Oh, CLASS 32)',INK)],
 ['2','PRISM {101̄0} PLUS BIPYRAMID {101̄1}','24 OPERATIONS: 1 SIX-FOLD ALONG [0001] WITH COINCIDENT 3, 2, 6̄ AND S6, 6 BASAL TWO-FOLD (3 TO FACES + 3 TO EDGES), 7 MP (1 BASAL + 6 VERTICAL), CENTRE i',('6/mmm (D6h, CLASS 27)',INK)],
],[1.6,4.3,9.5,3.6])
item('EXCLUSIONS','SPECIMEN 1: 432 AND 4̄3m EXCLUDED BY THE MP PLUS CENTRE; m3̄ EXCLUDED BY THE 6 FACE-DIAGONAL TWO-FOLD AXES; 23 EXCLUDED BY BOTH.')
item('','SPECIMEN 2: 6mm EXCLUDED BY THE IDENTICAL CAPS DEMANDING A BASAL MP; 6/m EXCLUDED BY THE 6 BASAL DIADS; 6 AND 622 EXCLUDED BY MP PLUS CENTRE; 6̄m2 AND THE TRIGONAL MIMICS 3̄m, 32 AND 3m EXCLUDED BECAUSE ALL 6 CAP FACES ARE EQUAL.')
item('LIMIT','EXTERNAL FORM FIXES THE CLASS ONLY UP TO THE HOLOHEDRY OF THE LATTICE, SO THESE ARE THE MOST PROBABLE POINT GROUPS AND NOT A PROOF. PYROELECTRIC, PIEZOELECTRIC AND OPTICAL-ACTIVITY TESTS WERE NOT PERFORMED, SO CENTROSYMMETRY IS INFERRED FROM FORM EQUIVALENCE ALONE. THE SPECIMEN IDENTITIES AND THE MEASURED {100}/{111} INTERFACIAL ANGLE ISSUED IN CLASS ARE STILL TO BE ENTERED.',RED)
qbox('$ cat partB_segment1.txt','[MODULE 2 : PART B (SEGMENT 1)]  PEROVSKITE DISTORTIONS AND FERROELECTRIC HYSTERESIS',[
 ('OBJECTIVE','MODEL THE QUALITATIVE FERROELECTRIC SWITCHING MECHANISM IN BaTiO3 BY SYSTEMATIC Ti OFF-CENTERING IN A'),
 ('','SYMMETRY-REDUCED P1 UNIT CELL, CORRELATING MICROSCOPIC POLARISATION STATES TO THE MACROSCOPIC P-E HYSTERESIS LOOP.'),
 ('CELL','TETRAGONAL P1 (SPACE GROUP No 1, TRICLINIC SETTING WITH ALL CELL ANGLES 90 DEGREES).'),
 ('LATTICE','LP1 = LP2 = 399.04 pm, LP3 = 410.27 pm, RATIO LP3/LP1 = 1.0282.'),
 ('SHIFTS','Ti DISPLACEMENT ALONG THE POLAR c AXIS ACROSS FIVE STATES FROM z = 0.480 (-Ps) TO z = 0.520 (+Ps).'),
 ('REFERENCE','z = 0.500 IS THE NON-POLAR BARRIER CONFIGURATION, P4/mmm AT FIXED RATIO 1.0282.'),
 ('METRICS','+Ps / -Ps AT z = 0.520 / 0.480; +Pr / -Pr AT z = 0.510 / 0.490; +Ec / -Ec WHERE THE CELL REACHES z = 0.500.'),
])

# ===================== CONTINUED =====================
head('SOLUTION B SEGMENT 1',INK)
item('BASIS','Ba(+2, SPIN UNASSIGNED) 0,0,0  |  Ti(+4, SPIN UNASSIGNED) 1/2,1/2,z  |  O1(-2, SPIN UNASSIGNED) 1/2,1/2,0  |  O2(-2, SPIN UNASSIGNED) 1/2,0,1/2  |  O3(-2, SPIN UNASSIGNED) 0,1/2,1/2')
item('MODEL','u = (z - 1/2) x LP3 ;  P = (1/V) SUM q u = 4e u / V  WITH V = 6.5325e7 pm3. NINE STATES WERE BUILT AT STEP 0.005; THE FIVE STATES NAMED IN THE BRIEF ARE THE SUBSET z = 0.480, 0.490, 0.500, 0.510, 0.520.')
rows=[['z','0.480','0.485','0.490','0.495','0.500','0.505','0.510','0.515','0.520'],
      ['Ti OFFSET u / pm','-8.21','-6.15','-4.10','-2.05','0.00','+2.05','+4.10','+6.15','+8.21'],
      ['Ti-O1 UP / pm','213.3','211.3','209.2','207.2','205.1','203.1','201.0','199.0','196.9'],
      ['Ti-O1 DOWN / pm','196.9','199.0','201.0','203.1','205.1','207.2','209.2','211.3','213.3'],
      ['P / (C m-2)','-0.0805','-0.0604','-0.0402','-0.0201','0.0000','+0.0201','+0.0402','+0.0604','+0.0805'],
      ['STATE','-Ps','','-Pr','','Ec, P = 0','','+Pr','','+Ps']]
table(rows,[3.4]+[1.73]*9,size=6.6,hdr=False)
item('CHECKS','Ti-O1 UP PLUS Ti-O1 DOWN IS EXACTLY 410.27 pm = LP3 IN EVERY STATE; THE COLUMNS READ 410.2 OR 410.3 ONLY FROM ONE-DECIMAL ROUNDING. P(z) = -P(1 - z). THE EQUATORIAL Ti-O2 AND Ti-O3 CONTACTS MOVE ONLY FROM 199.52 pm TO 199.69 pm ACROSS THE WHOLE SCAN, SO THE DISTORTION IS ESSENTIALLY AXIAL. WORKED CASE z = 0.520: P = 4(1.602e-19)(8.21e-12) / 6.5325e-29 = +0.0805 C m-2.')
item('HYSTERESIS','THE LOOP IS DRAWN WITH TWO BRANCHES. THE DESCENDING BRANCH REACHES P = 0 AT E = -Ec AND THE ASCENDING BRANCH REACHES P = 0 AT E = +Ec, SO IT IS DOUBLE VALUED AND NEVER PASSES THROUGH THE ORIGIN; A SINGLE S CURVE THROUGH THE ORIGIN IS NOT A HYSTERESIS LOOP. PLOTTED FROM THE MEASURED Ps = 0.26 C m-2, Pr = 0.21 C m-2 AND Ec = 0.5 MV m-1 WITH A TANH SWITCHING MODEL; IT IS A SCHEMATIC, NOT DATA.')
item('CORRECTIONS','(1) THE Ti-ONLY RIGID-ION SUM REACHES ONLY 0.0805 C m-2 BECAUSE Ba AND O ARE HELD FIXED; THE TRUE SOFT MODE ALSO MOVES O AGAINST Ba, WHICH IS WHY THE MEASURED Ps IS 0.26 C m-2.',RED)
item('','(2) THE POLAR PHASE OF BaTiO3 IS P4mm (No 99) BELOW Tc = 393 K AND CUBIC Pm3̄m ABOVE IT; P4/mmm IS ONLY THE NON-POLAR REFERENCE AT FIXED RATIO 1.0282 AND IS NOT AN OBSERVED PHASE.',RED)
item('','(3) THE ISSUED RATIO 1.0282 EXCEEDS THE LITERATURE 300 K TETRAGONALITY OF ABOUT 1.011, SO THE ISSUED CELL IS AN EXAGGERATED TETRAGONAL AND THE TREND, NOT THE MAGNITUDE, IS THE RESULT.',RED)
item('','(4) REVERSAL IS NOT HOMOGENEOUS: 180-DEGREE DOMAIN WALLS NUCLEATE AND SWEEP, WHICH IS WHY REAL Ec IS 1e5 TO 1e6 V m-1 AND NOT THE ABOUT 1e8 V m-1 A RIGID LATTICE WOULD DEMAND.',RED)
qbox('$ cat partB_segment2.txt','[MODULE 2 : PART B (SEGMENT 2)]  NINE BINARY CUBIC CRYSTAL PROTOTYPES',[
 ('OBJECTIVE','CLASSIFY NINE BINARY CUBIC CRYSTALS ACROSS FIVE STRUCTURAL FAMILIES, GIVING SPACE GROUP, LATTICE PERIOD, CONTENTS,'),
 ('','COORDINATION AND THE INTERSTITIAL FILLING THAT DEFINES EACH PROTOTYPE.'),
 ('ROCK SALT (B1)','NaCl (LP = 564.0 pm) AND CaTe (LP = 635.6 pm)        [Fm3̄m, 6:6]'),
 ('CsCl TYPE (B2)','CsCl (LP = 412.0 pm) AND AuZn (LP = 319.0 pm)        [Pm3̄m, 8:8]'),
 ('FLUORITE (C1)','CaF2 (LP = 546.3 pm) AND CeO2 (LP = 541.1 pm)        [Fm3̄m, 8:4]'),
 ('ANTIFLUORITE','K2O (LP = 644.9 pm)                                  [Fm3̄m, 4:8]'),
 ('ZINC BLENDE (B3)','ZnS (LP = 540.6 pm) AND GaP (LP = 544.8 pm)          [F4̄3m, 4:4]'),
])
head('SOLUTION B SEGMENT 2')
mt=[['PHASE','PROTOTYPE','SG','LP / pm','PER CELL','NEAREST / pm','CN','RADII USED / pm','SUM','DIFF','RATIO','WINDOW','VERDICT'],
 ['NaCl','ROCK SALT','Fm3̄m','564.0','Na4 Cl4','282.0','6:6','102 + 181 IONIC','283','-1.0','0.5635','OCTA','AGREES'],
 ['CaTe','ROCK SALT','Fm3̄m','635.6','Ca4 Te4','317.8','6:6','100 + 221 IONIC','321','-3.2','0.4525','OCTA','AGREES'],
 ['CsCl','CsCl TYPE','Pm3̄m','412.0','Cs1 Cl1','356.8','8:8','174 + 181 IONIC','355','+1.8','0.9613','CUBIC','AGREES'],
 ['AuZn','CsCl B2','Pm3̄m','319.0','Au1 Zn1','276.3','8:8','144 + 134 METALLIC','278','-1.7','0.9306','NONE',('METALLIC',RED)],
 ['CaF2','FLUORITE','Fm3̄m','546.3','Ca4 F8','236.6','8:4','112 + 131 IONIC','243','-6.4','0.8550','CUBIC','AGREES'],
 ['CeO2','FLUORITE','Fm3̄m','541.1','Ce4 O8','234.3','8:4','97 + 138 IONIC','235','-0.7','0.7029','OCTA',('FAILS, EDGE',RED)],
 ['K2O','ANTIFLUOR','Fm3̄m','644.9','K8 O4','279.2','4:8','137 + 142 IONIC','279','+0.2','0.9648','CUBIC',('FAILS, STOICH',RED)],
 ['ZnS','ZINC BLENDE','F4̄3m','540.6','Zn4 S4','234.1','4:4','122 + 105 COVALENT','227','+7.1','0.3261','TETRA','AGREES'],
 ['GaP','ZINC BLENDE','F4̄3m','544.8','Ga4 P4','235.9','4:4','126 + 107 COVALENT','233','+2.9','0.8492','NONE',('COVALENT',RED)]]
table(mt,[1.15,2.05,1.15,1.05,1.25,1.35,0.75,2.65,0.95,0.95,1.05,1.15,1.55],size=6.3)
item('NEAREST','UNLIKE-PAIR SEPARATION IS LP/2 FOR ROCK SALT, LP x 3^0.5 / 2 FOR THE CsCl TYPE AND LP x 3^0.5 / 4 FOR FLUORITE, ANTIFLUORITE AND ZINC BLENDE.')
item('WINDOWS','TETRAHEDRAL 0.225 TO 0.414 (CN 4)  |  OCTAHEDRAL 0.414 TO 0.732 (CN 6)  |  CUBIC ABOVE 0.732 (CN 8). EACH WINDOW IS TWO SIDED; QUOTING ONLY ONE EDGE IS NOT A PREDICTION, AND THE RULE IS SILENT ON METALLIC AND COVALENT BONDING.')
item('READING','CaTe IS LARGER THAN NaCl ONLY BECAUSE Te(-2) AT 221 pm EXCEEDS Cl(-1) AT 181 pm; THE TWO CATIONS DIFFER BY 2 pm, SO THE ANION SETS THE CELL. THE CsCl TYPE IS PRIMITIVE CUBIC AND NOT BODY-CENTRED, BECAUSE THE CORNER AND CENTRE CARRY DIFFERENT SPECIES. FLUORITE AND ANTIFLUORITE DIFFER ONLY BY EXCHANGING THE CATION AND ANION SITES. ZINC BLENDE FILLS HALF THE TETRAHEDRAL HOLES, WHICH REMOVES THE INVERSION CENTRE AND MAKES ZnS AND GaP PIEZOELECTRIC, UNLIKE THE CENTROSYMMETRIC ROCK SALT PAIR. CeO2 AND K2O ARE THE TWO CASES WHERE THE RADIUS-RATIO RULE FAILS AGAINST THE OBSERVED COORDINATION.')
item('FILES','cif_prototypes/ 9 SINGLE-PHASE P1 CIFS  |  cif_batio3/ 9 STATES  |  renders/ 9 PNG  |  figures/ hysteresis_loop PNG AND PDF  |  slides/ 18-SLIDE PPTX, 15 NUMBERED ANSWERS PLUS 3 UNNUMBERED QUESTION SLIDES  |  README.md. EVERY CIF IS P1 WITH THE FULL BASIS ENUMERATED, SO THE FILE MAKES NO SYMMETRY CLAIM; THE PARENT SG COLUMN IS THE IDEALISED PROTOTYPE SYMMETRY.',MUT)
item('OUTSTANDING','THE TWO SPECIMEN IDENTITIES AS ISSUED IN CLASS AND THE MEASURED {100}/{111} INTERFACIAL ANGLE. THE WALKTHROUGH IS SERVED FROM THE REPOSITORY ITSELF AT THE VIDEO LINK ABOVE, NOT FROM YOUTUBE.',RED)
item('FIGURE','THE CORRECTED TWO-BRANCH HYSTERESIS LOOP IS SLIDE 08 OF THE DECK AND figures/hysteresis_loop_{dark,light}.{png,pdf} IN THE REPOSITORY.',MUT)
doc.save('/data/docx/Nisheal_2025CYS7090_Assignment1.docx')
print('saved')
