# CORRECTED NARRATION: NOTICE 02a, SLIDES 03 AND 04, AND SLIDE 15

STATUS: WRITTEN 2026-10-04, AFTER EVALUATION; RECORDED BY THE AUTHOR AND BUILT INTO THE
28:31 VIDEO ON 2026-10-05 (SEE `CHANGELOG.md` SECTION 10.2).

PART A WAS CORRECTED FROM m3̄m TO mmm AFTER THE INSTRUCTOR'S FEEDBACK (SEE THE NOTICE SLIDE
`slides/png/02a.png` AND THE README). THIS IS THE SCRIPT FOR THE SLIDES THAT CHANGED. THE
EVALUATED SCRIPT, `PART_A_NARRATION.md`, IS KEPT UNCHANGED AS THE RECORD OF WHAT WAS SAID.

| SLIDE | TAKE | WORDS | AT YOUR PACE (115 wpm) | AS BUILT |
|---|---|---|---|---|
| 02a NOTICE | NONE: HELD SILENT FOR 15 s (`CML_NOTICE_HOLD`) | - | 0:15 | 0:15 |
| 03 | NEW TAKE FROM THE TEXT BELOW | 308 | ABOUT 2:41 | 2:49 |
| 04 | NEW TAKE FROM THE TEXT BELOW | 325 | ABOUT 2:50 | 2:54 |
| 15 | NEW TAKE; THE EVALUATED TAKE WAS ONLY 4.4 s | 174 | ABOUT 1:31 | 1:58 |

AS BUILT = THE CONDITIONED TAKE, SILENCE TRIMMED AND 0.85 s OF LEAD-IN AND LEAD-OUT ADDED, FROM
`timeline.csv`. EACH NEW TAKE OPENS BY READING ITS HEADING ALOUD (FOR EXAMPLE "SLIDE 3, MORPHOLOGY, ONE
ANGLE, MANY SHAPES, CORRECTED") AND THE SLIDE 15 TAKE CLOSES "THAT'S IT. THANK YOU FOR WATCHING.";
OTHERWISE THE TAKES FOLLOW THE TEXT BELOW. THE STATUTORY NOTE ON SLIDE 15 IS ON SCREEN ONLY.

115 wpm IS YOUR MEASURED PACE ON THE EVALUATED TAKES (947 WORDS IN 8:14). WITH THE UNCHANGED
SLIDE 02 TAKE (2:18), THE PART A BLOCK COMES TO ABOUT 8:05 INCLUDING THE NOTICE, AGAINST
THE BRIEF'S 5 TO 8 MINUTES, SO READ A LITTLE BRISKLY. SLIDES 01, 02 AND 05 TO 14 KEEP THEIR TAKES. AS BUILT, SLIDES
02 TO 04 COME TO 8:01, AND 8:16 WITH THE NOTICE.

HOW IT WAS REBUILT ON 2026-10-05, AND HOW TO REPEAT IT: SAVE THE NEW TAKES AS `Slide 3.wav`, `Slide 4.wav` AND `Slide 15.wav` IN
`voicenotes/` (REPLACING THE OLD ONES), POINT THE BUILDER AT THE 19 SLIDE RASTERS
(`CML_SLIDES=../slides/png`) AND RUN `python3 BUILD_VIDEO.py --check`, THEN
`python3 BUILD_VIDEO.py`. IF THE `build/` CACHE FROM THE LAST RUN IS STILL THERE, ONLY THE
THREE NEW TAKES AND THE NOTICE HOLD ARE BUILT. THE NEW MP4 REPLACES THE ONE IN `docs/`; THE EVALUATED RECORDING STAYS
AVAILABLE AT COMMIT `1bebbc3`.

SPOKEN FORMS: "m m m" FOR mmm, "m three-bar m" FOR m3̄m, "four over m m m" FOR 4/mmm,
"D two h" FOR D2h, "two over m" FOR 2/m. SLIDE 02 STILL ENDS WITH "ON THE NEXT SLIDE, I
REPLACE THE WORD SQUARE WITH A MEASUREMENT"; THE SLIDE 03 TAKE PICKS THAT UP AFTER THE NOTICE.

---

## SLIDE 02a: NOTICE, PART A CORRECTED AFTER EVALUATION (NEW, NOT NARRATED)

ON SCREEN: THE WHATSAPP FEEDBACK OF 4 OCTOBER 2026 AS RECEIVED, AND WHAT CHANGED. IT IS HELD
IN SILENCE LIKE THE QUESTION SLIDES, SO THERE IS NOTHING TO RECORD; THE FIRST SENTENCE OF THE
SLIDE 03 TAKE REFERS BACK TO IT.

---

## SLIDE 03: MORPHOLOGY, ONE ANGLE, MANY SHAPES (CORRECTED)

As the notice says, after evaluation my instructor pointed out that these crystals
have no three-fold or three-bar axis, so this slide and the next are corrected,
for the record only.

To measure "square", a line-segment detector found the straight edges, and every
edge I kept is drawn on these overlays: cyan for side edges, green for a clean
end, red for a chipped one.

The top plot is the result. Eleven clean corners lie between eighty-six point two
and eighty-nine point nine degrees, with a mean of eighty-eight point one. Edge
noise always folds back below ninety, so these are right angles. The six chipped
ends never come in parallel pairs, so they are damage, not faces.

The bottom plot is the length over width, from one point zero zero to two point
zero three in one batch. The shape varies two-fold while the angle does not, which
is Steno's law. And a crystal twice as long as it is wide is not a cube.

On the right is the corrected habit: three pinacoids, one-zero-zero, zero-one-zero
and zero-zero-one, a box with three unequal edges but the same right angles as a
cube. The pink diamonds are its three two-fold axes, face centre to face centre.

The green line is my mistake. A square corner looks three-fold up close, but an
axis of the crystal must pass through its centre, the white dot, and this line
misses it. Below, the whole box is given a third of a turn about a body diagonal:
length, width and thickness trade places, and the red outline misses the box. That
works only if all three edges are equal and all six faces are alike. These
crystals are up to twice as long as they are wide, with frosted and smooth faces,
so the crystal as a whole has no three-fold axis.

---

## SLIDE 04: POINT GROUP, OPERATIONS, EXCLUSIONS AND VERDICT (CORRECTED)

Now the corrected point group, m m m. In the stereogram, the amber circles are the
six observed face poles, three pinacoids. Each carries a lens, the symbol of a
two-fold axis, and none is four-fold. The crossed-out triangles mark where my
earlier m three-bar m answer put its three-fold axes. The circle and the two
diameters are the three mirror planes.

On the crystal that makes eight operations: the identity, three two-fold axes from
face centre to face centre, three mirror planes each parallel to a face pair, and
a centre of symmetry, since every face has a parallel partner.

The exclusion chain tests each candidate against the photos. Triclinic needs an
oblique corner, and every clean corner is square. Monoclinic needs a tilted pair
of parallel ends, and the tilted ends are chipped and never parallel. Hexagonal
and trigonal need sixty or one-hundred-and-twenty-degree corners, and there are
none. Cubic is the row that changed: its three-fold axes need length, width and
thickness to be equal, so a length over width of two and faces of two kinds
exclude it. Tetragonal needs four alike side faces, but the lone crystal is
frosted in view A, smooth in view B, and two to one along its length. m m m needs
three unlike pairs of faces at ninety degrees, which is what all eleven crystals
are. Two-two-two and m m two would show half-faces or a polar end, and none are
seen, so I take the holohedry.

The verdict: m m m, Schoenflies D two h, orthorhombic, class eight, full symbol
two over m, two over m, two over m.

Two limits remain. A square cross-section on every crystal would make it
four over m m m, so calipers on all three edges decide. And between crossed
polarisers, an m m m crystal goes dark every ninety degrees on all three face
types, but never stays dark through a full turn. That completes Part A.

---

## SLIDE 15: VERIFICATION, MANIFEST AND WHAT IS STILL MISSING (ITEM [1] CHANGED)

This last slide is the verification and the manifest. On the left, the radius-
ratio rule is tested against the coordination I built. Five phases agree: sodium
chloride, calcium telluride, caesium chloride, calcium fluoride and zinc sulfide.
Two fail, usefully. Ceria, at zero point seven zero three, sits just below the
zero point seven three two edge, yet it is eight-coordinate. Potassium oxide fails
by stoichiometry: in the antifluorite the potassium ion is four-coordinate,
whatever its ratio says. Gold-zinc is metallic and gallium phosphide covalent, so
no ionic window applies to them.

All eighteen CIF files parse, all nine nearest separations match the radius sums
within ten picometres, every coordination number matches its prototype, and the
barium titanate sum rule holds.

On the right is the manifest, and what is still outstanding. First, the Part A
correction made after evaluation, from m three-bar m to m m m, with the polariser
check still to be run. Second, the video is self-hosted on the repository's player
page rather than on YouTube. Thank you for watching.
