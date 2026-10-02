#!/usr/bin/env python3
"""
ANNOTATE THE VESTA BaTiO3 FRAMES SO THE Ti OFF-CENTRING IS ACTUALLY READABLE.

THE BARE RENDERS ARE VISUALLY IDENTICAL: ACROSS THE WHOLE SCAN THE Ti SPHERE MOVES
ABOUT 14 px WHILE BEING DRAWN ABOUT 96 px WIDE, SO LESS THAN 0.01 OF THE FRAME
CHANGES. THIS SCRIPT MEASURES THE Ti CENTRE IN EACH FRAME, DRAWS THE z = 0.500
REFERENCE AGAINST IT, ADDS A 3 TIMES MAGNIFIED DETAIL, AND PRINTS THE BOND NUMBERS.

RE-RUNNABLE: POINT IT AT FRESHLY RE-RENDERED FRAMES AFTER THE CIF CHARGE PATCH AND
IT WILL RE-MEASURE EVERYTHING FROM THE IMAGES.
"""
import numpy as np, cv2, pathlib
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG     = (255, 255, 255)
HEAD   = (11, 20, 16)
GREEN  = (82, 231, 150)
DIM    = (126, 164, 146)
INK    = (16, 20, 18)
PANEL  = (244, 246, 244)
EDGE   = (58, 68, 62)
REF    = (198, 28, 58)
ACT    = (22, 78, 198)
MONO   = "/usr/share/fonts/liberation-mono/LiberationMono-Regular.ttf"
MONOB  = "/usr/share/fonts/liberation-mono/LiberationMono-Bold.ttf"
def f(sz, bold=False): return ImageFont.truetype(MONOB if bold else MONO, sz)

# ---- PHYSICAL CONSTANTS AND THE SUPPLIED CELL -------------------------------
LP1, LP3 = 399.04, 410.27                 # pm
VOL      = LP1 * LP1 * LP3                # pm^3
QE       = 1.602176634e-19                # C
STATES   = [('0480', 0.480), ('0490', 0.490), ('0500', 0.500),
            ('0510', 0.510), ('0520', 0.520)]
LOOP = {'0480': '-Ps SATURATION', '0490': '-Pr REMANENCE',
        '0500': 'Ec COERCIVE POINT', '0510': '+Pr REMANENCE',
        '0520': '+Ps SATURATION'}

def physics(z):
    u    = (z - 0.5) * LP3                                   # pm, + IS TOWARD +c
    up   = LP3 / 2 - u                                       # pm, Ti TO O1 ABOVE
    dn   = LP3 / 2 + u                                       # pm, Ti TO O1 BELOW
    eq   = (( LP1 / 2) ** 2 + u ** 2) ** 0.5                 # pm, EQUATORIAL
    P    = 4 * QE * (u * 1e-12) / (VOL * 1e-36)              # C m^-2
    return u, up, dn, eq, P

def ti_centre(img):
    """CENTRE OF THE LARGEST INSCRIBED CIRCLE IN THE Ti-BLUE MASK."""
    a = np.array(img.convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = ((b - r) > 35) & (b > 95) & (r < 160) & (g < 170) & (b > g)
    m[:, :420] = False
    m = cv2.morphologyEx((m * 255).astype(np.uint8), cv2.MORPH_CLOSE,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    dt = cv2.distanceTransform(m, cv2.DIST_L2, 5)
    y, x = np.unravel_index(int(np.argmax(dt)), dt.shape)
    return int(x), int(y), float(dt[y, x])

def dashed(d, x0, x1, y, col, dash=13, gap=9, wd=3):
    x = x0
    while x < x1:
        d.line([(x, y), (min(x + dash, x1), y)], fill=col, width=wd)
        x += dash + gap

# ---- MEASURE EVERY FRAME FIRST SO z = 0.500 CAN SERVE AS THE REFERENCE ------
raw, cen = {}, {}
for tag, _ in STATES:
    raw[tag] = Image.open(f"raw_z{tag}.png").convert("RGB")
    cen[tag] = ti_centre(raw[tag])
REFX, REFY, TIR = cen['0500']
PXPM = abs(cen['0480'][1] - cen['0520'][1]) / (2 * abs(physics(0.520)[0]))   # px per pm

out = pathlib.Path("/data/repo/renders/batio3"); out.mkdir(parents=True, exist_ok=True)
print(f"  Ti DRAWN RADIUS {TIR:.1f} px | PROJECTED SCALE {PXPM:.3f} px per pm")
print(f"  z=0.500 REFERENCE AT (x={REFX}, y={REFY})\n")

for idx, (tag, z) in enumerate(STATES, 1):
    u, up, dn, eq, P = physics(z)
    src = raw[tag]
    cx, cy, _ = cen[tag]
    RX, RY = 0, 112                                     # WHERE THE RENDER SITS
    cv = Image.new("RGB", (W, H), BG)
    d  = ImageDraw.Draw(cv)

    # HEADER STRIP
    d.rectangle([0, 0, W, 96], fill=HEAD)
    d.text((44, 24), "BaTiO3  TETRAGONAL P4mm (99)  -  Ti OFF-CENTRING ALONG c",
           font=f(29, True), fill=GREEN)
    d.text((44, 62), "SUPPLIED CELL  LP1 = LP2 = 399.04 pm   LP3 = 410.27 pm   "
                     "RATIO LP3/LP1 = 1.0282", font=f(18), fill=DIM)
    t = "CML6032 ASSIGNMENT 1  |  NISHEAL MICHAEL KALEY  |  2025CYS7090"
    d.text((W - 44 - d.textlength(t, font=f(18)), 40), t, font=f(18), fill=DIM)

    cv.paste(src, (RX, RY))

    # REFERENCE AND ACTUAL Ti LINES, SPANS STAGGERED SO BOTH ENDS STAY VISIBLE
    dashed(d, RX + 516, RX + 900, RY + REFY, REF, 13, 9, 3)
    d.line([(RX + 604, RY + cy), (RX + 992, RY + cy)], fill=ACT, width=3)

    # STATE BADGE, TOP-LEFT WHITE MARGIN OF THE RENDER
    bx, by, bw, bh = 36, 150, 400, 176
    d.rectangle([bx, by, bx + bw, by + bh], fill=PANEL, outline=EDGE, width=2)
    d.text((bx + 18, by + 16), f"FRAME {idx} OF {len(STATES)}, STEP 0.010", font=f(19, True), fill=EDGE)
    d.text((bx + 18, by + 52), f"Ti FRACTIONAL z = {z:.3f}", font=f(26, True), fill=INK)
    d.text((bx + 18, by + 92), "LOOP POINT, AS LABELLED", font=f(16), fill=EDGE)
    d.text((bx + 18, by + 112), "IN THE ASSIGNMENT BRIEF:", font=f(16), fill=EDGE)
    d.text((bx + 18, by + 138), LOOP[tag], font=f(22, True), fill=ACT)

    # MAGNIFIED DETAIL, RIGHT WHITE MARGIN OF THE RENDER
    K, CW2, CH2 = 2.5, 208, 160
    sx, sy = REFX - CW2 // 2, REFY - CH2 // 2
    crop = src.crop((sx, sy, sx + CW2, sy + CH2)).resize((int(CW2*K), int(CH2*K)), Image.LANCZOS)
    ix, iy = 1300, 150
    cv.paste(crop, (ix, iy))
    IW, IH = int(CW2 * K), int(CH2 * K)
    d.rectangle([ix, iy, ix + IW, iy + IH], outline=EDGE, width=2)
    ryi, ayi = iy + int((REFY - sy) * K), iy + int((cy - sy) * K)
    dashed(d, ix + 4, ix + IW - 160, ryi, REF, 15, 10, 3)
    d.line([(ix + 54, ayi), (ix + IW - 160, ayi)], fill=ACT, width=3)
    if abs(ayi - ryi) > 4:                                   # OFFSET BRACKET
        ax = ix + IW - 138
        d.line([(ax, ryi), (ax, ayi)], fill=ACT, width=3)
        for yy in (ryi, ayi):
            d.line([(ax - 11, yy), (ax + 11, yy)], fill=ACT, width=3)
        lab, fnt = f"{abs(u):.1f} pm", f(18, True)
        lw, lx, lyy = d.textlength(lab, font=fnt), ax + 20, (ryi + ayi) // 2 - 13
        d.rectangle([lx - 6, lyy - 4, lx + lw + 6, lyy + 26], fill=(255, 255, 255), outline=ACT)
        d.text((lx, lyy), lab, font=fnt, fill=ACT)
    d.text((ix, iy - 30), f"DETAIL, {K:g} TIMES SCALE", font=f(19, True), fill=EDGE)
    ly = iy + IH + 10
    d.text((ix, ly), "DASHED  z = 0.500 Ti CENTRE, NON-POLAR REFERENCE", font=f(16), fill=REF)
    d.text((ix, ly + 24), "SOLID   Ti CENTRE IN THIS STATE", font=f(16), fill=ACT)
    d.text((ix, ly + 48), f"MEASURED SEPARATION {abs(cy - REFY)} px "
                          f"= {abs(cy - REFY) / PXPM:.1f} pm", font=f(16), fill=INK)

    # DATA PANEL ACROSS THE BOTTOM
    px, py, pw, ph = 192, 770, 1536, 236
    d.rectangle([px, py, px + pw, py + ph], fill=PANEL, outline=EDGE, width=2)
    rows = [
        ("Ti OFFSET FROM CELL CENTRE, U",     f"{u:+.2f} pm"),
        ("d(Ti-O1) TOWARD +c",                f"{up:.1f} pm"),
        ("d(Ti-O1) TOWARD -c",                f"{dn:.1f} pm"),
        ("SUM OF THE TWO APICAL BONDS",       f"{up + dn:.2f} pm  = LP3 EXACTLY"),
    ]
    rows2 = [
        ("d(Ti-O) EQUATORIAL, 4 BONDS",       f"{eq:.2f} pm"),
        ("CELL VOLUME",                       "6.5325e7 pm^3"),
        ("P FROM THE Ti POINT CHARGE ALONE",  f"{P:+.4f} C m^-2"),
        ("MEASURED Ps FOR COMPARISON",        "0.26 C m^-2"),
    ]
    for col, rs in ((0, rows), (1, rows2)):
        for i, (k, v) in enumerate(rs):
            yy = py + 20 + i * 38
            xx = px + 24 + col * 764
            d.text((xx, yy), k, font=f(19), fill=EDGE)
            d.text((xx + 430, yy), v, font=f(20, True), fill=INK)
    d.text((px + 24, py + 186),
           "MODEL CAVEAT: ONLY Ti IS DISPLACED. THE CELL AND THE OXYGEN SUBLATTICE ARE "
           "UNCHANGED, SO P IS A LOWER BOUND ON Ps.", font=f(17), fill=REF)
    d.text((ix, ly + 72), "RENDERED IN VESTA FROM", font=f(15), fill=EDGE)
    d.text((ix, ly + 92), f"cif_batio3/BaTiO3_P1_z{tag}.cif", font=f(15, True), fill=EDGE)
    d.text((px + 24, py + 208),
           "REMANENCE AND COERCIVITY ARE DOMAIN PROPERTIES AND ARE NOT PREDICTED BY A "
           "SINGLE-CELL RIGID-DISPLACEMENT MODEL.", font=f(17), fill=REF)

    p = out / f"BaTiO3_annotated_z{tag}.png"
    cv.save(p)
    print(f"  {p.name}  z={z:.3f}  U={u:+6.2f} pm  Ti-O1 {up:.1f}/{dn:.1f} pm  "
          f"P={P:+.4f}  Ti y={cy} (ref {REFY}, {cy-REFY:+d} px)")
