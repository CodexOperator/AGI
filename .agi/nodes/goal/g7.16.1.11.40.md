---
id: goal:g7.16.1.11.40
mint_id: f6eb1ecf342a425cb63b038e36f7c3cc
type: goal
parents:
  - goal:g7.16.1.11
next_edges: []
confidence: 0.5
edited_by: sanctuary-master
goal_id: G7.16.1.11.40
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
seeds: []
tags: []
role: director
scaffold_hash: 27392968a4e2fe04
season: 2
status: active
title: "G7.16.1.11.40: engine parity is owed only to capabilities still NEEDED -- the 3 short rows are ported or retired by ruling, the 12 not-run rows are measured"
town: core
---
# goal:g7.16.1.11.40

# G7.16.1.11.40: engine parity is owed only to capabilities still NEEDED -- the 3 short rows are ported or retired by ruling, the 12 not-run rows are measured

## Why this exists
outcome:g7-16-1-11-3-5-live-posts-boot-under-8k reads ADJUST. The new engine's parity table (doc:g716111-stage25-rootplan, PARITY PROOFS, 55 rows) stands at 40 matched-or-better LIVE, 3 named SHORT and 12 not run; the 52/55 in the title was the plan figure (SM mur RI1, 10-07). Those 15 rows have no owning leaf. The council (alive 02:5xZ 10-11, remark 2 on 0a8aa43672) asked the .11 bigger_outcome to place them as ONE leaf. Parity is owed only to capabilities still NEEDED: a row for old-engine-only behaviour retires with the old engine, by ruling (all-is-one).

## Target end-state
1. THE 3 SHORT rows (18 key rotation / key_history at a v4 rotation; 30 dispatch parents/kids, which needs a key broker; 33 review / detached workflows, which needs linger + key mints) are each PORTED (a landing sha) or RETIRED by a council ruling that says why the capability is no longer needed.
2. THE 12 NOT-RUN rows are each MEASURED live (matched-or-better, or a new named SHORT under target 1), or retired by ruling as old-engine-only.
3. The parity doc's count is rewritten to what was measured, never to the plan figure.

## Invariants
- No row closes on a plan figure or a quote: a sha, a measurement, or a ruling.
- A row that touches keys / signing / spawn stays under the g7.16.1.11.11 HOLD unless belam lanes it.

## Falsifier
1. The parity doc's PARITY PROOFS table has 0 rows reading neither MATCH / EXCEEDS (with a measurement) nor SHORT-ported / RETIRED (with a sha or a ruling).
2. Negative: the string "52/55" appears in no live node as a current claim (history rows are marked as history).

## Out of scope
The engine fence (goal:g7.16.1.11.5.1) · the AGI_SEAT retirement (goal:g7.16.1.11.37).
