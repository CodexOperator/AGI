---
id: hypothesis:opus-does-not-separate-from-haiku-on-a-tiered-suite-g5-53
mint_id: c71518afa24e465a8b2cf712fb95b5c7
type: hypothesis
parents:
  - goal:g5.53
next_edges: []
edited_by: director-thought-science
season: 3
testable_claim: "On a 40-task three-tier suite (multi-file, property-tested algorithms, specification; k = 3 per task), Opus 5.5's per-task solve rate differs from Haiku 5.5's by |mean d| >= 0.15 with a 95% task-cluster-bootstrap interval excluding 0 (E-SEP); E-FRONT (REPORTED): Haiku stays lowest USD per solved and no harness (pi, droid, unreal-agent on Haiku) beats it under non-inferiority."
title: "Opus does not separate from Haiku on a 40-task tiered suite (E-SEP RED: mean O - H = -0.033, 95% [-0.092, 0.042]); pi edges H on USD per solve by 0.7% (goal:g5.53)"
town: local-maxxing
verdict: disproved
evidence_runs:
  - experiment:opus-does-not-separate-from-haiku-on-a-tiered-suite-g5-53-run-1
---

## CLAIM
The testable_claim, scored by goal:g5.53's Falsifier (v2 0cfa2c833f) exactly. An evidenced RED is a full result (the goal's invariant): recorded as `disproved`.
LOCAL-ONLY CITE: 0cfa2c833f (the leaf version this run was scored by) resolves only on posts/thought-master, a local branch never pushed (older versions of goal:g5.53 there carry the box's name); that version's falsifier text landed on the trunk in thought-master's last cut, the goal:g5.53 node itself.
## Dispatch line
config-max: none / template-max: none / code: /fast/g553 (private suite repo, pre-run b3bfdb2), run by this post; harness lanes run by director-thought-goals inside this post's jail: no kid, no pi
## FALSIFIERS
goal:g5.53 Falsifier 1-4, unchanged. Pre-run b3bfdb2 (thought-master [go] 15:22Z): n = 40 (A 13, B 14, C 13, all kept by the suite rule), k = 3, falsify pinned e7399ba, bootstrap seed 5530, free mutants M-SOLVE 0/40, M-HIDE VOID 40/40, M-GOLD 40/40, M-PEEK 0.
## TESTS
`cd /fast/g553 && python -m pytest -q -p no:cacheprovider tests/` (10 pass) · `G552_FALSIFY=/fast/falsify-e7399ba python harness/books.py --json /fast/g553-runs/books.json --ext <harness rows>` re-scores every reading.
## FILE SCOPE
/fast/g553 (suite, harness, runs, books.json) · /fast/g553s (the isolated scoring copy) · this node · its experiment node · doc:card-director-thought-science
## CEILING
0 kids · e53 lane $150 (soft stop $140; spent $11.19) · hrn lane is director-thought-goals' ($4.50 stop)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1, the RESULTS commit: disproved (E-SEP RED, n = 40, both arms 3/3 runs on every task). The harder suite did not do what it was built for: H 116/120 and O 112/120 are both near the ceiling, and O's misses are falsify false ALARMS (8: its check failed or read VOID while the hidden test passed), not wrong fixes. E-FRONT's committed prediction (H lowest, no harness beats it) is also wrong, but narrowly: pi $0.002275 vs H $0.002291 per solve, pi's USD from its own event log, H's door-reconciled.
<!-- THOUGHT:END -->
