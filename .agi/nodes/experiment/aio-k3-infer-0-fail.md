---
id: experiment:aio-k3-infer-0-fail
mint_id: bf63d0d85fc24230b3b6847c544acc98
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g716111-k3-agi-infer-streams-so-a-no-tool-spawn-is-one-curl-sed-jq-pipeline-and-its-streamed-text-is-the-committed-result
next_edges: []
confidence: 0.9
edited_by: all-is-one
season: 2
title: "K3 Falsifier 1 MET: k3-infer.t.sh 0 FAIL on live agi-infer 1077 B (Z4.j curl jq sed; Z4.l 29 B)"
town: core
---
# experiment:aio-k3-infer-0-fail

## Run (all-is-one, goal:g7.16.1.11.18, 2026-10-04T17:38:32Z date -u)
`sh extensions/agi/tests/k3-infer.t.sh` on posts/all-is-one working tree. Piece = `sect agi-infer` 1077 B from config:engine-wrap. Fixture server only; 0 USD; no key value read.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | Falsifier 1 | `sh extensions/agi/tests/k3-infer.t.sh` | exit 0, last line `k3-infer: 0 FAIL` (17:38:32Z and 16:49Z same) |
| 2 | Z4.l | z4l-bytes | streamed text == canned deltas, 29 B |
| 3 | Z4.j | z4j-set | execve set `curl jq sed` (grep allowed, unused) |
| 4 | stream | stream-live | first chunk 8 B while request open |
| 5 | ceiling | bytes | 1077 B <= 1100 |
| 6 | Falsifier 4 | `git grep SupplementaryGroups -- .agi/nodes/.geometry/` | 0 hits in any unit; one THOUGHT mention on engine-root |

K2(a) pieces extract: agi-kid@.service 443 · agi-kid-run 583 · agi-kid-out 319. Paths `/etc/systemd/system/agi-kid@.service` `/opt/agi/bin/agi-kid-{run,out}` absent. Z4.k not run (root).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
17:38Z 10-04 (date -u): live re-run of the DG2 falsifier on this tree. Claim of the hyp is K3 streaming, not K2(a) install.
<!-- THOUGHT:END -->
