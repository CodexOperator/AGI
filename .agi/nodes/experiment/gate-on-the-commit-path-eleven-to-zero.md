---
id: experiment:gate-on-the-commit-path-eleven-to-zero
mint_id: 54fcfdb0b6bf4d2f8004910be6c54a87
type: experiment
parents:
  - hypothesis:gate-must-sit-on-the-commit-path
next_edges: []
confidence: 0.9
edited_by: parent
evidence_runs:
  - experiment:gate-on-the-commit-path-eleven-to-zero
scaffold_hash: dee63186d6500726
thought_session: L1.08
title: Gate on the commit path eleven to zero
verdict: proved
---
# experiment:gate-on-the-commit-path-eleven-to-zero

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
**Placement.** The evidence gate now runs on the non-session path of `grid.py commit` (`cmd_commit` calls `evidence_gate.enforce_on_disk(root, paths)` before any node is versioned). Chosen over the smoke/render step and a new `commands.py` step because commit is where a node file is ACCEPTED as a version, it already reads every node file to decide what changed, and it runs every iteration, on the 5-minute cron, and last in the `verify` workflow -- so no write path (cli.py done, post_wire, write.py set, a plain file write) can reach a version without passing it. D3 session drafts are not gated: a draft is under review, not accepted.

**Before.** `python3 extensions/agi/bin/metrics.py` on 2026-09-03 ~21:30: `unevidenced_decisive_verdicts=11`. `evidence_gate.py enforce --dry-run` listed exactly those 11 (the metric definition, not a naive grep: a list citing a real node counts, so the-falsifier-and-the-corpus-census and scaffolds-are-born-valid-now are NOT in it): experiment:a00-521484bb-c1dd5f, experiment:a00-71589f54-a3c13c, experiment:a00-875ec777-07cb04, experiment:per-spawn-keys-were-never-used, experiment:the-bound-at-eight-real-agents, experiment:the-renderer-retired-and-what-it-took-with-it, experiment:the-serializer-ate-the-command-node, experiment:the-viewport-reaches-parity, mvp:a00-eeaa5239-8e388f, verdict:a00-a667efeb-43f94e, verdict:a00-e3daad09-469593. Five of the eleven had no evidence_runs at all; six carried a bare int (`evidence_runs: 1` or `2`, edited_by: director, written through write.py), which goal:g7.3 counts as 0.

**Run.** `python3 extensions/agi/bin/grid.py commit --all` printed one `EVIDENCE-GATE demoted <id>: proved -> inconclusive_lean_proved:50` line per node (disproved -> inconclusive_lean_disproved:50 for per-spawn-keys-were-never-used) and the summary `grid: 27 new version(s), 0 error(s) (missing mint_id), 221 with payload, 1 payload(s) unresolved, 11 demoted by the evidence gate`. Each node kept its body and THOUGHT, gained `demoted_from` and a `demote_reason` ending in `[caught at grid commit, not by a writer path]`, and kept its author-written evidence_runs value (the commit path reviews bytes it did not write; the count is already in the reason).

**After.** The 11 read 0. The metric read `unevidenced_decisive_verdicts=1`: hypothesis:an-mvp-that-points-backward-is-score-neutral, modified by a concurrent parent 22 seconds before the read (`verdict: proved`, `evidence_runs: 1`, via write.py), uncommitted and mid-edit -- the exact defect, reproduced live during the sweep. Left untouched because it is another agent in flight; `enforce --dry-run` already lists it for the next `commit --all`.

**Falsifier, red then green.** With the `enforce_on_disk` call removed from `cmd_commit`: `test_commit_path_demotes_a_hand_written_unevidenced_proved` -> `AssertionError: assert "proved" == "inconclusive_lean_proved:50"` and `test_commit_path_drives_the_metric_to_zero` -> `assert 2 == 0`; the captured grid summary read `0 demoted by the evidence gate`. Call restored byte-identical (cmp), both green.

**Tests.** 14 fixture tests on the commit path in tests/test_grid.py (real git repo, hand-written nodes: demotes unevidenced proved, byte-identical on evidenced, idempotent, leaves pending and leans, honours bypass, session drafts ungated, status shadow in lockstep, lifecycle status untouched, bare int demoted with attestation kept, dangling citation kept, taxonomy violation demoted, self-citation asymmetry, named-file commit resolves against the whole corpus, never deletes or moves, unparseable node skipped with a report, drives metrics.evidence_stats to 0) and 27 pure tests in tests/test_evidence_gate.py. Full suite after the last edit: 1452 passed, 0 failed (baseline 1381 + 41 here + other agents concurrent additions).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. Minted by the parent owning hypothesis:gate-must-sit-on-the-commit-path to record the one live application of the gate at the commit path, with the before and after numbers and the red output the falsifier required. Cites itself: an experiment IS its own run.
<!-- THOUGHT:END -->
