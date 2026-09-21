---
id: idea:engine-stitch
mint_id: db49423d700447349931cf1632f092e2
type: idea
parents:
  - goal:g6.1
confidence: 1.0
edited_by: season.py
origin: engine-decomp
scale: small
season: 1
status: open
tags:
  - engine
  - census
  - l19
thought_session: season
title: "Engine surface: extensions/agi/bin/stitch.py"
unit_kind: bin_script
unit_path: extensions/agi/bin/stitch.py
---
`extensions/agi/bin/stitch.py` — an engine bin entry-point script.

stitch.py — materialize level-3 nodes back into a runnable directory tree.

Reads `<PROJECT>/nodes/level3/*.md` (the graph repo) and either:

  --out DIR     resolve every level-3 node's `payload_ref` against the
                **engine repo** and copy that file into DIR, preserving the
                repo-relative path (`extensions/agi/bin/metrics.py` lands at
                `DIR/extensions/agi/bin/metrics.py`). This is the "graph is
                the source of truth" round trip stated in `goal:g6.1`.

  --verify      write nothing; report drift between the graph and the live
                engine tree in four categories (see below). This is the more
                valuable mode — it is the thing a plain `cp -r` cannot do at
                all, because `cp -r` has no independent record of what the
                tree is *supposed* to contain.

**Be honest about what this is.** Source code lives on disk exactly once —
never inlined into a node (`hyp:level3-node-anatomy`). A level-3 node is a
pointer (`payload_ref`) plus a mechanically-derived contract of that file's
imports/exports. So for an *existing* repo, `--out` materialization is
near-identity: resolve 73 pointers, copy 73 files. It is not a compiler and
it does not reconstruct anything `cp -r extensions/agi DIR` would not also
produce, byte for byte, given the same source tree.

**What the graph adds that `cp -r` cannot**: `cp -r` has no opinion about
whether the tree it copied is *complete* or *correct* — it just moves bytes.
The graph is an independent, separately-mintable claim about what the tree
should contain, so it can be checked against the tree instead of trusted
blindly. `--verify` turns that claim into four concrete checks a `cp -r`
literally cannot perform because it has nothing to compare against:

  1. missing_payload   — a node's `payload_ref` no longer exists on disk
                          (the node outlived the code).
  2. orphan_files       — a file in level3.py's scan scope
                          (`extensions/agi/src/**/*.py`, `extensions/agi/
                          bin/*.py`) with no level-3 node claiming it (the
                          code outran the graph).
  3. duplicate_payload_ref — two or more nodes claim the same `payload_ref`
                          (ambiguous materialization; the anatomy node says
                          reject this at mint time — level3.py does not
                          currently enforce that, so this is also a level3.py
                          gap this script surfaces, not just a stitch-time
                          check).
  4. stale_contracts    — a node's contract block (the mechanically-derived
                          `how` half: imports, top-level defs, read/write
                          call sites) no longer matches what re-running the
                          *same* derivation against the *current* file would
                          produce.

On (4): the obvious design is a content hash of the source recorded in the
contract block at mint time, compared against a hash of the current file.
This script does **not** do that, and the reason is not laziness — it is
strictly worse than what it does instead, for this specific job:

  - No node in the corpus carries a mint-time hash (level3.py, which this
    script does not own, never wrote one) — there is nothing to compare
    against retroactively for the 73 real nodes. A hash-based check could
    only start protecting nodes minted *after* the generator is changed to
    add one; it is silent about every node that already exists.
  - A hash is binary (changed / not changed) and coarse — it fires on a
    changed docstring or a renamed local variable exactly as loudly as it
    fires on a changed import. It cannot say *what* drifted, so a human (or
    another agent) still has to re-derive the contract by hand to find out,
    which is the same `ast` walk this script already needs to do to compute
    the hash's comparison target in the first place. The hash adds a stored
    field and a mint-time write path; it does not remove the recompute step.
  - `how` is *specified* as mechanically reproducible (`hyp:level3-node-
    anatomy`, `exp:level3-scan-r1`) — deterministic given the same source
    text and the same `ast`-walk code. That means the freshness check does
    not need a stored fingerprint at all: this script re-runs the exact
    same derivation level3.py used (`level3.analyze_file`, imported by file
    path, never re-implemented — same reuse discipline level3.py itself
    uses for `write_frontmatter`) and diffs the result against what is
    stored, entry by entry. That is strictly more informative than a hash
    match/mismatch, and it costs nothing extra to store — the file is
    already being read for the missing/orphan checks in the same pass.

What a hash *would* still buy, and what this script cannot claim instead:
change detection that does not require re-running the deriving code, i.e. a
freshness check for a language `ast` cannot parse, or a `how` derivation
that stops being a pure function of the file (grows external inputs). The
recompute approach used here is coupled to `level3.py` staying importable
and staying a pure function of file content — a real cost, named plainly:
if `analyze_file`'s logic changes shape (new fields, new heuristics) without
this script's comparison logic changing to match, every existing node looks
"stale" even though nothing about the underlying code moved. That false
positive is not hypothetical — it is exactly what happens the day someone
edits level3.py's derivation and forgets this script exists. There is no
mint-time marker that would help there either; only keeping the two files
walked together (as this script already notes it must) prevents it.

**Scope limits, stated plainly:**

  - Materialization treats every node under `nodes/level3/*.md` as canonical
    (copies its `payload_ref`). The anatomy node describes a possible future
    "non-canonical / sub-file" node that would be read-only and skipped —
    no such node currently exists in the real corpus (verified: all 73 are
    one-node-per-file, per `exp:level3-scan-r1`) and there is no frontmatter
    field distinguishing the two shapes yet, so this script cannot honor
    that distinction; it is not implemented, not silently ignored.
  - `--verify`'s orphan-file scan reuses `level3.discover_files`'s scope
    definition exactly (imported, not reimplemented) so "orphan" always
    means "outside the graph but inside level3.py's own declared scope" —
    never a guess at what *should* have been scanned.
  - Non-`.py` engine files (`driver.sh`, the TypeScript bridge) have no
    level-3 nodes at all today and are correctly invisible to every check
    here — they are out of level3.py's scope, not silently dropped by this
    script.

Run:
    python3 bin/stitch.py --project PATH --verify [--engine-root PATH] [--strict]
    python3 bin/stitch.py --project PATH --out DIR [--engine-root PATH] [--force]

Generated by `decompose-engine.py` (see `idea:engine-self-decomposition` in the graph repo for the census design). This node records that the surface exists; it is not itself a design argument.