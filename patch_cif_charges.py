#!/usr/bin/env python3
"""
ADD _atom_type_oxidation_number TO EVERY CIF SO VESTA CAN RESOLVE IONIC RADII.

WITHOUT A FORMAL CHARGE ON EACH SPECIES VESTA HAS NOTHING TO LOOK UP AND SILENTLY
FALLS BACK TO NEUTRAL ATOMIC RADII, WHICH DRAWS Na LARGER THAN Cl AND Ti LARGER
THAN O - THE EXACT REVERSE OF THE IONIC PICTURE THE RADIUS-RATIO ARGUMENT NEEDS.

CHARGE SCHEME. IONIC CHARGES ARE ASSIGNED WHERE THE BONDING IS IONIC. AuZn AND
GaP ARE LEFT NEUTRAL ON PURPOSE: AuZn IS METALLIC AND GaP IS COVALENT, SO THE
METALLIC AND COVALENT RADII THAT VESTA USES AT ZERO CHARGE ARE THE CORRECT ONES
AND THE IONIC RADIUS-RATIO WINDOWS DO NOT APPLY TO EITHER.
"""
import re, pathlib

CHARGES = {
    'NaCl':   {'Na': +1, 'Cl': -1},
    'CaTe':   {'Ca': +2, 'Te': -2},
    'CsCl':   {'Cs': +1, 'Cl': -1},
    'CaF2':   {'Ca': +2, 'F':  -1},
    'CeO2':   {'Ce': +4, 'O':  -2},
    'K2O':    {'K':  +1, 'O':  -2},
    'ZnS':    {'Zn': +2, 'S':  -2},
    'AuZn':   {'Au':  0, 'Zn':  0},   # METALLIC - NEUTRAL ON PURPOSE
    'GaP':    {'Ga':  0, 'P':   0},   # COVALENT  - NEUTRAL ON PURPOSE
    'BaTiO3': {'Ba': +2, 'Ti': +4, 'O': -2},
}
NOTE = {
    'AuZn': 'ZERO CHARGE IS DELIBERATE: AuZn IS A METALLIC BETA-BRASS TYPE PHASE,\n#                       SO VESTA MUST USE METALLIC RADII (Au 144 pm, Zn 134 pm).',
    'GaP':  'ZERO CHARGE IS DELIBERATE: GaP IS COVALENT, SO VESTA MUST USE COVALENT\n#                       RADII (Ga 126 pm, P 107 pm), NOT IONIC RADII.',
}

def patch(path, key):
    txt = path.read_text()
    if '_atom_type_oxidation_number' in txt:
        return 'ALREADY PRESENT'
    charges = CHARGES[key]
    # ORDER THE TYPE LOOP TO MATCH THE ORDER THE SPECIES FIRST APPEAR IN THE SITE LOOP
    order = []
    for sym in re.findall(r'^\s+\S+\s+[\d.]+\s+[-\d.]+\s+[-\d.]+\s+[-\d.]+\s+\S+\s+\S+\s+(\S+)\s*$',
                          txt, re.M):
        if sym in charges and sym not in order:
            order.append(sym)
    for s in charges:                      # SAFETY NET
        if s not in order:
            order.append(s)
    block = ['loop_', '   _atom_type_symbol', '   _atom_type_oxidation_number']
    for s in order:
        block.append(f'   {s:<4s} {charges[s]:+d}.0')
    extra = ('# FORMAL CHARGES       : ' +
             ', '.join(f'{s}({charges[s]:+d}, SPIN UNASSIGNED)' for s in order) + '\n')
    if key in NOTE:
        extra += '#                       ' + NOTE[key] + '\n'
    # INSERT THE COMMENT INTO THE EXISTING HEADER BLOCK
    txt = txt.replace('# PREPARED BY', extra + '# PREPARED BY', 1)
    # INSERT THE TYPE LOOP IMMEDIATELY BEFORE THE SITE LOOP
    anchor = 'loop_\n   _atom_site_label'
    txt = txt.replace(anchor, '\n'.join(block) + '\n\n' + anchor, 1)
    path.write_text(txt)
    return 'PATCHED -> ' + ' '.join(f'{s}{charges[s]:+d}' for s in order)

rows = []
for p in sorted(pathlib.Path('cif_prototypes').glob('*.cif')):
    rows.append((p.name, patch(p, p.stem)))
for p in sorted(pathlib.Path('cif_batio3').glob('*.cif')):
    rows.append((p.name, patch(p, 'BaTiO3')))
for n, r in rows:
    print(f'  {n:26s} {r}')
print(f'\n{len(rows)} CIF FILES PROCESSED')
