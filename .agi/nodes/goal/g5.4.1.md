---
id: goal:g5.4.1
mint_id: f0972bbe2ae64a1aae7b8d56e6051328
type: goal
parents:
  - goal:g5.4
next_edges: []
confidence: 0.7
edited_by: belam
goal_id: G5.4.1
goal_kind: subgoal
origin: goal
scaffold_hash: f0972bbe2ae64a1a
season: 2
seeds: []
status: active
tags:
  - goal
  - subgoal
  - season-close
  - s2
title: "G5.4.1: Season 2 close — outcomes to bigger_outcomes to one overview per vision, then manual core/season2/main → core/season3/main rollover"
town: core
---
# goal:g5.4.1

## Why this exists
goal:g5.4 (the season review and rollover, end to end): owner 2026-10-05 23:3xZ (via Grok Bot, to Prime) ordered the close now that W+AA1 are the remaining bundle, and authorized the branch create for this close only. Measured at mint: send.py still live (317680 B); DG6 last commit 90df7573f 22:32Z was a named merge, not the AA1 BUILD; season.py rollover --dry-run prints s2→s3 and would mint 3 visions unless --visions-from is supplied; SM card holds "no rollover" / "season close AFTER send lands".

## OWNER 2026-10-05 23:3xZ, verbatim (via Grok Bot)
> Once send lands, do the season close. Every completed subgoal leaf gets an outcome; outcomes keep bundling into bigger_outcomes until we arrive at an overview node set, one overview node per vision, handed to Prime as the season close report. Then do the actual season close. Build season rollover machinery on the new engine only as absolutely required; otherwise set the goal now and do the rollover manually for core/season2/main only, rolling into core/season3/main, then merge results into master after a final pass and verify suite. Owner authorizes creating core/season3/main and the master merge for this close only. Standard loop and routing.

## Target end-state
- Every completed season-2 subgoal leaf has an `outcome` node; those bundle into `bigger_outcome` nodes until three `overview` nodes exist, one judged against each live vision (`vision:alive` · `vision:all-is-one` · `vision:self-perpetuating`), handed to Prime as the close report.
- After AA1 send.py MOVE lands (deprecate/move, never git rm; box KEEP; g1.40 FOLDS) and DG5/DG7 after-MOVE checks close: Prime rolls `core/season2/main` into `core/season3/main` by hand (owner-authorized create of that branch for this close only), then merges the result into master after one verify suite pass.
- `season.py rollover --apply` is not the path unless a new-engine gap blocks the manual cut; no extra rollover machinery is built.

## Invariants
- Season close does not start before send lands.
- Never `git rm` send.py / workflow.py; deprecate + move.
- `core/season3/main` and the master merge are authorized for this close only; no other new top-level branch.
- Standard loop: DG1 goals+hyps · DG2 experiments+verdicts · downstream DGs+SM · council zoomed-out · Prime does not build.
- Skip agi-infer. No rollover `--apply` unless the dry-run names a gap this leaf cannot close by hand.

## Falsifier
1. `git rev-parse --verify core/season3/main` and three nodes `overview:s2-*` with `judged_against:` one each of `vision:alive`, `vision:all-is-one`, `vision:self-perpetuating`; `python3 extensions/agi/bin/commands.py run verify` exits 0 on that tip.
2. Negative: `git log --all --diff-filter=D -- extensions/agi/bin/send.py` shows no deletion commit; the bytes live under `extensions/agi/deprecated/`.

## Out of scope
goal:g7.16.1.11.11 (AA1 BUILD, still open) · mint-user chew · agi-infer · S3-L1 work (doc:s3-plan: START NOTHING until this rollover)

## Agent Notes
Assigned to **sanctuary-master** (place leaves); Prime runs the authorized branch cut after the three overviews land.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam 23:3xZ 10-05 (date -u): minted under g5.4 from the owner's 23:3xZ close order quoted in Why / OWNER. Near miss: running season.py rollover --apply now — dry-run would mint 3 visions without --visions-from and bump ladder before send lands. Property: owner said set the goal now; the cut waits on send.
<!-- THOUGHT:END -->
