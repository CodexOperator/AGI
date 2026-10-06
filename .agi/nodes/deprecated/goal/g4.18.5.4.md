---
id: goal:g4.18.5.4
mint_id: e3412530feb44ab38d2622e7846abb79
type: goal
parents:
  - goal:g4.18.5
next_edges: []
confidence: 0.7
edited_by: self-perpetuating
goal_id: G4.18.5.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: e77a6464d65466bc
season: 2
seeds: []
status: retired
tags:
  - s-goal-retirement
  - from-s21
  - retire
  - payload
title: "G4.18.5.4: moving a node address is ONE verb -- write.py retire (status + move, + payload removal for a build) and write.py renumber (mint_id kept, file + id + goal_id + parent edge + every reference re-pointed, old -> new THOUGHT), each ONE commit behind the write gate, for any node type (from goal:s21)"
town: core
---
# goal:g4.18.5.4

## OWNER 2026-09-30 01:2xZ, verbatim (relayed by alive gen 3, belam's post-reboot owner-task)
"All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals."

## Why this exists
goal:g4.18.5 (a write is ONE commit behind the permission layer): goal:s21 ("the graph can add a file to the engine but can never remove one") was retired on the owner's line above. It was measured at 02:1xZ 09-30 (self-perpetuating, read-only survey). Its hazard faded in practice: the five pre-fold files were removed by hand (6c3fe0673), the publish cron that could resurrect them is gone (de5507a17), and grid.py and links.py count a retired node's missing payload apart (a70ad4312). But the capability was never built. Retiring a build node together with its payload is a hand-made multi-step commit (deprecate, move, remove the engine file: 6c3fe0673, b8d232fc6, de5507a17) that no write.py verb performs, and stitch.py's `missing_payload` (stitch.py:489-498) still flags every retired payload whose file is gone under `--verify --strict`.

## Target end-state
- ONE verb retires a node of any type: `write.py retire <id>` sets the retired status the type schema names, moves the node where that type retires to, and for a build node also removes its payload file from the engine tree, all in ONE commit behind the same authorship gate as every write. The node and its grid ref are never deleted.
- ONE verb renumbers a node: `write.py renumber <id> <new id>` keeps the mint_id, moves the file, rewrites id + goal_id + the parent edge, re-points EVERY reference in the same commit, and records old -> new in the THOUGHT. Measured need (all-is-one lens 02:3xZ 09-30): FOUR renumbers were hand-made tonight (Opus refutation pass 05:3xZ): b9dc2c83b and 089d1369a (git renames), aa0bf6357 (s33 -> g4.18.2.1, add + delete) and s1 -> g1.6.1, because write.py refuses to set `id` (node_writer.py:668 MINTED_IDENTITY) and has no verb for it. The s1 renumber shows the hazard: write.py committed the new file (72cf37100) and the old file was removed only in d6f26f856, so for about three minutes TWO live files shared one mint_id. A renumber verb makes that one commit.
- `stitch.py --verify --strict` treats a deprecated node's absent file as retired, not drift.
- `--grid-version N` still yields the file as it was before retirement.

## Invariants
- A retirement never deletes a node or a grid ref: `active_node_count + deprecated_node_count` never drops.
- Only a payload whose node is deprecated in the same commit is ever removed.

## Falsifier
1. One test runs retire -> `grid.py commit --all` twice, then checks: the file is absent, `stitch.py --verify --strict` WITHOUT --from-grid reports 0 (with --from-grid, :998 already skips grid-held payloads, so the test would pass on today's code), and `stitch.py --from-grid --grid-version <pre-retire N> --out DIR` writes the file.
2. `write.py renumber goal:<a> goal:<b>` on a node with N referencing nodes leaves 0 live hits of the old address, the same mint_id, and one commit.
3. Negative: a `retire` on a node whose payload another live node still claims refuses by name and writes nothing, and a `renumber` onto an existing address refuses by name.

## Out of scope
goal:g6.7 (publish the engine as a grid ref) · goal:g7.16.1.6 (the write form) · s21's open question on files that have NO node at all (autoresearch.jsonl, the "139 unmanaged"): that question stays with goal:s18's successor, not here.

## Agent Notes
Assigned to **the council** (placement).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by self-perpetuating (council S-goal pass, alive convening) from goal:s21 remainder on the owner 01:2xZ 09-30 line; KEPT under g4.18.5 by all-is-one ("a write verb belongs with the write"). WIDENED on all-is-one lens (02:3xZ): retire and renumber are the same missing act, moving a node address, for EVERY type; three renumbers were hand-made tonight (b9dc2c83b, s35 -> g4.18.8, s1 -> g1.6.1), each a git mv plus a hand id edit because write.py refuses to set id. Two hand multi-step paths = the next one-source census FAIL row (goal:g7.16.1.1.6).
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
