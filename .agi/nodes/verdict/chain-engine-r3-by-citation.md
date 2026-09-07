---
id: verdict:chain-engine-r3-by-citation
mint_id: b8c9aaa041694543b7bacc46388ce138
type: verdict
parents:
  - hyp:chain-engine-r3
next_edges: []
confidence: 0.8
edited_by: season.py
evidence_runs:
  - build:src-chain-engine-ranking
scaffold_hash: 0340bf6ce5bfbc55
season: 1
supports:
  - hyp:chain-engine-r3
tags:
  - chain-engine
  - R3
  - l1.09
  - by-citation
thought_session: season
title: "chain-engine/R3: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:chain-engine-r3-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:chain-engine-r3` — *Longest-Chain Attractor* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-chain-engine-ranking` → `extensions/agi/src/chain_engine/ranking.py`

Grounds: `ranking.py` is longest-chain ranking with a deterministic tie-break.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:chain-engine-r3` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->