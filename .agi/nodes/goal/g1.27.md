---
id: goal:g1.27
mint_id: af8e63d1d8524363ac594e970ad569c9
type: goal
parents:
  - goal:g1
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G1.27
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 167058d30a0bdbe1
season: 2
seeds: []
status: horizon
tags:
  - engine
  - pass
  - residue
title: "G1.27: PASS 11 residues -- 4 engine defects (zero-usd pre-flight width, key-cap banner, provisioning import route, missing end-to-end tests) + the doc/skill batch closed by reviewed rounds (assigned: director-engine)"
town: core
---
# goal:g1.27

# goal:g1.27

## Why this exists
goal:g1: PASS 11 (OWNER 21:4xZ 09-27, "do a pass anyway as it's a lot of modifications that could use a look over") reviewed the trunk @707d8dbbea on pi-free -- 0 experiments since PASS 10, so two engine-delta rounds over 24 files (907+/136-): the zero-usd mint fix, the paid-mur closure, the facts + skills first_turn entries, ten flow skills, the duty briefs. Both rounds accept_with_residue (run mur-p11chunk1of1), merged 739969f48. Every verify verdict upheld its defect; this leaf closes them.

## Target end-state
- The zero-usd path is exactly as wide as its claim, its banner states the real key cap, and provisioning keeps one import route.
- The free-lane mint on a drained account and the `skills` first_turn entry each have a committed end-to-end test.
- No brief, skill, manifest description or config note names the paid `pi` harness as the route, points past its block, cites a wrong file:line, or hand-copies the skill index.

## Invariants
- No default or instructed route reaches a paid harness (goal:g4.20.1 carries the structural half).
- A residue is closed by a reviewed round, never by a note.

## Falsifier
1. `git grep -nE "on pi\b|--harness pi\b|read body 37:64" -- extensions/agi/briefs skills extensions/agi/workflows .agi/config.json` = 0 hits, and the tests named in each child hypothesis pass.
2. Negative: a dispatch dry-run on pi-free with a drained balance still runs check_runtime_key_usable (it is not skipped).

## Out of scope
goal:g4.20.1 (one harness source) · goal:g1.26 (PASS 10 residues).

## Agent Notes
Assigned to **director-engine**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-goals-1 10-24 (STEP B, alive 07:17:02Z, council 3/3: HORIZON. g1.27 FAIL  n1: 17 hits of "on pi\b|--harness pi\b|read body 37:64" in briefs, skills, workflows, config (named tests PYWAIT). STEP A at fb4812f204, dg1 [result] relayed by SM 07:11:51Z; season-2 residue, no current-wave consumer; revive by naming one (goal id). STEP B item 4: the one remaining hit to fix at revive is skills/agi-rotate's `read body 37:64`.)
<!-- THOUGHT:END -->
