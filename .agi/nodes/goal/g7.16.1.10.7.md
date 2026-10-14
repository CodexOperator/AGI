---
id: goal:g7.16.1.10.7
mint_id: 9ab2eff1f6684a0bbb6fb394dd27a1b8
type: goal
parents:
  - goal:g7.16.1.10
next_edges: []
confidence: 0.6
edited_by: sanctuary-master
goal_id: G7.16.1.10.7
goal_kind: subgoal
origin: council-loop
scaffold_hash: 21109a3e9b3e8039
season: 2
seeds: []
status: horizon
tags:
  - templates
title: "G7.16.1.10.7: the merge gate -- the PASS gives ONE word from the council report; a RED or a commit with no row refuses the merge by name"
town: core
---
# goal:g7.16.1.10.7

## OWNER 2026-10-14 ~20:0xZ + ~20:1xZ, verbatim (two messages, relayed by belam's [owner] 20:1xZ box mail to SM + the council; the quoted middle paragraph of (1) is belam's explanation to the owner, which the owner quoted)
(1) "I’m fine with option 1 for season 2,

But I saw this:

It looks at every commit in the range that touches engine code, skills or config. Each one must fall inside a range the council marked "accept" in a table, doc:council-report. It also runs the mechanical RED scan. If the table has no rows at all, the gate can't answer, which is where we are.

The table doesn’t need any rows those rows are already in the town board/bundle which is now gonna be a unified node. The mechanical check can still be ran via .sh scripts no? Or even py if needed if that’s better for log tracking"
(2) "And also as far as integrated workflows every workflow is just a subagent spawn using our new matrix math system but thay use it in a more limited way we can do that next season though"

## Why this exists
goal:g7.16.1.10 (merge-up reviews off the Prime): self-perpetuating's lens pass over the .10 leaves (13:4xZ 09-30) found that no leaf carries the END of the chain, the merge gate. So the parent's Falsifier 1 ("0 tracked run rows with launched_by=belam since last_pass_at, and the council report's rows cover every commit in BASE..TIP") has no owner. Depends on goal:g7.16.1.10.3 (REDs) and goal:g7.16.1.10.5 (the report).

## Target end-state
- The PASS reads the council report and gives ONE word: merge | hold.
- A merge is REFUSED by name over a RED, or over a commit in BASE..TIP with no report row; `unreviewed:budget` rows merge only on the Prime's word naming their count.
- skill agi-merge-pass §2 steps 2-4 (build rounds, launch chunks, verdicts) and step 6 (the Prime-minted residue leaf) retire BY NAME in the skill text, in the same commit; steps 0, 1, 5 and 7 stay as the mechanical merge.

## Invariants
- The Prime never runs a chunk review (goal:g7.16.1.10).
- A merge never lands over a RED or over a round with no row (goal:g7.16.1.10).

## Falsifier
1. The parent's Falsifier 1 on the next PASS: 0 tracked run rows with `launched_by=belam` since `last_pass_at`, and the report's rows cover every commit in BASE..TIP.
2. Negative: on a fixture, a merge over a commit with no report row is refused, naming the commit; 0 merges land over a missing row. (b) A fixture round with a planted RED row: the merge is refused, naming the RED. (c) An `unreviewed:budget` row without the Prime's word naming the count: the merge is refused. (A gate is only as true as its untested branch: alive lens 13:5xZ.)

## Out of scope
goal:g7.16.1.10.3 (the RED checks) · goal:g7.16.1.10.5 (the report rows) · the mechanical merge steps 0, 1, 5, 7

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
sanctuary-master gen 43 17:3xZ 10-14: status active -> horizon. HORIZON season 3 (council 3/3 17:35Z 10-14, alive answering SM's 17:32Z [decision], option A); falsifier untouched, mint id kept. Measured at the season-2 close gate (belam 17:32Z, re-run by alive + sp): F1 conjunct 1 MET (0 run rows launched_by=belam since last_pass_at; no runs/ dir in MAIN); conjunct 2 NOT MET: merge_gate.py check 4e9dbced38 dd48d342cf -> rc 2 'doc:council-report holds no old..new row -- the gate cannot answer' (1020 commits, 0 report rows: the report is filled only by council_report.py add from a workflow round, and every season-2 landing went through SM's gate + the council's box [approve] instead). (B) amending F1 to pass is barred; (C) a backfill [WITHDRAWN 18:12Z: it was reasoning; one row per merge covers the range, see below]. skills/agi-merge-pass/SKILL.md:44 says nothing merges over a hold, but merge_gate over the season range answers HOLD and the season-2 landings went through SM's gate + the council [approve], so merge_gate was not the season-2 land path's gate; the season 3 cut decides whether the land path calls it or the skill line goes. REOPEN: council_report rows are written from the box [approve] verdicts (or the gate reads them), so a landing range is covered. ADDED 18:1xZ (council 3/3 alive 18:12Z, which WITHDREW its 17:35Z citation of SM's '(C) measured to still HOLD': that was reasoning, now measured otherwise): merge_gate.uncovered over 4e9dbced38..4186bd26af with scratch rows: 1 first-parent row -> 178 uncovered; one row per landing merge -> 63; one row per merge (225 rows) -> 0. The season-2 PASS is to run on a one-time owner word, not merge_gate (council option B 18:12Z; asked via belam 18:16Z; not run at this version: origin/season2/main = ef9b043e68): council_report.py writes rows only from workflow review/verify JSON, so 225 backfilled rows would be records posing as runs. This node stays HORIZON on those grounds. REOPEN [SUPERSEDED as direction 20:1xZ by the owner word, see the last line] (replaces the line above): council_report gains a signed-box source (code, gated): signed [approve] commits by a council seat as their own state, belam's first-parent commits as unreviewed:budget under --prime-count, an unsigned or non-seat approve refused.
director-general-1 13:5xZ 09-30: owner set to director-general-3 on sanctuary-master's placement (agi-12, 13:49Z): the merge gate joins .10.3 and .10.5 on DG3, one source for the report schema and the gate; self-perpetuating proposed it. Minted HORIZON 13:4xZ on self-perpetuating's lens pass: the end of the .10 chain had no leaf, so the parent's Falsifier 1 had no owner. Status stays horizon.
v2 (director-general-3 10-14): the code half was already landed (merge_gate.py check BASE TIP [--prime-count N] -> merge|hold, rc 0/1/2; test_merge_gate.py 11 rows: uncovered commit, planted RED, budget row without the count, rc 2). This cut lands the SKILL half: agi-merge-pass §2 steps 2, 3, 4 and 6 are retired BY NAME (steps 0, 1, 5, 7 stay), the PASS word is merge_gate.py check, §3 tooling is marked the old route. LEFT, not mine: (a) config cell merge_gate.review_paths is absent -> rc 2 naming it (the Prime sets it); (b) Falsifier 1 is a LIVE read on the next PASS (0 launched_by=belam run rows since last_pass_at, report rows cover BASE..TIP). Status stays active until (b) is read.
ADDED 20:1xZ 10-14 (SM gen 44, belam's [owner] relay 20:1xZ): the owner word on the 18:12Z ask, verbatim above. 'option 1' = the season-2 PASS merges WITHOUT merge_gate (belam is to run PASS B7 on it; not run at this version: origin/season2/main = ef9b043e68). For season 3 (owner: 'we can do that next season'; the council's to cut, no row here changes): (a) the merge gate reads the town board / bundle (the unified node), not doc:council-report rows; (b) the mechanical REDs run as .sh (or .py for log tracking); (c) every workflow = a subagent spawn through the matrix, used in a more limited way. This supersedes the 18:1xZ REOPEN line (a signed-box source for council_report) as the reopen DIRECTION; the falsifier is unchanged until the season 3 council re-cuts it.
<!-- THOUGHT:END -->
