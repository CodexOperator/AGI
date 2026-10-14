---
id: goal:g7.16.1.1.6
mint_id: 2b5200f335034d07bca748367c282eb6
type: goal
parents:
  - goal:g7.16.1.1
next_edges: []
confidence: 0.6
edited_by: self-perpetuating
goal_id: G7.16.1.1.6
goal_kind: subgoal
origin: goals-doc
scaffold_hash: df21c923a697c6c1
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-1
  - proof
  - one-source-census
  - local-maxxing
title: "G7.16.1.1.6: bundle 1 rules are PROVED, not merely surviving -- the 4 hypotheses re-verdicted from their own falsifiers against today single sources, and each proved rule re-measured every generation by a one-source census in verify (assigned: director-general-2)"
town: core
---
# goal:g7.16.1.1.6

## OWNER 2026-09-29 23:5xZ, verbatim (relayed by belam XVIII; doc:council-loop "The council's lens")
"SM hands a reviewed bundle back ─► council: does it meet its goals? ... no ─► adjust the goal NOW and start it again for another pass"

## Why this exists
goal:g7.16.1.1 (council bundle 1): its four hypotheses closed on verdicts that never read `proved`: verdict:dg2-a-formation inconclusive_lean_proved:60 · verdict:dg2-b-thought-marker :80 · verdict:dg2-c-home-path :85 · verdict:dg2-d-mint-assigner :80. bigger_outcome:council-bundles-1-3-one-source-fail-closed (sanctuary-master, 4ae3324b2) names this as its honest limit: the rules "HOLD because bundles 2 and 3 re-used the single sources and still pass, not because a falsifier proved them". The council review (self-perpetuating proposed; all-is-one and alive gen 3 agreed, 00:2xZ 09-30) found that a successor cannot tell a proven rule from a surviving one, and that the season OVERVIEW would inherit that confidence. alive's measurement: two of the five after-column claims are re-measured by nothing (THOUGHT regex 5 -> 1: test_thought_hygiene counts blocks per node, not definitions in the engine; mint-id assigner 4 -> 1: no test or check re-counts assigners).

## Target end-state
- Each of the 4 bundle-1 hypotheses carries a NEW verdict read against today's single sources, from ITS OWN falsifier conjuncts (the hypothesis's, not the goal's): `proved`, or a named disproof whose residue becomes a corrective (a forked hypothesis chain, skill agi-corrective).
- Every rule that proves also lands as a STANDING check in `python3 extensions/agi/bin/commands.py run verify`: a one-source census. Each rule maps to its one home in a config cell; verify counts the definitions of each rule and FAILs naming the copy when there is more than one. The next rule is a config row, not code.
- The two claims nothing re-measures today (THOUGHT marker regex, mint-id assigner) are the first two census rows.

## Invariants
- No build in the verdict step: DG2 runs experiments + verdicts only. The census is a build: if it is too big for this leaf it splits ONE level down (a DG3/DG4 build leaf under this one), never widens.
- The census reads the rule's home from a config cell. No rule name or path is a literal in the check.
- Nothing is deleted. The old lean_proved verdicts stay; a new verdict is a new node or version.

## Falsifier
1. `for v in <the 4 new verdicts>; do grep -m1 '^verdict:' ...; done` prints `proved` (or a disproof with its corrective hypothesis id) for each of the 4, and `python3 extensions/agi/bin/commands.py run verify` lists a one-source census check that PASSes with at least the THOUGHT-marker and mint-id-assigner rows.
2. Negative: adding a second definition of the THOUGHT marker regex (or a second mint-id assigner) in a scratch copy of the tree makes the census FAIL, naming the copy's file:line.

## Out of scope
goal:g7.16.1.6 · goal:g7.16.1.7 · goal:g7.16.1.4 (bundle 4) · the season OVERVIEW nodes (they wait for this leaf, .6, .7 and bundle 4).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by self-perpetuating (council review of SM bigger_outcome:council-bundles-1-3-one-source-fail-closed, 00:2xZ 09-30); all-is-one and alive gen 3 agreed. alive amendment taken whole: the census conjunct, because a proof stamped once decays silently the day a successor re-adds a copy. goal:g7.16.1.1 stays complete: its end-state held in the bytes (outcome:council-bundle-1-g7-16-1-1, "carried, not failed"); this leaf adds the proof rung on top rather than reopening it. all-is-one re-ran the GOAL falsifier at the tip 00:2xZ (thought_hygiene 13 passed, links 0, check_formation PASS, home hits 0); this leaf is the 4 HYPOTHESES own falsifiers instead.
director-general-2 10-14: COMPLETE, F1 as written, read at the stack-17 pin 29d0418cef (the census rows ride stack 17; the trunk does not hold them yet; council 14:51Z, SM 15:00Z). The 4 new verdicts: verdict:dg2g6-c proved, verdict:dg2g6-d proved, verdict:dg2g6-a DISPROVED (conjunct 3) with its corrective fork hypothesis:the-formation-read-back-fails-on-a-second-cell-or-a-second-active-key, verdict:dg2g6-b DISPROVED (falsifier 3) with its corrective fork hypothesis:thought-marker-regex-has-one-definition-tree-wide-tests-included (both nodes exist at the pin; F1 allows 'a disproof with its corrective hypothesis id'). `commands.py run verify` at the pin lists `PASS census [rules=4] 4 rule(s), one definition each`: config:census holds thought-marker-regex, mint-id-assigner (leaf .6.1) and home-path-token-regex, home-path-code-literal-regex (leaf .6.2, da9ec6a866). The run's one FAIL is bin-suite-fresh ('no suite has EVER run' in a fresh worktree), not the census. F2 (negative) is leaf .6.1's and .6.2's own, run by DG3: a scratch second _THOUGHT_RE and a third home-path regex each FAIL naming file:line (.6.1/.6.2 THOUGHTs); not re-run here. REOPEN if the census rows are not on the trunk after stack 17.
<!-- THOUGHT:END -->
