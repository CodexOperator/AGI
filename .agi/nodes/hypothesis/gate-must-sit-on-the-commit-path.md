---
id: hypothesis:gate-must-sit-on-the-commit-path
mint_id: 8708cfbb5c4846c69f11709ae331e7e8
type: hypothesis
parents:
  - goal:g7
next_edges:
  - experiment:gate-on-the-commit-path-eleven-to-zero
confidence: 0.88
edited_by: season.py
evidence_runs:
  - experiment:gate-on-the-commit-path-eleven-to-zero
scaffold_hash: c11dacc844a74168
scale: engine
season: 1
testable_claim: Every decisive verdict that reaches a commit carries evidence_runs>=1 or is demoted, regardless of write path (cli.py done, post_wire, write.py, plain file write)
thought_session: season
title: Gate must sit on the commit path
verdict: proved
---
# hypothesis:gate-must-sit-on-the-commit-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"Measured 2026-09-03 in loop L1 waves 2-4: unevidenced_decisive_verdicts rose 6 -> 7 -> 10 -> 11 while bin/evidence_gate.py never fired, because pi parents and kids wrote node files directly. Session-new nodes carrying verdict: proved with no evidence_runs, no edited_by, no evidence_gate stamp: the-falsifier-and-the-corpus-census, scaffolds-are-born-valid-now, a01-de655bfd, a00-c96efd87, a01-6331daf4, a00-e3daad09. The gate is enforced only on cli.py done and post_wire.py. Claim: the gate must also run where bytes are accepted -- grid commit --all, the iteration commit, or the smoke/metrics read -- demoting to inconclusive_lean_*:50 and stamping demoted_from exactly as the writer paths do, so no write path can bypass it. Falsifier: hand-write a proved verdict with no evidence into a fixture node, run the commit/read path, assert it comes out demoted; remove the guard and watch that test go red."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Proved, by the falsifier the brief named: a hand-written proved with no evidence, run through grid.py commit --all, comes out demoted (inconclusive_lean_*:50, demoted_from, demote_reason, status shadow in lockstep, node kept, THOUGHT kept), and removing the call turns that test red. Applied once live: 11 -> 0 for everything that had reached a commit. Placement is the non-session commit path, not smoke or a commands.py step, because commit is where bytes are accepted and it already sees every changed node. Confidence below 1 for two measured reasons: the gate holds at acceptance, so a decisive verdict written between commits is on disk unevidenced until the next commit (a concurrent parent produced exactly one such node during the sweep, and the metric read 1 until the next commit), and fantasia runs an older engine clone under its cron until it is updated.
<!-- THOUGHT:END -->