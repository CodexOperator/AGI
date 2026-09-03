---
id: verdict:chain-engine-r6-by-citation
mint_id: b8bd8bcdf6c240a1b5dee88948c77b32
type: verdict
parents:
  - hyp:chain-engine-r6
next_edges: []
confidence: 0.8
edited_by: l1.09-execution-parent
evidence_runs:
  - build:src-chain-engine-attractiveness
  - build:tests-chain-engine-test-attractiveness-impact
scaffold_hash: b46bda3c40593abd
supports:
  - hyp:chain-engine-r6
tags:
  - chain-engine
  - R6
  - l1.09
  - by-citation
thought_session: L1.09
title: "chain-engine/R6: closed by citation"
verdict: inconclusive_lean_proved:80
---
# verdict:chain-engine-r6-by-citation

## Verdict

`inconclusive_lean_proved:80` — **closed by citation, not by a run** (L1.09, 2026-09-03).

## Evidence

`hyp:chain-engine-r6` — *Attractiveness Function* — was specified by the cavekit build-site and never reached a verdict there. The real, non-build-site tree already carries what it asked for:

- `build:src-chain-engine-attractiveness` → `extensions/agi/src/chain_engine/attractiveness.py`
- `build:tests-chain-engine-test-attractiveness-impact` → `extensions/agi/tests/chain_engine/test_attractiveness_impact.py`

Grounds: `attractiveness.py` is the pure attractiveness function and `test_attractiveness_impact.py` its suite.

Survey: `.agi/sessions/L1.09-mining/report.md` §C. Nothing was executed for this verdict; the suites named above are the ones `commands.py run tests` already runs.

## Confidence

0.8 — the citations are real files with real test suites, but this verdict cites them rather than running them, which is why it is `inconclusive_lean_proved:80` and not `proved`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written 2026-09-03 in L1.09 to close `hyp:chain-engine-r6` by citation per the build-site survey (§C); the hypothesis is deprecated in the same pass with its `origin: build-site` cohort (goal:s18), and this verdict is the live record of where its claim is actually satisfied.
<!-- THOUGHT:END -->
