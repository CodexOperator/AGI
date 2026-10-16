#!/usr/bin/env python3
"""media_sibling.py SCRIPT.md DIFF.md OLD_SHA [REPO]: the SIBLING-GREP table of a council return (goal:g5.4.2, council 06:23Z 10-16).

A claim the council RETURNED can survive in ANOTHER sentence (N5 -> R2, H1; U2 -> R3). The diff file therefore carries, for each returned
claim, the grep that was run over the narration and html sentences, and every sentence the grep hit, marked `fixed` or `kept: REASON`.
  grep ID: REGEX                         (case-insensitive; run over the tag-stripped sentences of every ### narration / ### html section)
  hit ID | fixed | OLD SENTENCE => NEW SENTENCE      the old sentence is gone from the script and the new one is in it
  hit ID | kept: REASON | SENTENCE                    the sentence is in the script; the reason is at least three words
The universe of hits is the grep over the script at OLD_SHA plus the grep over the script now. Findings (exit = their sum): `unlisted`
(a hit with no row), `stale` (a row no grep hits), `not_fixed` (a `fixed` row whose old sentence is still in the script, or whose new
sentence is not), `no_reason` (a `kept` row with fewer than three words of reason), `no_greps` (no grep line: nothing was checked).
"""
import re
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
import media_fm2  # noqa: E402

REL = ".agi/context/media/season3-explainer-script.md"


def sentences(text):
    """[(chapter, sentence without its tag)] for every sentence of every narration / html section."""
    out, sec, chap, in_fence, block = [], None, None, False, []

    def flush():
        if block and sec:
            joined = " ".join(block)
            parts = media_fm2.TAG.split(joined)
            for k in range(0, len(parts), 2):
                for s in media_fm2.split_sentences(parts[k]):
                    out.append((chap, s.strip()))
        block.clear()

    for ln in text.split("\n"):
        m = re.match(r"^## (C\d+)\b", ln)
        if m:
            flush()
            chap, sec = m.group(1), None
        if ln.startswith("~~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^### (narration|html)\b", ln)
        if m:
            flush()
            sec = m.group(1)
            continue
        if re.match(r"^##+ ", ln):
            flush()
            sec = None
            continue
        if sec is None or re.match(r"^(@@excerpt|fn:|live:|uncalled:|sha:|pair )", ln):
            continue
        if not ln.strip():
            flush()
        else:
            block.append(ln.strip())
    flush()
    return out


def check(script, diff, old_sha, repo, emit=False):
    new = sentences(open(script, encoding="utf-8").read())
    old = sentences(subprocess.run(["git", "-C", repo, "show", f"{old_sha}:{REL}"], capture_output=True, text=True, check=True).stdout)
    new_s, old_s = {s for _, s in new}, {s for _, s in old}
    greps, rows = {}, []
    for ln in open(diff, encoding="utf-8").read().split("\n"):
        m = re.match(r"^grep (\S+): (.+)$", ln)
        if m:
            greps[m.group(1)] = re.compile(m.group(2), re.I)
        m = re.match(r"^hit (\S+) \| (fixed|kept:[^|]*) \| (.+)$", ln)
        if m:
            rows.append(m.groups())
    unlisted, stale, not_fixed, no_reason = [], [], [], []
    hits = {}                                    # (id, sentence) -> "kept" | "fixed"
    for gid, rx in greps.items():
        for _, s in new:
            if rx.search(s):
                hits[(gid, s)] = "kept"
        for _, s in old:
            if rx.search(s) and s not in new_s:
                hits[(gid, s)] = "fixed"
    if emit:
        for (gid, s), kind in sorted(hits.items()):
            print(f"hit {gid} | {kind} | {s}")
    listed = set()
    for gid, verdict, body in rows:
        if verdict == "fixed":
            o, _, n = body.partition(" => ")
            listed.add((gid, o.strip()))
            if (gid, o.strip()) not in hits:
                stale.append(f"{gid}: {o[:80]!r} is hit by no grep")
            if o.strip() in new_s or n.strip() not in new_s or o.strip() not in old_s:
                not_fixed.append(f"{gid}: {o[:80]!r} => {n[:60]!r}")
        else:
            reason = verdict[len("kept:"):].strip()
            listed.add((gid, body.strip()))
            if (gid, body.strip()) not in hits or body.strip() not in new_s:
                stale.append(f"{gid}: {body[:80]!r} is hit by no grep")
            if len(reason.split()) < 3:
                no_reason.append(f"{gid}: {body[:80]!r} kept with reason {reason!r}")
    for key in hits:
        if key not in listed:
            unlisted.append(f"{key[0]}: {key[1][:90]!r}")
    print(f"greps={len(greps)} rows={len(rows)} hits={len(hits)}")
    for name, lst in (("unlisted", unlisted), ("stale", stale), ("not_fixed", not_fixed), ("no_reason", no_reason)):
        print(f"{name}={len(lst)}")
        for x in lst[:30]:
            print("  " + name.upper(), x)
    n = len(unlisted) + len(stale) + len(not_fixed) + len(no_reason)
    if not greps:
        print("no_greps=1\n  NO_GREPS no `grep ID: REGEX` line: nothing was checked")
        n += 1
    return n


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--emit"]
    if len(a) < 3:
        sys.exit(__doc__)
    sys.exit(min(check(a[0], a[1], a[2], a[3] if len(a) > 3 else ".", "--emit" in sys.argv), 99))
