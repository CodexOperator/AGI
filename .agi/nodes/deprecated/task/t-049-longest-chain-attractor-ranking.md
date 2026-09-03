---
id: task:t-049
mint_id: 67c9ed5da6094f86b957735ac16683f9
type: task
parents:
  - hyp:chain-engine-r3
acceptance_criteria:
  - R3.1 (rank chains by attractiveness with deterministic tie-break)
  - R3.2 (longest chain is among top-ranked when no other factor dominates)
  - R3.3 (short chains can rank above longer ones when non-length scores higher)
  - {"R3.4 (ranking is pure": "equal inputs \u2192 equal outputs)"}
blocked_by:
  - task:t-047
  - task:t-052
cavekit_req: chain-engine/R3
edited_by: l1.09-execution-parent
effort: M
origin: build-site
status: deprecated
tags:
  - M
  - tier--1
thought_session: L1.09
tier: "-1"
title: "T-049: Longest-chain attractor + ranking"
---
**Description:** Implement `rank_chains(chains, weights, config)` that calls the attractiveness function (T-052) and sorts descending. Tie-break by chain id sequence lexicographically. Ranking is pure (no mutation).

**Files:** `agi-tree/src/chain_engine/ranking.py`, `agi-tree/tests/chain_engine/test_ranking.py`

**Test Strategy:** Three-fixture suite: long chain wins under length-only weights; short-but-recent chain wins when recency dominates; pure-function test calls function twice and asserts equal outputs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §E); task `chain-engine/R3` under `hyp:chain-engine-r3`, whose disposition is disposition CLOSE-BY-CITATION -- closed by `verdict:chain-engine-r3-by-citation` citing `build:src-chain-engine-ranking`: `ranking.py` is longest-chain ranking with a deterministic tie-break.
<!-- THOUGHT:END -->
