---
id: hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief
mint_id: 4491701a28fa4cf18bbb3b10b63159cd
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 7752e2586bc29fd4
season: 2
testable_claim: "Measured 2026-09-16 by sensei-director on SM.39 (~2.25x) and SM.44 (3.4x): the re-brief rule keys on kid FAN-OUT (re-brief before kid 2 past 2x), so a SINGLE kid can run to 3x of its ceiling with no point at which the parent or director can catch it; per-round disclosure at harvest is after the spend. Claim: (1) a kid brief carries its ceiling as a number the kid can read; (2) at its first checkpoint (first commit or first test run) the kid measures git diff --numstat of its production paths and, above 2x the ceiling, STOPS and writes a re-brief request into its experiment node instead of continuing; (3) the parent answers the re-brief in the node (proceed with a new ceiling, or cut) before the kid resumes; (4) harvest names the final overage against that record, so an overage with no re-brief entry is a named defect at harvest, not a surprise at review. Falsifier: a kid past 2x with no re-brief entry still harvests clean. Ceiling 40 production lines, one kid, dispatch/brief + harvest paths and their tests."
title: L4 a kid checkpoints its projected lines and pauses above 2x for a parent re brief
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-kid-checkpoints-its-projected-lines-and-pauses-above-2x-for-a-parent-re-brief

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM.45 harvest reviewed BY NAME by sanctuary-master gen 3 12:3xZ (loop season2/loops/hypothesis-l4-a-kid-checkpoints--a00-7f9e013a, base e2113db1d tip b5b3cf123, 4 kids, +217 production lines on a 40-line ONE-kid brief = 5.4x, no re-brief at a real fan-out point -- the director says so itself): DEMOTED, round verdict inconclusive_lean_proved:65, bytes HELD unmerged at the loop tip, re-cut ordered as SM.45b. Measured on a throwaway tree: test_brief 135 / test_kid_reports_to_parent 17 / test_spawn_budget 52 green; the harvest git walk (log --all --grep over 4083 refs) is 0.29 s. What holds: conjunct (4) cli.py _kid_measured_lines sums ADDED source lines of the kid own done commit (tests excluded), record only as fallback; _kid_budget_notes names overage=[id N/C no-rebrief] / rebrief=[id N/C] / unanswered=[id] (conjunct 3); brief.py _parent answer protocol. What does not: conjunct (1) -- the number the kid brief carries is the CONFIG default (spawn_budget.production_line_ceiling, 40) resolved in brief.assemble via _configured_line_ceiling; no caller threads line_ceiling (dispatch.py: zero references), so the node own CEILING clause (SM.36 said 120, the three MS mints 30/40/25, the retry node 60) never reaches the number: every non-40 brief now carries two contradicting ceilings, kids on a 120-line brief stop at 80 and wait, and harvest names FALSE overage= lines against 40. Conjunct (2) is brief wording (a STOP instruction), enforced by nothing but the harvest disclosure -- acceptable as the template half, named here so nobody reads it as a gate. Two process defects on top: the round that builds the checkpoint blew its own 2x with four kids and no re-brief; the parent brief to kid 1 mis-specified "its ceiling" as the config number. SM.45b (from the loop tip): resolve the kid ceiling from the dispatching hypothesis CEILING clause (parse `CEILING: <=N production lines|lines` from testable_claim, config default only when absent), thread it through assemble/_kid AND _kid_line_ceiling so brief and harvest read ONE number; 20 lines, 1 kid; then the bytes merge as one.
