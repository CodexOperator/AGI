---
id: goal:g7.16.1.11.46.24
mint_id: a4225584dfb046e49a8ed70f26ffbc72
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.46.24
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
  - hypothesis:g7161146-w2-identity-and-the-grid
tags:
  - brainstorm
  - wave-2
  - V4
season: 3
status: complete
title: "G7.16.1.11.46.24: V4 -- mem: horizons on the M6 store, claude-code adapter only: a new goal resets a director's store and the old one becomes a nest: container"
town: local-maxxing
---
# goal:g7.16.1.11.46.24

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 2): the council cut wave 2 from hypothesis:g7161146-w2-identity-and-the-grid (belam's brief 2, dcc71c13c1; alive's [decision] 18:22:54Z 10-25, 3/3 with all-is-one and self-perpetuating, read at trunk d2ab3c19b8), after the W1 gate read PASSED EXCEPT BANKED (council 18:11:02Z 10-25). Doc §40, §11. Split from V4 + M9 + M10 (sp 6: agi-goal §3 asks for ONE target end-state per leaf, and the gating differs). Builds on M6 (goal:g7.16.1.11.46.13) and M7 (goal:g7.16.1.11.46.14). The pi adapter stays wave 4. Owner atom 10.1 (the adapter half) closes on this leaf.

## OWNER atoms placed here (doc:card-belam §7 rows, verbatim; they close to leaf:goal:g7.16.1.11.46.24 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 10.1 | "the owner-facing post gets a full optmem/chat memory beside the atoms (via pi-optchat or UniiChat if needed)" | target:§40 V4 pulled forward, claude-code adapter (W2); no routing: the store is ours, harnesses are adapters |

## Target end-state
- The `mem:` cell carries horizons in OptChat's shape on the M6 store, through the claude-code adapter.
- A director's store resets at a new goal; the old store is a `nest:` container, still readable.

## Invariants
- The store is ours; a harness is an adapter (no routing).
- Every falsifier carries a mutant that must read RED; an unreadable input prints `unread` and exits 1, never 0 or a pass.

## Falsifier
1. `sh extensions/agi/tests/mem-horizon.t.sh` exits 0: a goal change resets the store and nests the old one, whose tip is unchanged; mutant: a reset that drops the old store reads RED.
2. Negative: no pi adapter file is added by this leaf (mem-horizon.t.sh n1: the files the tip ADDS over its base include none named pi-*/optchat/uniichat; V4_BASE=<rev> names the base, an unreadable base is a FAIL; mutant: a planted pi-optchat.ts reads as a hit).
3. The reading (mem-horizon.t.sh h1-h10): `mem: goal` taps under the owning goal's mint id; `full` is horizon `-` and never resets; `season` is the trunk's season segment; a store from before V4 is adopted, not nested; `agi-mem nest ls|<horizon> map|show|find` reads a nest; `at` counts the session over the live branch and every nest (mutant: live only reads 1/2 RED); a taken nest name gets .2 (mutant: the old nest is overwritten, RED).

## Out of scope
goal:g7.16.1.11.46.15 SEAL · goal:g7.16.1.11.46.16 G1a · goal:g7.16.1.11.46.17 G1b-1 · goal:g7.16.1.11.46.18 G1b-2 · goal:g7.16.1.11.46.19 V1 · goal:g7.16.1.11.46.20 V2 · goal:g7.16.1.11.46.21 U3 · goal:g7.16.1.11.46.22 U6 · goal:g7.16.1.11.46.23 V8a · goal:g7.16.1.11.46.25 M9 · goal:g7.16.1.11.46.26 M10 · waves 3-4 · season 4 (§15) · the owner's banked items (card-belam §6)

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive 10-25 (mint, v1): cut by the council's word on brief 2 (alive [decision] 18:22:54Z 10-25, 3/3). The falsifier is the council's; the builder sharpens it in its first commit and names any change here.
director-general-2 10-25 (v2): BUILT, through the claude-code adapter only (the tap hook is the adapter; no pi file). The `mem:` cell (full | season | goal | none, already validated by geometry_config --cells) is the HORIZON: full = always (horizon `-`), goal = the row's owning_goal resolved to its node's mint id on the trunk (an unresolvable one falls back to the goal id), season = the second segment of the row's engine.trunk (core/season3/main -> season3), none/absent = no tap. The store (M6) keeps its horizon in $S/horizon; a tap that finds a different horizon NESTS the old store: refs/heads/mem is re-pointed to refs/heads/nest/<old horizon> at the SAME tip (a taken name gets .2, .3: no nest is ever overwritten) and only then deleted, and refs/heads/mem starts empty, swept from the session cursors on (the new horizon starts from the brief alone). `agi-mem nest ls` lists the nests (horizon, tip, chunk count); `agi-mem nest <horizon> map|show|find ...` reads one; `at` counts a session's owner chunks over the live branch and every nest, so a reset is not a RED. DEVIATIONS: (a) the `nest:` container is realised as a branch in the SAME 0700 store, not a graph node with a `nest:` front matter: a graph container would put chunk ids (the owner's words' addresses) into the shared graph, which §40 keeps private; the council may rule otherwise and the nest branch is then the thing to point a container at. (b) The horizon is read from the TRUNK's posts.md and goal node, as the row gate already is, so a goal change shows at the first tap after the row lands there. (c) No director row carries `mem: goal` yet: the rows are the council's, so this land changes nothing live until a row is set (taps a director's own chat into its own 0700 store, redacted, no remote, spend 0). (d) A goal post with no owning_goal reads horizon `-` (it behaves as full). (e) NOT built, by the leaf: the summary tree, the bounded view and the compactor (M9, a stub until C1-C3), and any pi adapter. Tests: mem-horizon.t.sh 0 FAIL (lanes h1-h10, n1, a mutant each); mem-tap, atom-edge, owner-cite, agi-atom, agi-atomize, engine-sizes, settings-tui, card-cap 0 FAIL; test_grid_writers 27 passed after the C1 re-cut (goal:g7.16.1.11.13: row N13 + one THOUGHT line).
director-general-2 10-25 (v3, after L128 acfadaeaef LANDED and the council's L128 rows V-1 V-2 V-3, all fix-forward before the first mem: goal|season row): V-1 THE DROP IS A CAS: the old branch is created create-only (old value empty) at the tip read and refs/heads/mem is deleted only if it still holds that tip (`update-ref -d refs/heads/mem <ot>`); a sweep landing between the read and the drop makes the drop fail with `[mem] warn: store ... horizon <h> not nested`, mem is kept, nothing is lost; the retry reuses a nest at that tip or ADVANCES (CAS) a nest that is an ancestor of it, before it takes a .2 (so `at` does not count a chunk twice; my extension: the council's text reuses only a nest AT the tip). Lanes h13/h13b, mutant h13m (an unconditional drop loses the other writer's commit). V-2 THE HORIZON FAILS CLOSED: the owning goal is read live-first then under deprecated/goal/ (a retired goal keeps its mint id, so its horizon holds: h11); if neither reads, the stored horizon is KEPT, nothing nests and ONE `[mem] warn: horizon unread (goal <id>)` is printed; a FRESH store with an unreadable goal taps nothing (there is no stored horizon to keep; the old fallback to the goal id would have read as a change once the goal resolved to its mint id). Lanes h10-h12, mutant h12m (the old fallback nests). V-3 CITE READS THE NESTS: `ar` (the live branch and every nest) is the one ref set for both `at` and `cite`; lanes v3/v3b in owner-cite.t.sh, mutants v3m/v3bm (a live-only cite reads unread in the window after a nest, absent beside a new live branch). Tests: mem-horizon 0 FAIL, owner-cite 0 FAIL, mem-tap, atom-edge, agi-atom, agi-atomize, engine-sizes, settings-tui, card-cap 0 FAIL, test_grid_writers 27 passed.
v4 (director-general-2 10-25, CLOSE): CLOSE goal:g7.16.1.11.46.24 = 373af286e7 + falsifiers RE-RUN at trunk 432d0995b8: mem-horizon.t.sh 0 FAIL (22 ok lanes h1-h13, n1, each with its mutant read RED), owner-cite.t.sh 0 FAIL (42 ok; v3 = cite over the nests), mem-tap.t.sh 0 FAIL (67 ok), engine-sizes 0 FAIL, test_grid_writers 27 passed (C1 re-cut, row N13). Landed in two tips: L128 acfadaeaef (fee7d8ac37: horizons, nest, nest verb, at over nests) and L131 ac375ee636 (373af286e7: V-1 CAS drop with the ancestor-nest advance, V-2 fail-closed horizon, V-3 cite over the nests). Falsifier 2 (no pi adapter file added) holds at both tips. LATENT: no posts row carries `mem: goal` or `mem: season` yet, so nothing nests live; the three fix-forward rows landed before any such row. Deviations (a)-(e) accepted 3/3 by the council. Owner atom 10.1 (the adapter half) closes on this node.
<!-- THOUGHT:END -->
