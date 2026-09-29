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
heading_level: 4
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
title: "G7.16.1.4: COUNCIL BUNDLE 4 -- the write/render split: W-G GOALS.md retired -> W0 one live goal per act (g4.19) -> W1 g4.18.5 rows + a write is a commit -> W2 g4.18.6 links are mint ids -> W3 g4.18.7 read leaves write.py, one render path"
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
- **W-G · GOALS.md is retired** (moved UNBUILT from bundle 3 row G, council 20:2xZ; OWNER 17:3xZ 09-29, verbatim on goal:g7.16.1: "Go ahead and retire GOALS.md. We don't need it anymore stop bothering with it or the render byte round trip script"). ONE row: the live render callers (driver.sh:240 on every --smoke, the rotation closeout, the review gates), the same-row couplings (retire --from-doc + its unlink, the closeout --check gate, node_writer's goal-type reason, the goals_file cell) CLAUDE.md's "Read YOUR goal by id" line, its --check table row and its "GOALS.md is derived" convention move together (every --smoke rewrites GOALS.md in MAIN today, leaving it dirty); goals are then read through W3's render path (goal:g4.18.7): GOALS.md is a second read surface, so W-G and W3 are one act. No half-retire: until W-G lands the render and --check stay live and a red --check is W-G's by name, never waived. --smoke still reports a node count after the render goes (the Prime's [red] 18:00Z: the node-count floor never goes blind).
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
Minted by alive (council convener) 18:2xZ 09-29 on the Prime belam-S2-L5-XVI [owner] relay (the write/render split, placed AFTER bundle 3 by all three lenses; conditions on W1-W3 as in the body). This version (20:3xZ) adds row W-G: bundle 3 row G was NEVER BUILT -- 30f4db55f + e662637ac edit only goal/g7.16.1.3.md, driver.sh is untouched in 9181cee26^..9966e3050 and driver.sh:240 at 9966e3050 still runs --render --strict-goals (verified by alive, all-is-one and self-perpetuating), which is why SM clean handoff carried a red render --check. GOALS.md is a second read surface for goals and W3 makes viewport the one, so W-G and W3 are one act (all-is-one). Couplings move with it as ONE row (all-is-one 1, self-perpetuating b); no half-retire (all-is-one 2).
<!-- THOUGHT:END -->
