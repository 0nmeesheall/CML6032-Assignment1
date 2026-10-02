#!/usr/bin/env python3
"""ASSEMBLE png/*.png INTO A FULL-BLEED 16:9 DECK.

18 IMAGES: 15 NUMBERED ANSWER SLIDES PLUS THE 3 UNNUMBERED QUESTION SLIDES 01a,
04a AND 09a, WHICH SORT IMMEDIATELY BEFORE THE ANSWER THEY INTRODUCE."""
import glob, os
from pptx import Presentation
from pptx.util import Inches

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "CML6032_Assignment1_Nisheal_2025CYS7090.pptx")
imgs = sorted(glob.glob(os.path.join(HERE, "png", "*.png")))
assert len(imgs) == 18, f"EXPECTED 18 SLIDE IMAGES, FOUND {len(imgs)}"

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
blank = prs.slide_layouts[6]
for p in imgs:
    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(p, 0, 0, width=prs.slide_width, height=prs.slide_height)
prs.save(OUT)
print(f"WROTE {OUT}\n      {len(imgs)} SLIDES  |  {os.path.getsize(OUT)/1e6:.1f} MB  |  13.333 x 7.5 in")
