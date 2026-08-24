---
confidence: 0.85
evidence_runs: []
id: "mvp:level3-boundary-scope"
parents:
  - goal:g6.8
subgraph: false
tags:
  - g6.6
  - g6.8
  - level3
title: "Point level3.py's scan at the G6.8 payload-boundary predicate instead of its hardcoded src/bin prefixes"
type: mvp
---

**Verified, not guessed.** I built the exact diff below in scratch, ran it
against a mirrored copy of the real test suite, and dry-ran it against the
real `agi` engine repo + real `agi-tree` project (`--dry-run`, zero writes).
All numbers below are from those runs, not estimates. Scratch artifacts:
`sessions/iter-9011/kid-l/scratch-bin/level3.py` (the modified file),
`sessions/iter-9011/kid-l/scratch-repo/` (mirrored test tree),
`sessions/iter-9011/kid-l/dryrun-output.txt` (full real dry-run log).

## The change, as applicable code

Three files. All text below is exact — current and replacement — for the
parent to apply without guessing.

### 1. New file: `extensions/agi/bin/payload_boundary.py`

Copy verbatim from `sessions/iter-9010/kid-i/payload_boundary.py` (already
falsified against all 316 tracked files, 0 adjudication needed — see
`mvp:payload-boundary-predicate`). No changes to its logic; this is the
"become engine code" step for problem 3 below, not a rewrite.

```python
#!/usr/bin/env python3
"""
G6.8 payload boundary predicate.

Classifies every tracked file in the `agi` engine repo as `in` (a candidate
payload for a node) or `out` (no thought attaches). Total, mechanical: every
file gets exactly one verdict from properties a script can read off the path
and off git's own configuration -- no per-file allowlist.

Usage:
    python3 payload_boundary.py /path/to/agi/repo

Exit: prints a TSV of `path<TAB>verdict<TAB>reason` to stdout, and a summary
to stderr.
"""
import subprocess
import sys
from pathlib import Path


def git_ls_files(repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True, text=True, check=True,
    )
    return [l for l in out.stdout.splitlines() if l]


def gitignore_matched(repo: Path, paths: list[str]) -> set[str]:
    """
    Which of `paths` match a pattern in the repo's own .gitignore (or any
    nested gitignore), evaluated with --no-index so already-tracked files
    are not silently exempted just because git stopped flagging them as
    ignored the moment they were added to the index. This is the mechanical
    reading of "under a directory the engine itself declares transient":
    ask the engine's own version-control config, not our outside judgment.
    """
    if not paths:
        return set()
    proc = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "--no-index", "-z", "--stdin"],
        input="\0".join(paths), capture_output=True, text=True,
    )
    # check-ignore exits 1 when *some* paths don't match -- that's normal,
    # only treat >1 as a real error.
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"git check-ignore failed: {proc.stderr}")
    matched = set(p for p in proc.stdout.split("\0") if p)
    return matched


def is_test_fixture(path: str) -> bool:
    """
    Directory-naming convention, not a filename allowlist: any path that
    passes through a `tests/fixtures/` (or `test/fixtures/`) directory.
    Category reason: these files are synthetic input manufactured for a
    test harness to read -- deliberately fake headings, placeholder JSON,
    dummy directory trees -- authored to be consumed by test code, not to
    communicate anything to a human or an agent forming a thought.
    """
    parts = Path(path).parts
    for i, part in enumerate(parts):
        if part in ("tests", "test") and i + 1 < len(parts) and parts[i + 1] == "fixtures":
            return True
    return False


def is_log_stream(path: str) -> bool:
    """
    Extension-based, category reason: `.jsonl` (newline-delimited JSON) is
    an append-only event-stream format by construction -- one line per run
    event, not one authored thought. This catches every jsonl file whether
    or not it happens to live under a gitignored directory (sessions/*.jsonl
    does; autoresearch.jsonl at repo root does not, despite being the same
    kind of artifact) -- the extension rule is what makes the exclusion
    consistent instead of needing a directory-shaped special case.
    """
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


def main():
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rows = classify(repo)

    for path, verdict, reason in rows:
        print(f"{path}\t{verdict}\t{reason}")

    total = len(rows)
    n_in = sum(1 for _, v, _ in rows if v == "in")
    n_out = total - n_in
    from collections import Counter
    reason_counts = Counter(r for _, v, r in rows if v == "out")
    print(f"\ntotal={total} in={n_in} out={n_out}", file=sys.stderr)
    for reason, count in reason_counts.most_common():
        print(f"  out[{reason}]={count}", file=sys.stderr)


if __name__ == "__main__":
    main()
```

### 2. `extensions/agi/bin/level3.py` — five sites

**Site A — module docstring, opening paragraph.**

Current:
```
Reads the **engine repo** (this repo — `agi`, not the graph repo) and writes one
`type: level3` node per Python file under `extensions/agi/src/**/*.py` and
`extensions/agi/bin/*.py` into `<PROJECT_ROOT>/nodes/level3/`. See
`hyp:level3-node-anatomy` and `goal:g2.1` in the graph repo for the design
this script implements — read those before changing this file's shape.
```
Replacement:
```
Reads the **engine repo** (this repo — `agi`, not the graph repo) and writes one
`type: level3` node per tracked file that passes the G6.8 payload-boundary
predicate (`payload_boundary.classify`, in this directory) into
`<PROJECT_ROOT>/nodes/level3/`. See `hyp:level3-node-anatomy` and `goal:g2.1`
in the graph repo for the design this script implements, and `goal:g6.8` /
`mvp:payload-boundary-predicate` for the scope this script now scans instead
of its original hardcoded prefixes — read those before changing this file's
shape.
```

**Site B — module docstring, scope paragraph.**

Current:
```
Scope is deliberately narrow: `extensions/agi/src/**/*.py` and
`extensions/agi/bin/*.py` only (~70 files). Shell scripts
(`driver.sh`, `find-root.sh`, `cc-session-start.sh`) and the TypeScript
bridge (`extensions/agi-bridge/index.ts`) are out of scope for this first
pass — no ast-equivalent mechanical `how` derivation is implemented for them
here, so scanning them would force a choice between silently skipping their
contract or fabricating one. Neither is acceptable; they are just not
discovered.
```
Replacement:
```
Scope is the G6.8 payload boundary (`payload_boundary.classify`): every
tracked file in the engine repo is `in` unless it is gitignore-declared
transient, sits under a `tests/fixtures/` (or `test/fixtures/`) directory, or
is a `.jsonl` event-stream file — no per-extension allowlist, so shell
scripts, prose, and config are in scope now too, not just `.py` files. `ast`
has no equivalent mechanical `how` derivation for non-Python files, so
`analyze_file` is unchanged: a file it cannot parse gets `parse_ok: false`
and an empty contract, same as a `.py` file with a syntax error, never a
fabricated one. See `verdict:noncode-coverage` for why a real prose contract
(the "why does this file exist" half) is a deliberately separate, unstarted
goal — this scan only buys coverage, not comprehension.
```

**Site C — "Three safety properties" list, item 2.**

Current:
```
2. Prune reach — stamps `origin: level3-scan` and prunes *only* nodes
   carrying that exact stamp. A missing/unreadable engine tree is a no-op:
   nothing is written and nothing is pruned.
```
Replacement:
```
2. Prune reach — stamps `origin: level3-scan` and prunes *only* nodes
   carrying that exact stamp. A missing/unreadable engine tree is a no-op:
   nothing is written and nothing is pruned. A *readable* engine tree whose
   discovered scope comes back empty is treated as a failure, not a valid
   "nothing in scope" state, and also writes/prunes nothing — a real engine
   repo is never empty, so an empty result means the scope resolved against
   the wrong tree, not that the boundary genuinely matched zero files.
```

**Site D — imports block.** Remove the now-dead `subprocess` import (its
only caller, `git_ls_files`, is deleted at site E).

Current:
```python
import argparse
import ast
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path
```
Replacement:
```python
import argparse
import ast
import importlib.util
import os
import re
import sys
from pathlib import Path
```

**Site E — the reuse block + `git_ls_files` + `discover_files`.** This is
the actual scope change.

Current:
```python
_SNAPSHOT_GOALS_PATH = BIN_DIR / "snapshot-goals.py"
_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter


# --- file discovery -----------------------------------------------------------

SRC_PREFIX = "extensions/agi/src/"
BIN_PREFIX = "extensions/agi/bin/"


def git_ls_files(engine_root: Path) -> list[str] | None:
    """Tracked files under `engine_root`, or None if unreadable (no-op signal)."""
    if not engine_root.is_dir():
        return None
    try:
        result = subprocess.run(
            ["git", "-C", str(engine_root), "ls-files"],
            capture_output=True, text=True, timeout=30,
        )
    except Exception:
        return None
    if result.returncode != 0:
        return None
    return [line for line in result.stdout.splitlines() if line]


def discover_files(engine_root: Path) -> list[str] | None:
    """Tracked `.py` files under the two target trees, or None on a no-op.

    `src/**/*.py` is unbounded depth (unlike decompose-engine.py's top-level
    package grouping) — level 3 is per-*file*, so nesting depth is
    irrelevant. `bin/*.py` stays direct-children-only: nested bin/ dirs are
    not part of this scan's declared scope.
    """
    files = git_ls_files(engine_root)
    if files is None:
        return None
    out = []
    for f in files:
        if f.startswith(SRC_PREFIX) and f.endswith(".py"):
            out.append(f)
        elif (f.startswith(BIN_PREFIX) and f.endswith(".py")
              and "/" not in f[len(BIN_PREFIX):]):
            out.append(f)
    return sorted(out)
```
Replacement:
```python
_SNAPSHOT_GOALS_PATH = BIN_DIR / "snapshot-goals.py"
_spec = importlib.util.spec_from_file_location("snapshot_goals", _SNAPSHOT_GOALS_PATH)
snapshot_goals = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(snapshot_goals)
write_frontmatter = snapshot_goals.write_frontmatter

# --- reuse payload_boundary.py's classify() (the G6.8 boundary predicate) ---
# Loaded by file path for the same reason snapshot-goals.py is above (keeps
# the "one function, never re-implemented" discipline this repo already
# applies to write_frontmatter and, via stitch.py, to discover_files itself).
# See `goal:g6.8` / `mvp:payload-boundary-predicate` in the graph repo for the
# rule this implements: every tracked file is `in` unless gitignore-declared
# transient, a `tests/fixtures/` path, or a `.jsonl` event stream.
_PAYLOAD_BOUNDARY_PATH = BIN_DIR / "payload_boundary.py"
_pb_spec = importlib.util.spec_from_file_location("payload_boundary", _PAYLOAD_BOUNDARY_PATH)
payload_boundary = importlib.util.module_from_spec(_pb_spec)
_pb_spec.loader.exec_module(payload_boundary)


# --- file discovery -----------------------------------------------------------


def discover_files(engine_root: Path) -> list[str] | None:
    """Tracked files passing the G6.8 payload-boundary predicate, or None on
    a no-op (missing/unreadable engine root, or not a git repo).

    Previously this scanned only `extensions/agi/src/**/*.py` and
    `extensions/agi/bin/*.py` directly (~74 files) — see `goal:g6.6`, which
    named that scope as the thing blocking G6.1: half the engine (the skill
    doc, the kid brief, the shell surfaces, every non-.py file) was invisible
    to the graph. `payload_boundary.classify()` is the mechanical boundary
    `goal:g6.8` drew to replace it: every file `git ls-files` returns is `in`
    unless it is gitignore-declared transient, sits under a `tests/fixtures/`
    (or `test/fixtures/`) directory, or is a `.jsonl` event-stream file. No
    per-extension allowlist — a non-`.py` file that passes the boundary still
    gets a node; `analyze_file` below already degrades a file `ast` cannot
    parse to `parse_ok: false` with an empty contract, which is exactly the
    honest behavior a non-Python file needs (see `verdict:noncode-coverage`
    for why a real prose contract is deliberately not attempted here).
    """
    if not engine_root.is_dir():
        return None
    try:
        rows = payload_boundary.classify(engine_root)
    except Exception:
        # Any failure in `git ls-files` / `git check-ignore` inside
        # classify() (missing repo, not a git repo, git itself erroring)
        # collapses to the same no-op signal the old git_ls_files() gave —
        # never a partial or guessed file list.
        return None
    return sorted(f for f, verdict, _reason in rows if verdict == "in")
```

**Site F — `main()`, immediately after the existing `files is None` no-op
block.** This is the H0/H0i prune-safety guard (problem 2 below).

Current (the block right after `discover_files` is called):
```python
    if files is None:
        # A missing/unreadable engine tree is a no-op: nothing written, nothing pruned.
        print(f"WARN: engine root {engine_root} is missing or unreadable "
              f"(not a git repo?) — no-op, nothing written or pruned",
              file=sys.stderr)
        return 0

    snapshot_goals._set_project_root(project_root)
```
Replacement:
```python
    if files is None:
        # A missing/unreadable engine tree is a no-op: nothing written, nothing pruned.
        print(f"WARN: engine root {engine_root} is missing or unreadable "
              f"(not a git repo?) — no-op, nothing written or pruned",
              file=sys.stderr)
        return 0

    if not files:
        # H0/H0i guard: an empty scope is never treated as "prune everything".
        # `git ls-files` on a real engine repo is never empty, so a zero-length
        # result here means the predicate resolved against the wrong tree (or
        # some other upstream failure) rather than a genuine "nothing in
        # scope" state. Fail loud as a no-op instead of silently pruning every
        # existing `origin: level3-scan` node — this is the exact shape that
        # cost this project 29k nodes twice before (see CLAUDE.md, TODO.md
        # H0i). Contrast with a *missing* engine root above, which is a
        # legitimate, expected no-op signal on its own.
        print(f"ERROR: discover_files returned zero files for engine root "
              f"{engine_root} — refusing to treat this as authoritative scope; "
              f"no-op, nothing written or pruned", file=sys.stderr)
        return 1

    snapshot_goals._set_project_root(project_root)
```

### 3. `extensions/agi/tests/test_level3.py` — two tests

Current:
```python
def test_discovers_expected_files_and_excludes_out_of_scope(project, engine):
    r = run(project, engine)
    assert r.returncode == 0, r.stderr
    ids = set(level3_nodes(project))
    assert ids == {
        "level3:src-graph-core-init",
        "level3:src-graph-core-node",
        "level3:src-graph-core-persistence-filesystem",
        "level3:src-graph-core-broken",
        "level3:bin-cli",
        "level3:bin-orphan",
        "level3:src-init",
    }
    # nested bin/ dir and driver.sh are out of scope, not merely unmatched
    assert "level3:bin-nested-inner" not in ids
    assert not any("driver" in nid for nid in ids)


def test_files_scanned_count_reported(project, engine):
    r = run(project, engine)
    assert "files scanned: 7" in r.stdout
```
Replacement:
```python
def test_discovers_expected_files_and_matches_g6_8_boundary(project, engine):
    r = run(project, engine)
    assert r.returncode == 0, r.stderr
    ids = set(level3_nodes(project))
    assert ids == {
        "level3:src-graph-core-init",
        "level3:src-graph-core-node",
        "level3:src-graph-core-persistence-filesystem",
        "level3:src-graph-core-broken",
        "level3:bin-cli",
        "level3:bin-orphan",
        "level3:src-init",
        # G6.8 broadened the boundary past src/**/*.py + bin/*.py (direct
        # children only): a nested bin/ dir file and a non-.py file are now
        # in scope too, since neither is gitignored, under tests/fixtures/,
        # nor a .jsonl stream -- exactly the two ENGINE_FILES cases the old
        # test asserted OUT, inverted here on purpose.
        "level3:bin-nested-inner",
        "level3:driver.sh",
    }


def test_files_scanned_count_reported(project, engine):
    r = run(project, engine)
    assert "files scanned: 9" in r.stdout
```

No other test in this file needed a change — verified by running all 20
original tests against the modified module (see "Tests affected" below for
the full accounting).

## Census parents

**Exact count, computed against the real repo, not estimated.** Of the 177
in-scope files, 103 were never in the old 74-file scope. Of those 103 new
files:

- **101 have no matching `idea:engine-*` census unit** (`find_parent()`
  returns `None`) — things like `skills/agi/SKILL.md`,
  `extensions/agi/driver.sh`, all 51 files under `extensions/agi/tests/`,
  `package.json`, `GOALS.md`, root-level docs, the TypeScript bridge. None of
  these live under a directory `decompose-engine.py` ever censused, because
  its own scan is the *same* hardcoded `src/`/`bin/` prefix pair this task is
  replacing in `level3.py` — a sibling instance of the identical scope bug,
  deliberately **not** touched here (see "what this deliberately does not
  do").
- **2 do get a parent**: `extensions/agi/src/graph_core/templates/embeddings.toml`
  and `.../graph-core.toml` — both fall inside the directory prefix of the
  already-censused `idea:engine-graph-core` unit, so the existing
  directory-prefix match (`find_parent`, unchanged) picks them up for free.

Total after the change: **75 of 177 (42%) have a parent, 102 of 177 (58%)
don't** — versus 73 of 74 (99%) before. (The pre-existing lone exception,
`extensions/agi/src/__init__.py`, stays parentless; that is an old,
unrelated gap, not introduced here.)

**Solution: leave them parentless and flagged — do not extend
`decompose-engine.py`'s scope in this change.** `build_node()` already has
the correct machinery for this (it is what today's one orphan,
`src/__init__.py`, already exercises): the frontmatter simply omits the
`parents:` key — never a fabricated or guessed edge — and the body states in
plain text "Census parent: none — flagged", plus a `NO_PARENT:` line to
stdout for every one of the 102. **This satisfies G7.1's referential-integrity
concern precisely because it is an absence, not a dangling reference**: no
node ever points at a census unit that doesn't exist. G7.1 is about broken
pointers, not about every node having a parent.

**The cost, named plainly:** the parentless fraction of the level-3 corpus
jumps from 1% to 58%. That is a real, visible degradation in graph
connectivity for these nodes, not a rounding error — it is exactly the
signal that `decompose-engine.py`'s own census scope needs the same G6.8
treatment `level3.py` is getting here. That is follow-up work, out of scope
for this coverage-only change (widening `decompose-engine.py`'s scan and
minting new `idea:engine-*` units for e.g. `skills/`, `extensions/agi/tests/`,
root-level config is a second, larger change to a different script with its
own unit-boundary design questions — what counts as one census "unit" for a
directory of 51 test files is not obvious and is not this task).

## Prune safety

**Argument.** `discover_files()` can now fail in three ways instead of two:
(1) `engine_root` doesn't exist → `None`, existing no-op path, unchanged.
(2) `payload_boundary.classify()` raises (git failure, not a repo) → caught,
returns `None`, same no-op path. (3) **new risk**: `classify()` succeeds but
returns zero `"in"` rows — impossible on the real repo today (177 files) but
not provably impossible forever (e.g. a future `.gitignore` rewritten to
match `**`, or `--engine-root` pointed at an empty repo). Before this change
that risk didn't exist as a distinct case because the two-prefix scan had no
external classification step that could return "everything excluded" short
of `git ls-files` itself failing.

**Guard added (site F above):** `main()` now checks `if not files` right
after the existing `if files is None` check, and — if the scope is readable
but empty — prints an `ERROR:`, exits 1, and returns before touching
`written_paths`/`stale_generated` at all. The prune block never executes.
This is a hard stop, not a soft warning, because the failure mode being
guarded against is exactly H0i: the parent must run `driver.sh`/live-run and
see it fail loudly rather than see a clean exit-0 log that quietly wiped
every `level3-scan` node.

**Verified empirically, not just argued:** the real dry-run against the live
`agi` + `agi-tree` repos (177 files discovered) reports `stale level3-scan
nodes would prune: 0`. Every one of the 74 previously-scanned files is still
in the new 177-file set (verified directly: `old_scope ⊆ new_scope`, all 74
present), so every existing real `level3-scan` node's `payload_ref` is still
produced this run — nothing stale, nothing pruned.

## Dry-run result

Real numbers, from `python3 level3.py --project /home/ubuntu/work/agi-tree
--engine-root /home/ubuntu/work/agi --dry-run` (full log in
`sessions/iter-9011/kid-l/dryrun-output.txt`):

- **files scanned: 177** (was 74)
- **would create: 102**, **would update: 75** (73 pre-existing real
  `level3-scan` nodes + 2 files that happen to already have a node on disk:
  `src-init.md`, and `skills-agi-SKILL.md.md` — the latter is a hand-minted
  `origin: iter-9007-probe` node from `exp:prose-surface-probe` that this
  change legitimately promotes to a real `origin: level3-scan` node,
  matching exactly what its own body predicted: *"a real scan would never
  write or keep this node"* under the old scope — it now does, correctly)
- **with census parent: 75, flagged NO_PARENT: 102**
- **stale level3-scan nodes would prune: 0**
- contract entries: 2097 derivable, 0 uncovered, 46 files failed to parse
  (37 `.md`, 6 `.sh`, 1 `.ts`, 1 `.sql`, 1 extensionless — all correctly
  `parse_ok: false` with an honest `parse_error`, never a fabricated
  contract)

## Tests affected

Baseline: `python3 -m pytest extensions/agi/tests/test_level3.py -q` →
**20 passed** (confirmed before any change).

After applying the diff (verified in a mirrored copy —
`sessions/iter-9011/kid-l/scratch-repo/` — not the real repo): **49 passed,
2 failed** across `test_level3.py` + `test_stitch.py` together (71 tests
total; `test_stitch.py`'s ~27 all pass unchanged since its fixture's 3 files
were already in-scope under both the old and new predicate). The 2 failures
are exactly the two hardcoded-scope tests named above:

- `test_discovers_expected_files_and_excludes_out_of_scope` (renamed to
  `test_discovers_expected_files_and_matches_g6_8_boundary` in the diff)
- `test_files_scanned_count_reported`

Both fail for the correct reason (asserting the old 7-file/exclude-driver.sh
behavior against the new 9-file scope of the test's own `ENGINE_FILES`
fixture) and both are fixed by the replacement text above. No other test in
`test_level3.py`, and no test in `test_stitch.py` — which imports
`level3.discover_files` directly for its own orphan-file scan — needed any
change; `stitch.py` inherits the new scope for free with zero code change of
its own, since it never re-implements `discover_files`.

## What this deliberately does not do

- **No prose contract.** `verdict:noncode-coverage` already settled that the
  eventual shape is *extracted claims* (directive clauses / numbered rules
  with line numbers), and that it needs a fifth cross-node drift category
  `stitch.py` doesn't have yet. Building that is separate, larger work. Here,
  every file `ast` cannot parse — all 46 non-Python files in the real scan —
  gets exactly what `level3.py` already does today for a `.py` syntax error:
  `parse_ok: false`, an honest `parse_error` string, empty `inputs`/
  `outputs`/`uncovered`. No content is read out of a `.md`/`.sh`/`.ts`/`.sql`
  file and no claim is invented.
- **Does not extend `decompose-engine.py`'s census scope.** Named above under
  "Census parents" — a second, larger change to a different script.
- **Does not fix the pre-existing `src/__init__.py` orphan** — unrelated,
  predates this change.
- **One honesty edge, named but not fixed:** 5 of the 177 files (`package.json`,
  `autoresearch.config.json`, `decompose-engine.goalmap.json`, and the two
  `.toml` templates) happen to be syntactically valid as Python expressions
  (a JSON object literal and TOML `key = value` lines both parse as legal
  Python), so they get `parse_ok: true` rather than `false`. Verified this is
  harmless in practice — `analyze_file` finds zero imports/defs/calls in any
  of the 5, so the emitted contract is `inputs: [] outputs: []`, identical in
  content to what a parse failure would emit, just with a misleading
  `parse_ok` flag. Not fixed here because doing so correctly (distinguishing
  "parses as Python" from "is Python") is exactly the per-extension
  allowlist the G6.8 predicate deliberately avoids; flagging it for whoever
  builds the extracted-claims contract next, since that pass will need a
  real language-detection step anyway.
- **Where the predicate lives, and its own reflexivity:** `payload_boundary.py`
  lands at `extensions/agi/bin/payload_boundary.py`, loaded by `level3.py`
  the same by-file-path way `snapshot-goals.py` already is. It is itself a
  direct child of `extensions/agi/bin/`, so it is in scope under both the old
  *and* new predicate — the very next `level3.py` run mints
  `level3:bin-payload-boundary` for it automatically, no special-casing
  needed. It will land parentless (no `idea:engine-*` census unit named it
  yet), same as the other 101.
