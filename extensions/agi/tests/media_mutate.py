#!/usr/bin/env python3
"""goal:g5.4.2 M4: the hand-break sweep as CODE (council 10-21 09:52Z: the 10-21 sweep was run by a harness that let Python load a stale .pyc, so '28 of 28 killed' was unproven).
  media_mutate.py            run MUTANTS against media_video.py with test_media_video.py; prints killed / survived per row; exit 1 if any survivor, or if the harness's own checks fail
Harness rules, enforced HERE and greped by test_media_mutate.py:
  - every run of pytest has PYTHONDONTWRITEBYTECODE=1 and `python3 -B`;
  - every cached .pyc of the target and of the tests is REMOVED before each mutant is written and again after the original is restored (a same-second, same-size edit keeps the pyc's
    recorded mtime and size, so an old .pyc would be loaded as if it were the new source);
  - the original is kept in memory and put back byte for byte (compared) in a finally.
Its own mutants: a byte-equal 'mutant' (NOOP) must SURVIVE (else the harness kills what is not broken), and a same-size edit made within the same second (SAME_SIZE) must be KILLED."""
import glob
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "media_video.py"
TESTS = [HERE / "test_media_video.py"]

NOOP = ("noop: byte-equal", "TOL = 0.7 ", "TOL = 0.7 ")
SAME_SIZE = ("same size: min_diff 0.8 -> 0.0", "min_ink=0.004, min_diff=0.8", "min_ink=0.004, min_diff=0.0")
MUTANTS = [
    ("verify: pause end not checked", 'if not any(abs(e - m) < 0.01 for m in mids):', 'if False:'),
    ("verify: speech check off", 'elif k > 0 and kinds[k - 1] == "pause" and abs(', 'elif False and abs('),
    ("fallback max 0.5", 'FALLBACK_MAX = 0.25', 'FALLBACK_MAX = 0.5'),
    ("REL 0.12 -> 0.5", 'REL = 0.12 ', 'REL = 0.5 '),
    ("drawn substring check off", 'if not d.get("text") or d["text"] not in txt:', 'if not d.get("text"):'),
    ("drawn: missing-strand check off", 'if by_beat.get(b["i"], 0) < len(b["pairs"]):', 'if False:'),
    ("drawn: zero-checked RED off", 'if feed and checked == 0:', 'if False:'),
    ("drawn: rows re-join check off", 'if "".join(d["rows"]) != d.get("text", "").replace("\\n", ""):', 'if False:'),
    ("drawn: token row off", 'out += [f"beat {d.get(\'beat\')}: {f}" for f in token_findings(d["rows"])]', 'pass'),
    ("drawn: scale line 0.55 -> 0.3", 'MIN_SCALE = 0.55 ', 'MIN_SCALE = 0.3 '),
    ("wrap: any cut is legal", 'return not (WORD.match(part[e - 1]) and WORD.match(part[e]))', 'return True'),
    ("wrap: '.' is not a word character", 'WORD = re.compile(r"[A-Za-z0-9_.]")', 'WORD = re.compile(r"[A-Za-z0-9_]")'),
    ("token row never fires", 'WORD.match(a[-1]) and WORD.match(b[0])]', 'False]'),
    ("wrap: drops a character", 'spans.append((part[a:end], a + pos >= i0 and a + pos < i1))', 'spans.append((part[a:end - 1] if end - a > 3 else part[a:end], a + pos >= i0 and a + pos < i1))'),
    ("window: past the line (left)", 'a = max(ls, i - ctx)', 'a = max(0, i - ctx)'),
    ("window: no snap left", '    if a > ls:', '    if False:'),
    ("window: no snap right", '    if b < le:', '    if False:'),
    ("start: MemAvailable 2.5", 'lambda v: v >= 3.0', 'lambda v: v >= 2.5'),
    ("start: anon 3500 -> 4000", 'v < 3500', 'v < 4000'),
    ("start: fail open", 'ok = False\n        else:\n            pass', 'pass\n        else:\n            pass'),
    ("start: gate ignored", 'lambda v: v is False', 'lambda v: True'),
    ("start: headroom -300 -> +0", 'memory.high") / MIB - 300', 'memory.high") / MIB'),
    ("stop: 4200 -> 9000", 'if a > 4200:', 'if a > 9000:'),
    ("stop: psi 10 -> 99", 'if p > 10:', 'if p > 99:'),
    ("publish: tmp inside deliver allowed", 'or os.path.abspath(tmp_dir) == os.path.abspath(deliver):', 'or False:'),
    ("publish: static not kept", 'os.link(dst, keep)', 'pass'),
    ("publish: red still moves", 'if not green:\n        return None', 'if False:\n        return None'),
    ("publish: check after off", 'if pre is not None and (sha256(keep) != pre or os.stat(keep).st_ino == os.stat(dst).st_ino):', 'if False:'),
    ("joined tolerance 0.5 -> 5", 'def joined_findings(joined_s, deliver, tol=0.5):', 'def joined_findings(joined_s, deliver, tol=5.0):'),
    ("queue: animated anywhere", 'chapter C(\\d+), animated version\\b")', 'chapter C(\\d+), .*animated")'),
    ("queue: sha not compared", 'j.get("sha256") == sha256(mp4)', 'True'),
    ("queue: red counts", 'j.get("green") is True and', ''),
    ("schedule: extra frame", 'return want, max(rest, 0)', 'return want, max(rest, 0) + 1'),
    ("watcher: three tries", 'def run(self, tries=2):', 'def run(self, tries=3):'),
    ("lint: Code not raw", '"Text", "Code", ', '"Text", '),
    ("lint: aliases ignored", 'if a.name in RAW and a.asname:', 'if False:'),
    ("duration tolerance 0.2 -> 2.0", 'DUR_TOL = 0.2 ', 'DUR_TOL = 2.0 '),
    ("profile: fps ignored", 'for k, v in profile.items() if info.get(k) != v]', 'for k, v in profile.items() if k != "r_frame_rate" and info.get(k) != v]'),
    ("blank frames ok", 'if ink < min_ink:', 'if False:'),
    ("exception: accepted without the offsets", 'if offs and all(x["ok"] for x in offs):', 'if True:'),
    ("exception: offset line off", '"ok": off < sh}', '"ok": True}'),
    ("exception: C7 too", 'EXCEPTIONS = {6:', 'EXCEPTIONS = {7: "x", 6:'),
    ("counts: greedy is zero", '"greedy": place_greedy(lens, duration, pauses)}', '"greedy": 0}'),
    ("ulimit 2500000 -> 4000000", 'VMLIMIT_KB = 2500000 ', 'VMLIMIT_KB = 4000000 '),
    ("hold after 3600 -> 36000", 'hold_after=3600', 'hold_after=36000'),
    ("hold touched at once", 'if not held and waited >= hold_after:', 'if not held:'),
    ("rendering file left behind", 'if os.path.exists(QUEUE):\n                os.remove(QUEUE)', 'pass'),
    ("rendering not touched first", '    open(queue, "a").close()\n    t0, held = now(), False', '    t0, held = now(), False'),
]


def clean_pyc(*paths):
    """Remove every cached .pyc of these source files (any interpreter tag) from their __pycache__."""
    for p in paths:
        p = Path(p)
        for f in glob.glob(str(p.parent / "__pycache__" / (p.stem + ".*.pyc"))):
            os.remove(f)


def run_tests(cwd, tests, extra=()):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([sys.executable, "-B", "-m", "pytest", *map(str, tests), "-q", "-x", "-p", "no:cacheprovider", *extra], cwd=cwd, env=env, capture_output=True, text=True)
    return r.returncode == 0, (r.stdout.strip().split("\n") or [""])[-1]


def sweep(target, tests, table, cwd, extra=(), log=print):
    """-> [(name, 'KILLED'|'SURVIVED'|'PATTERN MISSING', last pytest line)]. The target is restored byte for byte after every mutant (checked)."""
    target = Path(target)
    original = target.read_bytes()
    out = []
    try:
        for name, a, b in table:
            src = original.decode("utf-8")
            if a not in src:
                out.append((name, "PATTERN MISSING", "")); log(out[-1]); continue
            clean_pyc(target, *tests)
            target.write_bytes(src.replace(a, b, 1).encode("utf-8"))
            ok, tail = run_tests(cwd, tests, extra)
            target.write_bytes(original)
            clean_pyc(target, *tests)
            out.append((name, "SURVIVED" if ok else "KILLED", tail)); log(out[-1])
    finally:
        target.write_bytes(original)
        clean_pyc(target, *tests)
    if target.read_bytes() != original:
        raise RuntimeError("the target was not restored byte for byte")
    return out


def verdict(results):
    """The harness's own rules: NOOP must survive, SAME_SIZE must be killed, no row may be a missing pattern, no real mutant may survive. -> [problem]"""
    bad = []
    for name, st, tail in results:
        if name == NOOP[0] and st != "SURVIVED":
            bad.append(f"harness: the byte-equal no-op was {st}")
        elif name == SAME_SIZE[0] and st != "KILLED":
            bad.append(f"harness: the same-size same-second edit was {st}")
        elif name not in (NOOP[0], SAME_SIZE[0]) and st != "KILLED":
            bad.append(f"{name}: {st}")
    return bad


def main():
    base = os.environ.get("MUT_BASETEMP", "/data/work/director-general-3-media/season3/pt/mut")
    res = sweep(TARGET, TESTS, [NOOP, SAME_SIZE] + MUTANTS, HERE.parents[2], extra=("--basetemp=" + base,))
    k = sum(1 for _, s, _ in res if s == "KILLED")
    print(f"killed {k} of {len(MUTANTS) + 1} (the no-op survived: {any(n == NOOP[0] and s == 'SURVIVED' for n, s, _ in res)})")
    bad = verdict(res)
    print("\n".join(bad) or "sweep: clean")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
