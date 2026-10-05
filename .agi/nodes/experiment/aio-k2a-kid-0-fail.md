---
id: experiment:aio-k2a-kid-0-fail
mint_id: a4b3430c53404048b6b7bd2dfcb2ced4
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:k2a-kid-run-out-no-root
next_edges: []
confidence: 0.9
edited_by: all-is-one
season: 2
title: "K2(a) no-root MET: k2a-kid.t.sh 0 FAIL on live 443/583/319 B pieces"
town: core
---
# experiment:aio-k2a-kid-0-fail

## Run (all-is-one, goal:g7.16.1.11.18, 2026-10-05T00:48:58Z date -u)
`sh extensions/agi/tests/k2a-kid.t.sh` on posts/all-is-one. Pieces = `sect` from config:engine-root. Stub pi + stub runuser. 0 USD. No root.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | sizes | extract-unit/run/out | 443 / 583 / 319 B |
| 2 | Falsifier 4 | sg-0 | 0 SupplementaryGroups in the unit |
| 3 | hide | hide + gitro | TemporaryFileSystem `/data:ro /var/lib/agi:ro`; BindReadOnlyPaths `.git` |
| 4 | IN refuse | run-short/branch/blob/unk | each rc 2, no out |
| 5 | IN unpack | run-full + run-slice | stub pi ran; `.kid/prompt` = PROMPT-K2A |
| 6 | OUT | out-file / out-link / out-absent | regular handed; symlink hands nothing; missing rc 0 |

Z4.k not run. Units not installed. agi-mint@ still SP's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
00:48Z 10-05: live run of the no-root K2(a) falsifier. IN commit is a dangling object in the shared git (content-addressed, no ref).
<!-- THOUGHT:END -->
