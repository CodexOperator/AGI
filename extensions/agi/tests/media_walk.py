#!/usr/bin/env python3
"""g5.4.2 THE WALK (council 07:59Z (4), 08:02Z): one unattended runner, no Claude needed. Renders the chapters' NARRATION in order (C2 first = the pilot) under the key caps.
Per chunk (<= 1500 chars at sentence boundaries): TTS (Gemini Schedar, description v2, default temperature) -> PCM duration check (media_pcm) -> mp3 -> measured f0 + pace ->
STT (scribe-v2) of the RAW chunk -> fidelity (media_fidelity, REF = the chunk text) -> local normalisation to TARGET (rubberband, formant preserved, tempo 1, ratio = TARGET / measured f0)
-> output f0 within 5 percent of TARGET and pace within 15 percent of the c2a anchor. Any RED -> re-render ONCE; still RED -> the chunk is SKIPPED with a README line and the walk goes on.
Two keys, each capped and counted at its full limit: a TTS key (Gemini only) and an STT key (scribe only). Every request is logged BEFORE it is sent; a failed request (HTTP/network) stops the walk CLEAN (no retry).
Before each chapter the remaining life of both keys must cover the chapter's estimated time, else: 'stopped: key expiry'. A finished chapter goes to deliver/ at once (644) and README-narration.txt is rewritten.
usage: walk.py TTSKEYFILE STTKEYFILE [--chapters=C2,C3,...] [--target=100] [--dry]   (--dry: no request is sent; a stored take stands in, to test the flow)"""
import base64, hashlib, json, os, re, shutil, subprocess, sys, time, urllib.request, urllib.error
sys.path.insert(0, '/var/lib/agi/director-general-3/w-sg/extensions/agi/tests')
import media_fidelity, media_fm2, media_pcm
REPO = '/var/lib/agi/director-general-3/w-sg'
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
now = lambda: time.strftime('%H:%M:%SZ', time.gmtime())
KEYS = {}
if not DRY:
    for kind, f in (('tts', args[0]), ('stt', args[1])):
        KEYS[kind] = open(os.path.expanduser('~/keys/' + f)).read().strip()
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
    """Log first, send once. A failure stops the walk clean (no retry)."""
    sent = json.dumps(body, sort_keys=True).encode()
    log(kind, {**rec, 'body_sha256': hashlib.sha256(sent).hexdigest()})
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, data=sent, headers=H(kind)), timeout=900)
        return r.read()
    except urllib.error.HTTPError as e:
        say('ERROR', rec, e.code, e.read()[:200].decode('utf-8', 'replace'))
    except Exception as e:
        say('ERROR', rec, type(e).__name__, str(e)[:160])
    STOP.append('request failed'); return None


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


def render_chunk(chap, i, text, attempt, reuse):
    d = f'{W}/{chap}'; os.makedirs(d, exist_ok=True)
    raw_mp3, hyp_f = f'{d}/c{i}-a{attempt}.mp3', f'{d}/c{i}-a{attempt}.txt'
    if reuse and attempt == 1:
        shutil.copy(reuse[0], raw_mp3); open(hyp_f, 'w').write(open(reuse[1]).read())
        notes = ['reused ' + os.path.basename(reuse[0])]
    else:
        notes = []
        if DRY:
            return None, ['dry: no stored take for this chunk']
        body = {'model': 'google/gemini-3.8-flash-tts', 'response_format': 'pcm', 'input': text, 'voice': 'Schedar', 'instructions': DESC}
        pcm = post('tts', 'https://openrouter.ai/api/v1/audio/speech', body, {'chapter': chap, 'chunk': i, 'attempt': attempt, 'chars': len(text)})
        if pcm is None:
            return None, ['tts request failed']
        if media_pcm.check(len(pcm), len(text), 24000, echo=False):
            return 'RED', ['pcm duration check RED']
        open(f'{d}/c{i}-a{attempt}.pcm', 'wb').write(pcm)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 's16le', '-ar', '24000', '-ac', '1', '-i', f'{d}/c{i}-a{attempt}.pcm', '-c:a', 'libmp3lame', '-b:a', '128k', raw_mp3], check=True)
        raw = open(raw_mp3, 'rb').read()
        res = post('stt', 'https://openrouter.ai/api/v1/audio/transcriptions',
                   {'model': 'elevenlabs/scribe-v2', 'language': 'en', 'input_audio': {'data': base64.b64encode(raw).decode(), 'format': 'mp3'}},
                   {'chapter': chap, 'chunk': i, 'attempt': attempt, 'audio_sha256': hashlib.sha256(raw).hexdigest()})
        if res is None:
            return None, ['stt request failed']
        open(hyp_f, 'w').write(json.loads(res).get('text', ''))
    f0, cps = f0_pace(raw_mp3, len(text))
    fid = media_fidelity.check(text, open(hyp_f).read(), echo=False)
    out_mp3 = f'{d}/c{i}-a{attempt}-norm.mp3'
    f_in, ratio, f_out = normalise(raw_mp3, out_mp3)
    pace_ok = abs(cps - ANCHOR_CPS) / ANCHOR_CPS <= 0.15
    pitch_ok = abs(f_out - TARGET) / TARGET <= 0.05
    notes += [f'f0 {f0:.1f} Hz, ratio {ratio:.3f}, out {f_out:.1f} Hz, pace {cps:.1f} c/s, fidelity {"RED" if fid else "GREEN"}']
    ok = (not fid) and pace_ok and pitch_ok
    if not pace_ok: notes.append('pace RED')
    if not pitch_ok: notes.append('output pitch RED')
    return (out_mp3 if ok else 'RED'), notes


def join(chap, files, dst):
    sil = f'{W}/silence.mp3'
    if not os.path.exists(sil):
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i', 'anullsrc=r=44100:cl=mono', '-t', str(PAUSE), '-c:a', 'libmp3lame', '-b:a', '128k', sil], check=True)
    lst = f'{W}/{chap}/list.txt'
    with open(lst, 'w') as f:
        for k, p in enumerate(files):
            f.write(f"file '{p}'\n" + (f"file '{sil}'\n" if k < len(files) - 1 else ''))
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-ac', '1', '-ar', '44100', '-c:a', 'libmp3lame', '-b:a', '128k', dst], check=True)


def readme(rows):
    txt = ['season 3 narration (voice DRAFT): written by the walk (director-general-3). Voice: Gemini 3.8 Flash TTS, Schedar, the owner-quoted description, pitch normalised locally to %.0f Hz (formant kept).' % TARGET,
           'The pick was made by the council while the owner slept; he can overrule. Banked beside it: raw, 91 Hz. Status per file: pilot = chapter 2, partial = a chunk was skipped or the walk stopped, final = all chunks passed.', '']
    txt += rows
    open(f'{DELIVER}/README-narration.txt', 'w').write('\n'.join(txt) + '\n'); os.chmod(f'{DELIVER}/README-narration.txt', 0o644)


def main():
    os.makedirs(W, exist_ok=True); os.makedirs(DELIVER, exist_ok=True)
    text = narration()
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
        good, skipped, notes_all = [], [], []
        for i, c in enumerate(cs):
            res = None
            for attempt in (1, 2):
                res, notes = render_chunk(chap, i, c, attempt, reuse_map.get((chap, i)))
                notes_all.append(f'  chunk {i} attempt {attempt}: ' + '; '.join(notes))
                say(chap, i, attempt, notes)
                if STOP or res not in (None, 'RED'):
                    break
            if STOP:
                break
            if res in (None, 'RED'):
                skipped.append(i)
            else:
                good.append(res)
        if good:
            dst = f'{DELIVER}/season3-{chap}-narration.mp3'
            join(chap, good, dst); os.chmod(dst, 0o644)
            status = 'pilot' if chap == 'C2' and not skipped and not STOP else ('final' if not skipped and not STOP else 'partial')
            rows.append(f'season3-{chap}-narration.mp3: chapter {chap} narration, {len(good)} of {len(cs)} chunks, status {status}' + (f', SKIPPED chunks {skipped}' if skipped else ''))
        rows += notes_all
        readme(rows)
        if STOP:
            rows.append(f'stopped: {STOP[0]}'); readme(rows); break
    say('walk ends'); readme(rows)


if __name__ == '__main__':
    main()
