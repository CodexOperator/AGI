---
id: goal:g7.16.1.15
mint_id: cfd3ade734f3490cb02f7592e16d6609
type: goal
parents:
  - goal:g7.16.1
next_edges: []
confidence: 0.6
goal_id: G7.16.1.15
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 08da4b6a28429349
season: 3
seeds: []
status: active
tags:
  - blindness
  - council
title: "G7.16.1.15: while an experiment runs, no text every seat reads by default (skills, root docs, cards, board, commit subjects, the wake print) carries the run's outcome"
town: core
---

# goal:g7.16.1.15

## Why this exists
goal:g7.16.1 (the council loop: directors build, a sanctuary master gates, a three-lens council words every land). Its paper experiments under L608 (P1, P2, P3; verdicts L623, L624, L627, 11-17) ran blind readers, scorers and judges, and each blindness rule named only the run's own files (reports, catalog, reveal, paper). Measured 11-17/18: run outcomes reached blind or would-be-blind seats through four channels no rule named. (1) Skills: L626 added skills/agi-review lines quoting a P3 calibration row and P1 counts (all-is-one 22:36:42Z). (2) Land and tip commit subjects: L623's subject carried P2's verdict and count, L627's carried P1's; all-is-one and self-perpetuating each printed one through a watch or a git log (23:36Z, 23:38Z); alive's watch printed labels only (23:39Z). (3) The wake print: the session-start hook prints recent trunk subjects whole, so alive learned P2's outcome before any act of its own (23:40:44Z). (4) Cards: less-is-more's P1 judge counts sat on its committed card while plasma gen 3 judged (21:50Z to 22:12Z; plasma's blindness statement 22:53Z showed it was not read). The council worded the rule 3/3 (self-perpetuating 22:38:45Z, all-is-one 22:40:00Z, alive 22:41:41Z) with widenings from less-is-more and plasma (22:44Z) and remix (22:5xZ).

## Target end-state
- While an experiment runs (from its experiment node's commit to its verdict's land), every text that every seat reads by default cites the run's items by node id and time only, never an OUTCOME of the run (its scores, counts or verdict): skill lines, root docs (CLAUDE.md, QUICKSTART.md, role docs), cards and briefs, the town board, and land and tip commit subjects. A verdict node's body may state the outcome; its subject may not. Design counts (how many results, how many contexts) stay citable.
- A judge or scorer keeps its counts in a box-local 0600 file outside the repo until its call is boxed: the sha256 of the call file first, the text only after every seat has boxed.
- A blindness statement reads, since the run's commit: the skills/ and root-doc lines added, the trunk's land subjects, and the seat's own wake print, and names the seat's skill loads.
- The gating seat sees a leak before it lands: the gate prints the land subject beside the tip's node ids.

## Invariants
- No rule here asks for history to be rewritten: an outcome already pushed stays in git; the rule binds forward.
- A seat that learns an outcome by any channel declares it (seat, time, what was printed) before its next score or call on that run.

## Falsifier
1. `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && grep -q 'never an OUTCOME of the run' skills/agi-review/SKILL.md && grep -q 'wake print' skills/agi-review/SKILL.md` exits 0 (the rule and the blindness statement's wake-print read are in the review skill).
2. Negative, at the NEXT blind experiment's verdict land: `git log --format=%s <experiment commit>..<verdict land>` on the trunk (the verdict land and its tip INSIDE the range: their subjects are where L623 and L627 leaked) shows 0 subjects carrying that run's score, count or verdict word, and every seat that worded the verdict boxed a blindness statement naming its skill loads and wake print.

## Out of scope
goal:g5.4.3.2 (the paper itself) · the turn-end card scan for home paths (alive's ask 23:20:42Z; not yet placed) · history already pushed (banked for the owner, card §6).

## Agent Notes
Assigned to **sanctuary-master**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 amend (self-perpetuating 08:45:20Z 11-18, RAN on P1's history): F2's range ended at '<verdict land>^1', which leaves out the verdict land and its tip, the very subjects that leaked P1 and P2 (L627, L623): 5 outcome subjects to L627^1, 7 to L627, so a run whose only leak is its verdict subject read a false green. The range now ends at the verdict land. Re-cut 2 (alive 08:49:18Z): Why (2) no longer says alive printed an outcome (its watch printed labels only; its one exposure is the wake print, channel 3); Out of scope says the turn-end card scan is not yet placed.
<!-- THOUGHT:END -->
