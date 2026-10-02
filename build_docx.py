"""
REGENERATES THE ONE-PAGE SUBMISSION SHEET, Nisheal_2025CYS7090_Assignment1.docx.

LAYOUT RULES, CHOSEN SO THE PAGE CAN BE COPIED STRAIGHT INTO AN MS TEAMS FIELD:
  - ONE PARAGRAPH PER LINE OF CONTENT, A BOLD LABEL FOLLOWED BY PLAIN TEXT
  - NO TABLES, NO TABS, NO WORD LIST NUMBERING, NO SHADING, BLACK TEXT
  - EVERY URL IS A LIVE HYPERLINK WHOSE VISIBLE TEXT IS THE URL ITSELF, SO IT
    SURVIVES EVEN A PLAIN-TEXT PASTE
  - ARIAL THROUGHOUT (METRIC-IDENTICAL IN WORD AND LIBREOFFICE, SO THE ONE-PAGE
    CHECK BELOW IS FAITHFUL). ARIAL HAS NO U+0304, SO A RENDERER GHOSTS THE BASE
    DIGIT OF A BARRED SYMBOL (m3̄m CAME OUT AS m33m). ONLY THE TWO-CHARACTER
    CLUSTERS 3̄ AND 4̄ ARE THEREFORE SET IN 'CML Bar Sans', A SMALL SUBSET OF
    Liberation Sans (ARIAL'S METRIC TWIN, SIL OFL 1.1, RENAMED AS THE LICENCE ASKS
    FOR A MODIFIED COPY) WHOSE U+0304 OUTLINE IS MOVED TO SIT CENTRED ABOVE A DIGIT.
    THE FONT CARRIES NO GPOS, SO WORD DRAWS THE BAR WHERE THE OUTLINE PUTS IT AND
    LIBREOFFICE CENTRES IT BY ITS OWN FALLBACK; BOTH LAND ABOVE THE DIGIT. IT IS
    EMBEDDED IN THE DOCX (ARIAL AS altName), SO NO INSTALL IS NEEDED
THE SCRIPT REFUSES TO FINISH UNLESS LIBREOFFICE RENDERS EXACTLY ONE PAGE.
"""
import io, os, re, shutil, subprocess, sys, tempfile, uuid, zipfile
from fontTools import subset as ftsubset
from fontTools.ttLib import TTFont
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.opc.constants import RELATIONSHIP_TYPE as RT

HERE  = os.path.dirname(os.path.abspath(__file__))
OUT   = os.path.join(HERE, 'Nisheal_2025CYS7090_Assignment1.docx')
FONT  = 'Arial'; BARF = 'CML Bar Sans'
LIBSANS = {'Regular': '/usr/share/fonts/liberation-sans/LiberationSans-Regular.ttf',
           'Bold':    '/usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf'}
BODY  = 9.5; HEAD = 10.5; TITLE = 12.5
BLACK = RGBColor(0, 0, 0); BLUE = RGBColor(0x05, 0x63, 0xC1); GREY = RGBColor(0x40, 0x40, 0x40)
REPO  = 'https://github.com/0nmeesheall/CML6032-Assignment1'
PAGES = 'https://0nmeesheall.github.io/CML6032-Assignment1/'
MP4   = REPO + '/raw/main/docs/CML6032_Assignment1_Nisheal_2025CYS7090.mp4'

doc = Document()
for p in list(doc.paragraphs): p._element.getparent().remove(p._element)
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
sec.left_margin = sec.right_margin = Cm(1.6)
sec.top_margin = sec.bottom_margin = Cm(1.4)
st = doc.styles['Normal']; st.font.name = FONT; st.font.size = Pt(BODY)
rpr = st.element.get_or_add_rPr(); rf = rpr.find(qn('w:rFonts'))
if rf is None: rf = OxmlElement('w:rFonts'); rpr.append(rf)
for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'): rf.set(qn(k), FONT)
pf = st.paragraph_format; pf.space_before = Pt(0); pf.space_after = Pt(1.5); pf.line_spacing = 1.0
doc.core_properties.author = 'NISHEAL MICHAEL KALEY'
doc.core_properties.title  = 'CML6032 ASSIGNMENT 1, 2025CYS7090'

BAR = re.compile(r'(\S\u0304)')             # BASE CHARACTER + COMBINING OVERHEAD BAR

def run(p, txt, bold=False, size=BODY, color=BLACK):
    for i, part in enumerate(BAR.split(txt)):
        if not part: continue
        r = p.add_run(part); r.bold = bold; r.font.size = Pt(size); r.font.color.rgb = color
        if i % 2:                            # BARRED CLUSTER
            r.font.name = BARF
            f = r._element.get_or_add_rPr().get_or_add_rFonts()
            for k in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'): f.set(qn(k), BARF)
    return p

def link(p, url, size=BODY):
    rid = p.part.relate_to(url, RT.HYPERLINK, is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
    r = OxmlElement('w:r'); rp = OxmlElement('w:rPr')
    c = OxmlElement('w:color'); c.set(qn('w:val'), '0563C1'); rp.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rp.append(u)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(int(size * 2))); rp.append(sz)
    r.append(rp); t = OxmlElement('w:t'); t.text = url; t.set(qn('xml:space'), 'preserve'); r.append(t)
    h.append(r); p._p.append(h)

def para(label='', text='', size=BODY, before=0.0, after=1.5, bold=False, color=BLACK):
    p = doc.add_paragraph(); f = p.paragraph_format
    f.space_before = Pt(before); f.space_after = Pt(after)
    if label: run(p, label + ' ', True, size, color)
    if text: run(p, text, bold, size, color)
    return p

def head(txt): return para(txt, size=HEAD, before=5, after=1.5)

# ------------------------------------------------------------------ HEADER
para('20261005 CML6032 ASSIGNMENT 1 : MATERIALS CHEMISTRY, STRUCTURAL ANALYSIS', size=TITLE, after=1)
para('', 'NISHEAL MICHAEL KALEY  |  ENTRY NO 2025CYS7090  |  IIT DELHI  |  10 OCTOBER 2026', size=BODY + 0.5, after=3)
p = para('VIDEO, 26:38 WITH CHAPTERS:'); link(p, PAGES)
para('SAME VIDEO AS ONE MP4 FILE, DOWNLOADS DIRECTLY EVEN IF THE PLAYER PAGE IS DOWN:', after=0)
p = para(); link(p, MP4, size=8.5)            # 8.5 pt KEEPS THE LONG URL ON ONE LINE
p = para('REPOSITORY:'); link(p, REPO)
run(p, '  (PPTX IN slides/, 18 CIF FILES IN cif_batio3/ AND cif_prototypes/, PART A PHOTOS IN part_a_photos/)')
para('NOTATION:', 'LENGTHS IN pm (1 ANGSTROM = 100 pm), RATIOS NOT PER-100, OXIDATION STATES AS TUPLES, MIRROR PLANES AS MP, '
     'OVERHEAD BARS ON ROTOINVERSION AXES AND SPACE GROUPS.', color=GREY)

# ------------------------------------------------------------------ PART A
head('PART A (3 MARKS): POINT GROUP OF THE CRYSTALS ISSUED IN CLASS')
para('CRYSTALS:', '11 COLOURLESS, VITREOUS, BLOCKY CRYSTALS IN 5 PHOTOS: C1 TO C10, PLUS ONE CRYSTAL PHOTOGRAPHED ALONE IN 3 VIEWS.')
para('MORPHOLOGY:', '6 FLAT FACES IN 3 MUTUALLY PERPENDICULAR PARALLEL PAIRS AND STRAIGHT EDGES; NO PYRAMID, DOME OR CORNER FACET ON ANY CRYSTAL.')
para('MEASURED:', 'EDGES FITTED ON THE PHOTOS BY LINE-SEGMENT DETECTION. 11 CLEAN CORNERS ARE 86.2 TO 89.9 DEGREES (MEAN 88.1, = 90 WITHIN '
     'EDGE NOISE); 6 CHIPPED ENDS (70.8 TO 84.1) NEVER FORM PARALLEL PAIRS; L/W RUNS 1.00 TO 2.03, SO THE SHAPE VARIES 2-FOLD WHILE '
     'THE ANGLE DOES NOT (STENO 1669).')
para('FORM:', 'ONE FORM, THE CUBE {100}, REPRODUCES EVERY FACE AND EVERY ANGLE SEEN.')
para('POINT GROUP:', 'm3̄m (Oh, CLASS 32), FULL SYMBOL 4/m 3̄ 2/m, 48 OPERATIONS: 3 FOUR-FOLD AXES FACE TO FACE, 4 THREE-FOLD CORNER TO '
     'CORNER, 6 TWO-FOLD EDGE TO EDGE, 9 MP AND A CENTRE i.')
para('WHY MOST PROBABLE:', 'TRICLINIC, MONOCLINIC, TRIGONAL AND HEXAGONAL CLASSES FAIL ON THE 90-DEGREE CORNERS. 23, m3̄, 432 AND 4̄3m '
     'WOULD SHOW STRIATIONS, ETCH PITS OR EXTRA FACETS; NONE ARE SEEN, SO THE HOLOHEDRY IS TAKEN. RUNNER-UP 4/mmm, THEN mmm: SAME '
     'ANGLES, BUT 2 OR 3 FORMS AND A FIXED UNIQUE AXIS, WHICH THE VARYING L/W DOES NOT SHOW.')
para('LIMIT:', 'FORM CANNOT RULE OUT A 90-DEGREE TETRAGONAL OR ORTHORHOMBIC BOX. DECISIVE CHECK, NOT YET RUN: CROSSED POLARISERS, '
     'WHERE A CUBIC CRYSTAL STAYS DARK ON ALL 3 FACE TYPES, 4/mmm ON ONE AND mmm ON NONE.')

# ------------------------------------------------------------------ PART B SEGMENT 1
head('PART B (7 MARKS), SEGMENT 1: BaTiO3 FERROELECTRIC DISTORTION SERIES FROM BaTiO3std_P1.cif')
para('CELL:', 'P1, LP1 = LP2 = 399.04 pm, LP3 = 410.27 pm, RATIO 1.028. BASIS Ba(+2, SPIN UNASSIGNED) 0,0,0 | Ti(+4, SPIN UNASSIGNED) '
     '1/2,1/2,z | O(-2, SPIN UNASSIGNED) 1/2,1/2,0; 1/2,0,1/2; 0,1/2,1/2.')
para('SERIES:', '9 CIFS WITH Ti AT z = 0.480 TO 0.520 IN STEPS OF 0.005 ALONG c. OFFSET u = (z - 1/2) x LP3; RIGID-ION '
     'P = 4e u / V WITH V = 6.533e7 pm3.')
para('LOOP STATES:', '-Ps AT z = 0.480 (u = -8.21 pm, P = -0.0805 C m-2) | -Pr AT 0.490 (-4.10 pm, -0.0402) | P = 0 AT -Ec AND '
     '+Ec, z = 0.500 | +Pr AT 0.510 (+4.10 pm, +0.0402) | +Ps AT 0.520 (+8.21 pm, +0.0805).')
para('CHECKS:', 'Ti-O1 UP + DOWN = 410.27 pm = LP3 IN EVERY STATE AND P(z) = -P(1 - z). THE LOOP HAS TWO BRANCHES AND NEVER '
     'PASSES THROUGH THE ORIGIN.')
para('PHYSICS:', 'THE Ti-ONLY SUM (0.0805 C m-2) IS BELOW THE MEASURED Ps OF 0.26 C m-2 BECAUSE O ALSO MOVES AGAINST Ba. THE POLAR '
     'PHASE IS P4mm, CUBIC Pm3̄m ABOVE Tc = 393 K. THE ISSUED RATIO 1.028 EXCEEDS THE LITERATURE 1.011. 180-DEGREE DOMAIN WALLS '
     'SET THE REAL Ec AT 1e5 TO 1e6 V m-1.')

# ------------------------------------------------------------------ PART B SEGMENT 2
head('PART B, SEGMENT 2: NINE BINARY CUBIC PROTOTYPES, CIFS EDITED FROM BaTiO3std_P1.cif FOR VESTA')
para('ROCK SALT, Fm3̄m, CN 6:6:', 'NaCl, LP 564.0 pm, Na-Cl 282.0 pm  |  CaTe, LP 635.6 pm, Ca-Te 317.8 pm.')
para('CsCl TYPE, Pm3̄m, CN 8:8:', 'CsCl, LP 412.0 pm, Cs-Cl 356.8 pm  |  AuZn, LP 319.0 pm, Au-Zn 276.3 pm. PRIMITIVE CUBIC, NOT BODY-CENTRED.')
para('FLUORITE, Fm3̄m, CN 8:4:', 'CaF2, LP 546.3 pm, Ca-F 236.6 pm  |  CeO2, LP 541.1 pm, Ce-O 234.3 pm.')
para('ANTIFLUORITE, Fm3̄m, CN 4:8:', 'K2O, LP 644.9 pm, K-O 279.2 pm.')
para('ZINC BLENDE, F4̄3m, CN 4:4:', 'ZnS, LP 540.6 pm, Zn-S 234.1 pm  |  GaP, LP 544.8 pm, Ga-P 235.9 pm. HALF THE TETRAHEDRAL HOLES '
     'ARE FILLED, SO THERE IS NO INVERSION CENTRE.')
para('RADIUS-RATIO RULE:', '5 AGREE (NaCl, CaTe, CsCl, CaF2, ZnS); 2 FAIL (CeO2, RATIO 0.7029 JUST BELOW THE 0.732 EDGE; K2O, BY '
     'STOICHIOMETRY); 2 OUTSIDE THE RULE (AuZn METALLIC, GaP COVALENT). ALL 9 NEAREST SEPARATIONS MATCH THE RADIUS SUMS WITHIN 10 pm.')

# ------------------------------------------------------------------ FILES
head('FILES')
para('SUBMITTED:', '18 CIFS, ALL P1 WITH THE FULL BASIS (cif_batio3/ 9 STATES, cif_prototypes/ 9 PHASES)  |  18-SLIDE PPTX  |  '
     'RENDERS, HYSTERESIS FIGURE AND PART A PHOTOS, ALL IN THE REPOSITORY ABOVE.')
para('VIDEO NOTE:', 'SELF-HOSTED ON GITHUB PAGES RATHER THAN YOUTUBE; THE DIRECT MP4 LINK ABOVE DOWNLOADS THE SAME FILE.', after=0)

doc.save(OUT)

# ------------------------------------------------------------------ EMBED THE BAR FONT
def _bar_font(src, style):
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.pens.boundsPen import BoundsPen
    o = ftsubset.Options(); o.layout_features = []; o.name_IDs = ['*']; o.name_languages = ['*']
    o.notdef_outline = True; o.hinting = False
    o.drop_tables += ['FFTM', 'GPOS', 'GSUB', 'GDEF', 'kern', 'hdmx', 'LTSH', 'VDMX']
    f = TTFont(src); s = ftsubset.Subsetter(o)
    s.populate(unicodes=list(range(0x20, 0x7F)) + [0xA0, 0x304]); s.subset(f)
    cm, gs, glyf = f.getBestCmap(), f.getGlyphSet(), f['glyf']
    bar, adv = cm[0x304], f['hmtx'][cm[ord('3')]][0]           # DIGITS ARE TABULAR, ONE ADVANCE FOR ALL
    top = max(glyf[cm[ord(c)]].yMax for c in '0123456789')
    bp = BoundsPen(gs); gs[bar].draw(bp); x0, y0, x1, y1 = bp.bounds
    sx = 1.45                                                   # A LITTLE WIDER, LIKE A PRINTED OVERBAR
    pen = TTGlyphPen(gs)
    gs[bar].draw(TransformPen(pen, (sx, 0, 0, 1, -sx * (x0 + x1) / 2 - adv / 2, top + 0.054 * f['head'].unitsPerEm - y0)))
    glyf[bar] = pen.glyph(); glyf[bar].recalcBounds(glyf); f['hmtx'][bar] = (0, glyf[bar].xMin)
    nm = f['name']; full = BARF + ('' if style == 'Regular' else ' ' + style); ps = BARF.replace(' ', '') + '-' + style
    for r in list(nm.names):
        if r.nameID in (18, 21, 22): nm.names.remove(r)
    for pid, eid, lid in ((3, 1, 0x409), (1, 0, 0)):
        for i, v in ((1, BARF), (2, style), (3, ps + ';2025CYS7090'), (4, full), (6, ps), (16, BARF), (17, style),
                     (10, 'SUBSET OF Liberation Sans 2 FOR CML6032, U+0304 MOVED ABOVE THE DIGITS. SIL OFL 1.1.')):
            if i in (16, 17) and nm.getName(i, pid, eid, lid) is None: continue
            nm.setName(v, i, pid, eid, lid)
    b = io.BytesIO(); f.save(b); return b.getvalue()

def _obfuscate(data, key):                   # ECMA-376 PART 1, 17.8.1: XOR THE FIRST 32 BYTES WITH THE REVERSED GUID
    h = key.strip('{}').replace('-', '')
    k = bytes(int(h[i:i + 2], 16) for i in range(30, -1, -2))
    b = bytearray(data)
    for i in range(32): b[i] ^= k[i % 16]
    return bytes(b)

def embed_bar_font(path):
    with zipfile.ZipFile(path) as z: items = {n: z.read(n) for n in z.namelist()}
    rels, tags = [], []
    for i, (style, tag) in enumerate((('Regular', 'embedRegular'), ('Bold', 'embedBold')), 1):
        key = '{' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'cml6032-2025cys7090-bar-' + style)).upper() + '}'
        items[f'word/fonts/font{i}.odttf'] = _obfuscate(_bar_font(LIBSANS[style], style), key)
        rels.append(f'<Relationship Id="rIdFont{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/'
                    f'relationships/font" Target="fonts/font{i}.odttf"/>')
        tags.append(f'<w:{tag} r:id="rIdFont{i}" w:fontKey="{key}"/>')
    items['word/_rels/fontTable.xml.rels'] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships '
        'xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + ''.join(rels) + '</Relationships>').encode()
    entry = (f'<w:font w:name="{BARF}"><w:altName w:val="{FONT}"/><w:panose1 w:val="020B0604020202020204"/>'
             '<w:charset w:val="00"/><w:family w:val="swiss"/><w:pitch w:val="variable"/>' + ''.join(tags) + '</w:font>')
    items['word/fontTable.xml'] = items['word/fontTable.xml'].decode().replace('</w:fonts>', entry + '</w:fonts>').encode()
    st, n = re.subn(r'(<w:zoom[^>]*/>)', r'\1<w:embedTrueTypeFonts/><w:saveSubsetFonts/>', items['word/settings.xml'].decode(), count=1)
    assert n == 1; items['word/settings.xml'] = st.encode()
    ct = items['[Content_Types].xml'].decode()
    ct = ct.replace('<Default Extension="rels"', '<Default Extension="odttf" ContentType="application/'
                    'vnd.openxmlformats-officedocument.obfuscatedFont"/><Default Extension="rels"', 1)
    items['[Content_Types].xml'] = ct.encode()
    order = ['[Content_Types].xml'] + [n for n in items if n != '[Content_Types].xml']
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in order: z.writestr(n, items[n])
embed_bar_font(OUT)

# ------------------------------------------------------------------ ONE-PAGE GATE
def pages(path):
    tmp = tempfile.mkdtemp()
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', tmp, path],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
    pdf = os.path.join(tmp, os.path.splitext(os.path.basename(path))[0] + '.pdf')
    info = subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout
    n = int(re.search(r'Pages:\s+(\d+)', info).group(1))
    return n, pdf
if shutil.which('soffice') and shutil.which('pdfinfo'):
    n, pdf = pages(OUT)
    print(f'saved {OUT} | LIBREOFFICE PAGES: {n}')
    if n != 1: sys.exit('FATAL: THE SHEET IS NOT EXACTLY ONE PAGE')
    shutil.copy(pdf, '/tmp/sheet_check.pdf')
else:
    print(f'saved {OUT} | ONE-PAGE CHECK SKIPPED, NO LIBREOFFICE')
