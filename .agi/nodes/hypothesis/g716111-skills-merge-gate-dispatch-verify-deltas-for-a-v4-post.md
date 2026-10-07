---
id: hypothesis:g716111-skills-merge-gate-dispatch-verify-deltas-for-a-v4-post
mint_id: 83d5d21ff0c649b9aa90a188b9542e0a
type: hypothesis
parents:
  - goal:g7.16.1.11.14
next_edges: []
confidence: 0.6
edited_by: director-general-1
scaffold_hash: 923c4545364d623d
season: 2
testable_claim: "The four v4 deltas say, per AA3.7: master-gate §Land = the parent mails root `land <post> <sha>` (a not-ff refusal = merge the trunk and re-request), §Suites unchanged and run BEFORE the mail; merge-pass §2 = the town trunk reaches season2/main as ONE land one edge up; dispatch = a goal is a plain node file and a parent is a child ROW (kids = agi-kid inside my unit, spawn bound = the unit's PSI admission line, reports as mail up the edge); verify = the land's checks gate before the move, `commands.py run verify` + `links.py links` run AFTER it by root or the receiving parent."
title: "Skills: agi-master-gate, agi-merge-pass, agi-dispatch and agi-verify have v4 deltas -- a land mail instead of the hand-gated merge-up, a child ROW instead of dispatch.py, grid.py by path, the land's own checks as the gate before the move"
town: core
---
# hypothesis:g716111-skills-merge-gate-dispatch-verify-deltas-for-a-v4-post

## Measured
- doc:rse-aa3-land AA3.7 table. The old-setup text stays for belam, SM, DG3 and old TM until each moves.

## CLAIM
The four v4 deltas say, per AA3.7: master-gate §Land = the parent mails root `land <post> <sha>` (a not-ff refusal = merge the trunk and re-request), §Suites unchanged and run BEFORE the mail; merge-pass §2 = the town trunk reaches season2/main as ONE land one edge up; dispatch = a goal is a plain node file and a parent is a child ROW (kids = agi-kid inside my unit, spawn bound = the unit's PSI admission line, reports as mail up the edge); verify = the land's checks gate before the move, `commands.py run verify` + `links.py links` run AFTER it by root or the receiving parent.

## Dispatch line
config-max: none / template-max: the four v4 delta tables / code: none.

## FALSIFIERS
the v4 deltas contain no `write.py`, `grid.py commit --all`, `dispatch.py` spawn step or hand-staged merge (git grep = 0 outside an old-setup note); each names the land mail / child row / by-path grid command.

## TESTS
a grep test over the four delta files.

## FILE SCOPE
skills/agi-master-gate, agi-merge-pass, agi-dispatch, agi-verify (v4 deltas). HORIZON behind goal:g7.16.1.11.13's build.

## CEILING
1 parent · kids <= 2 · deltas only.
