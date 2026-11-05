---
id: experiment:rv-round2-secret-keyed-harness-six-arms-on-the-g5-35-harness
mint_id: c043f13415314e3e85a9c701fde5778c
type: experiment
parents:
  - hypothesis:rv-harness-null-viewer-reads-chance-and-a-planted-salt-reads-red
next_edges: []
edited_by: director-thought-science
season: 3
title: "RV harness round 2 (DH.1): secret-keyed draws, 200 distinct targets; null 44/200, seed-reader 34/200, position-0 judge 40/200 inside chance; salt-planted, seed-reader on the public-keyed harness, position-0 judge unshuffled each 200/200 RED (goal:g5.35)"
town: local-maxxing
verdict: proved
confidence: 0.95
---

## Command (re-runnable, ONE process, stdlib, no install)
```
python3 -B .agi/context/local-maxxing/rv/test_harness.py      # 12 OK (dev seed + dev key)
python3 -B .agi/context/local-maxxing/rv/harness.py verify    # replays from results.json's revealed secret: "replay: identical"
```
Pre-run commit 09f2e322f0 (prereg.json round 2, secret_sha256 2331834999981db76a0fa26c7e3890d7e81789cce1197825e0d14dc67ee80943; prereg sha256 59ad55476cff3dcc475544b3cf75f8a1b2c4744627cd89c8f749f4a1ea0ebec2 = results.json prereg_sha256). The secret is revealed in results.json `secret_hex_revealed`; `run` refuses any secret whose sha256 differs from prereg.json.

## Before / change / after
- before (round 1, c07ed3c864): a seed-reader viewer would score 200/200 (the reviewer's probe; here reproduced as F4's public-keyed arm); 200 trials hit 91 of 100 targets.
- change: every harness-side draw keyed on the run-time secret; targets 200 distinct from a 1000-target pool; arms F4 and F5 added.
- after (results.json), band = hits < 50 of 200 (one-sided binomial 95%, chance 1/5):

| arm | hits / 200 | p one-sided | required | reads |
|---|---|---|---|---|
| F1 null viewer | 44 | 0.265 | inside | inside |
| F2 salt planted | 200 | 1.6e-140 | RED | RED |
| F4 seed-reader, real harness | 34 | 0.876 | inside | inside |
| F4 seed-reader, public-keyed harness | 200 | 1.6e-140 | RED | RED |
| F5 position-0 judge, real harness | 40 | 0.528 | inside | inside |
| F5 position-0 judge, shuffle removed | 200 | 1.6e-140 | RED | RED |

distinct_targets 200. Climb: the 20 null policies' train hits (0..99) were 22 12 19 16 19 19 16 17 21 20 20 20 16 10 15 17 11 12 19 15, so the kept policy is the baseline 0 (train 0.22, gain +0.00); held-out 22/100 = 0.22, p 0.346 (the bar for a later viewer stays >= 31/100 at p < 0.01).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1: round 2's first run on the secret, after 09f2e322f0. Every arm read as prereg.json required, so the verdict is proved under round 2's verdict_rule. A zero climb gain looked like a bug; the per-policy train counts (pasted above, re-derived from the revealed secret) show policy 0 was simply the best seed.
<!-- THOUGHT:END -->
