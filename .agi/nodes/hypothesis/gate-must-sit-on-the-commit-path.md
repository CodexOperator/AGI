---
id: hypothesis:gate-must-sit-on-the-commit-path
mint_id: 8708cfbb5c4846c69f11709ae331e7e8
type: hypothesis
parents:
  - goal:g7
next_edges: []
edited_by: director
scaffold_hash: c11dacc844a74168
scale: engine
testable_claim: Every decisive verdict that reaches a commit carries evidence_runs>=1 or is demoted, regardless of write path (cli.py done, post_wire, write.py, plain file write)
thought_session: L1.08
title: Gate must sit on the commit path
---
# hypothesis:gate-must-sit-on-the-commit-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
"Measured 2026-09-03 in loop L1 waves 2-4: unevidenced_decisive_verdicts rose 6 -> 7 -> 10 -> 11 while bin/evidence_gate.py never fired, because pi parents and kids wrote node files directly. Session-new nodes carrying verdict: proved with no evidence_runs, no edited_by, no evidence_gate stamp: the-falsifier-and-the-corpus-census, scaffolds-are-born-valid-now, a01-de655bfd, a00-c96efd87, a01-6331daf4, a00-e3daad09. The gate is enforced only on cli.py done and post_wire.py. Claim: the gate must also run where bytes are accepted -- grid commit --all, the iteration commit, or the smoke/metrics read -- demoting to inconclusive_lean_*:50 and stamping demoted_from exactly as the writer paths do, so no write path can bypass it. Falsifier: hand-write a proved verdict with no evidence into a fixture node, run the commit/read path, assert it comes out demoted; remove the guard and watch that test go red."

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"Director-minted after watching the metric climb across three live waves. Placement question (which path owns the gate), not a brief-text question. Re-minted once: the first copy vanished uncommitted between waves."
<!-- THOUGHT:END -->
