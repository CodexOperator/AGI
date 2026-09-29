---
id: goal:g7.16.1.4
mint_id: 11bb853511b54358ade2d89ae72f9b47
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.75
edited_by: alive
goal_id: G7.16.1.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: d910b9051143108f
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-4
  - local-maxxing
  - write-path
  - render-path
title: "G7.16.1.4: COUNCIL BUNDLE 4 -- the write/render split: W0 one live goal per act (g4.19) -> W1 g4.18.5 rows + a write is a commit -> W2 g4.18.6 links are mint ids -> W3 g4.18.7 read leaves write.py, one render path"
town: core
---
# goal:g7.16.1.4

## OWNER 2026-09-29 18:0xZ, verbatim (Prime pane, relayed by belam-S2-L5-XVI to the council)
"Write shouldn't need a read path. We should only need a render path. Add it to bundle if needed I've been meaning to improve the way the graph is rendered for agents for a while. Unify everything into the correct slots. Read doesn't belong to write semantically im surprised the council didn't catch it"

## Why this exists
goal:g7.16.1 (the council loop): the Prime handed the council three owner orders from 17:2xZ-18:0xZ as ONE bundle, "the write/render split", and asked the council to place it. Council placement 18:1xZ (alive · all-is-one · self-perpetuating, all three agree): its OWN bundle after bundle 3, NOT folded in. Bundle 3 (goal:g7.16.1.3) is mid-build with DG2 since 17:56Z, and its H1 (goal:g4.18.3) edits write.py, while goal:g4.18.5 rewrites write.py's core write path. goal:g4.18.7 addresses rows by goal:g4.18.5's index and resolves names through goal:g4.18.6, hence the order.

## Target end-state
Rows in council order. A row closes when its line holds in the bytes.
- **Base.** Cut from bundle 3's SM-clean tip, never 900a4017a, so goal:g4.18.3's authorship-gate test already stands when the write path is rewritten under it. Core's write.py +125 (the bundle-5 file list) is read as INPUT: each hunk is absorbed or rejected by name, so bundle 5 never ports onto a dead shape.
- **W0 · one live goal per act.** goal:g4.19 (its title routes Read THROUGH write.py) is retitled under the owner's 18:0xZ line or parked by the tag `parked:g4.18.7`; no two live goals route one act opposite ways.
- **W1 · rows, and a write is a commit.** goal:g4.18.5, carrying goal:g4.18.3's invariant verbatim: "One authorship gate for every write.py verb that writes a node; no verb returns ahead of it."
- **W2 · links are mint ids.** goal:g4.18.6, minus its end-state bullet 2's read routing (one home: goal:g4.18.7). Couplings, in the SAME row: CLAUDE.md's renumber rule ("re-point every reference in the SAME commit") and the agi-goal skill's matching renumber text retire, since no link ever needs re-pointing.
- **W3 · read leaves write.py.** goal:g4.18.7: `read` leaves VERBS in the same row that repoints the 23 teaching files (the agi-node-write skill grammar and CLAUDE.md included). No alias, never two read paths.
- **Hygiene when touched:** goal:g4.18.3 / .5 / .6 bodies carry a doubled `# goal:<id>` H1; the row that next edits each fixes it by `replace body`.

## Invariants
- No parent/kid dispatch (goal:g7.16.1). Every node is written through write.py. Nothing is deleted. Nothing is written on core/season2/main or core/main.
- One director works the bundle at a time: DG1 -> DG2 -> DG3 -> sanctuary-master -> council. Tests run ONE file at a time while a PASS runs on this box.
- The viewport never gains a write path (goal:g9); `viewport.py --verify` exits 0.

## Falsifier
1. goal:g4.18.5, goal:g4.18.6 and goal:g4.18.7 read complete, with their own falsifiers run; `python3 extensions/agi/bin/viewport.py --verify` exits 0.
2. Negative: `git grep -n '"read":' -- extensions/agi/bin/write.py` prints nothing; `git grep -n "re-point every reference" -- CLAUDE.md skills` prints nothing; goal:g4.19's title no longer names Read routed through write.py.

## Out of scope
goal:g7.16.1.3 (bundle 3, and its row R: goal:g6.41.1 P1+P6, P5) · bundle 5 = goal:g6.41.1 P2-P4 + its Falsifier 1 (RESUMED) + core's edits to EXISTING files (write.py +125 after W-input, dispatch.py +86, boxes.py +87, provisioning.py, rotate.py) + profile_sync · the season-2 close.

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by alive (council convener) 18:2xZ 09-29 on the Prime belam-S2-L5-XVI [owner] relay: "Three owner orders from 17:2xZ to 18:0xZ belong in ONE bundle, which I would call the write/render split. The council places it: after bundle 3, or folded in." All three lenses: AFTER bundle 3, its own bundle, order g4.18.5 -> .6 -> .7. Conditions taken verbatim in spirit: base on bundle 3 SM-clean tip (self-perpetuating a, all-is-one 3); carry g4.18.3 invariant into g4.18.5 (all-is-one 3); one home for reads = g4.18.7, cut from g4.18.6 (all-is-one 1); g4.19 resolved as row W0, not flagged (all-is-one 2); .6 retires the renumber re-point rule in CLAUDE.md + agi-goal (self-perpetuating c); core write.py +125 read as input (alive, both agree). The old bundle 4 (core edits + profile_sync) is bundle 5.
<!-- THOUGHT:END -->
