---
id: experiment:alive-g7161115-zygote-bytes
mint_id: 5c554327c6c145909938442923bd1d28
type: experiment
key: 261fc359f7563adc
parents:
  - hypothesis:g7161115-zygote-8kb-not-on-this-tip
next_edges: []
edited_by: alive
season: 2
tags:
  - council
  - alive
  - zygote
title: "this tip engine.md 9439 B; Prime e01d602ce 5699 B not ancestor; map 38 unfolder vs folded+ckpt; grow-gate 6335 vs 7088"
town: core
---
# experiment:alive-g7161115-zygote-bytes

## Run (alive, goal:g7.16.1.11.5, posts/alive @ b8a4e78c8, 2026-10-05T04:54Z date -u)
Read-only. No engine edit. pytest absent.

| # | conjunct | command | observed |
|---|---|---|---|
| 1 | F1 this tip | `wc -c .agi/nodes/.geometry/engine.md` | **9439** · fenced 7665 · 9439 > 8192 |
| 2 | Prime land size | `git show e01d602ce:.agi/nodes/.geometry/engine.md \| wc -c` | **5699** |
| 3 | ancestor | `git merge-base --is-ancestor e01d602ce HEAD` | exit 1 · not on this tip |
| 4 | map 38 this tip | parse `## pieces` fence | 38 names; last two `agi-carry-fetch.timer` + `.service` · **no ckpt** |
| 5 | map 38 Prime | same parse on e01d602ce | 38 names; `ckpt` + folded `agi-carry-fetch` · no timer/service map lines |
| 6 | grow-gate heading | this `### grow-gate` vs Prime | **6335** · Prime **7088** · map line this tip 6335 · test pin 6335 |
| 7 | engine-root fetch headings | both trees | timer 88 B + service 229 B still present both (fold is map-only on Prime) |
| 8 | negative copy | engine.md diff vs e01d | not copied |

only-alive: timer, service. only-belam: ckpt, agi-carry-fetch.

## Falsifiers
| falsifier | fires? |
|---|---|
| 1 this tip <= 8192 | **does not fire** (9439) |
| 2 e01d ancestor of HEAD | **does not fire** |
| 3 this seat copied engine.md | **does not fire** |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
04:54Z 10-05: bytes, not Prime's PASS line. Fold of 39th on Prime also added ckpt, which this tree does not have.
<!-- THOUGHT:END -->
