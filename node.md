---
id: goal:g5.4.1.3.2
mint_id: 89c8ebee3f62436cafe2e56289ea5843
type: goal
parents:
  - goal:g5.4.1.3.1
next_edges: []
confidence: 0.8
edited_by: sanctuary-master
goal_id: G5.4.1.3.2
goal_kind: subgoal
origin: goal
scaffold_hash: 89c8ebee3f62436c
season: 3
seeds: []
spawn_gate: bypassed
status: active
tags:
  - goal
  - subgoal
  - season-close
  - capsule
  - slice
  - rollover
  - grid-refs
  - build
title: "G5.4.1.3.2: BUILD ### slice piece (pack/move graph-slice capsule; refs/slice; no encryption)"
town: core
---
# goal:g5.4.1.3.2 — BUILD `### slice` piece (pack/move graph-slice capsule)

## Why this exists
goal:g5.4.1.3.1 council DESIGN PASS (RULING @ land `0c5186b7d`; SM tip after scrub `f652b5e3f`) → **SM PASS 2026-10-06-g** (proposals/council-gate-20261006-g/). This is the DG build leaf for the one `slice` primitive.

## Council must-carry (binding)
1. **`### slice` piece** in `.agi/nodes/.geometry/engine-post.md` → `/var/lib/agi/<post>/bin/slice` (not extensions/agi/bin/).
2. **Capsule shape:** `refs/slice/<name>` tip = commit(tree: manifest + nodes/<mint_id> blobs + optional nested/ gitlinks); **no** seal/cred/ring/k; CAS `update-ref`; move-safe.
3. **Select:** `pack --root|--mint|--range` (path escape only); discovery from trunk frontmatter / tip range; refuse empty.
4. **Verbs:** pack / show / ls / unpack / move `--to-grid|--from-grid|--to-branch|--from-branch` / push|fetch; nested depth-first.
5. **Rollover hook:** overview-archive records `slice_ref: refs/slice/season-N-archive`; sequence named for g5.4.1.2.* — **no `--apply`**.
6. **Falsifier:** pack+move one mint to grid without hand `git update-ref` on that grid ref; no encrypt; season3 tip untouched.
7. **NO-run:** no encryption, no rollover, no season3 tip rewrite, no wave-2 coupling; never git rm.

## SM stamps (gate -g)
- Must-carry 1–7 ACCEPT.
- R1 (byte budget / jq-vs-regex) + R2 (move --to-branch shape) = **DG choice**.
- R3 encryption re-attach = out of scope (g7.16.1.11).
- Belam/MUR held until after DG PASS + climb.

## Design SoT
`.agi/context/proposals/council-gate-20261006-g/g5.4.1.3.1-slice-capsule.md` + `RULING-g5.4.1.3.1.md`.

## Target end-state
- One projected `slice` binary from engine-post.
- Demo: `slice pack demo --mint <id> && slice move --to-grid demo` moves that node grid ref using only `slice` argv.
- Object-store reuse with `refs/grid/<trunk>/node/<mint_id>` (hash-identical blobs when equal).

## Invariants
- Engine.v4 Write/Edit + agi-turn — never write.py.
- Never git rm; mint_id durable link.
- Leave `core/season3/main` tip alone; leave wave-2 tip `ae180ab6d` alone.
- Do not wake Belam; do not run MUR from this seat.
- Master untouched.

## Falsifier
1. `git rev-parse refs/slice/demo` exists after pack.
2. Blob at `refs/slice/demo:nodes/<mint>` via `git cat-file -t`.
3. move updates grid node ref without hand update-ref of that grid ref.
4. No encrypt/seal/cred/ring in `### slice` piece.
5. No rollover `--apply`; season3 tip unchanged.

## Out of scope
Encryption · live rollover · g5.34.10.* · wave-2 g5.35.3–.6 · master archive · replacing grid.py

## Agent Notes
Assigned to **director-general-4** after SM PASS 2026-10-06-g. BUILD on own loop branch (`de-dg4-1` / posts/director-general-4). Box SM PASS when done. Climb later DG2→DG1→SM MUR→council→Belam. Do NOT wake Belam.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SM PASS 2026-10-06-g on council DESIGN g5.4.1.3.1. One builder (DG4) — no fan-out map in graph. engine.v4 Write+agi-turn. Belam/MUR held until after DG PASS.
<!-- THOUGHT:END -->
