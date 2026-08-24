---
confidence: 0.75
evidence_runs: []
id: "mvp:payload-boundary-predicate"
parents:
  - goal:g6.8
subgraph: false
tags:
  - g6.8
  - level3
title: "A three-rule predicate for the G6.8 payload boundary, run against all 316 tracked files in agi"
type: mvp
---

**The predicate:**

```python
#!/usr/bin/env python3
"""
G6.8 payload boundary predicate. Classifies every tracked file in the `agi`
engine repo as `in` (candidate payload for a node) or `out` (no thought
attaches). Total: every file gets exactly one verdict. Mechanical: decided
by git's own config and by path shape, never by filename.
"""
import subprocess, sys
from pathlib import Path
from collections import Counter


def git_ls_files(repo: Path) -> list[str]:
    out = subprocess.run(["git", "-C", str(repo), "ls-files"],
                          capture_output=True, text=True, check=True)
    return [l for l in out.stdout.splitlines() if l]


def gitignore_matched(repo: Path, paths: list[str]) -> set[str]:
    """Which paths match a pattern in the repo's own .gitignore, evaluated
    with --no-index so already-tracked files aren't exempted just because
    git stopped flagging them once added to the index. This is the
    mechanical reading of "under a directory the engine declares transient":
    ask the engine's own VCS config, not our outside judgment."""
    if not paths:
        return set()
    proc = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "--no-index", "-z", "--stdin"],
        input="\0".join(paths), capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"git check-ignore failed: {proc.stderr}")
    return set(p for p in proc.stdout.split("\0") if p)


def is_test_fixture(path: str) -> bool:
    """Directory-naming convention: any path passing through tests/fixtures/
    or test/fixtures/. Reason: synthetic input manufactured for a test
    harness to read (placeholder markdown, dummy JSON, fake directory
    trees) -- authored to be consumed by test code, not to communicate
    anything to a human or agent forming a thought."""
    parts = Path(path).parts
    for i, part in enumerate(parts):
        if part in ("tests", "test") and i + 1 < len(parts) and parts[i + 1] == "fixtures":
            return True
    return False


def is_log_stream(path: str) -> bool:
    """Extension-based: .jsonl (newline-delimited JSON) is an append-only
    event-stream format by construction -- one line per run event, not one
    authored thought. Catches every jsonl file whether or not it happens to
    sit under a gitignored directory (sessions/*.jsonl does;
    autoresearch.jsonl at repo root does not) -- the extension rule is what
    makes the exclusion consistent instead of needing a directory-shaped
    special case."""
    return path.endswith(".jsonl")


def classify(repo: Path) -> list[tuple[str, str, str]]:
    files = git_ls_files(repo)
    ignored = gitignore_matched(repo, files)
    rows = []
    for f in sorted(files):
        if f in ignored:
            rows.append((f, "out", "gitignore-declared-transient"))
        elif is_log_stream(f):
            rows.append((f, "out", "jsonl-event-stream"))
        elif is_test_fixture(f):
            rows.append((f, "out", "test-fixture-directory"))
        else:
            rows.append((f, "in", "file-in-repo"))
    return rows


if __name__ == "__main__":
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rows = classify(repo)
    for path, verdict, reason in rows:
        print(f"{path}\t{verdict}\t{reason}")
    total = len(rows)
    n_in = sum(1 for _, v, _ in rows if v == "in")
    reason_counts = Counter(r for _, v, r in rows if v == "out")
    print(f"\ntotal={total} in={n_in} out={total - n_in}", file=sys.stderr)
    for reason, count in reason_counts.most_common():
        print(f"  out[{reason}]={count}", file=sys.stderr)
```

Three exclusion rules, OR'd; anything none of them catch is `in`. No rule
ever tests a specific filename — each is a path/extension/git-config
property, so the same three lines apply to a file that doesn't exist yet.

**Classification of the engine repo:** ran against `git ls-files` in
`/home/ubuntu/work/agi` (commit at run time, 316 tracked files). Full
per-file output kept at
`sessions/iter-9010/kid-i/classified.tsv` alongside the script at
`sessions/iter-9010/kid-i/payload_boundary.py` for re-run.

| verdict | rule | count |
|---|---|---|
| in | code (`.py .sh .ts .sql`) | 134 |
| in | docs/prose (`.md`, non-fixture) | 37 |
| in | config/data (`.json .toml`, `.gitignore`) | 6 |
| **in total** | | **177** |
| out | gitignore-declared-transient | 125 |
| out | test-fixture-directory | 13 |
| out | jsonl-event-stream | 1 |
| **out total** | | **139** |
| **total** | | **316** |

The 125 gitignore-matched files are: `experiments/*/output.txt` (96),
`sessions/*.jsonl` (24), `__pycache__/*.pyc` (3), `.gitnexus_cache.json` (1),
`pi-agi.log` (1) — every one of these is either directly listed in `.gitignore`
by literal name/prefix or falls under a gitignored directory, verified with
`git check-ignore --no-index` rather than trusting the pattern text by eye.
The single jsonl-event-stream file is `autoresearch.jsonl`, which is *not*
gitignored (checked directly — `git check-ignore` returns nothing for it)
but is the same append-only artifact shape as the 24 files in `sessions/`;
the extension rule is what catches it, not the gitignore rule.

**Falsifier result: pass — 0 of 316 files needed adjudication.** Every
tracked file got `in` or `out` from the script with no filename ever
appearing in the rule set. `diff` against `git ls-files` confirms the
predicate's output set is exactly the tracked-file set (no file skipped, none
invented).

That is the mechanical falsifier. It is not the whole story — see "what this
does not settle" below, which names a case where the rule's *correctness*,
as opposed to its *totality*, is closer than it looks.

**The edges** — every file/category I was tempted to special-case, in
descending order of how much it worried me:

1. **`extensions/agi/bin/decompose-engine.goalmap.json`.** Its own header
   says: *"Declared deliberately by a human or a verdict decision;
   decompose-engine.py never infers this from the file tree."* That sentence
   is a direct answer to the question the brief asked me to test —
   "is generated-vs-authored even decidable from the path?" — and the
   answer is **no**. Nothing about the path
   `extensions/agi/bin/decompose-engine.goalmap.json` distinguishes it from
   a generated cache; it classifies `in` here only because it isn't
   gitignored and isn't `.jsonl` or under `tests/fixtures/`. If this exact
   file had instead lived under a directory the project later decided to
   gitignore (a `.cache/` or `build/`-style rename), my predicate would flip
   it to `out` despite it being genuinely hand-authored, and nothing in the
   predicate would notice the contradiction. I decided **in**, because the
   correct classification for *this* file is in, but I want to be honest
   that the rule got there by good luck (gitignore currently tracks
   generated-vs-authored faithfully for every file that exists today), not
   because "generated" is actually a path-decidable property. This is the
   sharpest edge in the whole run.

2. **`tests/fixtures/**` (13 files).** I excluded these on a directory-naming
   convention (`tests/fixtures/` or `test/fixtures/`), reasoned as: synthetic
   input manufactured for test code to read, not authored to communicate
   anything (`sample.md`, `[hypothesis].md`, a fake nested directory tree
   four levels deep, all placeholder content). This is defensible and it is
   mechanical in the sense the brief asked for — a path-prefix rule, not a
   filename allowlist — but it depends on the convention holding: nothing
   compels a fixture to live under a directory literally named `fixtures`,
   and nothing prevents genuine reference material from being filed there
   for unrelated reasons. Compare directly to edge 4 below — the prior
   census left these *in* the eligible set instead of excluding them, so
   this is also the single largest disagreement with the earlier work.

3. **`context/refs/zoom-roundtrip-ground-truth/**` (14 files, all `in`).**
   These are literally what an experiment's zoom-in/zoom-out agents wrote —
   the exact shape of thing G6.8's "out" bullet names ("sessions, run logs,
   and ephemeral output... they are evidence a node can cite; they are not
   thoughts"). I was tempted to exclude them by content-shape. I did not,
   and the predicate doesn't either, because they are *not* gitignored — a
   human deliberately un-ignored and kept them, with a `README.md`
   explaining why ("next L1 node is an A/B against exactly this baseline").
   The predicate's gitignore rule ends up tracking that editorial decision
   exactly: gitignored ephemeral output (`experiments/`, `sessions/`) is
   out, kept-and-cited ephemeral output is in. That the rule lands on the
   same side as the human's actual choice, without reading a single byte of
   content, is the strongest positive result in this run — but it is worth
   naming as an edge because it depends on that human decision having been
   made correctly (un-ignoring it) in the first place, which is exactly the
   kind of judgment call the falsifier is suspicious of.

4. **`.gitignore` itself.** The prior census excluded it ("VCS meta, no
   contract semantics"). I include it, and disagree with that call: this
   predicate treats `package.json` and the `.toml` templates as `in`
   because they are authored, contentful config a thought can attach to
   (e.g. "should this dependency be pinned"), and `.gitignore` is the same
   kind of file by the same test — it is a real authored decision list
   (this very node exists because two of its lines, `sessions/` and
   `experiments/`, turned out to matter enough to drive three of my
   exclusion buckets). Excluding it as "meta" while keeping `package.json`
   as "config" was an inconsistency in the earlier hand-built list, not a
   principled split. My rule doesn't special-case it either way — it's just
   an `.md`-adjacent tracked file that matches none of the three exclusion
   rules, so it falls through to `in`.

5. **`extensions/agi/tests/**` (50 `.py` files) + `conftest.py` (1).**
   Classified `in`, as code, no exclusion rule fires. The brief asks "does a
   test carry a thought, or is it evidence for one?" — a real question, but
   it's a question about *what kind of node* a test file should become
   (does it spawn a hypothesis the way `src/` code does, or does it only
   ever attach as evidence to a node about the code it tests?), not about
   membership. G6.8's falsifier is about in/out, and "code, already in" is
   unambiguous for `.py` regardless of directory. I did not create a
   test-vs-src distinction in the predicate; flagging it here so the
   distinction doesn't get silently smuggled back in at authoring time.

**Disagreement with the prior census: 177 vs 189 — accounted for, and it
resolves to exactly two rule differences, not noise.** Both runs agree,
file-for-file, that the same 126 files are excluded:
`experiments/*/output.txt` (96), all 25 `.jsonl` files, `__pycache__/*.pyc`
(3), `.gitnexus_cache.json` (1), `pi-agi.log` (1). The 189 vs 177 gap is
exactly:

- prior census kept `tests/fixtures/**` (13) in the eligible set; this
  predicate excludes them → −13
- prior census excluded `.gitignore` (1) as "VCS meta"; this predicate
  includes it → +1

`189 − 13 + 1 = 177`. No other file moved sides. The prior census was a
one-time hand list, not wrong exactly — both of its calls were reasonable —
but restating them as *rules* (a fixtures-directory convention, an
authored-config test) rather than a list is what makes the difference
explainable in two lines instead of requiring a full re-diff.

**What this does not settle:**

- **Generated-vs-authored is not actually a path-decidable property in
  general.** Edge 1 (`decompose-engine.goalmap.json`) shows the predicate's
  gitignore rule is a proxy that happens to be accurate for every file that
  exists in the repo *today*, because whoever maintains `.gitignore` has so
  far correctly declared everything actually generated. That is an
  empirical fact about this repo's current hygiene, not a guarantee the
  predicate enforces. A generated file that someone forgets to gitignore
  will silently classify `in`, and the predicate has no second signal (no
  header convention, no directory convention) to catch that case the way it
  caught fixtures via directory naming.
- **The fixtures rule is a convention, not an invariant.** It depends on
  test data continuing to live under a directory named exactly `fixtures`
  under a directory named `tests`/`test`. Nothing in the repo enforces that
  layout.
- **This predicate answers membership, not node granularity or node
  lifecycle.** It says a file is a legitimate payload; it says nothing
  about whether it should be one node or many (a 50-file `tests/`
  directory), whether a retired file like `TODO.md` should carry a
  `deprecated`-style status once it becomes a node, or how often the node
  should be re-synced against the file. Those are `G6.1`/`G6.3` questions,
  deliberately out of scope here.
- **Scope, restated from G6.8 itself:** this is today's line, drawn at the
  filesystem for tractability. `G10`'s horizon (git refs, sessions, and run
  history as addressable regions of the same hypergraph) would make several
  of today's `out` verdicts — the gitignored session/experiment files in
  particular — reachable by a different mechanism than "become a node,"
  without contradicting this predicate; that horizon is not attempted here.
