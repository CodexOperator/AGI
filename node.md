---
id: goal:g7.16.1.11.46.16
mint_id: 785a56ca1046434badd968bce6a1719e
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-3
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
status: complete
title: "G7.16.1.11.46.16: G1a -- ONE grid namespace refs/grid/node/<mint>, written additively: each diverged pair merged with the live tree, the writer re-pointed in the same land, a five-number census cell"
town: local-maxxing
---
# goal:g7.16.1.11.46.16

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §25, §34.5. Box readings at d2ab3c19b8: 6010 refs under refs/grid/local-maxxing/node and 3807 under refs/grid/node; every one of the 3807 also has a local-maxxing ref, and ALL 3807 pairs have DIVERGED (0 share a tip, neither side is an ancestor); over all 3807, 2073 pairs have equal trees and 1734 do not; refs/grid/node/* has been frozen since 09-21 11:47Z, while local-maxxing is the live writer (newest 10-25 17:32Z); a ref named TBD exists in both namespaces (K2, sp G1a-T). K3: 22 local-maxxing mints have no mint_id in any trunk node file, where the brief says 46. Council picks 3/3: ADDITIVE only (sp 1 over aio's archive move: a move is a delete on the remote); G1a-T and G1a-W (sp).

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.16 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 8.1 | "seat_status.py retire" | CLOSED: leaf:goal:g7.16.1.11.46.16 (seat_status.py retired; owner ruling 05:0xZ 10-26) |
| 4.3 | "census: count tips; old versions as deprecated?" | CLOSED: leaf:goal:g7.16.1.11.46.16 (`grid.py census`: tips yes; versions are commits, not deprecated nodes) |

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
director-general-3 gen 19, 10-27 ~16:5xZ: CLOSED (status complete), on the falsifier AS WRITTEN, measured on the landed trunk 6f7b9ae3d9 (L214's wrap; SM's [landed] 16:37Z asked whether it closes). This version differs only by the close: status, edited_by, the two owner atoms' state; the build record that stood here (G1a, the third history, census orphans, the unrelated-root unify, the fixture class, item 2 + part (B)) is the previous grid version (`grid.py diff goal:g7.16.1.11.46.16`).
ROW 1: extensions/agi/tests/grid-namespace.t.sh on the tip: 61 ok, 0 FAIL, rc 0 (the mutants included); on the LIVE refs `grid.py unify --check`: unified 6026/6026 (refs/grid/local-maxxing -> refs/grid; snapshot 20261026T072045Z, 3807 refs) -- 6026, not the 6025 written, being one mint more since the falsifier was written: N/N is the row.
ROW 2: the newest tip under refs/grid/local-maxxing/node is 10-26 06:32:10Z (well over an hour after the host act, and nothing since: 0 changed); the writer lands on refs/grid/node (the newest there 10-27 16:33:56Z); the hold rows w0, t9a-c green in the lane.
ROW 3: `grid.py census` rc 0: mints=6318 live=6070 retired=248 versions=61656 orphans=309 double_mints=10 never_landed=299 unclassified=0.
ROW 4: the lane's negative rows (no delete, node/ + session/ push specs only, the forced wildcard fetch spec and the config-check mutants RED) green. NOT read by me: the live `git push --dry-run` of the refspecs (my uid has no origin credentials, rc 128); it is belam's one reading at the gate.
CARRIED, named, none a falsifier of this goal (no new goal invented): (i) the 40 CONFLICT pairs of the origin unify stay the OWNER's batch (card-belam §6). (ii) The orphan count rose 22 -> 309 by the origin-snap adoption, not by a writer: 284 of the 299 never-landed are origin-only names (287 adopted, never on this trunk), 15 are local (14 experiment:a00-* + 1 hypothesis, 17 at 10-26); double_mints 5 -> 10, the 09-29 five (goal:g7.31.3.3.1-.5; .4's ghost is on origin too) plus five new, all from origin: goal:g7.33.9 (FIVE versions, so a real choice, unlike the one-version 09-29 ghosts), goal:g7.32.5, experiment:a00-db75bb99-6d7472, experiment:a00-230456c1-1abcda, and hypothesis:a00-1467544f-chain-600hop under a malformed ref name refs/grid/node/hyp/a00-1467544f-chain-600hop (not a 32-hex mint). The commit-path double-mint refusal (row (5)) is in grid.py (double_mint_holder) and its lane is green. (iii) refs/grid/et-grok-pilot (460 on origin) stays outside grid.py, as R6 named. (iv) refs/grid/local-maxxing removal is an OWNER act (card-belam §6). (v) crons.py retire (atom c2) was never in this goal.
<!-- THOUGHT:END -->
