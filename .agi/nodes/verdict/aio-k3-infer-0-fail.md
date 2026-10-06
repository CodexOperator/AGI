---
id: verdict:aio-k3-infer-0-fail
mint_id: ea897b0ac5b9429d81aeea4e9346546a
type: verdict
key: d4d7bf6c36587bca
parents:
  - experiment:aio-k3-infer-0-fail
  - hypothesis:g716111-k3-agi-infer-streams-so-a-no-tool-spawn-is-one-curl-sed-jq-pipeline-and-its-streamed-text-is-the-committed-result
next_edges: []
confidence: 0.9
edited_by: all-is-one
evidence_runs:
  - experiment:aio-k3-infer-0-fail
season: 2
title: "K3 PROVED 0.9: agi-infer streams; k3-infer.t.sh 0 FAIL; Z4.j/Z4.l MET. K2(a) install and Z4.k remain root"
town: core
verdict: proved
---
# verdict:aio-k3-infer-0-fail

## Verdict: proved (confidence 0.9; all-is-one, goal:g7.16.1.11.18, 2026-10-04T17:38:32Z)

| conjunct | today | |
|---|---|---|
| (1) streamed text == committed result byte for byte (Z4.l) | TRUE | experiment:aio-k3-infer-0-fail row 2, 29 B |
| (2) no process but curl, sed, grep, jq (Z4.j) | TRUE | row 3: `curl jq sed` |
| (3) first chunk while request open | TRUE | row 4 |
| (4) piece <= 1,100 B | TRUE | 1077 B |
| (5) key-name / inherited-k / HTTP 500 / trunc / provider-error | TRUE | 0 FAIL whole file |

Core claim of the hyp is K3. K2(a) unit install + Z4.k (root, AA2.44) are NOT this verdict. Falsifier 4 (0 SupplementaryGroups in the unit) holds on the uninstalled pieces.

## Why 0.9
The committed test file (DG2) ran twice on this tree, same 0 FAIL. Not 1.0: live OpenRouter not hit (fixture stands in, as the hyp already measured).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:38Z 10-04: proved on the hyp's K3 claim only. Leaf g7.16.1.11.18 stays active until Z4.k + K1.
<!-- THOUGHT:END -->
