---
confidence: 0.75
evidence_runs:
  - exp:grid-payload-roundtrip
id: "verdict:payload-in-node"
parents:
  - exp:grid-payload-roundtrip
status: open
subgraph: false
tags:
  - g6.3
  - grid
title: "Grid-ref payload roundtrip proves the core claim; reusing commit_file() as-is is unendorsed"
type: verdict
verdict: proved
---

**VERDICT: proved.** The git-plumbing mechanism (`hash-object`/`mktree`/
`commit-tree`/`update-ref`) can carry a level-3 node's payload losslessly —
bytes, exec bit, and symlink target — across real version history. The
`commit_file()` implementation that ships in `grid.py` today cannot, and must
not be pointed at as-is to resolve `payload_ref`.

**Core claim — held:** "A git ref can carry a level-3 node's payload
losslessly" is established with real numbers, not just argued. The mode-aware
variant matched sha256 against an old-way (non-git) baseline for all 4 files
— `bin/grid.py` (100644), `lib/find-root.sh` (100755, exec bit),
`lib/agent-prompt.md` (100644, non-ASCII), and the synthetic
`lib/find-root-link.sh` (120000, symlink) — across 3 version bumps each
(v1→v2→v3, 3 distinct per-file sha256, confirming real edits), matching
G6.3's own bar exactly (>=2 real files, >=3 version bumps). Neither variant
ever had to fall back to the engine-repo disk path to reconstruct correctly
— the hypothesis's literal disproof clause never fired. This is proved at
the mechanism level, using the same four primitives `commit_file()` already
calls, not a hypothetical alternative implementation.

**Explicitly unendorsed:** Two of the hypothesis's three collateral claims
did not survive; one did.

- **"No new command" — survives only at the CLI surface.** `grid commit`
  stays `grid commit`, but the code underneath it is not a zero-change
  reuse: `commit_file()` needs a mode/symlink-aware rewrite (~15-20 lines,
  per the experiment's own estimate) before pointing `payload_ref`
  resolution at it reproduces the passing (mode-aware) result instead of
  the failing (naive) one. The hypothesis undersold this.
- **"Existing grid.py machinery can be reused as-is" — disproved, not
  weakened.** `commit_file()` at `extensions/agi/bin/grid.py:154` hashes
  `str(path.resolve())`, which dereferences a symlink before hashing and
  commits the *wrong object's bytes* — not a dropped-metadata edge case, a
  silently wrong result, with no error or warning. `grid.py:160` also
  hardcodes the tree line's mode to `100644` unconditionally, silently
  downgrading the exec bit on any 100755 payload. The experiment's "naive"
  variant is a literal transcription of `commit_file()` as it ships today,
  and it reproduced both failures exactly: exec bit dropped on
  `find-root.sh`, and `find-root-link.sh` materialized as a regular file
  with the wrong content (sha256 `1ee3aa9f...` vs. the correct
  `dbe4c5a1...`), not merely the wrong mode.
- **"Zero new frontmatter" — survives untouched.** This claim is about
  `payload_ref`'s shape (stays a path-like pointer string; only its
  resolution rule changes), not about `commit_file()`'s internals. Nothing
  in the experiment required a new frontmatter key, and the mode-aware fix
  is entirely inside the resolution/commit code path.

**What this means for G6.3:** The falsifier is passable — the version layer
*can* become a source of truth for a build node's payload — but not by
wiring `payload_ref` resolution to `commit_file()` as it exists today. G6.3
needs the mode-aware rewrite of `commit_file()` (and a matching
mode/symlink-aware read path in `stitch.py --out`) written first. Until that
lands, "payload lives in the node's grid ref" is a proved *design*, not a
proved *deployment* — the gap is real, small, and unwritten, not a wall.

**What this means for G6.7:** Yes, D4 inherits the same defect, and worse:
structurally, not incidentally. D4's plan is to `mktree` each build node's
payload directly into the release tree using the same plumbing primitives —
if that machinery is the unmodified `commit_file()`/naive path, D4 will
silently mis-hash any symlinked payload and downgrade any exec-bit payload
across the *entire* published engine tree in one atomic commit. Atomicity
(G6.7's own selling point — "either the ref moves or nothing happened")
does not help here, because the tree it atomically publishes would simply
be the wrong tree, moved cleanly. D4 must depend on the same mode-aware
rewrite this verdict requires for G6.3, applied before its own falsifier is
attempted, not discovered after. That rewrite is shared infrastructure: G6.3
and G6.7 are not two defects to fix separately, they are one fix with two
callers.
