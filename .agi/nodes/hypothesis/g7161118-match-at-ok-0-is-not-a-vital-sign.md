---
id: hypothesis:g7161118-match-at-ok-0-is-not-a-vital-sign
mint_id: f833bcacf7df48ae8703821964595736
type: hypothesis
key: 21e059b9381fa3cf
parents:
  - goal:g7.16.1.11.8
next_edges: []
confidence: 0.8
edited_by: alive
season: 2
tags:
  - council
  - alive
  - g7.16.1.11.8
testable_claim: "goal:g7.16.1.11.8 F1 is NOT MET: parity row 20 reads MATCH while write.py is present (230669 B) and live grow-check ok=0. A report-only grow-check over live nodes (minus deprecated) prints four buckets and must not print MATCH, and must not exit 0 as a passing gate, while ok=0."
title: "MATCH at ok=0 is not a vital sign (goal:g7.16.1.11.8 F1; alive lens)"
town: core
---
# hypothesis:g7161118-match-at-ok-0-is-not-a-vital-sign

## Measured
- 17:47Z 10-04 (date -u), alive, posts/alive @ 8d131aeb8. vision:alive: a system reporting a vital sign it does not have.
- `extensions/agi/bin/write.py` 230669 B present. `grow-gate` not on PATH. `sect grow-check` 1298 B.
- grow-check: DG1 keyed hyp `ok 21e059b9381fa3cf *` rc 0 · g733 outcome `ok b5f5a4d317521645 *` rc 0 · doc:card-alive `locked: key none is not 3dbc163531a12b56` rc 1 · goal:g7.16.1.11.8 `locked: key none is not 664244b07d7040d2` rc 1.
- frontmatter `key:` 2 of 5729 live fm nodes (those two). Corpus `ok=0` at 16:49Z Z4.a (5421 locked, 299 wrong, 2 notnode) still the live shape; two keyed adds are experiments, not F1.
- parity `doc:g716111-stage25-parity` row 20 MATCH: "plain paths in the clone; write.py runs unchanged there".
- W1 last 30: G 22 · N 8. Not 100 consecutive G. config:posts `grow` cells 0/33.
- SM 17:3xZ: 11.8 UNHELD, SM does not assign Z2, no dispatch, HOLD stays.

## CLAIM
goal:g7.16.1.11.8 F1 is NOT MET: parity row 20 reads MATCH while write.py is present (230669 B) and live grow-check ok=0. A report-only grow-check over live nodes (minus deprecated) prints four buckets and must not print MATCH, and must not exit 0 as a passing gate, while ok=0.

## Dispatch line
config-max: none / template-max: none / code: none (report-only wrap of `sect grow-check`; SM does not assign Z2; council does not dispatch).

## FALSIFIERS
1. `test -f extensions/agi/bin/write.py` is true AND row 20 of doc:g716111-stage25-parity contains MATCH → F1 not met (this tip: both true).
2. A report-only pass that prints MATCH, or exits 0 as passing, while its own `ok` bucket is 0 → claim holds; a pass that labels HOLD / not-MET at ok=0 → the report side of the claim is met.
3. Negative: F1 met only when write.py is absent from the clone AND a live grow-check prints `ok <nid>` for a node the engine itself added (Y2 window), not a hand-keyed experiment.

## TESTS
scratch: `sect grow-check` on the four paths above + `wc -c write.py` + `rg '| 20 |' doc:g716111-stage25-parity`. Neighbourhood: Z4.a 16:49Z 5722-file table on doc:rse-aa1-boxes AA1.Z4a. No live-tree write besides this node.

## FILE SCOPE
this node. No engine-grow edit. No MAIN hooks (belam:belam). No Z2 issue (SM). No key: sweep of the corpus.

## CEILING
0 production lines · 0 USD · no kids · no dispatch.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 2026-10-04 16:46Z, verbatim: "Owner nudge: you are stalled at the prompt. Continue graph work now. Run AGI_POST=alive box read, take the next open graph goal for this seat, and keep going autonomously. Do not wait. No push. Encryption-town only."
OWNER 2026-10-04 16:50Z, verbatim: "go"
SM left 11.8 UNHELD and will not assign Z2. Alive lens on F1: MATCH over write.py-present + ok=0 is the false vital sign. First version. key: = hypothesis-under-goal nid (W3 on this add only; corpus HOLD stays).
<!-- THOUGHT:END -->
