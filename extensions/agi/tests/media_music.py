#!/usr/bin/env python3
"""goal:g5.4.2 M6: up to THREE ~30 s Lyria music samples for the owner's ear (council 11:54Z: <= 3 short samples on their own key, no full track until he picks).
usage: media_music.py KEYFILE   (key file under ~/keys/; ONE key, google only, limit and expiry set by belam's mint)
Per sample: HARD counter (3 requests ever per run), the prompt is checked against a guard list (artist/song names, 'in the style of') and REFUSED before any send, the request is logged
BEFORE it is sent, stream:true (audio output requires it), NO retry (a failure stops the run clean: 'stopped: http'). The mp3 comes back as SSE audio deltas (base64); it must be a real mp3
of 25..35 s, else the take is flagged RED (kept out of deliver/, never silently shipped). Deliverables: deliver/music-sample-<letter>-<slug>.mp3 (644) + README-music.txt lines (c2pa manifest untouched)."""
import base64, hashlib, json, os, re, subprocess, sys, time, urllib.error, urllib.request

BASE = '/data/work/director-general-3-media/season3'
M = os.environ.get('MUSIC_DIR', BASE + '/music')
DELIVER = os.environ.get('MUSIC_DELIVER', BASE + '/deliver')
MODEL = 'google/lyria-3-clip-preview'
MAX_REQUESTS = 3
DUR_MIN, DUR_MAX = 25.0, 35.0
URL = 'https://openrouter.ai/api/v1/chat/completions'
# names the owner's goal cites as references (goal:g5.4.2 :36) and phrasings that ask for a named artist: a prompt is style descriptors only
GUARD = ['delinquent habits', 'balkan beat box', 'return of the tres', 'hermetico', 'in the style of', 'sounds like', 'in the vein of', 'covers of']
PROMPTS = [
    ('a', 'swing-flamenco', 'Instrumental, exactly 30 seconds, ending cleanly. A two-beat swing pulse with a muted trombone lead, nylon-string guitar rasgueado, palmas handclaps and a cajon, upright bass. D Phrygian, about 150 bpm. Cheeky, warm, dancing.'),
    ('b', 'balkan-brass-swing', 'Instrumental, exactly 30 seconds, ending cleanly. A brass-band shout section with clarinet and accordion, a swung groove that leans on odd-meter accents, handclaps and a big bass drum. A bright turn between minor and major. About 160 bpm. Rowdy, joyful, street-party.'),
    ('c', 'trombone-flamenco-jazz', 'Instrumental, exactly 30 seconds, ending cleanly. A slow warm theme on trombone over a flamenco compas, wood-brush drums and upright bass, nylon guitar answering. A wordless crowd shout of olé at the very end. About 110 bpm. Smoky, dignified, late evening.'),
]
now = lambda: time.strftime('%H:%M:%SZ', time.gmtime())
STOP, SENT = [], []


def say(*a):
    print(now(), *a, flush=True)


def guard(prompt):
    low = prompt.lower()
    return [g for g in GUARD if g in low]


def log(rec):
    os.makedirs(M, exist_ok=True)
    with open(f'{M}/walk-requests-music.log', 'a') as f:
        f.write(json.dumps({'t': now(), **rec}) + '\n')


def duration(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:format=format_name', '-of', 'json', path], capture_output=True, text=True)
    if r.returncode:
        return None, None
    f = json.loads(r.stdout).get('format', {})
    return float(f.get('duration', 0)), f.get('format_name', '')


def collect(lines):
    """SSE lines (bytes or str) -> (mp3 bytes, text)."""
    audio, text = [], []
    for raw in lines:
        ln = raw.decode('utf-8', 'replace') if isinstance(raw, bytes) else raw
        ln = ln.strip()
        if not ln.startswith('data:') or ln.endswith('[DONE]'):
            continue
        try:
            d = json.loads(ln[5:].strip())
        except ValueError:
            continue
        for ch in d.get('choices', []):
            dl = ch.get('delta', {})
            if dl.get('content'):
                text.append(dl['content'])
            a = dl.get('audio')
            if isinstance(a, dict) and a.get('data'):
                audio.append(a['data'])
    return base64.b64decode(''.join(audio)) if audio else b'', ''.join(text)


def sample(key, letter, slug, prompt):
    """-> ('ok'|'red'|'refused'|'stopped', note). One request at most; never a retry."""
    hit = guard(prompt)
    if hit:
        return 'refused', f'prompt names a reference ({hit}); nothing sent'
    if len(SENT) >= MAX_REQUESTS:
        return 'refused', f'request {len(SENT) + 1} would pass the hard limit of {MAX_REQUESTS}; nothing sent'
    body = {'model': MODEL, 'modalities': ['text', 'audio'], 'audio': {'format': 'mp3'}, 'stream': True, 'messages': [{'role': 'user', 'content': prompt}]}
    sent = json.dumps(body, sort_keys=True).encode()
    log({'sample': letter, 'slug': slug, 'model': MODEL, 'prompt_sha256': hashlib.sha256(prompt.encode()).hexdigest(), 'body_sha256': hashlib.sha256(sent).hexdigest(), 'n': len(SENT) + 1})
    SENT.append(letter)
    try:
        r = urllib.request.urlopen(urllib.request.Request(URL, data=sent, headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}), timeout=300)
        mp3, text = collect(r)
    except urllib.error.HTTPError as e:
        say('ERROR', letter, e.code, e.read()[:200].decode('utf-8', 'replace')); STOP.append('http'); return 'stopped', f'http {e.code}'
    except Exception as e:
        say('ERROR', letter, type(e).__name__, str(e)[:160]); STOP.append('http'); return 'stopped', type(e).__name__
    os.makedirs(M, exist_ok=True)
    raw = f'{M}/sample-{letter}.mp3'
    open(raw, 'wb').write(mp3); open(f'{M}/sample-{letter}.txt', 'w').write(text)
    dur, fmt = duration(raw)
    if not mp3 or dur is None or 'mp3' not in (fmt or '') or not (DUR_MIN <= dur <= DUR_MAX):
        return 'red', f'not a usable sample (bytes {len(mp3)}, format {fmt}, duration {dur}); kept out of deliver/'
    dst = f'{DELIVER}/music-sample-{letter}-{slug}.mp3'
    os.makedirs(DELIVER, exist_ok=True)
    open(dst, 'wb').write(mp3); os.chmod(dst, 0o644)
    return 'ok', f'{dur:.1f} s, {len(mp3)} bytes'


def main(keyfile):
    key = open(os.path.expanduser('~/keys/' + keyfile)).read().strip()
    rows = ['season 3 music samples (DRAFT, for the owner\'s ear): Lyria 3 clip (google/lyria-3-clip-preview) via OpenRouter, 30 s each, instrumental, prompts are style descriptors only (no artist or song names). The owner picks a direction; no full track exists yet. The mp3s carry the provider\'s c2pa manifest.', '']
    for letter, slug, prompt in PROMPTS:
        status, note = sample(key, letter, slug, prompt)
        say(letter, status, note)
        rows.append(f'music-sample-{letter}-{slug}.mp3: {status.upper() if status != "ok" else "ready"}: {note}. Prompt: {prompt}')
        if STOP:
            rows.append(f'stopped: {STOP[0]}'); break
    os.makedirs(DELIVER, exist_ok=True)
    open(f'{DELIVER}/README-music.txt', 'w').write('\n'.join(rows) + '\n'); os.chmod(f'{DELIVER}/README-music.txt', 0o644)
    say('music run ends')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
