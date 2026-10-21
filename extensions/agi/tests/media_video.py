#!/usr/bin/env python3
"""goal:g5.4.2 M4, the animated explainer: the parts that need no manim (stdlib only, so every rule here has a test and a mutant). 0 provider spend.
  media_video.py plan CHAPTER [OUT.json]     beats + timing for one chapter (C2): the narration's tagged sentences, the mp3's silences, the placed boundaries
  media_video.py timing                      the timing report for all 18 chapters (ffmpeg silencedetect only), RED lines included
  media_video.py lint FILE...                no raw Text / Code / MarkupText / Tex ... in a scene file (council C1): engine text goes through media_vocab.Strand
  media_video.py start [PEAK_MIB]            the start test, read now (council 10-21 08:03Z); exit 0 = may start, 1 = refuse
  media_video.py queue                       the chapters still to render, from bytes (council C5)
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

REPO = "/var/lib/agi/director-general-3/w-sg"
SCRIPT = REPO + "/.agi/context/media/season3-explainer-script.md"
BASE = "/data/work/director-general-3-media/season3"
FPS = 25
PROFILE = {"codec_name": "h264", "width": 1280, "height": 720, "r_frame_rate": "25/1", "pix_fmt": "yuv420p", "a_codec": "aac", "sample_rate": "44100", "channels": 1}
TOL = 0.7                    # a picked pause is kept when its sentence is within this (or REL of its length, if more) of its character-proportional speech time
REL = 0.12
FALLBACK_MAX = 0.25          # council C2: more than this share of a chapter's boundaries on the prior = RED
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


def timing_findings(pl, max_frac=FALLBACK_MAX):
    """-> [finding]; [] = green. RED: a chapter with more than max_frac of its boundaries on the prior (C2)."""
    out = []
    if pl["boundaries"] and pl["fallback"] / pl["boundaries"] > max_frac:
        out.append(f"fallback {pl['fallback']} of {pl['boundaries']} boundaries on the prior ({pl['fallback'] / pl['boundaries']:.0%} > {max_frac:.0%})")
    return out


def verify_ends(pl, pauses, duration, lens, tol=TOL, rel=REL):
    """The placed ends, re-checked against the mp3's own pauses and the sentences' lengths (not trusted from place()): increasing; each 'pause' end IS a pause middle and the sentence it
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


# ---- the engine bytes a picture shows
def strand_window(repo, sha, path, lo, hi, needle, ctx=34):
    """-> (window, i0, i1): the needle with up to `ctx` characters each side, never past the ends of its line(s) in L<lo>-L<hi> at the sha; window[i0:i1] == needle.
    A needle that is not in the range is a ValueError (the pair check of the script already forbids it)."""
    text = media_html.lines_at(repo, sha, path, lo, hi)
    i = text.find(needle)
    if i < 0:
        raise ValueError(f"needle not at {sha}:{path}:L{lo}-L{hi}")
    a = max(text.rfind("\n", 0, i) + 1, i - ctx)
    j = i + len(needle)
    nl = text.find("\n", j)
    b = min(len(text) if nl < 0 else nl, j + ctx)
    return text[a:b], i - a, i - a + len(needle)


def wrap(window, i0, i1, width=44):
    """The window as lines of spans [(text, is_needle)]. Cut at `width` columns (preferring a space in the last 10), every character kept: the spans re-join to the window
    exactly; a hard newline of the window is kept as a ("\n", False) span at the end of its line, and is not drawn."""
    lines, pos = [], 0
    parts = window.split("\n")
    for pi, part in enumerate(parts):
        s = 0
        while True:
            if len(part) - s <= width:
                end = len(part)
            else:
                end = s + width
                sp = part.rfind(" ", s + width - 10, s + width)
                if sp > s:
                    end = sp + 1
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
        try:
            txt = media_html.lines_at(repo, d["sha"], d["path"], d["lo"], d["hi"])
        except (ValueError, KeyError) as e:
            out.append(f"beat {d.get('beat')}: {d.get('path')} unreadable ({e})"); continue
        if d["kind"] == "strand":
            checked += 1
            by_beat[d["beat"]] = by_beat.get(d["beat"], 0) + 1
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


def frame_findings(frames, kinds, min_ink=0.004, min_diff=2.0):
    """frames = [bytes of one small grey frame per beat (taken mid-beat)]; kinds = 'feed'|'calm' per beat. A frame is BLANK when under `min_ink` of its pixels differ from its most common
    value by more than 8; a FEED beat's frame must differ from the beat before it (mean absolute difference >= min_diff). -> [finding]"""
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
    """Council C3 + C4. tmp_mp4 must lie in `tmp_dir` (a sibling of deliver/ on the same filesystem, never inside it). Only a GREEN chapter moves: the static card is kept in
    static_dir (a hard link, so deliver/<name> never disappears for the watcher), the checks file is written for the new bytes, then ONE os.replace puts the animated file in.
    undo() is one rename back. -> the new sha256."""
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
    os.chmod(tmp_mp4, 0o644)
    os.replace(tmp_mp4, dst)
    return digest


def undo(name, deliver, static_dir):
    """One rename: the static card back over the animated file."""
    os.replace(f"{static_dir}/{name}", f"{deliver}/{name}")


# ---- cli
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
