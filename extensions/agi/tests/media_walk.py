#!/usr/bin/env python3
"""g5.4.2 THE WALK (council 07:59Z (4), 08:02Z): one unattended runner, no Claude needed. Renders the chapters' NARRATION in order (C2 first = the pilot) under the key caps.
Per chunk (<= 1500 chars at sentence boundaries): TTS (Gemini Schedar, description v2, default temperature) -> PCM duration check (media_pcm) -> mp3 -> measured f0 + pace ->
STT (scribe-v2) of the RAW chunk -> fidelity (media_fidelity, REF = the chunk text) -> local normalisation to TARGET (rubberband, formant preserved, tempo 1, ratio = TARGET / measured f0)
-> output f0 within 5 percent of TARGET and pace within 15 percent of the c2a anchor. Any RED -> re-render ONCE. Still RED (council 08:08Z, W3): a 2nd FIDELITY-only RED KEEPS the take with fewer error ops,
flagged in the README with its runs (chapter 'partial: N flagged'); a 2nd PCM RED (or pace/pitch RED) is SKIPPED with a README line. The walk goes on.
Two keys, each capped and counted at its full limit: a TTS key (Gemini only) and an STT key (scribe only). Every request is logged BEFORE it is sent; W2: a 5xx or timeout waits 60 s and retries that request ONCE; a 2nd failure or any 4xx stops the walk CLEAN ('stopped: http').
Before each chapter the remaining life of both keys must cover the chapter's estimated time, else: 'stopped: key expiry'. A finished chapter goes to deliver/ at once (644) as season3-CNN-narration.mp3 AND (W4) explainer-chNN-<slug>.mp4 (a static title card + the narration, ONE fixed encode profile, PROFILE below); README-narration.txt is rewritten.
usage: walk.py TTSKEYFILE STTKEYFILE [--chapters=C2,C3,...] [--target=100] [--dry]   (--dry: no request is sent; a stored take stands in, to test the flow)"""
import base64, hashlib, json, os, re, shutil, subprocess, sys, time, urllib.request, urllib.error
REPO = os.environ.get('MEDIA_REPO') or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))   # the checkout that holds this file; a COPY of this file (season3/walk/walk.py) must set MEDIA_REPO
sys.path.insert(0, REPO + '/extensions/agi/tests')
import media_fidelity, media_fm2, media_pcm
SHA = '6432bf88d5'
SCRIPT = REPO + '/.agi/context/media/season3-explainer-script.md'
BASE = '/data/work/director-general-3-media/season3'
W, DELIVER = os.environ.get('WALK_DIR', BASE + '/walk'), os.environ.get('WALK_DELIVER', BASE + '/deliver')
DESC = open(BASE + '/r2/r3/description.txt', 'rb').read().decode()
assert hashlib.sha256(DESC.encode()).hexdigest() == '56acfac76bdbcd180043059d29c38e85fa3fb33ce196789e00b7f6cd8ff870c5'
args = [a for a in sys.argv[1:] if not a.startswith('--')]
opt = {a.split('=')[0]: a.split('=')[1] for a in sys.argv[1:] if a.startswith('--') and '=' in a}
DRY = '--dry' in sys.argv
TARGET = float(opt.get('--target', 100))
CHAPTERS = opt['--chapters'].split(',') if '--chapters' in opt else ['C2'] + [f'C{i}' for i in range(0, 18) if i != 2]
ANCHOR_CPS = 13.8                   # schedar-c2a
CHUNK_MAX, PAUSE = 1500, 0.5
RETRY_WAIT = 60                     # W2: seconds before the ONE retry of a 5xx / timeout
# W4: ONE fixed encode profile for every explainer-chNN-<slug>.mp4 (recorded once on the run doc, so the watcher can join them without a re-encode)
PROFILE = {'codec_name': 'h264', 'width': 1280, 'height': 720, 'r_frame_rate': '25/1', 'pix_fmt': 'yuv420p', 'a_codec': 'aac', 'sample_rate': '44100', 'channels': 1}
CARD_FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
now = lambda: time.strftime('%H:%M:%SZ', time.gmtime())
KEYS = {}
if not DRY:
    for kind, f in (('tts', args[0]), ('stt', args[1])):
        KEYS[kind] = open(os.path.join(os.path.expanduser('~'), 'keys', f)).read().strip()
H = lambda kind: {'Authorization': 'Bearer ' + KEYS[kind], 'Content-Type': 'application/json'}
STOP = []


def key_info(kind):
    r = urllib.request.urlopen(urllib.request.Request('https://openrouter.ai/api/v1/key', headers=H(kind)), timeout=30)
    return json.load(r).get('data', {})


def say(*a):
    print(now(), *a, flush=True)


def narration():
    """{chapter: [rendered sentences of the narration, tags stripped]} from the M2 script."""
    text = open(SCRIPT, encoding='utf-8').read().split('\n')
    chap, sec, fence, blk, out = None, None, False, [], {}
    def flush():
        if blk and sec == 'narration':
            out.setdefault(chap, []).append(media_fm2.render(' '.join(blk), REPO, SHA))
        blk.clear()
    for ln in text:
        m = re.match(r'^## (C\d+)\b', ln)
        if m:
            flush(); chap, sec = m.group(1), None
        if ln.startswith('~~~~'):
            fence = not fence; continue
        if fence:
            continue
        m = re.match(r'^### (narration|html)\b', ln)
        if m:
            flush(); sec = m.group(1); continue
        if re.match(r'^##+ ', ln):
            flush(); sec = None; continue
        if sec is None or re.match(r'^(@@excerpt|fn:|live:|uncalled:|sha:|pair )', ln):
            continue
        if not ln.strip():
            flush()
        else:
            blk.append(ln.strip())
    flush()
    return out


def chunks(paras):
    sents = media_fm2.split_sentences(' '.join(paras))
    out, cur = [], ''
    for s in sents:
        if cur and len(cur) + 1 + len(s) > CHUNK_MAX:
            out.append(cur); cur = s
        else:
            cur = (cur + ' ' + s).strip()
    return out + ([cur] if cur else [])


def log(kind, rec):
    with open(f'{W}/walk-requests-{kind}.log', 'a') as f:
        f.write(json.dumps({'t': now(), **rec}) + '\n')


def post(kind, url, body, rec):
    """Log first, send. W2: a 5xx or timeout/network error waits RETRY_WAIT s and retries that request ONCE (logged before it is sent);
    a 4xx, or a 2nd failure, stops the walk clean with 'http'."""
    sent = json.dumps(body, sort_keys=True).encode()
    for attempt in (1, 2):
        log(kind, {**rec, 'try': attempt, 'body_sha256': hashlib.sha256(sent).hexdigest()})
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, data=sent, headers=H(kind)), timeout=900)
            return r.read()
        except urllib.error.HTTPError as e:
            say('ERROR', rec, e.code, e.read()[:200].decode('utf-8', 'replace'))
            transient = e.code >= 500
        except Exception as e:
            say('ERROR', rec, type(e).__name__, str(e)[:160])
            transient = True
        if attempt == 1 and transient:
            say('transient failure: one retry in', RETRY_WAIT, 's'); time.sleep(RETRY_WAIT)
            continue
        break
    STOP.append('http'); return None


def f0_pace(path, chars):
    sys.path.insert(0, BASE + '/r2')
    import norm
    return norm.median_f0(path), chars / norm.dur(path)


def normalise(src, dst):
    sys.path.insert(0, BASE + '/r2')
    import norm
    f_in = norm.median_f0(src); ratio = TARGET / f_in
    flt = f'rubberband=tempo=1:pitch={ratio:.4f}:formant=preserved:pitchq=quality'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-ac', '1', '-ar', '44100', '-af', flt, '-c:a', 'libmp3lame', '-b:a', '128k', dst], check=True)
    return f_in, ratio, norm.median_f0(dst)


def take(status, mp3=None, errs=0, runs=(), notes=()):
    """One render attempt. status: ok | fid (fidelity-only RED, audio sound) | pcm (broken audio) | other (pace/pitch RED) | fail (request stopped the walk)."""
    return {'status': status, 'mp3': mp3, 'errs': errs, 'runs': list(runs), 'notes': list(notes)}


def render_chunk(chap, i, text, attempt, reuse):
    d = f'{W}/{chap}'; os.makedirs(d, exist_ok=True)
    raw_mp3, hyp_f = f'{d}/c{i}-a{attempt}.mp3', f'{d}/c{i}-a{attempt}.txt'
    if reuse and attempt == 1:
        shutil.copy(reuse[0], raw_mp3); open(hyp_f, 'w').write(open(reuse[1]).read())
        notes = ['reused ' + os.path.basename(reuse[0])]
    else:
        notes = []
        if DRY:
            return take('fail', notes=['dry: no stored take for this chunk'])
        body = {'model': 'google/gemini-3.8-flash-tts', 'response_format': 'pcm', 'input': text, 'voice': 'Schedar', 'instructions': DESC}
        pcm = post('tts', 'https://openrouter.ai/api/v1/audio/speech', body, {'chapter': chap, 'chunk': i, 'attempt': attempt, 'chars': len(text)})
        if pcm is None:
            return take('fail', notes=['tts request failed'])
        if media_pcm.check(len(pcm), len(text), 24000, echo=False):
            return take('pcm', notes=['pcm duration check RED'])
        open(f'{d}/c{i}-a{attempt}.pcm', 'wb').write(pcm)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', f'{d}/c{i}-a{attempt}.pcm', '-c:a', 'libmp3lame', '-b:a', '128k', raw_mp3], check=True)
        raw = open(raw_mp3, 'rb').read()
        res = post('stt', 'https://openrouter.ai/api/v1/audio/transcriptions',
                   {'model': 'elevenlabs/scribe-v2', 'language': 'en', 'input_audio': {'data': base64.b64encode(raw).decode(), 'format': 'mp3'}},
                   {'chapter': chap, 'chunk': i, 'attempt': attempt, 'audio_sha256': hashlib.sha256(raw).hexdigest()})
        if res is None:
            return take('fail', notes=['stt request failed'])
        open(hyp_f, 'w').write(json.loads(res).get('text', ''))
    f0, cps = f0_pace(raw_mp3, len(text))
    fid, errs, runs = media_fidelity.score(text, open(hyp_f).read())
    out_mp3 = f'{d}/c{i}-a{attempt}-norm.mp3'
    f_in, ratio, f_out = normalise(raw_mp3, out_mp3)
    pace_ok = abs(cps - ANCHOR_CPS) / ANCHOR_CPS <= 0.15
    pitch_ok = abs(f_out - TARGET) / TARGET <= 0.05
    notes += [f'f0 {f0:.1f} Hz, ratio {ratio:.3f}, out {f_out:.1f} Hz, pace {cps:.1f} c/s, fidelity {"RED" if fid else "GREEN"} ({errs} error ops)']
    if not pace_ok: notes.append('pace RED')
    if not pitch_ok: notes.append('output pitch RED')
    status = 'other' if not (pace_ok and pitch_ok) else ('fid' if fid else 'ok')
    return take(status, out_mp3, errs, runs, notes)


def walk_chunk(chap, i, text, reuse, notes_all):
    """Up to two attempts. -> (mp3 or None, flag or None). flag = (errs kept, errs of the other take or None, runs): W3, a 2nd fidelity RED keeps the take with fewer error ops."""
    takes = []
    for attempt in (1, 2):
        t = render_chunk(chap, i, text, attempt, reuse)
        notes_all.append(f'  chunk {i} attempt {attempt}: ' + '; '.join(t['notes']))
        say(chap, i, attempt, t['notes'])
        takes.append(t)
        if STOP or t['status'] in ('ok', 'fail'):
            break
    if takes[-1]['status'] == 'ok':
        return takes[-1]['mp3'], None
    fids = [t for t in takes if t['status'] == 'fid']
    if not fids:
        return None, None
    best = min(fids, key=lambda t: t['errs'])           # a tie keeps the first take
    other = [t for t in fids if t is not best]
    return best['mp3'], (best['errs'], other[0]['errs'] if other else None, best['runs'])


def join(chap, files, dst):
    sil = f'{W}/silence.mp3'
    if not os.path.exists(sil):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', str(PAUSE), '-c:a', 'libmp3lame', '-b:a', '128k', sil], check=True)
    lst = f'{W}/{chap}/list.txt'
    with open(lst, 'w') as f:
        for k, p in enumerate(files):
            f.write(f"file '{p}'\n" + (f"file '{sil}'\n" if k < len(files) - 1 else ''))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '128k', dst], check=True)


def chapter_titles():
    """{'C2': 'The ribosome: the unit turns pieces into tools'} from the '## C2 · Title' headings."""
    out = {}
    for ln in open(SCRIPT, encoding='utf-8').read().split('\n'):
        m = re.match(r'^## (C\d+)\s*[·:\-]\s*(.+?)\s*$', ln)
        if m:
            out[m.group(1)] = m.group(2)
    return out


def video_name(chap, title):
    """W4: explainer-chNN-<slug>.mp4, NN = the script chapter number in two digits (C0 -> ch00, C17 -> ch17)."""
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:48].strip('-') or 'chapter'
    return f'explainer-ch{int(chap[1:]):02d}-{slug}.mp4'


def card_video(chap, title, mp3):
    """W4: a static title card + the narration under the ONE fixed PROFILE. drawtext only if the font file exists, else a plain frame (the title is in the README)."""
    dst = f'{DELIVER}/{video_name(chap, title)}'
    vf = 'format=yuv420p'
    if os.path.exists(CARD_FONT):
        tf = f'{W}/{chap}/card.txt'
        open(tf, 'w', encoding='utf-8').write(f'Chapter {int(chap[1:])}\n{title}')
        vf = f"drawtext=fontfile={CARD_FONT}:textfile={tf}:fontcolor=white:fontsize=52:line_spacing=24:x=(w-text_w)/2:y=(h-text_h)/2,format=yuv420p"
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', f"color=c=0x14181f:s={PROFILE['width']}x{PROFILE['height']}:r=25", '-i', mp3,
                    '-vf', vf, '-c:v', 'libx264', '-tune', 'stillimage', '-r', '25', '-c:a', 'aac', '-ar', PROFILE['sample_rate'], '-ac', str(PROFILE['channels']), '-b:a', '128k',
                    '-shortest', '-movflags', '+faststart', dst], check=True)
    os.chmod(dst, 0o644)
    return dst


def readme(rows):
    txt = ['season 3 narration (voice DRAFT): written by the walk (director-general-3). Voice: Gemini 3.8 Flash TTS, Schedar, the owner-quoted description, pitch normalised locally to %.0f Hz (formant kept).' % TARGET,
           'The pick was made by the council while the owner slept; he can overrule. Banked beside it: raw, 91 Hz. Status per file: pilot = chapter 2, partial = a chunk was skipped or the walk stopped, \'partial: N flagged\' = N chunks kept after a 2nd fidelity RED (listed below), final = all chunks passed. explainer-chNN-*.mp4 = static title card + narration, one fixed profile: %s.' % json.dumps(PROFILE), '']
    txt += rows
    open(f'{DELIVER}/README-narration.txt', 'w').write('\n'.join(txt) + '\n'); os.chmod(f'{DELIVER}/README-narration.txt', 0o644)


def main():
    os.makedirs(W, exist_ok=True); os.makedirs(DELIVER, exist_ok=True)
    text, titles = narration(), chapter_titles()
    rows, reuse_map = [], {('C2', 0): (BASE + '/r2/r4/schedar-c2a.mp3', BASE + '/r2/r4/schedar-c2a.txt')}
    for chap in CHAPTERS:
        paras = text.get(chap)
        if not paras:
            continue
        cs = chunks(paras); est = sum(len(c) for c in cs) / ANCHOR_CPS / 3.0 + 60 * len(cs) * 0.3
        if not DRY:
            left = [(time.mktime(time.strptime(key_info(k)['expires_at'][:19], '%Y-%m-%dT%H:%M:%S')) - time.mktime(time.gmtime()) + time.timezone) for k in ('tts', 'stt')]
            if min(left) < est * 1.5:
                say('stopped: key expiry before', chap); rows.append(f'{chap}: stopped: key expiry'); break
        say(chap, len(cs), 'chunks', [len(c) for c in cs])
        good, skipped, flagged, notes_all = [], [], [], []
        for i, c in enumerate(cs):
            mp3, flag = walk_chunk(chap, i, c, reuse_map.get((chap, i)), notes_all)
            if mp3 is not None:
                good.append(mp3)
            elif not STOP:
                skipped.append(i)
            if flag:
                flagged.append(i)
                kept, other, runs = flag
                notes_all.append(f'  chunk {i} FLAGGED (2nd fidelity RED, kept the take with fewer error ops: {kept}' + (f' vs {other}' if other is not None else '') + '): ' + ' | '.join(runs))
            if STOP:
                break
        if good:
            dst = f'{DELIVER}/season3-{chap}-narration.mp3'
            join(chap, good, dst); os.chmod(dst, 0o644)
            clean = not skipped and not flagged and not STOP
            status = 'pilot' if chap == 'C2' and clean else ('final' if clean else 'partial' + (f': {len(flagged)} flagged' if flagged else ''))
            rows.append(f'season3-{chap}-narration.mp3: chapter {chap} narration, {len(good)} of {len(cs)} chunks, status {status}' + (f', SKIPPED chunks {skipped}' if skipped else '') + (f', STOPPED' if STOP else ''))
            try:
                mp4 = card_video(chap, titles.get(chap, chap), dst)
                rows.append(f'{os.path.basename(mp4)}: chapter {chap}, static-card version; the animated render is pending')
            except Exception as e:           # the mp3 is already delivered; a card failure must not stop the walk
                rows.append(f'{video_name(chap, titles.get(chap, chap))}: NOT written ({type(e).__name__}); the mp3 stands')
        rows += notes_all
        readme(rows)
        if STOP:
            rows.append(f'stopped: {STOP[0]}'); readme(rows); break
    say('walk ends'); readme(rows)


if __name__ == '__main__':
    main()
