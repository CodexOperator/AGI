---
id: verdict:chain-engine-r9-by-citation
mint_id: 0417d34340e4452cb9369b5c828a373c
type: verdict
parents:
  - hyp:chain-engine-r9
next_edges: []
confidence: 0.8
edited_by: l1.09-execution-parent
evidence_runs:
  - build:src-chain-engine-queries
scaffold_hash: aae5bbcb71cdfd1f
supports:
  - hyp:chain-engine-r9
tags:
  - chain-engine
  - R9
  - l1.09
  - by-citation
thought_session: L1.09
title: "chain-engine/R9: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:chain-engine-r9-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:chain-engine-r9` — *Chain Query API* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-chain-engine-queries` → `extensions/agi/src/chain_engine/queries.py`

Grounds: `queries.py` has `longest_n`, `branching_factor` and `mid_chain_candidates` by name, plus `all_chain_queries_pure`.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:chain-engine-r9` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->
