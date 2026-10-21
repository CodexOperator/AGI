#!/usr/bin/env python3
"""goal:g5.4.2 M4, the animated explainer: the parts that need no manim (stdlib only, so every rule here has a test and a mutant). 0 provider spend.
  media_video.py plan CHAPTER [OUT.json]     beats + timing for one chapter (C2): the narration's tagged sentences, the mp3's silences, the placed boundaries
  media_video.py timing                      the timing report for all 18 chapters (ffmpeg silencedetect only), RED lines included
  media_video.py lint FILE...                no raw Text / Code / MarkupText / Tex ... in a scene file (council C1): engine text goes through media_vocab.Strand
  media_video.py start [PEAK_MIB]            the start test, read now (council 10-21 08:03Z); exit 0 = may start, 1 = refuse
  media_video.py queue                       the chapters still to render, from bytes (council C5)
  media_video.py joinprobe JOINED.mp4 N      is chapter N in the joined full file the ANIMATED one (frames at +30/60/120 s, PSNR vs deliver/ and deliver-static/); exit 1 unless animated
  media_video.py recheck CHAPTER             the file checks again on a rendered chapter in deliver-tmp/ (no render), rewrites its report
  media_video.py publish CHAPTER             publish a green rendered chapter waiting in deliver-tmp/ (after its keyframes were viewed)
  media_video.py render CHAPTER [--publish]  one chapter, end to end (plan -> start test -> manim under the watcher -> mux -> checks -> keyframes -> publish if green and asked)
Pieces
  beats()/place()/verify_ends()   one beat per tagged sentence; the sentence ENDS are the pauses of the mp3 (running character-rate prior, a pause within TOL
                                  of the prior wins, else the prior stands and the fallback is counted); > FALLBACK_MAX of a chapter's boundaries on the prior = RED (C2)
  strand_window()/wrap()          the engine bytes a picture shows: a window of the cited line around the needle, cut into lines that re-join to it exactly
  check_drawn()                   every string a scene drew is recorded and must be a substring of `git show SHA:PATH` lines; feed beats with 0 checked strings = RED (C1)
  schedule()                      run times snapped to whole frames, so a chapter's video is as long as its mp3, not as long as the sum of rounded animations
  start_test()/stop_reason()      anon+shmem < 3500 MiB, MemAvailable >= 3 GB, mem PSI full avg60 < 2, io PSI avg60 < 50, no gate pytest, anon+shmem+slab+peak < high-300;
                                  a read that is missing or not a number REFUSES. Stop at anon+shmem > 4200 MiB or mem PSI full avg60 > 10 (SIGTERM, never SIGSTOP)
  publish()/undo()/pending()      .tmp OUTSIDE deliver/ (sibling dir, same fs) then one rename; the static card is kept in deliver-static/; the queue reads README + checks files
"""
import ast
import bisect
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import media_fm2  # noqa: E402
import media_html  # noqa: E402

REPO = os.environ.get("MEDIA_REPO") or str(Path(__file__).resolve().parents[3])      # the checkout that holds this file (or MEDIA_REPO): engine bytes are read with `git show` from here
SCRIPT = REPO + "/.agi/context/media/season3-explainer-script.md"
BASE = "/data/work/director-general-3-media/season3"
FPS = 25
PROFILE = {"codec_name": "h264", "width": 1280, "height": 720, "r_frame_rate": "25/1", "pix_fmt": "yuv420p", "a_codec": "aac", "sample_rate": "44100", "channels": 1}
TOL = 0.7                    # a picked pause is kept when its sentence is within this (or REL of its length, if more) of its character-proportional speech time
REL = 0.12                   # DEVIATION 5 from the approved design (a flat 0.7 s): 12 % of a sentence's expected speech time loosens every sentence over 5.8 s of speech (council 10-21 09:52Z)
FALLBACK_MAX = 0.25          # council C2: more than this share of a chapter's boundaries on the prior = RED
MIN_SCALE = 0.55             # a strand scaled below this of its font is too small to read at 720p
DUR_TOL = 0.2                # the video is as long as the mp3, within this
ORDER = [2, 0, 1] + list(range(3, 18))     # the pilot first, then C0, C1, C3..C17
SIL_RE = re.compile(r"silence_(start|end): (-?[0-9.]+)")


# ---- beats
def beats(chap, repo=REPO):
    """One beat per tagged sentence of a chapter's `### narration`: {i, para, tag, spoken, pairs [pair dict], kind feed|calm}. `spoken` is what the voice read (slots spoken)."""
    out = []
    for pi, para in enumerate(chap["narration"]):
        parts = media_fm2.TAG.split(para)
        for k in range(0, len(parts), 2):
            seg = parts[k].strip()
            tag = parts[k + 1] if k + 1 < len(parts) else "image"
            if not seg:
                continue
            ids = [] if tag == "image" else tag.split(",")
            pairs = [dict(chap["pairs"][p], id=p) for p in ids]
            out.append({"i": len(out), "para": pi, "tag": tag, "spoken": media_fm2.render(seg, repo, chap["sha"]), "pairs": pairs, "kind": "feed" if pairs else "calm"})
    return out


# ---- timing
def parse_silence(text):
    """ffmpeg silencedetect stderr -> [(start, end)]; an unclosed trailing start is dropped."""
    out, st = [], None
    for kind, v in SIL_RE.findall(text):
        if kind == "start":
            st = float(v)
        elif st is not None:
            out.append((st, float(v))); st = None
    return out


def silences(mp3, noise="-35dB", dur=0.25):
    r = subprocess.run(["nice", "-n", "10", "ffmpeg", "-nostats", "-hide_banner", "-i", mp3, "-af", f"silencedetect=noise={noise}:d={dur}", "-f", "null", "-"],
                       capture_output=True, text=True, check=True)
    return parse_silence(r.stderr)


def mp3_seconds(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


class Silence:
    """Silence arithmetic over the mp3's pauses: net(t0, t1) = the seconds of speech between two times (the pauses taken out)."""
    def __init__(self, pauses):
        self.p = sorted(pauses)
        self.cum, c = [], 0.0
        for a, b in self.p:
            self.cum.append(c); c += b - a
        self.total = c

    def upto(self, t):
        """silence seconds in [0, t]"""
        i = bisect.bisect_right([a for a, _ in self.p], t) - 1
        if i < 0:
            return 0.0
        a, b = self.p[i]
        return self.cum[i] + min(max(t - a, 0.0), b - a)

    def net(self, t0, t1):
        return (t1 - t0) - (self.upto(t1) - self.upto(t0))


def place(lens, duration, pauses, tol=TOL, rel=REL, reward=0.3):
    """The END time of each sentence, by one global assignment (measured 10-21: the nearest-pause rule on a running prior left 16 of 18 chapters on the prior, because a sentence's
    speaking time is not its character count to within 0.7 s; a global fit does not drift). lens = characters spoken per sentence.
    The chapter's speech rate r = characters / seconds of speech. DP over the pauses picks S-1 of them in order, minimising for each sentence (speech seconds between its two
    pauses - len/r)^2 / (len/r + 1), less `reward` x the pause's length (a sentence end is a long pause).
    A picked pause is KEPT ('pause') when the sentence it closes is within max(tol, rel x its expected speech time) of len/r; else that end stands on the prior ('prior': the previous end + len/r
    + the silence it spans), is COUNTED, and the chapter is RED over FALLBACK_MAX of its boundaries (council C2). -> {ends, kind, prior, dev, fallback, boundaries, rate}"""
    n, sil = len(lens), Silence(pauses)
    if n < 2 or len(pauses) < n - 1:
        ends = [duration * sum(lens[:k + 1]) / max(sum(lens), 1) for k in range(n)]
        return {"ends": ends[:-1] + [duration] if n else [], "kind": ["prior"] * (n - 1) + ["end"] if n else [], "prior": ends, "dev": [0.0] * n, "fallback": max(n - 1, 0),
                "boundaries": max(n - 1, 0), "rate": 0.0}
    r = sum(lens) / max(duration - sil.total, 1.0)
    P = len(sil.p)
    mids = [(a + b) / 2 for a, b in sil.p]
    inf = float("inf")

    def seg(k, left, right):
        exp = lens[k] / r
        got = sil.net(left, right)
        return (got - exp) ** 2 / (exp + 1), got - exp

    f = [[inf] * P for _ in range(n - 1)]
    back = [[None] * P for _ in range(n - 1)]
    for i in range(P):
        f[0][i] = seg(0, 0.0, sil.p[i][0])[0] - reward * min(sil.p[i][1] - sil.p[i][0], 1.0)
    for k in range(1, n - 1):
        for i in range(k, P):
            for j in range(k - 1, i):
                if f[k - 1][j] == inf:
                    continue
                c = f[k - 1][j] + seg(k, sil.p[j][1], sil.p[i][0])[0] - reward * min(sil.p[i][1] - sil.p[i][0], 1.0)
                if c < f[k][i]:
                    f[k][i], back[k][i] = c, j
    best, bi = inf, None
    for i in range(n - 2, P):
        if f[n - 2][i] < inf:
            c = f[n - 2][i] + seg(n - 1, sil.p[i][1], duration)[0]
            if c < best:
                best, bi = c, i
    idx = [bi]
    for k in range(n - 2, 0, -1):
        idx.append(back[k][idx[-1]])
    idx.reverse()
    ends, kinds, priors, devs, prev = [], [], [], [], 0.0
    for k, i in enumerate(idx):
        left = 0.0 if k == 0 else sil.p[idx[k - 1]][1]
        _, dev = seg(k, left, sil.p[i][0])
        exp = lens[k] / r
        prior = prev + exp + (sil.upto(mids[i]) - sil.upto(prev))
        nxt = mids[idx[k + 1]] if k + 1 < len(idx) else duration
        if abs(dev) <= max(tol, rel * exp):
            e, kd = mids[i], "pause"
        else:
            e, kd = min(prior, nxt - 0.2), "prior"
            prior = e
        if e <= prev:
            e = prev + 0.2
            if kd == "prior":
                prior = e
        ends.append(e); kinds.append(kd); priors.append(prior); devs.append(round(dev, 3)); prev = e
    ends.append(duration); kinds.append("end"); priors.append(duration); devs.append(0.0)
    return {"ends": ends, "kind": kinds, "prior": priors, "dev": devs, "fallback": kinds.count("prior"), "boundaries": n - 1, "rate": r}


def place_greedy(lens, duration, pauses, tol=TOL):
    """The approved design's rule, kept only to be counted beside the DP (council 10-21): a running character-rate prior, the longest pause within `tol` of it wins, else the prior.
    -> the number of boundaries left on the prior."""
    n = len(lens)
    total = max(sum(lens), 1)
    t, done, fb = 0.0, 0, 0
    mids = [((a + b) / 2, b - a) for a, b in pauses]
    for k in range(n - 1):
        rate = done / t if done >= 200 and t > 0 else total / duration
        prior = min(t + lens[k] / rate, duration - 0.25 * (n - 1 - k))
        cands = [(m, d) for m, d in mids if m > t + 0.2 and abs(m - prior) <= tol]
        if cands:
            t = max(cands, key=lambda c: (round(c[1], 2), -abs(c[0] - prior)))[0]
        else:
            fb += 1; t = max(prior, t + 0.2)
        done += lens[k]
    return fb


def timing_counts(lens, duration, pauses):
    """The three numbers the README carries per chapter (council 10-21 09:52Z, deviation 5): boundaries on the prior under the DP with REL 0.12, under the DP with the approved 0.7 s alone
    (rel = 0), and under the approved greedy rule."""
    return {"dp_rel": place(lens, duration, pauses)["fallback"], "dp_tol_only": place(lens, duration, pauses, rel=0.0)["fallback"], "greedy": place_greedy(lens, duration, pauses)}


def timing_findings(pl, max_frac=FALLBACK_MAX):
    """-> [finding]; [] = green. RED: a chapter with more than max_frac of its boundaries on the prior (C2)."""
    out = []
    if pl["boundaries"] and pl["fallback"] / pl["boundaries"] > max_frac:
        out.append(f"fallback {pl['fallback']} of {pl['boundaries']} boundaries on the prior ({pl['fallback'] / pl['boundaries']:.0%} > {max_frac:.0%})")
    return out


def verify_ends(pl, pauses, duration, lens, tol=TOL, rel=REL):
    """A CONSISTENCY re-check, not an independent one (it derives the same rate with the same TOL and REL as place()): the placed ends against the mp3's own pauses and the sentences' lengths (not trusted from place()): increasing; each 'pause' end IS a pause middle and the sentence it
    closes is within max(tol, rel x expected) of its character-proportional speech time (checked where the end before it is a pause too: after a 'prior' end its left edge is not a pause); each 'prior' end IS the prior stored for
    it; the last is the mp3's length; the stored fallback count is the real one. -> [finding]"""
    out, sil = [], Silence(pauses)
    mids = [(a + b) / 2 for a, b in pauses]
    ends, kinds, priors = pl["ends"], pl["kind"], pl["prior"]
    if not (len(ends) == len(kinds) == len(priors) == len(lens)):
        return ["ends/kind/prior/sentences differ in length"]
    r = sum(lens) / max(duration - sil.total, 1.0)
    prev = 0.0
    for k, (e, kd, pr) in enumerate(zip(ends, kinds, priors)):
        if e <= prev:
            out.append(f"end {k} ({e:.2f}) is not after the one before ({prev:.2f})")
        if kd == "pause":
            exp = lens[k] / r
            if not any(abs(e - m) < 0.01 for m in mids):
                out.append(f"end {k} ({e:.2f}) is not the middle of a pause")
            elif k > 0 and kinds[k - 1] == "pause" and abs(sil.net(prev, e) - exp) > max(tol, rel * exp) + 0.05:
                out.append(f"end {k} ({e:.2f}): {sil.net(prev, e):.1f} s of speech for {exp:.1f} s expected")
        elif kd == "prior" and abs(e - pr) > 0.01:
            out.append(f"end {k} ({e:.2f}) claims the prior ({pr:.2f})")
        elif kd == "end" and (k != len(ends) - 1 or abs(e - duration) > 0.01):
            out.append(f"end {k} is not the mp3's length")
        elif kd not in ("pause", "prior", "end"):
            out.append(f"end {k}: unknown kind {kd!r}")
        prev = e
    if kinds and kinds[-1] != "end":
        out.append("the last end is not the mp3's length")
    if kinds.count("prior") != pl["fallback"]:
        out.append(f"fallback {pl['fallback']} but {kinds.count('prior')} ends are on the prior")
    return out


def prior_offsets(plan):
    """Council 10-21 09:52Z (c): for each prior-placed end, |end - the nearest pause of the mp3| (to the pause's nearest edge: inside it is 0) and the SHORTER neighbouring sentence's
    expected speech length in seconds (characters / the chapter's speech rate). A named exception holds iff every offset is under that length: the end can then not have crossed a sentence.
    -> [{k, end, offset, shorter_s, ok}]"""
    bs, r = plan["beats"], plan["rate"]
    out = []
    for k, kd in enumerate(plan["kind"]):
        if kd != "prior":
            continue
        e = plan["ends"][k]
        off = min((0.0 if a <= e <= b else min(abs(e - a), abs(e - b)) for a, b in plan["pauses"]), default=float("inf"))
        sh = min(len(bs[k]["spoken"]), len(bs[k + 1]["spoken"])) / r
        out.append({"k": k, "end": round(e, 2), "offset": round(off, 2), "shorter_s": round(sh, 2), "ok": off < sh})
    return out


def chapter_plan(chap, mp3, repo=REPO, pauses=None, duration=None):
    """The whole plan of one chapter: beats with t0/t1, the timing report, nothing drawn yet (the strand bytes are read at draw time)."""
    bs = beats(chap, repo)
    duration = mp3_seconds(mp3) if duration is None else duration
    pauses = silences(mp3) if pauses is None else pauses
    pl = place([len(b["spoken"]) for b in bs], duration, pauses)
    t0 = 0.0
    for b, e, kd in zip(bs, pl["ends"], pl["kind"]):
        b["t0"], b["t1"], b["timing"] = round(t0, 3), round(e, 3), kd
        t0 = e
    return {"chapter": chap["id"], "n": chap["n"], "title": chap["title"], "sha": chap["sha"], "mp3": mp3, "duration": duration, "beats": bs, "pauses": pauses,
            "counts": timing_counts([len(b["spoken"]) for b in bs], duration, pauses),
            "ends": pl["ends"], "kind": pl["kind"], "prior": pl["prior"], "dev": pl["dev"], "rate": pl["rate"], "fallback": pl["fallback"], "boundaries": pl["boundaries"]}


# ---- frames: whole-frame run times
def schedule(t0, t1, parts, fps=FPS):
    """A beat from t0 to t1 -> [frames per part, wait frames]: `parts` = wanted seconds per animation, scaled down together if they do not fit; the wait takes the rest, so the
    beat is EXACTLY round((t1-t0)*fps) frames and the chapter never drifts from its mp3. Every part is at least one frame; a beat shorter than its parts is cut to fit."""
    total = max(round(t1 * fps) - round(t0 * fps), 1)
    want = [max(1, round(p * fps)) for p in parts]
    s = sum(want)
    if s > total:
        f = total / s
        want = [max(1, int(w * f)) for w in want]
        while sum(want) > total and any(w > 1 for w in want):
            want[want.index(max(want))] -= 1
    rest = total - sum(want)
    return want, max(rest, 0)


def pair_chunks(pairs, size=2):
    """A beat's pairs in groups of at most `size`: the scene shows one group at a time (a stack of four strands would be drawn too small to read), so EVERY pair is drawn (C3 beat 29 cites four)."""
    return [pairs[i:i + size] for i in range(0, len(pairs), size)] or [[]]


def chunk_times(t0, t1, k):
    """k equal slices of a beat as [(c0, c1)]; consecutive, first c0 = t0, last c1 = t1 (schedule() then gives each slice whole frames that add up to the beat)."""
    return [(t0 + (t1 - t0) * i / k, t0 + (t1 - t0) * (i + 1) / k) for i in range(k)]


# ---- the engine bytes a picture shows
DELIM = re.compile(r"[ \t;|&(){}\[\]\"'`,=<>/:$]")


def strand_window(repo, sha, path, lo, hi, needle, ctx=34):
    """-> (window, i0, i1): the needle with up to `ctx` characters each side, never past the ends of its line(s) in L<lo>-L<hi> at the sha; window[i0:i1] == needle.
    Where the window is cut inside a line (not at its end), the cut is moved inward to the nearest delimiter (a space, `;`, `|`, a quote, ...) so a window never opens or ends in the
    middle of a word. A needle that is not in the range is a ValueError (the pair check of the script already forbids it)."""
    text = media_html.lines_at(repo, sha, path, lo, hi)
    i = text.find(needle)
    if i < 0:
        raise ValueError(f"needle not at {sha}:{path}:L{lo}-L{hi}")
    ls = text.rfind("\n", 0, i) + 1
    a = max(ls, i - ctx)
    j = i + len(needle)
    nl = text.find("\n", j)
    le = len(text) if nl < 0 else nl
    b = min(le, j + ctx)
    if a > ls:
        m = DELIM.search(text, a, i)
        a = m.end() if m else i
    if b < le:
        k = max((m.start() for m in DELIM.finditer(text, j, b + 1)), default=-1)
        b = k if k >= 0 else j
    return text[a:b], i - a, i - a + len(needle)


WORD = re.compile(r"[A-Za-z0-9_.]")


def can_break(part, e):
    """A line may end before part[e] unless that cuts a word: both characters around the cut are [A-Za-z0-9_.] (council 10-21 09:52Z: `AGI_PIECE_GLO` / `B=engine.md` was a bug)."""
    return not (WORD.match(part[e - 1]) and WORD.match(part[e]))


def token_findings(rows):
    """rows = the drawn lines, each a string; -> [finding] for every line that ends inside a [A-Za-z0-9_.] run that continues on the next line."""
    return [f"line {k} ends inside a word: {a[-12:]!r} | {b[:12]!r}" for k, (a, b) in enumerate(zip(rows, rows[1:])) if a and b and WORD.match(a[-1]) and WORD.match(b[0])]


def wrap(window, i0, i1, width=44):
    """The window as lines of spans [(text, is_needle)]. Cut at the last legal break (can_break) at or before `width` columns, every character kept: the spans re-join to the window
    exactly; a hard newline of the window is kept as a ("\n", False) span at the end of its line, and is not drawn."""
    lines, pos = [], 0
    parts = window.split("\n")
    for pi, part in enumerate(parts):
        s = 0
        while True:
            if len(part) - s <= width:
                end = len(part)
            else:
                end = next((e for e in range(s + width, s, -1) if can_break(part, e)), None)
                if end is None:        # one token longer than the line: the line runs long to the token's end, and the strand is drawn in a smaller font (media_vocab scales it)
                    end = next((e for e in range(s + width + 1, len(part)) if can_break(part, e)), len(part))
            spans, a = [], s
            for cut in sorted({c for c in (i0 - pos, i1 - pos) if s < c < end}):
                spans.append((part[a:cut], a + pos >= i0 and a + pos < i1)); a = cut
            spans.append((part[a:end], a + pos >= i0 and a + pos < i1))
            lines.append([sp_ for sp_ in spans if sp_[0]])
            s = end
            if s >= len(part):
                break
        if pi < len(parts) - 1:
            lines[-1].append(("\n", False))      # a hard line end of the window itself, kept so the spans re-join to it exactly
        pos += len(part) + 1
    return lines


def rejoin(lines):
    return "".join(t for ln in lines for t, _ in ln)


# ---- C1: every drawn engine string is a substring of the engine
def check_drawn(drawn, plan, repo=REPO):
    """drawn = [{'kind': 'strand', 'beat', 'sha', 'path', 'lo', 'hi', 'text'} | {'kind': 'cite', 'beat', 'sha', 'path', 'lo', 'hi'}], written by media_vocab as it draws.
    -> [finding]. strand: `text` is a substring of the lines Lx-Ly of PATH at SHA, read here again from git. cite: the file and the lines exist. A feed beat that drew fewer
    strands than it has pairs is a finding; a chapter with feed beats and 0 checked strings is RED."""
    out, checked, by_beat = [], 0, {}
    for d in drawn:
        if d.get("kind") == "layout":
            if d.get("scale", 1.0) < MIN_SCALE:
                out.append(f"beat {d.get('beat')}: the strand stack was shrunk to {d['scale']:.2f} to clear the sentence (< {MIN_SCALE})")
            continue
        try:
            txt = media_html.lines_at(repo, d["sha"], d["path"], d["lo"], d["hi"])
        except (ValueError, KeyError) as e:
            out.append(f"beat {d.get('beat')}: {d.get('path')} unreadable ({e})"); continue
        if d["kind"] == "strand":
            checked += 1
            by_beat[d["beat"]] = by_beat.get(d["beat"], 0) + 1
            if "rows" in d:
                if "".join(d["rows"]) != d.get("text", "").replace("\n", ""):
                    out.append(f"beat {d.get('beat')}: the drawn lines do not re-join to the recorded text")
                out += [f"beat {d.get('beat')}: {f}" for f in token_findings(d["rows"])]
                if d.get("scale", 1.0) < MIN_SCALE:
                    out.append(f"beat {d.get('beat')}: strand drawn at {d['scale']:.2f} of its font (< {MIN_SCALE})")
            if not d.get("text") or d["text"] not in txt:
                out.append(f"beat {d.get('beat')}: drawn {d.get('text', '')[:50]!r} is not in {d['path']}:L{d['lo']}-L{d['hi']} at {d['sha']}")
        elif d["kind"] == "cite":
            if not txt.strip():
                out.append(f"beat {d.get('beat')}: cite {d['path']} has no text at L{d['lo']}-L{d['hi']}")
        else:
            out.append(f"beat {d.get('beat')}: unknown drawn kind {d['kind']!r}")
    feed = [b for b in plan["beats"] if b["kind"] == "feed"]
    if feed and checked == 0:
        out.append(f"RED: {len(feed)} feed beats and 0 checked strings")
    for b in feed:
        if by_beat.get(b["i"], 0) < len(b["pairs"]):
            out.append(f"beat {b['i']}: {len(b['pairs'])} pairs but {by_beat.get(b['i'], 0)} strands drawn")
    return out


# ---- C1: a lint on the scene files
RAW = {"Text", "Code", "MarkupText", "Tex", "MathTex", "Paragraph", "Title", "BulletedList", "DecimalNumber", "Integer", "Variable", "SingleStringMathTex"}


def lint_source(src, name="<scene>"):
    """-> [finding] for every call of a raw text mobject, and every import of one under another name. Only media_vocab.py may draw text."""
    out = []
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            nm = f.id if isinstance(f, ast.Name) else f.attr if isinstance(f, ast.Attribute) else None
            if nm in RAW:
                out.append(f"{name}:{node.lineno}: raw {nm}( ) outside media_vocab.py")
        elif isinstance(node, ast.ImportFrom):
            for a in node.names:
                if a.name in RAW and a.asname:
                    out.append(f"{name}:{node.lineno}: {a.name} imported as {a.asname}")
    return out


def lint(paths):
    out = []
    for p in paths:
        if Path(p).name == "media_vocab.py":
            continue
        out += lint_source(Path(p).read_text(encoding="utf-8"), Path(p).name)
    return out


# ---- the file checks
def probe(mp4):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels:format=duration", "-of", "json", mp4],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next((s for s in j["streams"] if s["codec_type"] == "video"), {})
    a = next((s for s in j["streams"] if s["codec_type"] == "audio"), {})
    return {"codec_name": v.get("codec_name"), "width": v.get("width"), "height": v.get("height"), "r_frame_rate": v.get("r_frame_rate"), "pix_fmt": v.get("pix_fmt"),
            "a_codec": a.get("codec_name"), "sample_rate": a.get("sample_rate"), "channels": a.get("channels"), "duration": float(j["format"]["duration"])}


def profile_findings(info, profile=PROFILE):
    return [f"{k}: {info.get(k)!r} != {v!r}" for k, v in profile.items() if info.get(k) != v]


def duration_findings(video_s, audio_s, tol=DUR_TOL):
    return [] if abs(video_s - audio_s) <= tol else [f"video {video_s:.2f} s vs mp3 {audio_s:.2f} s (> {tol} s apart)"]


def frame_findings(frames, kinds, min_ink=0.004, min_diff=0.4):
    """frames = [bytes of one small grey frame per beat (taken mid-beat)]; kinds = 'feed'|'calm' per beat. A frame is BLANK when under `min_ink` of its pixels differ from its most common
    value by more than 8; a FEED beat's frame must differ from the beat before it (mean absolute difference >= min_diff; calibrated twice on measured beats, 10-21: the same picture 0.00-0.18; beats that differ by a caption and one graph node 0.60-1.79 (C2 pilot 1.49-1.79; C7's two-second beats 0.60 and 0.80, where the caption is one short line). Line 0.4). -> [finding]"""
    out = []
    for i, f in enumerate(frames):
        if not f:
            out.append(f"beat {i}: no frame"); continue
        mode = Counter(f).most_common(1)[0][0]
        ink = sum(1 for p in f if abs(p - mode) > 8) / len(f)
        if ink < min_ink:
            out.append(f"beat {i}: blank frame (ink {ink:.4f})")
        if i and kinds[i] == "feed" and frames[i - 1] and len(frames[i - 1]) == len(f):
            d = sum(abs(a - b) for a, b in zip(f, frames[i - 1])) / len(f)
            if d < min_diff:
                out.append(f"beat {i}: frame does not differ from the beat before (mean diff {d:.2f})")
    return out


def grab_frames(mp4, times, w=64, h=36):
    out = []
    for t in times:
        r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", "-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True)
        out.append(r.stdout)
    return out


# ---- the start test (council 10-21 08:03Z); every path is a parameter so a test can hand it files
SLICE = "/sys/fs/cgroup/agi.slice"
MIB = 1048576


def _num(path, key=None):
    """A number from a file: the whole file, or the value after `key` on its own line. Anything else raises (the caller refuses)."""
    txt = open(path, encoding="utf-8").read()
    if key is None:
        return float(txt.strip())
    for ln in txt.split("\n"):
        p = ln.split()
        if p and p[0] == key:
            return float(p[1])
    raise ValueError(f"{key} not in {path}")


def _psi(path, which, field="avg60"):
    for ln in open(path, encoding="utf-8").read().split("\n"):
        if ln.startswith(which + " "):
            return float(dict(x.split("=") for x in ln.split()[1:])[field])
    raise ValueError(f"{which} not in {path}")


def gate_running(proc="/proc"):
    """A gate pytest: a process whose comm is pytest/python/python3 and whose cwd has a `gate` path component. By comm + cwd, never argv. An unreadable cwd is skipped
    (not ours); /proc itself unlistable raises."""
    for pid in (p for p in os.listdir(proc) if p.isdigit()):
        try:
            comm = open(f"{proc}/{pid}/comm").read().strip()
            if comm in ("pytest", "python", "python3") and "gate" in Path(os.readlink(f"{proc}/{pid}/cwd")).parts:
                return True
        except OSError:
            continue
    return False


def start_test(peak_mib=1500, slice_dir=SLICE, meminfo="/proc/meminfo", psi_dir="/proc/pressure", proc="/proc"):
    """-> (ok, [one line per read]). Every threshold is read in this one call; a read that is missing, unreadable or not a number REFUSES (fail closed)."""
    lines, ok = [], True

    def rd(name, fn, test, fmt):
        nonlocal ok
        try:
            v = fn()
            good = bool(test(v))
            lines.append(f"{'ok ' if good else 'NO '} {name} {fmt(v)}")
            ok = ok and good
        except (OSError, ValueError, KeyError, IndexError) as e:
            lines.append(f"NO  {name} unreadable ({type(e).__name__}): refused")
            ok = False
        else:
            pass

    stat = f"{slice_dir}/memory.stat"
    rd("anon+shmem", lambda: (_num(stat, "anon") + _num(stat, "shmem")) / MIB, lambda v: math.isfinite(v) and v < 3500, lambda v: f"{v:.0f} MiB (< 3500)")
    rd("MemAvailable", lambda: _num(meminfo, "MemAvailable:") / 1024 / 1024, lambda v: v >= 3.0, lambda v: f"{v:.2f} GB (>= 3)")
    rd("mem PSI full avg60", lambda: _psi(f"{psi_dir}/memory", "full"), lambda v: v < 2, lambda v: f"{v} (< 2)")
    rd("io PSI some avg60", lambda: _psi(f"{psi_dir}/io", "some"), lambda v: v < 50, lambda v: f"{v} (< 50)")
    rd("gate pytest", lambda: gate_running(proc), lambda v: v is False, lambda v: "running" if v else "none")
    rd("headroom", lambda: (_num(stat, "anon") + _num(stat, "shmem") + _num(stat, "slab_unreclaimable")) / MIB + peak_mib, lambda v: v < _num(f"{slice_dir}/memory.high") / MIB - 300,
       lambda v: f"anon+shmem+slab+peak {v:.0f} MiB < memory.high-300")
    return ok, lines


def stop_reason(slice_dir=SLICE, psi_dir="/proc/pressure"):
    """-> None to carry on, or the reason to SIGTERM the render: anon+shmem > 4200 MiB or mem PSI full avg60 > 10. Unreadable raises (the watcher counts three in a row as a stop)."""
    stat = f"{slice_dir}/memory.stat"
    a = (_num(stat, "anon") + _num(stat, "shmem")) / MIB
    p = _psi(f"{psi_dir}/memory", "full")
    if a > 4200:
        return f"anon+shmem {a:.0f} MiB > 4200"
    if p > 10:
        return f"mem PSI full avg60 {p} > 10"
    return None


class Watcher:
    """Runs ONE render and watches it every `poll` seconds. spawn() -> an object with poll()/send_signal()/wait(); read() -> stop_reason(). A stop (or three unreadable
    reads in a row) sends SIGTERM and the chapter is re-queued; the SECOND stop of a chapter is 'stopped: memory' (council A2): no third try."""
    def __init__(self, spawn, read, sleep, term, poll=10):
        self.spawn, self.read, self.sleep, self.term, self.poll = spawn, read, sleep, term, poll

    def run(self, tries=2):
        stops = 0
        for _ in range(tries):
            p, bad, why = self.spawn(), 0, None
            while p.poll() is None:
                self.sleep(self.poll)
                try:
                    why, bad = self.read(), 0
                except (OSError, ValueError, KeyError):
                    bad += 1
                    why = "three unreadable reads in a row" if bad >= 3 else None
                if why:
                    self.term(p)
                    p.wait()
                    stops += 1
                    break
            else:
                return ("ok" if p.returncode == 0 else f"failed: exit {p.returncode}"), stops
            if stops >= tries:
                return "stopped: memory", stops
        return "stopped: memory", stops


# ---- README, the queue, the swap
def readme_row(name, chap, version):
    return f"{name}: chapter {chap}, {version}"


ANIMATED = re.compile(r"^(explainer-ch\d\d-[a-z0-9-]+\.mp4): chapter C(\d+), animated version\b")


def animated_rows(readme_text):
    """{chapter number: mp4 name} for rows that SAY animated version. The static row's 'the animated render is pending' is not one."""
    return {int(m.group(2)): m.group(1) for ln in readme_text.split("\n") if (m := ANIMATED.match(ln))}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def checks_green(checks_file, mp4):
    """Done means the checks file for this chapter exists, says green, and was made for THIS mp4's bytes."""
    try:
        j = json.load(open(checks_file))
        return j.get("green") is True and j.get("sha256") == sha256(mp4)
    except (OSError, ValueError, KeyError):
        return False


def pending(deliver, checks_dir, order=ORDER, only_pilot=False):
    """Chapters still to render, in ORDER, from bytes only (council C5): done = README says 'animated version' for the chapter AND its checks file is green for the mp4 in deliver/."""
    try:
        rows = animated_rows(open(f"{deliver}/README-narration.txt", encoding="utf-8").read())
    except OSError:
        rows = {}
    out = []
    for n in order:
        name = rows.get(n)
        if name and os.path.exists(f"{deliver}/{name}") and checks_green(f"{checks_dir}/ch{n:02d}.json", f"{deliver}/{name}"):
            continue
        out.append(n)
    return out


GAP_LINE = "while a chapter is replaced, the joined full file can lack that chapter for one watcher pass (~30 min; the watcher takes a replaced file one pass after its size changed); the per-chapter files are always complete."
LIMIT_LINE = "timing check cannot see a single dropped or swapped sentence (the DP re-fits around it, measured 10-21); the keyframe view is the check for that."


def ensure_readme_line(readme_path, line, index):
    """`line` once, at `index` of the README (after the head). Idempotent."""
    lines = open(readme_path, encoding="utf-8").read().split("\n")
    if line not in lines:
        lines.insert(index, line)
        tmp = readme_path + ".new"
        open(tmp, "w", encoding="utf-8").write("\n".join(lines))
        os.replace(tmp, readme_path)


def ensure_readme_limit(readme_path):
    """The documented limit of the timing check (council 10-21 11:08Z, R-fine) as the README's second line, and the one-pass gap of the joined file (11:37Z) as the third. Idempotent."""
    ensure_readme_line(readme_path, LIMIT_LINE, 1)
    ensure_readme_line(readme_path, GAP_LINE, 2)


def set_readme_row(readme_path, name, chap, version, extra=""):
    """Rewrite the one row of this mp4; the chunk lines under it stay. Raises if the row is not there."""
    lines = open(readme_path, encoding="utf-8").read().split("\n")
    hit = [i for i, ln in enumerate(lines) if ln.startswith(name + ":")]
    if len(hit) != 1:
        raise ValueError(f"README has {len(hit)} rows for {name}")
    lines[hit[0]] = readme_row(name, chap, version) + (f"; {extra}" if extra else "")
    tmp = readme_path + ".new"
    open(tmp, "w", encoding="utf-8").write("\n".join(lines))
    os.replace(tmp, readme_path)


def publish(tmp_mp4, name, deliver, static_dir, tmp_dir, checks_file, green, info):
    """Council C3 + C4 + the checks after (10-21 09:52Z). tmp_mp4 must lie in `tmp_dir` (a sibling of deliver/ on the same filesystem, never inside it). Only a GREEN chapter moves: the
    static card is kept in static_dir (a hard link, so deliver/<name> never disappears for the watcher), the checks file is written for the new bytes, then ONE os.replace puts the
    animated file in. AFTER: static_dir/<name> must hash to the static card's sha256 from before the publish and must not be the inode of deliver/<name>; if not, the static card is put
    back and ValueError is raised (RED). undo() is one rename back. -> the new sha256."""
    if os.path.dirname(os.path.abspath(tmp_mp4)) != os.path.abspath(tmp_dir) or os.path.abspath(tmp_dir) == os.path.abspath(deliver):
        raise ValueError("the .tmp must be written OUTSIDE deliver/, in the sibling tmp dir")
    if os.stat(tmp_dir).st_dev != os.stat(deliver).st_dev:
        raise ValueError("tmp dir and deliver/ are on different filesystems: the rename would not be atomic")
    digest = sha256(tmp_mp4)
    json.dump(dict(info, green=bool(green), sha256=digest), open(checks_file, "w"), indent=1)
    if not green:
        return None
    os.makedirs(static_dir, exist_ok=True)
    dst, keep = f"{deliver}/{name}", f"{static_dir}/{name}"
    if os.path.exists(dst) and not os.path.exists(keep):
        os.link(dst, keep)
    pre = sha256(keep) if os.path.exists(keep) else None
    os.chmod(tmp_mp4, 0o644)
    os.replace(tmp_mp4, dst)
    if pre is not None and (sha256(keep) != pre or os.stat(keep).st_ino == os.stat(dst).st_ino):
        os.replace(keep, dst)
        raise ValueError(f"publish check failed for {name}: the kept static card is not the card from before, or is the same file as deliver/; the static card was put back")
    return digest


def deliver_total(deliver):
    """The seconds the re-joined full mp4 must equal (+-0.5 s): the sum of the explainer-chNN-*.mp4 files in deliver/ (council 10-21 09:52Z; never the old C2, never both)."""
    return sum(probe(f"{deliver}/{f}")["duration"] for f in sorted(os.listdir(deliver)) if re.match(r"explainer-ch\d\d-.*\.mp4$", f))


def joined_findings(joined_s, deliver, tol=0.5):
    want = deliver_total(deliver)
    return [] if abs(joined_s - want) <= tol else [f"re-joined full mp4 is {joined_s:.1f} s, the {len(os.listdir(deliver))}-file deliver/ sums to {want:.1f} s (> {tol} s apart)"]


def undo(name, deliver, static_dir):
    """One rename: the static card back over the animated file."""
    os.replace(f"{static_dir}/{name}", f"{deliver}/{name}")


# ---- one chapter, end to end
import resource  # noqa: E402
import signal  # noqa: E402
import threading  # noqa: E402
import time  # noqa: E402

VMLIMIT_KB = 2500000        # ulimit -v for a render: 1.6 x the pilot's VmPeak (council 10-21 09:52Z). A chapter that dies at it: stop and ask, never raise it
EXCEPTIONS = {6: "council ruling 09:52Z 10-21"}   # a NAMED timing exception: > 25 % on the prior is accepted iff every prior-placed end is nearer a pause than the shorter neighbouring sentence is long (prior_offsets)
BANKED = {6: "BANKED FAULT (council 14:10Z 10-21, no STT): beat 28 'So here we are.' is on screen 0.28 s (183.59-183.87 s) for about 1 s of speech, so that caption comes up ~0.7 s early, once; the next sentence then holds 6.5 s for ~4 s of speech"}
QUEUE = os.path.dirname(BASE) + "/RENDERING"       # SM's gates wait while it exists (15 s poll): touched BEFORE a chapter's start test, removed after the chapter
HOLD = os.path.dirname(BASE) + "/HOLD-GATES"        # touched when a chapter has waited an hour on the start test; removed by me when the 17 are done or at a stop-and-ask


def tree_peaks(pgid, proc="/proc"):
    """(VmPeak kB, VmHWM kB) summed-max over the processes of one process group right now: the render and the ffmpeg it starts."""
    vp = hw = 0
    for pid in (p for p in os.listdir(proc) if p.isdigit()):
        try:
            if os.getpgid(int(pid)) != pgid:
                continue
            st = dict(ln.split(":", 1) for ln in open(f"{proc}/{pid}/status").read().split("\n") if ":" in ln)
            vp = max(vp, int(st.get("VmPeak", "0 kB").split()[0])); hw = max(hw, int(st.get("VmHWM", "0 kB").split()[0]))
        except (OSError, ValueError, ProcessLookupError):
            continue
    return vp, hw


class Sampler(threading.Thread):
    """Reads the render's VmPeak and VmHWM once a second until stop(): the figures the pilot reports (and the next ulimit -v is set from)."""
    def __init__(self, pgid, proc="/proc"):
        super().__init__(daemon=True)
        self.pgid, self.proc, self.vmpeak, self.vmhwm, self._halt = pgid, proc, 0, 0, threading.Event()

    def run(self):
        while not self._halt.is_set():
            a, b = tree_peaks(self.pgid, self.proc)
            self.vmpeak, self.vmhwm = max(self.vmpeak, a), max(self.vmhwm, b)
            self._halt.wait(1.0)

    def stop(self):
        self._halt.set(); self.join(3)


def mux(scene_mp4, mp3, dst, seconds, audio_offset=0.0):
    """The scene's picture + the chapter's narration under the ONE profile; the file is exactly the mp3's length. `audio_offset` exists only for the R-sync mutant (-itsoffset 1)."""
    subprocess.run(["nice", "-n", "10", "ffmpeg", "-v", "error", "-y", "-i", scene_mp4] + (["-itsoffset", str(audio_offset)] if audio_offset else []) + ["-i", mp3, "-map", "0:v:0", "-map", "1:a:0", "-t", f"{seconds:.3f}",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-r", "25", "-s", f"{PROFILE['width']}x{PROFILE['height']}",
                    "-c:a", "aac", "-ar", PROFILE["sample_rate"], "-ac", str(PROFILE["channels"]), "-b:a", "128k", "-movflags", "+faststart", dst], check=True)


def stream_starts(mp4):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,start_time", "-of", "json", mp4], capture_output=True, text=True, check=True)
    st = {x["codec_type"]: float(x.get("start_time", 0) or 0) for x in json.loads(r.stdout)["streams"]}
    return st.get("video", 0.0), st.get("audio", 0.0)


def sync_findings(mp4, ends, tol_start=0.05, tol_median=0.1):
    """R-sync (council 10-21 11:08Z), on every final mp4: the audio and the video start within `tol_start` of each other, AND silencedetect on the mp4's OWN audio track finds a pause within
    `tol_median` (median over the stored sentence ends, the last one excluded) of where the plan says the sentences end. Mutant: mux with -itsoffset 1 -> RED. -> [finding]"""
    out = []
    v, a = stream_starts(mp4)
    if abs(v - a) > tol_start:
        out.append(f"video starts at {v:.3f} s, audio at {a:.3f} s (> {tol_start} s apart)")
    mids = [(x + y) / 2 for x, y in silences(mp4)]
    diffs = sorted(min((abs(e - m) for m in mids), default=float("inf")) for e in ends[:-1])
    med = diffs[len(diffs) // 2] if diffs else 0.0
    if med > tol_median:
        out.append(f"the mp4's own audio pauses are {med:.2f} s (median) from the stored sentence ends (> {tol_median} s)")
    return out


def keyframes(mp4, plan, out_prefix):
    """Three PNGs for the taste review: a third, the middle and two thirds of the chapter's FEED beats."""
    feed = [b for b in plan["beats"] if b["kind"] == "feed"] or plan["beats"]
    got = []
    for k, f in enumerate((0.15, 0.5, 0.85)):
        b = feed[min(int(f * len(feed)), len(feed) - 1)]
        t = b["t0"] + 0.6 * (b["t1"] - b["t0"])
        dst = f"{out_prefix}-{k + 1}.png"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", mp4, "-frames:v", "1", dst], check=True)
        got.append(dst)
    return got


def kill_group(p, wait=60):
    """SIGTERM to the render's whole process group (never SIGSTOP); SIGKILL only if it is still there after `wait` seconds."""
    try:
        os.killpg(p.pid, signal.SIGTERM)
    except ProcessLookupError:
        return
    t0 = time.time()
    while p.poll() is None and time.time() - t0 < wait:
        time.sleep(0.5)
    if p.poll() is None:
        os.killpg(p.pid, signal.SIGKILL)


def run_chapter(n, chap, mp3, d, render_cmd, repo=REPO, publish_it=False, vmlimit_kb=VMLIMIT_KB, peak_mib=1500, poll=10, gate=None, read=None, plan=None):
    """The whole chapter. d = {video, deliver, tmp, static, checks} dirs. Steps: plan + timing (RED stops here, nothing rendered) -> the start test (refuse stops here)
    -> render under the Watcher (flock render.lock, nice, /usr/bin/time -v, ulimit -v) -> mux to d['tmp'] -> checks (profile, duration, drawn bytes, frames) -> keyframes
    -> publish only if `publish_it` and GREEN. -> a dict report (status, findings, wall, vmpeak, vmhwm, ...) also written to d['checks']/chNN.report.json."""
    t_start = time.time()
    rep = {"chapter": f"C{n}", "status": None, "findings": []}
    nn = f"ch{n:02d}"
    for k in ("video", "tmp", "checks"):
        os.makedirs(d[k], exist_ok=True)
    plan = plan or chapter_plan(chap, mp3, repo)
    lens = [len(b["spoken"]) for b in plan["beats"]]
    rep["timing"] = {"boundaries": plan["boundaries"], "fallback": plan["fallback"], "beats": len(plan["beats"]), "duration": plan["duration"]}
    tf = timing_findings(plan) + verify_ends(plan, plan["pauses"], plan["duration"], lens)
    if n in EXCEPTIONS and any(f.startswith("fallback") for f in tf):
        offs = prior_offsets(plan)
        if offs and all(x["ok"] for x in offs):
            tf = [f for f in tf if not f.startswith("fallback")]
            rep["exception"] = f"C{n}: timing approximate, {plan['fallback']} of {plan['boundaries']} boundaries on the prior (> 25 % line, {EXCEPTIONS[n]})"
        else:
            tf = tf + [f"named exception C{n} refused: offset >= the shorter neighbouring sentence at ends {[x['k'] for x in offs if not x['ok']]}"]
    json.dump(plan, open(f"{d['video']}/{nn}-plan.json", "w"), indent=1)
    if tf:
        rep.update(status="red: timing", findings=tf)
        return _finish(rep, d, nn, t_start)
    ok, lines = (gate or start_test)(peak_mib)
    rep["start_test"] = lines
    if not ok:
        rep.update(status="refused: start test")
        return _finish(rep, d, nn, t_start)
    drawn = f"{d['video']}/{nn}-drawn.json"
    media = f"{d['video']}/media-{nn}"
    env = dict(os.environ, M4_PLAN=f"{d['video']}/{nn}-plan.json", M4_DRAWN=drawn, M4_REPO=repo, M4_MEDIA=media, M4_OUT=nn)
    if os.path.exists(drawn):
        os.remove(drawn)
    timefile = f"{d['video']}/{nn}-time.txt"
    cmd = [x.format(plan=env["M4_PLAN"], media=media, out=nn, time=timefile) for x in render_cmd]
    samplers = []

    def spawn():
        p = subprocess.Popen(cmd, env=env, start_new_session=True, stdout=open(f"{d['video']}/{nn}-render.log", "ab"), stderr=subprocess.STDOUT,
                             preexec_fn=lambda: resource.setrlimit(resource.RLIMIT_AS, (vmlimit_kb * 1024, vmlimit_kb * 1024)))
        smp = Sampler(p.pid); smp.start(); samplers.append(smp)
        return p

    w = Watcher(spawn, read or stop_reason, time.sleep, kill_group, poll)
    t_render = time.time()
    status, stops = w.run()
    rep.update(render_wall=round(time.time() - t_render, 1), stops=stops, vmpeak_kb=max((s.vmpeak for s in samplers), default=0), vmhwm_kb=max((s.vmhwm for s in samplers), default=0))
    for s in samplers:
        s.stop()
    if status != "ok":
        rep.update(status=status)
        return _finish(rep, d, nn, t_start)
    scene = next(iter(sorted(Path(media).rglob(f"{nn}.mp4"))), None) or next(iter(sorted(Path(media).rglob("*.mp4"))), None)
    if scene is None:
        rep.update(status="failed: no scene file", findings=[f"no mp4 under {media}"])
        return _finish(rep, d, nn, t_start)
    name = rep["name"] = video_name(chap)
    tmp = f"{d['tmp']}/{name}"
    mux(str(scene), mp3, tmp, plan["duration"])
    fs = file_checks(tmp, plan, drawn, repo)
    rep["findings"], rep["keyframes"] = fs, keyframes(tmp, plan, f"{d['video']}/keyframes-{nn}")
    green = not fs
    rep["status"] = "green" if green else "red: checks"
    checks_info = {"chapter": f"C{n}", "findings": fs, "timing": rep["timing"], "vmpeak_kb": rep["vmpeak_kb"], "vmhwm_kb": rep["vmhwm_kb"], "render_wall": rep["render_wall"], "repo_head": _head(repo)}
    rep["checks_info"] = checks_info
    rep["unpublished"] = tmp
    if publish_it and green:
        publish_chapter(n, d, rep, plan)
    elif publish_it:
        publish(tmp, name, d["deliver"], d["static"], d["tmp"], f"{d['checks']}/{nn}.json", False, checks_info)      # writes the RED checks file, moves nothing
    return _finish(rep, d, nn, t_start)


def file_checks(tmp, plan, drawn_path, repo=REPO):
    """Every check on a rendered, muxed chapter file: profile, duration, what was drawn (re-read from git), R-sync, frames. -> [finding]"""
    info = probe(tmp)
    fs = profile_findings(info) + duration_findings(info["duration"], plan["duration"])
    try:
        fs += check_drawn(json.load(open(drawn_path)), plan, repo)
    except (OSError, ValueError) as e:
        fs.append(f"no record of what was drawn ({type(e).__name__})")
    fs += sync_findings(tmp, plan["ends"])
    mids = [(b["t0"] + b["t1"]) / 2 for b in plan["beats"]]
    return fs + frame_findings(grab_frames(tmp, mids), [b["kind"] for b in plan["beats"]])


def recheck_chapter(n, d, repo=REPO):
    """Run the file checks again on a rendered chapter waiting in deliver-tmp/ (no render), e.g. after a check's line was recalibrated; rewrites its report. -> the report"""
    nn = f"ch{n:02d}"
    rep = json.load(open(f"{d['checks']}/{nn}.report.json"))
    plan = json.load(open(f"{d['video']}/{nn}-plan.json"))
    fs = file_checks(rep["unpublished"], plan, f"{d['video']}/{nn}-drawn.json", repo)
    rep["findings"], rep["status"] = fs, ("green" if not fs else "red: checks")
    rep["checks_info"] = dict(rep["checks_info"], findings=fs, repo_head=_head(repo), rechecked=True)
    json.dump(rep, open(f"{d['checks']}/{nn}.report.json", "w"), indent=1)
    return rep


def publish_chapter(n, d, rep, plan):
    """Publish a GREEN, rendered chapter from deliver-tmp/: the swap with its checks after (publish()), then the README row with the three timing counts and any named exception."""
    nn, name = f"ch{n:02d}", rep["name"]
    if rep.get("status") != "green" or not os.path.exists(rep["unpublished"]):
        raise ValueError(f"C{n} is not a green rendered chapter waiting in {d['tmp']}")
    sha = publish(rep["unpublished"], name, d["deliver"], d["static"], d["tmp"], f"{d['checks']}/{nn}.json", True, rep["checks_info"])
    c = plan["counts"]
    extra = (f"timing: {plan['fallback']} of {plan['boundaries']} boundaries on the prior (DP with 12 % REL; the approved 0.7 s alone {c['dp_tol_only']}; the approved greedy rule {c['greedy']}); "
             + (rep["exception"] + "; " if "exception" in rep else "") + (BANKED[n] + "; " if n in BANKED else "") + "the static card is kept in deliver-static/")
    set_readme_row(f"{d['deliver']}/README-narration.txt", name, f"C{n}", "animated version", extra)
    ensure_readme_limit(f"{d['deliver']}/README-narration.txt")
    if n in BANKED:
        ensure_readme_line(f"{d['deliver']}/README-narration.txt", f"C{n}: {BANKED[n]}.", 3)
    rep["published"] = sha
    rep.pop("unpublished", None)
    json.dump(rep, open(f"{d['checks']}/{nn}.report.json", "w"), indent=1)
    return sha


def wait_start(peak_mib, poll=30, hold_after=3600, queue=None, hold=None, start=None, sleep=time.sleep, now=time.time, log=print, max_wait=None):
    """The schedule of council 10-21 09:52Z: touch RENDERING first (SM's unstarted gates then wait), then poll the start test until it passes; after `hold_after` s of waiting touch
    HOLD-GATES and say so (I tell SM in a [word]). Never removes anything: the caller removes RENDERING after the chapter. -> (ok, [lines]); ok False only on max_wait."""
    queue, hold, start = queue or QUEUE, hold or HOLD, start or start_test
    open(queue, "a").close()
    t0, held = now(), False
    while True:
        ok, lines = start(peak_mib)
        if ok:
            return True, lines
        waited = now() - t0
        if not held and waited >= hold_after:
            open(hold, "a").close(); held = True
            log(f"HOLD-GATES touched after {waited / 60:.0f} min on the start test")
        if max_wait is not None and waited >= max_wait:
            return False, lines
        sleep(poll)


def _head(repo):
    r = subprocess.run(["git", "-C", repo, "rev-parse", "--short=10", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip()


def video_name(chap):
    """explainer-chNN-<slug>.mp4 exactly as the walk names the static card (media_walk.video_name)."""
    slug = re.sub(r"[^a-z0-9]+", "-", chap["title"].lower()).strip("-")[:48].strip("-") or "chapter"
    return f"explainer-ch{chap['n']:02d}-{slug}.mp4"


def _finish(rep, d, nn, t_start):
    rep["wall"] = round(time.time() - t_start, 1)
    json.dump(rep, open(f"{d['checks']}/{nn}.report.json", "w"), indent=1)
    return rep


# ---- the content probe of a joined file (council 10-21 11:41Z): the duration cannot see a stale join (the animated and the static chapter are as long as each other)
def psnr(a, b):
    """PSNR in dB of two equal-length gray frames; inf when identical."""
    if not a or len(a) != len(b):
        return 0.0
    mse = sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)
    return float("inf") if mse == 0 else 10 * math.log10(255 * 255 / mse)


def join_probe(joined, n, deliver, static_dir, offsets=(30, 60, 120), same_db=30.0, apart_db=25.0, w=320, h=180):
    """Is chapter n IN the joined full mp4 the ANIMATED one? The chapter starts at the sum of the durations of chapters 0..n-1 in deliver/ (the join order); at start + each of `offsets`
    (clamped inside the chapter) a frame of the joined file is compared with the same time of deliver/explainer-chNN (animated) and of deliver-static/ (the card). ANIMATED iff at every
    offset PSNR(joined, animated) >= same_db and PSNR(joined, static) < apart_db; the static card in the join is RED. A missing card -> 'no card', an empty frame -> 'no frame' (both RED).
    -> (verdict 'animated'|'static'|'other'|'no card'|'no frame', [(offset, db_animated, db_static)])"""
    files = sorted(f for f in os.listdir(deliver) if re.match(r"explainer-ch\d\d-.*\.mp4$", f))
    names = [f for f in files]
    me = next(f for f in files if f.startswith(f"explainer-ch{n:02d}-"))
    start = sum(probe(f"{deliver}/{f}")["duration"] for f in names if f < me)
    dur = probe(f"{deliver}/{me}")["duration"]
    if not os.path.exists(f"{static_dir}/{me}"):
        return "no card", []                                     # belam 14:2xZ: with no card, 'PSNR 0.0 against the card' passed whatever the join held (a false GREEN)
    rows = []
    for o in offsets:
        o = min(o, max(dur - 1.0, 0.0))
        j, a, st = (grab_frames(p, [t], w, h)[0] for p, t in ((joined, start + o), (f"{deliver}/{me}", o), (f"{static_dir}/{me}", o)))
        if not (j and a and st):
            return "no frame", rows                              # an empty frame is never read as 'differs': psnr() of nothing is 0.0
        rows.append((o, psnr(j, a), psnr(j, st)))
    if all(da >= same_db and ds < apart_db for _, da, ds in rows):
        return "animated", rows
    if all(ds >= same_db and da < apart_db for _, da, ds in rows):
        return "static", rows
    return "other", rows


# ---- cli
def glob_one(pattern):
    import glob as _g
    return sorted(_g.glob(pattern))[0]


def load_chapters(script=SCRIPT, repo=REPO):
    return {c["n"]: c for c in media_html.parse(script)}


def main(argv):
    if not argv:
        sys.exit(__doc__)
    cmd, rest = argv[0], argv[1:]
    if cmd == "lint":
        f = lint(rest)
        print("\n".join(f) or "lint: clean"); return 1 if f else 0
    if cmd == "start":
        ok, ls = start_test(float(rest[0]) if rest else 1500)
        print("\n".join(ls)); print("START OK" if ok else "REFUSED"); return 0 if ok else 1
    if cmd == "queue":
        print(" ".join(f"C{n}" for n in pending(BASE + "/deliver", BASE + "/video/checks"))); return 0
    chaps = load_chapters()
    if cmd == "render":
        n = int(rest[0].lstrip("C"))
        V = BASE + "/video"
        d = {"video": V, "deliver": BASE + "/deliver", "tmp": BASE + "/deliver-tmp", "static": BASE + "/deliver-static", "checks": V + "/checks"}
        cmd_ = ["flock", V + "/render.lock", "nice", "-n", "10", "/usr/bin/time", "-v", "-o", "{time}", V + "/venv/bin/manim", "-r", "1280,720", "--fps", "25", "--media_dir", "{media}",
                "-v", "WARNING", "--progress_bar", "none", "-o", "{out}", str(Path(__file__).resolve().parent / "media_scene.py"), "Chapter"]
        kw = {"vmlimit_kb": int(os.environ["M4_VMLIMIT_KB"])} if os.environ.get("M4_VMLIMIT_KB") else {}
        signal.signal(signal.SIGTERM, lambda *a: sys.exit(143))      # so the finally below runs and RENDERING never outlives the job
        try:
            rep = run_chapter(n, chaps[n], f"{BASE}/deliver/season3-C{n}-narration.mp3", d, cmd_, publish_it="--publish" in rest, peak_mib=float(os.environ.get("M4_PEAK_MIB", 1500)),
                              gate=lambda peak: wait_start(peak), **kw)
        finally:
            if os.path.exists(QUEUE):
                os.remove(QUEUE)
        print(json.dumps({k: v for k, v in rep.items() if k != "start_test"}, indent=1))
        print("\n".join(rep.get("start_test", [])))
        return 0 if rep["status"] == "green" else 1
    if cmd == "recheck":
        n = int(rest[0].lstrip("C"))
        V = BASE + "/video"
        rep = recheck_chapter(n, {"video": V, "deliver": BASE + "/deliver", "tmp": BASE + "/deliver-tmp", "static": BASE + "/deliver-static", "checks": V + "/checks"})
        print(f"C{n}: {rep['status']}", *rep["findings"], sep="\n  ")
        return 0 if rep["status"] == "green" else 1
    if cmd == "publish":
        n = int(rest[0].lstrip("C"))
        V = BASE + "/video"
        d = {"video": V, "deliver": BASE + "/deliver", "tmp": BASE + "/deliver-tmp", "static": BASE + "/deliver-static", "checks": V + "/checks"}
        rep = json.load(open(f"{d['checks']}/ch{n:02d}.report.json"))
        sha = publish_chapter(n, d, rep, json.load(open(f"{V}/ch{n:02d}-plan.json")))
        print(f"C{n} published {sha[:16]}; the joined full mp4 must be {deliver_total(d['deliver']):.1f} s +-0.5 (sum of the explainer-ch*.mp4 in deliver/)")
        return 0
    if cmd == "sync":
        n = int(rest[0].lstrip("C"))
        plan = json.load(open(f"{BASE}/video/ch{n:02d}-plan.json"))
        f = sync_findings(rest[1] if len(rest) > 1 else glob_one(f"{BASE}/deliver/explainer-ch{n:02d}-*.mp4"), plan["ends"])
        v, a = stream_starts(rest[1] if len(rest) > 1 else glob_one(f"{BASE}/deliver/explainer-ch{n:02d}-*.mp4"))
        print(f"C{n}: video start {v:.3f} s, audio start {a:.3f} s;", "RED " + "; ".join(f) if f else "sync green")
        return 1 if f else 0
    if cmd == "joinprobe":
        verdict, rows = join_probe(rest[0], int(rest[1].lstrip("C")), BASE + "/deliver", BASE + "/deliver-static")
        for o, da, ds in rows:
            print(f"  +{o:.0f} s: vs animated {da:.1f} dB, vs static card {ds:.1f} dB")
        print(f"C{rest[1].lstrip('C')} in the joined file: {verdict.upper()}")
        return 0 if verdict == "animated" else 1
    if cmd == "offsets":
        n = int(rest[0].lstrip("C"))
        pl = chapter_plan(chaps[n], f"{BASE}/deliver/season3-C{n}-narration.mp3")
        rows = prior_offsets(pl)
        for r_ in rows:
            print(f"C{n} end {r_['k']:>2} at {r_['end']:7.2f} s: offset {r_['offset']:.2f} s, shorter neighbour {r_['shorter_s']:.2f} s -> {'ok' if r_['ok'] else 'FAIL'}")
        print(f"C{n}: {len(rows)} prior-placed ends, counts {pl['counts']}, {'ACCEPT' if rows and all(x['ok'] for x in rows) else 'NOT accepted'}")
        return 0 if all(x["ok"] for x in rows) else 1
    if cmd == "plan":
        n = int(rest[0].lstrip("C"))
        pl = chapter_plan(chaps[n], f"{BASE}/deliver/season3-C{n}-narration.mp3")
        f = timing_findings(pl) + verify_ends(pl, pl["pauses"], pl["duration"], [len(b['spoken']) for b in pl['beats']])
        if len(rest) > 1:
            json.dump(pl, open(rest[1], "w"), indent=1)
        print(f"C{n}: {len(pl['beats'])} beats, {pl['fallback']}/{pl['boundaries']} on the prior, {pl['duration']:.1f} s", *f, sep="\n  " if f else "")
        return 1 if f else 0
    if cmd == "timing":
        red = 0
        for n in sorted(chaps):
            pl = chapter_plan(chaps[n], f"{BASE}/deliver/season3-C{n}-narration.mp3")
            f = timing_findings(pl) + verify_ends(pl, pl["pauses"], pl["duration"], [len(b['spoken']) for b in pl['beats']])
            red += bool(f)
            print(f"C{n:<2} {len(pl['beats']):>3} beats {pl['duration']:6.1f} s  prior {pl['fallback']:>2}/{pl['boundaries']:<2} {'RED ' + '; '.join(f) if f else 'green'}")
        return 1 if red else 0
    sys.exit(__doc__)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
