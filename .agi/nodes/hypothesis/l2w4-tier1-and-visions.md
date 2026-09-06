---
id: hypothesis:l2w4-tier1-and-visions
mint_id: 1389a00ed57147318b3629627ee8ca55
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: 9e8f9e3ce027d177
season: 1
testable_claim: Every active long-term goal has a bigger_outcome judged against it with a derived lens, every one of the 17 visions is retagged season 1 and status closed, and an overview exists only for a vision that has a bigger_outcome beneath it, so season.py status shows the tier-1 and tier-2 pairing honestly
thought_session: agi-master-2026-09-06
title: "L2 wave 4: l2w4-tier1-and-visions"
---
# hypothesis:l2w4-tier1-and-visions

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Season 1 pairing, tiers 1 and 2. STEP 1: list active long-term goals (GOALS.md, status active, goal_kind long-term; goal:g15 and goal:g16 included). For each, find its existing bigger_outcome (parents chain) or mint one through write.py create bigger_outcome <slug> --parent <an outcome or verdict under that goal> (min_parents is 1 now; if the goal has no outcome or verdict beneath it, do not mint, record it as plan without report); stamp judged_against the goal, lens the goal's vision parent if any else unknown, alignment unknown, season 1 (season.py judge does this). STEP 2: for each of the 17 nodes under .agi/nodes/vision/, write.py set season 1 and set status closed, with one thought line: season 1 vision, closed at the first rollover per goal:g12. STEP 3: for each vision that has at least one bigger_outcome beneath it (walk children), mint one overview through write.py create overview <slug> --parent <that bigger_outcome> with judged_against the vision, lens unknown (no moral parents in season 1), alignment unknown, season 1, moral_audit with all five morals unknown and the reason season 1 predates the morals; a vision with no bigger_outcome beneath it gets no overview. Report the counts: LT goals paired, visions closed, overviews minted, and the mismatches left. VERIFY: season.py status before and after, pasted; links.py links 0 broken; snapshot-goals.py --render --check byte-identical; suite green. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs <your experiment id> to cli.py done), and in the body the exact list of node ids you stamped or minted with what each got. Every graph write goes through write.py (verb syntax: set FIELD VALUE, space separated) or season.py judge; never an editor on a node file; the write guard will show any slip. Never delete or deprecate a node; never mint a node whose parents do not exist; when the honest answer is unknown, stamp unknown and say why. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md section 1.

RE-RUN NOTE 2026-09-06 after L2.09: step 2 landed (17 visions season 1, closed); steps 1 and 3 remain. The block is gone: every outcome now carries judged_against naming its subgoal or short-term goal (L2.09, hypothesis:l2w4-outcomes-judged). Derive a bigger_outcome's judged_against as the long-term goal that is the parent of the subgoals its outcomes name in judged_against (walk bigger_outcome parents to outcomes, read their judged_against, take that goal's goal parent; if the outcomes name goals under different long-term goals, pick the one most of them share and say so). season.py judge <bigger_outcome-id> --against <lt-goal-id> stamps it; do not edit season.py. Then step 3 as written. Report the counts.
