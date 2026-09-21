---
id: hypothesis:l2w4-outcomes-judged
mint_id: ff23ede817dd485cb1fa81356923a192
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: director
scaffold_hash: f255eba7f52c3eb3
season: 1
testable_claim: Every outcome node carries judged_against naming the subgoal or short-term goal its chain served, lens derived from that goal's parent, alignment unknown and season 1, or judged_against unknown with a recorded reason, so season.py status reports zero outcomes without a judgment record
thought_session: agi-master-2026-09-06
title: "L2 wave 4: l2w4-outcomes-judged"
---
# hypothesis:l2w4-outcomes-judged

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
Season 1 pairing, tier 0. Today season.py status says 23 outcomes have no judged_against and outcomes have no goal parents. For each node under .agi/nodes/outcome/ (and .agi/nodes/deprecated/outcome/ if any, live first): walk its parents (mvp, verdict) back through the chain (experiment, hypothesis, idea) to the goal the chain's seed cites (a goal's seeds list, or an idea's goal parent, or a goal id named in the seed node's body); that goal is judged_against; run python3 extensions/agi/bin/season.py judge <outcome-id> --against <goal-id> and confirm it stamped judged_against, lens, alignment unknown, season 1; if season.py judge cannot derive lens, set it yourself through write.py to the goal's first goal or vision parent, or unknown. Where no goal can be found, stamp judged_against unknown and a note naming the chain you walked. Do not mint new outcomes: a subgoal with no outcome is an unfinished plan, which is the honest state, not a gap to fill (brief invariants: measured at season close, never enforced). VERIFY: season.py status before and after, pasted; after must show 0 outcomes with no judged_against; links.py links 0 broken; suite green. REPORT: one experiment node under this hypothesis, verdict on the testable claim, evidence_runs as a list of node ids (pass --evidence-runs <your experiment id> to cli.py done), and in the body the exact list of node ids you stamped or minted with what each got. Every graph write goes through write.py (verb syntax: set FIELD VALUE, space separated) or season.py judge; never an editor on a node file; the write guard will show any slip. Never delete or deprecate a node; never mint a node whose parents do not exist; when the honest answer is unknown, stamp unknown and say why. Do not commit, push, or run grid.py commit. Report unexpected files in git status and never touch them. Design source: .agi/context/season-ladder-and-morals-brief.md section 1.
