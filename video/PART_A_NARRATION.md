# NARRATION TO RE-RECORD: SLIDE 01 (MODIFIED) AND PART A SLIDES 02 TO 04

> **POST-EVALUATION NOTE (4 OCTOBER 2026).** THIS IS THE SCRIPT AS RECORDED AND EVALUATED. ITS SLIDE 03
> AND 04 TEXT ARGUES FOR m3̄m, WHICH THE INSTRUCTOR'S FEEDBACK SHOWED TO BE WRONG: THE CRYSTALS HAVE NO 3
> OR 3̄ AXIS. THE CORRECTED ANSWER, mmm (D2h, CLASS 8), IS ON SLIDES 03 AND 04, ON THE ANSWER SHEET AND IN
> THE README. THIS SCRIPT IS KEPT UNCHANGED AS THE EVALUATED RECORD, AND THE EVALUATED 26:38 VIDEO STAYS
> AT COMMIT `1bebbc3`; THE CURRENT 28:31 VIDEO (5 OCTOBER 2026) USES THE CORRECTED TAKES FOR 03, 04 AND 15.
> THE CORRECTED SCRIPT FOR THE CHANGED SLIDES (03, 04 AND 15) IS `PART_A_CORRECTED_NARRATION.md`.

STATUS: RECORDED BY THE AUTHOR AND BUILT INTO THE 26:38 WALKTHROUGH ON 2026-10-02
(SEE `CHANGELOG.md` SECTION 9.1). THE TEXT BELOW IS KEPT AS THE SCRIPT OF RECORD.

THE PART A SLIDES WERE REDONE FROM THE FIVE CLASS PHOTOGRAPHS, SO THE OLD TAKES
(`Slide 2.wav` 76.2 s, `Slide 3.wav` 91.1 s, `Slide 4.wav` 105.3 s) NO LONGER MATCH
WHAT IS ON SCREEN. THE SLIDE 01 TAKE (`Slide 1.wav`, 56.5 s) STILL DESCRIBES "TWO
MACROSCOPIC CRYSTAL SPECIMENS", SO ITS PART A SENTENCE IS REWRITTEN TOO; THE SLIDE
ITSELF IS UNCHANGED. RECORD ONE TAKE PER SLIDE FROM THE TEXT BELOW, SAVE THEM AS
`Slide 1.wav` TO `Slide 4.wav` IN `voicenotes/`, POINT THE BUILDER AT THE NEW SLIDE
RASTERS (`CML_SLIDES=../slides/png`) AND RUN `python3 BUILD_VIDEO.py`. ONLY THE FOUR
NEW TAKES ARE RECONDITIONED; THE REST COMES FROM THE CACHE.

THE TEXT IS WRITTEN TO BE SPOKEN: UNITS AND SYMBOLS ARE SPELLED OUT ("DEGREES",
"m three-bar m", "four over m m m"). SLIDE 01 IS 156 WORDS, ABOUT 1:00. THE THREE
PART A TAKES ARE 947 WORDS: ABOUT 6:45 AT AN UNHURRIED 140 WORDS PER MINUTE, ABOUT
6:05 AT 155, INSIDE THE 5 TO 8 MINUTE WINDOW.

---

## SLIDE 01: TITLE AND SCOPE (MODIFIED)

Good morning. I am Nisheal Michael Kaley, entry number twenty twenty-five C Y S
seven zero nine zero, and this is my submission for C M L six zero three two,
Materials Chemistry, Assignment One. The work has three parts. Part A identifies
the point group of the crystals we were given in class. I work from my own
photographs of them, measure their corner angles directly on the images, and use
those angles to decide the most probable point group. Part B, segment one, models
the ferroelectric distortion of barium titanate by stepping the titanium cation
along the polar c axis, and links those microscopic states to the macroscopic
polarisation against field loop. Part B, segment two, classifies nine binary cubic
prototypes across five structural families. Throughout, lengths are in
picometres, ratios are plain ratios, mirror planes are written M P, and every bar
in a symbol is spoken, as in F m three-bar m.

---

## SLIDE 02: THE CRYSTALS ISSUED IN CLASS, AS PHOTOGRAPHED

Part A asks for the point group of the crystals we were given in class, so I start
from the crystals themselves. These are my five photographs. Picture one shows ten
crystals, which I have labelled C1 to C10; picture two is the same layout, retaken.
Pictures three, four and five show one more crystal on its own, turned between
shots. So in total I am looking at eleven crystals. There is no scale object in the
photos, so I only use angles and ratios, never absolute sizes.

Here is what I observe. The crystals are colourless. The slight warm tint is also
present in the shadows, so it comes from the lighting and not from the crystals.
The lustre is vitreous and the crystals are translucent, and some faces, on C5, C6,
C10 and view A, are frosted in the centre. The habit is blocky: in plan view, the
length over width runs from about one to about two. The faces are flat and come in
parallel opposite pairs, the edges are straight, and the ends are flat and blunt.
Every clean corner looks square.

What I do not see matters just as much. On none of the eleven crystals is there a
pyramid, a dome, or a small facet cutting off a corner. The defects are rounded
edges, chipped ends, and cracks that run parallel to a face, as in C1 and C10.

So the read-out from this slide is simple. There is only one geometry here: six
flat faces, in three parallel pairs, meeting square, whatever the length of the
crystal. On the next slide, I replace the word "square" with a measurement.

---

## SLIDE 03: MORPHOLOGY, ONE ANGLE, MANY SHAPES

To put a number on "square", I measured the angles on the photographs themselves.
Each crystal was cropped at full resolution, the contrast was equalised, and a
line-segment detector found the straight edges. I kept only the segments that lie
on real crystal edges, not on shadows or internal cracks, and every choice is drawn
on an overlay, as you can see here for C4, C6, C7 and view B. Cyan lines are the
side edges, green marks a clean end, and red marks a chipped end.

The top plot shows the result. Eleven clean corners lie between eighty-six point
two and eighty-nine point nine degrees, with a mean of eighty-eight point one. That
small offset below ninety is expected. I measure the acute angle between two edges,
so about two point four degrees of edge noise always folds back below ninety, and a
simulation of that folding gives the same mean and a similar spread. These corners are right
angles. The six red crosses are the chipped or rounded ends, from about seventy-one
to eighty-four degrees. They never come in parallel pairs, so they are damage, not a
second set of faces. Opposite edges are parallel to within one to seven degrees.

The bottom plot is the length over width in plan view. Within one batch it runs
from one point zero zero to two point zero three. So the shape changes by a factor
of two, while the angle does not change at all. That is Steno's law of constant
interfacial angles, seen directly on these crystals.

On the right is the idealised habit. A single form, the cube, with faces of the
type one-zero-zero, gives six faces at ninety degrees. If some faces grow faster
than others, only their distances from the centre change, and the cube becomes an
elongated box like C4, C7 and view B. So one form, the cube, explains every face I
have seen.

---

## SLIDE 04: POINT GROUP, OPERATIONS, EXCLUSIONS AND VERDICT

Now the point group. On the left is the stereogram of m three-bar m, with the
observed face poles in amber; the six cube faces sit on the three four-fold axes.
Mapped onto the crystal, the group has three four-fold axes from face centre to face
centre, four three-fold axes from corner to corner, six two-fold axes from edge
midpoint to edge midpoint, nine mirror planes, three parallel to the faces and six
through opposite edges, and a centre of symmetry, because every face has a parallel
partner. Together, these give forty-eight operations.

The table on the right is the exclusion chain: what each candidate needs, against
what the photos show. Triclinic needs a corner away from ninety degrees, and all
eleven clean corners are square. Monoclinic needs a tilted pair of parallel end
faces, and the six tilted ends are chipped and never parallel. Hexagonal and
trigonal need sixty or one-hundred-and-twenty-degree corners, and I see only right
angles. The tetragonal and orthorhombic boxes, four over m m m and m m m, are the
runner-up. They have the same right angles, but they need two or three different
forms and a fixed long axis with its own type of face, and nothing I measured ties
the elongation or a face type to one axis. The lower cubic classes would show
striations, twisted etch pits or extra facets, and none are resolved. So the most
probable point group is the full cubic class: m three-bar m, Schoenflies O h, class
thirty-two, full symbol four over m, three-bar, two over m.

I want to be clear about the limit. Form alone cannot rule out a tetragonal or
orthorhombic box with the same angles, and the centre of symmetry rests on the
parallel face pairs, because I did no piezoelectric or pyroelectric test. The
decisive check is simple: crossed polarisers, using an LCD screen and a polarising
filter. Turn the crystal on each of its three face types. A cubic crystal stays dark
on all three, a tetragonal one on only one, and an orthorhombic one on none. That
completes Part A.
