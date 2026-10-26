---
id: goal:g7.16.1.11.46.16
mint_id: 785a56ca1046434badd968bce6a1719e
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: alive
goal_id: G7.16.1.11.46.16
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - G1a
season: 3
status: active
title: "G7.16.1.11.46.16: G1a -- ONE grid namespace refs/grid/node/<mint>, written additively: each diverged pair merged with the live tree, the writer re-pointed in the same land, a five-number census cell"
town: local-maxxing
---
# goal:g7.16.1.11.46.16

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §25, §34.5. Box readings at d2ab3c19b8: 6010 refs under refs/grid/local-maxxing/node and 3807 under refs/grid/node; every one of the 3807 also has a local-maxxing ref, and ALL 3807 pairs have DIVERGED (0 share a tip, neither side is an ancestor); over all 3807, 2073 pairs have equal trees and 1734 do not; refs/grid/node/* has been frozen since 09-21 11:47Z, while local-maxxing is the live writer (newest 10-25 17:32Z); a ref named TBD exists in both namespaces (K2, sp G1a-T). K3: 22 local-maxxing mints have no mint_id in any trunk node file, where the brief says 46. Council picks 3/3: ADDITIVE only (sp 1 over aio's archive move: a move is a delete on the remote); G1a-T and G1a-W (sp).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.16 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 8.1 | "seat_status.py retire" | target:the §34.5 census-cell leaf (wave 2) |
| 4.3 | "census: count tips; old versions as deprecated?" | target:§34.5 (tips yes; versions are commits, not deprecated nodes) |

## Target end-state
- refs/grid/node/<mint> is the one namespace: per mint, its tip is a two-parent merge whose ancestors include BOTH old tips, and whose tree is the local-maxxing tip's tree (the live side).
- grid.py commit and grid_sync's push write refs/grid/node/<mint>, re-pointed IN THE SAME LAND as the merge.
- The census cell carries five numbers (mints · live · retired · versions · orphans), each one git command; the TBD ref is named, and 22 vs 46 orphans is reconciled by ONE pinned command before the cell is trusted.
- refs/grid/local-maxxing/* stays READ-ONLY: no delete is pushed. Its removal is an OWNER act, banked in card-belam §6.
- seat_status.py is retired (owner atom 8.1; status deprecated, moved under deprecated/, never deleted) once the census cell answers what it answered.

## Invariants
- Delete 0: no grid ref is deleted locally or on the remote by this leaf.
- A grid ref outlives its file (CLAUDE.md): retired nodes' refs merge like live ones.
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
(sharpened by the builder, director-general-3 10-26, and RE-CUT 10-26 under the council's rows R1-R6, alive 01:53:32Z 3/3; every change is named in the THOUGHT)
1. `sh extensions/agi/tests/grid-namespace.t.sh` exits 0: per mint, both old tips are ancestors of the new tip, `rev-list --count` new >= max(old), tree(new tip) == tree(legacy tip at the merge), m/m, measured in shell AND by `grid.py unify --check`, which trusts only the verb's OWN pre-write snapshot and the `Unify-Frozen: <old tip>` trailer of each merge (no caller-supplied file exists); mutants (each reads RED): one version dropped, one 09-21 tree carried on an unequal pair, a late snapshot plus a dropped version, a merge with no trailer. On the LIVE refs the host act runs `grid.py unify --check`: `unified 6025/6025`.
2. Read one hour after the land: refs under refs/grid/local-maxxing whose tip changed since the land = 0, and the land's probe edit is ONE commit on refs/grid/node/<mint> (lane rows w1, w2); mutant: the writer left alone (storage_trunk still the legacy namespace) -> 1 changed, RED. Before the unify, and after a pre-land writer strands a version in the legacy namespace, the writer HOLDS that mint (rc 1, naming `grid.py unify --write`), never forks; one more unify merges it (rows w0, t9a-c); mutants: the hold cut out -> a fork, RED; the legacy listing's rc ignored -> a fork, RED.
3. `grid.py census` prints `mints= live= retired= versions= orphans=`; a failed git command (a bad `--rev`), either namespace listing 0 refs, or a tip with no frontmatter prints `unread (...)`, rc 1, never 0; mutant: the empty-listing check cut out prints numbers, RED.
4. Negative: `git push --dry-run` of the land's refspecs lists 0 deletes, every ref the remote had is still there with its old tip an ancestor of the new one, `push-changed` never pushes a legacy ref again, and a fetch from a remote still at the frozen tips moves no merged tip (the fetch specs are node/ and session/, never forced); a `grid.legacy_namespaces` that is mis-typed refuses `commit` by name with 0 refs written. Mutants: a unify variant that deletes (RED), the namespace-wide push prefix (RED), the forced wildcard fetch spec (RED), the config check cut out (RED).

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.24 V4 · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-26 (v3 = the council's re-cut, alive 01:53:32Z 3/3, R1-R6): what G1a is in code, what it measured, and what is NOT done.
WORDS (R1): LEGACY = refs/grid/local-maxxing, the namespace every writer used until this land (6025 refs, live until then); refs/grid/node = the 09-21 FREEZE (3807 refs), which becomes the one namespace. "Live" never means refs/grid/node. The merge carries the LEGACY (current) side's tree.
CODE (one commit, grid.py + the lane): (1) config `grid.storage_trunk = refs/grid` and `grid.legacy_namespaces = [refs/grid/local-maxxing]` is the writer re-point (G1a-W); the namespace refusal exempts a declared legacy namespace; the branch-blind refusal is lifted when the trunk is DECLARED. (2) `grid.py unify [--write] [--into NS] [--legacy NS] [--check]` (dry-run by default, the commit-all flock, refused when grid_retired): per mint of each legacy namespace, a missing refs/grid/node ref is created at the legacy tip, a ref already inside the legacy history fast-forwards, a diverged pair gets ONE two-parent merge (tree = the legacy side's, FIRST parent = the legacy tip so `--first-parent` versions keep counting the live chain: a mint of 3 versions merges as v4, the next writer is v5), a mint whose history already holds the legacy tip is unchanged. Every write goes through ONE helper `_cas`; there is no delete. (3) R2: `--write` records its OWN pre-write `for-each-ref refs/grid/node` snapshot under the lock immediately before its first CAS (file in the sessions dir, created exclusively, never overwritten, path printed; a run that writes nothing leaves none), each merge carries `Unify-Frozen: <the new-side tip it took in>`, and `--check` reads ONLY the earliest snapshot and asserts per mint: both old tips ancestors, count >= max, the merge's tree = the legacy tree, the trailer = the second parent, != the current tip, and the snapshot tip = the trailer or inside it (a later delta merge records the earlier merge, which holds it). `--before` no longer exists; the host's step (a) file is the human record only. (4) The writer HOLDS a mint whose legacy tip is not in its ref's history (named line, counted, rc 1 naming `grid.py unify --write`). R4: the legacy tips are read ONCE per run by one for-each-ref whose rc is checked (a failure refuses the whole commit as unread, 0 refs written: a failed read can no longer look like 'no legacy ref'), and a present-but-malformed `grid.legacy_namespaces` (a string, a non-string item, a name outside refs/grid, the writer's own namespace) refuses commit and unify by name. (5) R3: `fetch_specs_for` = node/ and session/ only, never forced (`+refs/grid/*:refs/grid/*` would let a fetch from a remote still at the frozen tips move a merged tip back, and reached the legacy namespaces); `cmd_init` configures both; push-changed lists node/ and session/ only. (6) `grid.py census [--rev R]` = doc 34.5's five numbers, each from one git command, unread never 0. (7) The writer scanner node goal:g7.16.1.11.13 is RE-CUT (C1, C2, C3 blocks, rows W9, W11, W12, the G-E2 sentence), as that node requires for a new ref writer; the gate reads it.
MEASURED on the live refs in a scratch copy (nothing written in the live repo; first build, before R2-R4): 6025 legacy refs, 3807 frozen, ALL 3807 diverged; dry-run 3807 merged, 2218 adopted, 0 conflict of 6025 (2 min); --write 4 min; check 6025/6025; a second --write 0 changed. Census before: mints=6025 live=5779 retired=246 versions=8345 orphans=22. K2: the ref named TBD is a real node (experiment:a00-a2edba9e-75e24c has `mint_id: TBD`) in both namespaces; it merges like any mint. K3: the 22-vs-46 gap is one pinned command, `git grep -h '^mint_id:' <rev> -- .agi/nodes` set-differenced against `git for-each-ref refs/grid/node` = 22 at 695c008dfd (and 2 files with a mint_id and no ref); the brief's 46 was 5991 minus 5945, two different populations.
HOST ACT (R5; belam's, once, AFTER the gate's GO; additive, no rollback: once grid_sync pushes, every old tip stays an ancestor): (a) `git for-each-ref refs/grid/node` into a file (human record); (b) BEFORE the land, from the tip's checkout, `grid.py unify --into refs/grid --legacy refs/grid/local-maxxing --write` (~4 min; the pre-land writers go on); (c) the land; (d) at once `grid.py unify --write` again (only the mints versioned meanwhile merge; until then the writer holds them, rc 1, never forks); (e) `grid.py unify --check` -> unified 6025/6025, then `grid.py census`; stamp the time. (f) the stranded-writer lap: the hold lives only in NEW code, so a writer on PRE-land code (a detached trunk clone that has not merged the trunk, the board's old clone, a post mid-turn) keeps versioning into the legacy namespace after (d) and closeouts would HOLD again. For ONE lap after (e) the grid_sync chain runs `grid.py unify --write` too (idempotent: a second run moves nothing). The lap closes when `git for-each-ref --sort=-committerdate --count=1 --format='%(committerdate:unix)' refs/grid/local-maxxing/node` shows no tip newer than the (e) stamp for a full lap; then (f) leaves the chain. Lane rows t8, t9a-c, w0 are the legacy-commit-after-unify mutant (the next writer HOLDs; one more unify merges it). Rotation closeouts run grid commit --all: keep (c) to (d) short.
ADDITIVE ONLY (picks 3/3): refs/grid/local-maxxing is read, never deleted, never pushed again; its removal is an OWNER act, banked for card 6.
NOT COVERED, named (R6): refs/grid/et-grok-pilot/node holds 460 refs on origin and 0 locally; grid.py never names it, so unify and census do not cover it and the census is NOT remote-wide; the push narrowing deletes nothing there. The lane's TRUE row count is 49 rows (0 FAIL), not the 40 first reported.
NOT DONE, named: owner atom 8.1 'seat_status.py retire' stays OPEN (council 3/3: it does not invent the replacement). The reader census (every importer of seat_status.py x which of its four answers each reads: registry, meter fractions, lease count, cost roll-up) is made first and handed to belam for ONE owner question. The census cell's `orphans` counts against the composed view of `--rev` (default HEAD), the trunk, not a post's partial view.
RE-CUT 3 (GATE267, SM early notice 04:4xZ 10-26): test_commands_manifest.py flagged grid.py verbs census + unify as undeclared (pytest 1 failed, 1386 passed on the merged tree). Declared in command:commands: grid.py:census as a manifest entry (read, proposable), grid.py:unify as an excluded entry with its reason (--write adds merge commits to the grid refs: additive, compare-and-swap, no delete; the host act is belam's once after the gate; the bare form is a dry run). No code change; the re-cut is the G1a tip on the live trunk plus those two entries, one commit.
<!-- THOUGHT:END -->
