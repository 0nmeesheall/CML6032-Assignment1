#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CML6032 ASSIGNMENT 1 - SLIDE VIDEO ASSEMBLY FROM RECORDED VOICE NOTES
NISHEAL MICHAEL KALEY | ENTRY NO 2025CYS7090 | IIT DELHI

WHAT THIS REPLACES
------------------
THE EARLIER TRANSCRIPT.PY SYNTHESISED NARRATION WITH A TEXT-TO-SPEECH MODEL AND
NEEDED A GPU. THAT IS RETIRED. THE NARRATION IS NOW THE AUTHOR'S OWN RECORDED
VOICE NOTES, ONE PER NUMBERED SLIDE, SO THIS SCRIPT ONLY CONDITIONS AUDIO AND
MUXES. IT IS CPU ONLY, NEEDS NO MODEL DOWNLOAD AND NEEDS NO NETWORK.

INPUTS
------
  CML_SLIDES   DIRECTORY OF SLIDE PNG. DEFAULT ./slides
               FILES NAMED 01.png .. 15.png ARE ANSWER SLIDES AND ARE NARRATED.
               FILES WITH A LETTER SUFFIX ARE NOT NARRATED AND ARE HELD SILENT:
               01a.png, 04a.png AND 09a.png ARE QUESTION SLIDES; 02a.png IS THE
               POST-EVALUATION NOTICE (ADDED 2026-10-04), HELD LONGER SO THE
               PASTED FEEDBACK CAN BE READ.
  CML_VOICE    DIRECTORY OF RECORDINGS. DEFAULT ./voicenotes
               ONE FILE PER ANSWER SLIDE. ACCEPTED NAMES, CASE AND SPACING FREE:
               "Slide 7.wav", "slide_7.wav", "07.wav", "7.m4a", "Slide07.mp3" ...
               ACCEPTED CONTAINERS: wav m4a mp3 aac flac ogg opus webm
  CML_WORK     SCRATCH AND CACHE DIRECTORY. DEFAULT ./build
  CML_OUT      OUTPUT MP4. DEFAULT ./CML6032_Assignment1_Nisheal_2025CYS7090.mp4

OUTPUTS
-------
  THE MP4, 1920 x 1080, 30 fps, H.264 + AAC, FASTSTART
  chapters.json   ONE ENTRY PER SLIDE FROM THE REAL MEASURED DURATIONS
  timeline.csv    PER SLIDE START, DURATION AND SOURCE FILE
  build/norm/     PER SLIDE CONDITIONED WAV, REUSED ON RERUNS

AUDIO CONDITIONING PER SLIDE
----------------------------
  1 HIGHPASS AT 70 Hz TO DROP DESK RUMBLE AND BREATH THUMP
  2 OPTIONAL FFT DENOISE, OFF BY DEFAULT, SET CML_DENOISE=1 TO ENABLE
  3 LEADING AND TRAILING SILENCE TRIMMED AT -50 dB PEAK
  4 TWO PASS EBU R128 LOUDNESS NORMALISATION TO I = -16 LUFS, TP = -1.5 dBTP
    TWO PASS MATTERS: A SINGLE PASS IS DYNAMIC AND PUMPS THE QUIET SLIDES
  5 RESAMPLED TO 48 kHz STEREO s16 SO EVERY SEGMENT CONCATENATES CLEANLY
  6 0.25 s OF LEAD IN AND 0.60 s OF LEAD OUT SO CUTS DO NOT CLIP SPEECH

SAFETY CHECKS, ALL FATAL UNLESS STATED
--------------------------------------
  * EVERY ANSWER SLIDE MUST HAVE EXACTLY ONE RECORDING
  * A RECORDING THAT MATCHES NO SLIDE IS AN ERROR, NOT A SILENT SKIP
  * TWO RECORDINGS CLAIMING THE SAME SLIDE IS AN ERROR
  * A RECORDING SHORTER THAN 0.35 OF THE MEDIAN IS REPORTED AS A LIKELY
    TRUNCATED TAKE; IT IS A WARNING, AND CML_STRICT=1 PROMOTES IT TO FATAL
  * THE FINISHED MP4 DURATION IS COMPARED WITH THE PLANNED TIMELINE AND MUST
    AGREE TO WITHIN 0.5 s

USAGE
-----
  python3 BUILD_VIDEO.py            BUILD
  python3 BUILD_VIDEO.py --check    VALIDATE INPUTS AND PRINT THE PLAN ONLY
  python3 BUILD_VIDEO.py --force    IGNORE THE CACHE AND RECONDITION EVERY NOTE
  python3 BUILD_VIDEO.py --meta     REWRITE chapters.json AND timeline.csv ONLY,
                                    FROM THE CACHED AUDIO, WITHOUT RE-ENCODING
"""

import csv, json, os, re, shutil, subprocess, sys
from pathlib import Path

# ----------------------------------------------------------------- CONFIG
HERE   = Path(__file__).resolve().parent
# RESOLVED TO ABSOLUTE PATHS: THE FFMPEG CONCAT LISTS IN WORK/ NAME THEIR FILES BY PATH, AND A
# RELATIVE ENTRY IS READ RELATIVE TO THE LIST ITSELF (build/build/norm/...), WHICH BROKE RELATIVE
# SETTINGS SUCH AS THE NOTEBOOK'S CML_WORK = 'build'.
SLIDES = Path(os.environ.get('CML_SLIDES', HERE / 'slides')).expanduser().resolve()
VOICE  = Path(os.environ.get('CML_VOICE',  HERE / 'voicenotes')).expanduser().resolve()
WORK   = Path(os.environ.get('CML_WORK',   HERE / 'build')).expanduser().resolve()
OUT    = Path(os.environ.get('CML_OUT',    HERE / 'CML6032_Assignment1_Nisheal_2025CYS7090.mp4')).expanduser().resolve()

FPS           = int(os.environ.get('CML_FPS', 30))
CRF           = int(os.environ.get('CML_CRF', 20))
ABR           = os.environ.get('CML_ABR', '160k')
TARGET_I      = -16.0
TARGET_TP     = -1.5
TARGET_LRA    = 11.0
HIGHPASS_HZ   = 70
DENOISE       = os.environ.get('CML_DENOISE', '0') == '1'
TRIM_DB       = -50
HEAD_PAD      = float(os.environ.get('CML_HEAD_PAD', 0.25))
TAIL_PAD      = float(os.environ.get('CML_TAIL_PAD', 0.60))
QUESTION_HOLD = float(os.environ.get('CML_QUESTION_HOLD', 8.0))
NOTICE_HOLD   = float(os.environ.get('CML_NOTICE_HOLD', 15.0))
SHORT_FACTOR  = 0.35
STRICT        = os.environ.get('CML_STRICT', '0') == '1'

AUDIO_EXT = ('.wav', '.m4a', '.mp3', '.aac', '.flac', '.ogg', '.opus', '.webm')

TITLES = {
     1: "TITLE AND SCOPE",
     2: "PART A: THE CRYSTALS ISSUED IN CLASS, AS PHOTOGRAPHED",
     3: "MORPHOLOGY: ONE ANGLE, MANY SHAPES",
     4: "POINT GROUP: OPERATIONS, EXCLUSIONS AND VERDICT",
     5: "PART B SEGMENT 1: FERROELECTRIC DISTORTION OF BaTiO3",
     6: "Ti DISPLACEMENT SERIES ALONG c",
     7: "NINE DISTORTION STATES: GEOMETRY AND RIGID-ION POLARISATION",
     8: "FERROELECTRIC HYSTERESIS: CORRECTED TWO-BRANCH LOOP",
     9: "WHY A LOOP AND NOT A LINE: DOUBLE WELL, DOMAINS AND Tc",
    10: "PART B SEGMENT 2: NINE BINARY CUBIC PROTOTYPES",
    11: "ROCK SALT TYPE: NaCl AND CaTe",
    12: "CAESIUM CHLORIDE TYPE: CsCl AND AuZn",
    13: "FLUORITE AND ANTIFLUORITE: CaF2, CeO2 AND K2O",
    14: "ZINC BLENDE TYPE: ZnS AND GaP",
    15: "VERIFICATION, MANIFEST AND WHAT IS STILL MISSING",
}
QUESTION_TITLES = {
    '01a': "THE BRIEF: PART A AS ISSUED",
    '04a': "THE BRIEF: PART B SEGMENT 1 AS ISSUED",
    '09a': "THE BRIEF: PART B SEGMENT 2 AS ISSUED",
    '02a': "NOTICE: PART A CORRECTED AFTER EVALUATION",
}
NOTICES = {'02a'}            # HELD FOR NOTICE_HOLD AND LABELLED 'notice' IN THE METADATA

def hold(key):
    return NOTICE_HOLD if key in NOTICES else QUESTION_HOLD

def kind(it):
    if it['src'] is not None: return 'answer'
    return 'notice' if it['slide']['key'] in NOTICES else 'question'

# ------------------------------------------------------------------ UTIL
class Fail(SystemExit):
    def __init__(self, msg): super().__init__('FATAL: ' + msg)

def sh(args, capture=True):
    r = subprocess.run(args, stdout=subprocess.PIPE if capture else None,
                       stderr=subprocess.STDOUT if capture else None, text=True)
    return r.returncode, (r.stdout or '')

def need(tool):
    if not shutil.which(tool): raise Fail(f'{tool} IS NOT ON PATH')

def duration(path):
    rc, out = sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                  '-of', 'default=nw=1:nk=1', str(path)])
    if rc or not out.strip(): raise Fail(f'CANNOT PROBE {path}')
    return float(out.strip())

def hms(t):
    t = int(round(t)); return f'{t//60:02d}:{t%60:02d}'

# ------------------------------------------------- SLIDE AND NOTE PAIRING
SLIDE_RE = re.compile(r'^(\d{1,2})([a-z]?)$', re.I)

def read_slides():
    if not SLIDES.is_dir(): raise Fail(f'NO SLIDE DIRECTORY AT {SLIDES}')
    out = []
    for p in sorted(SLIDES.glob('*.png')):
        m = SLIDE_RE.match(p.stem)
        if not m:
            print(f'  SKIPPED NON SLIDE FILE {p.name}'); continue
        out.append({'path': p, 'key': p.stem.lower(),
                    'n': int(m.group(1)), 'suffix': m.group(2).lower()})
    if not out: raise Fail(f'NO SLIDE PNG FOUND IN {SLIDES}')
    out.sort(key=lambda s: (s['n'], s['suffix']))
    return out

NOTE_RE = re.compile(r'(?:^|[^0-9])(\d{1,2})\s*$')

def note_index(stem):
    s = re.sub(r'[\s_\-]+', ' ', stem.strip())
    s = re.sub(r'(?i)^(slide|sl|s|track|rec|recording|voice ?note|note)\b', '', s).strip()
    m = re.search(r'(\d{1,2})', s)
    return int(m.group(1)) if m else None

def read_notes():
    if not VOICE.is_dir(): raise Fail(f'NO VOICE NOTE DIRECTORY AT {VOICE}')
    found, unmatched = {}, []
    for p in sorted(VOICE.iterdir()):
        if not p.is_file() or p.suffix.lower() not in AUDIO_EXT: continue
        i = note_index(p.stem)
        if i is None: unmatched.append(p); continue
        if i in found:
            raise Fail(f'TWO RECORDINGS CLAIM SLIDE {i}: '
                       f'{found[i].name} AND {p.name}')
        found[i] = p
    if unmatched:
        raise Fail('THESE RECORDINGS CARRY NO SLIDE NUMBER: '
                   + ', '.join(p.name for p in unmatched))
    if not found: raise Fail(f'NO RECORDINGS FOUND IN {VOICE}')
    return found

# ----------------------------------------------------------- AUDIO CHAIN
def chain(ln=None):
    f = [f'highpass=f={HIGHPASS_HZ}']
    if DENOISE: f.append('afftdn=nr=12:nf=-30')
    f += [f'silenceremove=start_periods=1:start_duration=0:'
          f'start_threshold={TRIM_DB}dB:detection=peak',
          'areverse',
          f'silenceremove=start_periods=1:start_duration=0:'
          f'start_threshold={TRIM_DB}dB:detection=peak',
          'areverse']
    base = f'loudnorm=I={TARGET_I}:TP={TARGET_TP}:LRA={TARGET_LRA}'
    if ln is None:
        f.append(base + ':print_format=json')
    else:
        f.append(base + ':measured_I={input_i}:measured_LRA={input_lra}:'
                 'measured_TP={input_tp}:measured_thresh={input_thresh}:'
                 'offset={target_offset}:linear=true'.format(**ln))
        f += ['aformat=sample_fmts=s16:sample_rates=48000:channel_layouts=stereo',
              f'adelay={int(HEAD_PAD*1000)}:all=1',
              f'apad=pad_dur={TAIL_PAD}']
    return ','.join(f)

def measure(src):
    rc, out = sh(['ffmpeg', '-hide_banner', '-nostdin', '-i', str(src),
                  '-af', chain(None), '-f', 'null', '-'])
    blocks = re.findall(r'\{[^{}]*"input_i"[^{}]*\}', out, re.S)
    if not blocks: raise Fail(f'LOUDNORM MEASUREMENT FAILED FOR {src.name}\n{out[-1200:]}')
    d = json.loads(blocks[-1])
    for k in ('input_i', 'input_lra', 'input_tp', 'input_thresh', 'target_offset'):
        if k not in d or d[k] in ('-inf', 'inf', 'nan'):
            raise Fail(f'LOUDNORM RETURNED {k}={d.get(k)!r} FOR {src.name}; '
                       'THE TAKE IS PROBABLY SILENT')
    return d

def condition(src, dst, force):
    if dst.exists() and not force and dst.stat().st_mtime >= src.stat().st_mtime:
        return False
    ln = measure(src)
    rc, out = sh(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-i', str(src),
                  '-af', chain(ln), '-ar', '48000', '-ac', '2',
                  '-c:a', 'pcm_s16le', str(dst)])
    if rc or not dst.exists(): raise Fail(f'CONDITIONING FAILED FOR {src.name}\n{out[-1200:]}')
    return True

def silence(dst, secs, force):
    if dst.exists() and not force and abs(duration(dst) - secs) < 0.01: return False
    rc, out = sh(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-f', 'lavfi',
                  '-i', f'anullsrc=r=48000:cl=stereo', '-t', f'{secs}',
                  '-c:a', 'pcm_s16le', str(dst)])
    if rc: raise Fail(f'COULD NOT MAKE SILENCE\n{out[-600:]}')
    return True

# ------------------------------------------------------------- METADATA
# docs/index.html READS chapters.json AS {total, chapters:[{start, title}, ...]}
# AND FALLS BACK TO ITS OWN BUILT IN MARKS IF THE FETCH FAILS, SO THE SHAPE
# BELOW IS A CONTRACT WITH THAT PAGE. THE EXTRA KEYS ARE IGNORED BY THE PAGE
# AND ARE THERE FOR READING BY A HUMAN.
def write_meta(plan, total):
    doc = {'total': round(total, 2),
           'slides': len(plan),
           'generator': 'BUILD_VIDEO.py, FROM RECORDED VOICE NOTES',
           'chapters': [{'start': round(it['start'], 2),
                         'end': round(it['start'] + it['dur'], 2),
                         'duration': round(it['dur'], 2),
                         'title': it['title'],
                         'slide': it['slide']['key'],
                         'kind': kind(it)}
                        for it in plan]}
    (OUT.parent / 'chapters.json').write_text(json.dumps(doc, indent=1), encoding='utf-8')
    with (OUT.parent / 'timeline.csv').open('w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['slide', 'kind', 'start_s', 'duration_s', 'start_mmss', 'source', 'title'])
        for it in plan:
            w.writerow([it['slide']['key'],
                        kind(it),
                        f'{it["start"]:.2f}', f'{it["dur"]:.2f}', hms(it['start']),
                        it['src'].name if it['src'] else 'silence', it['title']])

# ------------------------------------------------------------------ MAIN
def main():
    force = '--force' in sys.argv
    check = '--check' in sys.argv
    meta  = '--meta'  in sys.argv
    for t in ('ffmpeg', 'ffprobe'): need(t)

    print('=' * 78)
    print('CML6032 ASSIGNMENT 1 - VIDEO FROM RECORDED VOICE NOTES')
    print('=' * 78)
    print(f'SLIDES  {SLIDES}\nVOICE   {VOICE}\nWORK    {WORK}\nOUT     {OUT}')
    print(f'DENOISE {"ON" if DENOISE else "OFF"}   QUESTION HOLD {QUESTION_HOLD:.1f} s   '
          f'NOTICE HOLD {NOTICE_HOLD:.1f} s   '
          f'CRF {CRF}   {FPS} fps\n')

    slides  = read_slides()
    answers = [s for s in slides if not s['suffix']]
    quests  = [s for s in slides if s['suffix']]
    notes   = read_notes()

    want = {s['n'] for s in answers}
    have = set(notes)
    if want - have:
        raise Fail('NO RECORDING FOR SLIDE(S) ' + ', '.join(str(n) for n in sorted(want - have)))
    if have - want:
        raise Fail('RECORDING(S) FOR SLIDE(S) ' + ', '.join(str(n) for n in sorted(have - want))
                   + ' BUT THERE IS NO SUCH ANSWER SLIDE')
    print(f'{len(answers)} ANSWER SLIDES, {len(quests)} HELD SLIDES (QUESTION OR NOTICE), '
          f'{len(notes)} RECORDINGS, ALL PAIRED')

    raw = {n: duration(p) for n, p in sorted(notes.items())}
    med = sorted(raw.values())[len(raw) // 2]
    short = [n for n, d in raw.items() if d < SHORT_FACTOR * med]
    if short:
        msg = ('LIKELY TRUNCATED TAKE(S): ' +
               ', '.join(f'SLIDE {n} IS {raw[n]:.1f} s AGAINST A MEDIAN OF {med:.1f} s'
                         for n in sorted(short)))
        if STRICT: raise Fail(msg)
        print('\n*** WARNING *** ' + msg)
        print('    THE BUILD CONTINUES. RE-RECORD AND RERUN TO REPLACE IT.\n')

    WORK.mkdir(parents=True, exist_ok=True)
    norm = WORK / 'norm'; norm.mkdir(exist_ok=True)

    plan = []
    for s in slides:
        if s['suffix']:
            wav = norm / f'{s["key"]}.wav'
            plan.append({'slide': s, 'wav': wav, 'src': None,
                         'title': QUESTION_TITLES.get(s['key'], 'THE BRIEF AS ISSUED')})
        else:
            wav = norm / f'{s["n"]:02d}.wav'
            plan.append({'slide': s, 'wav': wav, 'src': notes[s['n']],
                         'title': TITLES.get(s['n'], f'SLIDE {s["n"]}')})

    if check:
        print('PLAN (RAW RECORDING LENGTHS, BEFORE TRIM AND PAD)')
        for it in plan:
            s = it['slide']
            d = raw[s['n']] if it['src'] else hold(s['key'])
            tag = 'HOLD ' if it['src'] is None else 'VOICE'
            print(f'  {s["key"]:>4}  {tag}  {d:7.2f} s  '
                  f'{it["src"].name if it["src"] else "(silence)"}')
        print(f'\nRAW TOTAL {sum(raw.values()) + sum(hold(q["key"]) for q in quests):.1f} s')
        return

    print('CONDITIONING AUDIO')
    for it in plan:
        if it['src'] is None:
            did = silence(it['wav'], hold(it['slide']['key']), force)
        else:
            did = condition(it['src'], it['wav'], force)
        it['dur'] = duration(it['wav'])
        print(f'  {it["slide"]["key"]:>4}  {it["dur"]:7.2f} s  '
              f'{"BUILT" if did else "CACHED"}  '
              f'{it["src"].name if it["src"] else "silence"}')

    t = 0.0
    for it in plan:
        it['start'] = t; t += it['dur']
    total = t
    print(f'\nTIMELINE {total:.2f} s = {hms(total)}')

    if meta:
        write_meta(plan, total)
        print('REWROTE chapters.json AND timeline.csv FROM THE CACHED AUDIO, NO ENCODE')
        for it in plan:
            print(f'  {hms(it["start"])}  {it["slide"]["key"]:>4}  {it["dur"]:6.2f} s  {it["title"]}')
        return

    alist = WORK / 'audio.txt'
    alist.write_text(''.join(f"file '{it['wav'].as_posix()}'\n" for it in plan), encoding='utf-8')
    audio = WORK / 'audio.wav'
    rc, out = sh(['ffmpeg', '-hide_banner', '-nostdin', '-y', '-f', 'concat', '-safe', '0',
                  '-i', str(alist), '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', str(audio)])
    if rc: raise Fail('AUDIO CONCATENATION FAILED\n' + out[-1200:])
    ad = duration(audio)
    if abs(ad - total) > 0.25:
        raise Fail(f'CONCATENATED AUDIO IS {ad:.2f} s BUT THE TIMELINE SAYS {total:.2f} s')

    ilist = WORK / 'images.txt'
    lines = []
    for it in plan:
        lines.append(f"file '{it['slide']['path'].as_posix()}'\nduration {it['dur']:.6f}\n")
    lines.append(f"file '{plan[-1]['slide']['path'].as_posix()}'\n")   # CONCAT DEMUXER EATS THE LAST DURATION
    ilist.write_text(''.join(lines), encoding='utf-8')

    venc = ['-c:v', 'libx264', '-preset', 'medium', '-crf', str(CRF), '-tune', 'stillimage']
    rc, _ = sh(['ffmpeg', '-hide_banner', '-encoders'])
    if 'h264_nvenc' in _ and os.environ.get('CML_NVENC', '1') == '1':
        venc = ['-c:v', 'h264_nvenc', '-preset', 'p5', '-rc', 'vbr', '-cq', str(CRF), '-b:v', '0']
        print('USING h264_nvenc')
    else:
        print('USING libx264')

    print('ENCODING, ONE PASS')
    cmd = ['ffmpeg', '-hide_banner', '-nostdin', '-y',
           '-f', 'concat', '-safe', '0', '-i', str(ilist),
           '-i', str(audio),
           '-vf', f'scale=1920:1080:force_original_aspect_ratio=decrease,'
                  f'pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,fps={FPS},format=yuv420p',
           *venc, '-c:a', 'aac', '-b:a', ABR, '-ar', '48000', '-ac', '2',
           '-movflags', '+faststart', '-shortest', str(OUT)]
    rc, out = sh(cmd)
    if rc or not OUT.exists(): raise Fail('ENCODE FAILED\n' + out[-2500:])

    got = duration(OUT)
    if abs(got - total) > 0.5:
        raise Fail(f'OUTPUT IS {got:.2f} s BUT THE TIMELINE SAYS {total:.2f} s')

    write_meta(plan, total)

    print('\n' + '=' * 78)
    print(f'WROTE {OUT}')
    print(f'      {got:.2f} s = {hms(got)}   {OUT.stat().st_size/1e6:.1f} MB   1920x1080 @ {FPS} fps')
    print(f'      chapters.json AND timeline.csv BESIDE IT')
    print('=' * 78)
    for it in plan:
        print(f'  {hms(it["start"])}  {it["slide"]["key"]:>4}  {it["dur"]:6.2f} s  {it["title"]}')

if __name__ == '__main__':
    main()
