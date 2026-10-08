---
id: goal:g6.50
mint_id: 9ada5cc50ed54140a2b6a267cfdc58f8
type: goal
parents:
  - goal:g6
next_edges: []
confidence: 0.7
edited_by: self-perpetuating
goal_id: G6.50
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 5f9b020bec401f2f
season: 2
seeds: []
status: active
tags:
  - s-goal-retirement
  - from-s34
  - hazards
  - test-maxxing
title: "G6.50: the six hazards goal:s34 still carried close in the loop -- each a fix plus a red-on-purpose test, or moved to a named goal with a reason (budget read, backward-mvp regex, verify order, contradicts/contrasts, two mermaid.py, briefing disk re-read)"
town: core
---
# goal:g6.50

## OWNER 2026-09-30 01:2xZ, verbatim (relayed by alive gen 3, belam's post-reboot owner-task)
"All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals."

## Why this exists
goal:g6 (test-maxxing): goal:s34 ("every hazard carried in a handoff is closed in the loop, not carried again") was retired on the owner's line above. It was measured against the bytes at 02:1xZ 09-30 (self-perpetuating, read-only survey): of its 16 carried rows, 4 are DONE (2 dispatch key gating, 5 write.py set coercion, 9 no-TTL mint test gated @live, 11 experiment parents), 3 MOVED (3-4 -> goal:g4.9, 10 -> goal:g4.6.1 complete), 3 UNMEASURABLE from this repo (7 six demoted experiments with no carrier, 14 the fantasia/agi clone, 16 untracked nodes across a wave: working rule only), and 6 still OPEN. This leaf carries those six, under s34's own closing rule.

## Target end-state
Each row closes with a fix plus a red-on-purpose test, or moves to a named goal with a reason:
| row | open today (measured 02:1xZ 09-30) | proposed home |
|---|---|---|
| 1 | provisioning.py cannot read a workspace weekly budget: provisioning.py:182-187 says the provider exposes no endpoint "as of 2026-09-04" (a docstring quote, NOT re-measured: re-check the provider API before any won-t-fix) | goal:g1.11, as a named won't-fix with that reason, or a budget read if an endpoint appears |
| 6 | metrics.py:643 `_BACKWARD_MVP_RE` is still a regex heuristic (c9c82ae89 only made it score-neutral) | here: a structural test, or retire the metric |
| 8 | the verify sequence runs smoke, tests, viewport-verify, then grid-commit (command:commands verify, commands.md:3155-3159, `ordered:` at :3039) | goal:g6.18 |
| 12 | `[verdict].md` declares `contradicts`, the corpus uses both (10 `contradicts:` / 7 `contrasts:`), with no alias | here: one name, the other migrated or aliased by the schema |
| 13 | two mermaid.py (extensions/agi/src/renderers/mermaid.py 66 lines, extensions/agi/src/chain_engine/renderers/mermaid.py 132 lines) | goal:g4 (elegance): one renderer |
| 15 | briefing.py:188-200 re-reads idea status from disk via zoom._frontmatter_for | here: the status comes from the one read path |
Their hypotheses carry over: hypothesis:a00-3416528c-c05b85 (row 12) · hypothesis:provisioning-reads-the-workspace-weekly-budget (row 1) · hypothesis:verify-runs-grid-commit-before-smoke (row 8).

## Invariants
- A row is never carried again: it closes here, or it moves by name with a reason.
- Every fix lands with a red-on-purpose test.

## Falsifier
1. Each of rows 6, 12 and 15 closes in a commit that names its test file; that test is red on the parent commit and green on the closing commit.
2. Rows 1, 8 and 13 each name their destination goal id in that goal's body, with the reason.
3. Negative: `git grep -lE '^contradicts:' -- .agi/nodes/verdict` and `git grep -lE '^contrasts:' -- .agi/nodes/verdict` (frontmatter keys only, never prose) are not both non-empty while `[verdict].md` names only one.

## Out of scope
goal:g4.9 (rows 3-4) · goal:g4.6.1 (row 10, complete) · goal:g1.11 (per-spawn keys) · goal:g6.18 (grid-commit and evidence-gate tests).

## Agent Notes
Assigned to **the council** (placement).
