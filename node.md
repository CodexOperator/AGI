---
id: exp:graph-first-engine-publish
mint_id: 3f7c1a94e0b2489d8c5e6a7b0d1f2e34
type: experiment
parents:
  - hyp:payload-in-node
confidence: 0.9
edited_by: season.py
evidence_runs: 1
season: 1
subgraph: false
tags:
  - g6.1
  - g6.3
  - grid
  - stitch
thought_session: season
title: "Deploying the grid-ref payload: 180/180 byte-identical, 16 exec bits kept, and two real engine fixes that never touched the engine repo"
---
**What was run,** on the live corpus and the live engine, not a sandbox — the
sandbox half was `exp:grid-payload-roundtrip`, which proved the *design*; this
is the deployment that verdict explicitly declined to claim.

**1. The mode-aware rewrite S9 asked for, in `commit_file()`'s real call path.**
Three functions replace the two defective lines: `git_mode()` (`os.lstat()` →
`100644`/`100755`/`120000`), `hash_path()` (a symlink's blob is its
`readlink()` text via `hash-object --stdin`, and `os.path.abspath` replaces
`Path.resolve()` so the final component is not dereferenced), and
`materialize_entry()` — the inverse, which is the "matching mode/symlink-aware
read path" S9 named and nothing had. `commit_file` builds a two-entry tree,
`node.md` + `payload`, and compares the **whole tree** against the ref tip
rather than `node.md` alone.

**2. `grid.py commit --all` over 765 nodes.** 185 nodes carry `payload_ref`;
all 185 committed a payload, 0 unresolved, **0 errors from a missing
`mint_id`** — the S14 hook meant no backfill pass was needed, including on the
run immediately after two generators had minted new nodes, which is the exact
case that needed a second pass twice on 2026-08-25.

**3. The falsifier: materialise twice and compare.**
`stitch.py --out A` (engine tree) against `stitch.py --out B --from-grid`
(the nodes' own refs), then sha256 every file and read every mode.

| check | result |
|---|---|
| files written, each side | 180 / 180 |
| sha256 identical | **180 / 180** |
| modes vs the engine's own `git ls-files -s` | **180 / 180**, incl. all **16** `100755` |
| symlinks in the engine index | 0 — `120000` is covered by tests, not by this corpus |

The only difference on disk is the group-write bit (`0o664` vs `0o644`,
`0o775` vs `0o755`). That is not drift: git's tree format tracks the exec bit
and nothing else, so `--from-grid` reproduces exactly what `git checkout` of
the engine produces, and the `664` is this machine's umask on the engine
working tree. Compared against the engine's own index — the right baseline —
agreement is total.

**4. Two real engine changes made entirely from the graph.** `S12` (goal
bodies truncate visibly, at a block boundary, at a configurable cap; 83 lines
plus 87 lines of tests) and `--grid-version` (materialise a chosen version
rather than the tip). Both: edit `payloads/<payload_ref>` → `grid.py commit
--all` → `stitch.py --out <engine> --from-grid --publish`. `git status` in the
engine repo showed **exactly the files the graph changed, and nothing else.**
A third followed for `skills/agi/SKILL.md` — a prose surface, so the same path
carries `goal:g6.8`'s "philosophy and instruction prose … belongs in the `agi`
repo, arriving there from a node in `agi-tree`".

**5. Post-conditions.** `pytest extensions/agi/tests/` — **619 passed** against
the published engine (up from 599 pre-change; 20 new regression tests).
`stitch.py --verify` reports **0** in all four drift categories.
`node_count` held at **765** across every snapshot (G7's first invariant).

**What this does not show, stated so nobody reads it as more than it is:**

- **The reverse direction is still engine-first.** `level3.py` derives every
  contract by reading the engine tree, and `--verify` compares against files
  there. A payload edited only in the graph has a stale contract until it is
  published and rescanned. Nothing here tests derivation-from-ref because
  nothing implements it.
- **`120000` was never exercised on real content**, because the engine has no
  symlinks. The regression suite covers it; this corpus cannot.
- **The bootstrap was a direct engine edit.** The change enabling graph-first
  edits could not itself be made graph-first. One instance, recorded, not
  repeated.
- **The publish is not croned**, deliberately — `goal:g6.5` step 2 is
  unblocked, not automated, and should stay manual until the derivation
  direction closes.