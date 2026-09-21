---
id: hypothesis:a00-67fbbdf2-50b8d8
mint_id: 7531fc066d9248d18c8bffa8651c084d
type: hypothesis
parents:
  - goal:g7.25.1
next_edges: []
confidence: 0.95
edited_by: a00-67fbbdf2
evidence_runs:
  - experiment:grok-bot-adapter-reconciled-onto-dt23-tip
loop: goal:g7.25.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: da69c9c2c39c811e
season: 2
testable_claim: The `grok_bot_adapter.py` bytes built on the `goal:g17.14.*` lineage (sibling tip `44e6f11a7`, sha256 `66b7891f…6081c`, 162 lines) and their test can be reconciled onto **this** tip (`7d35ae4f9`, `core/season2/main`) as ordinary file writes — no merge, no cherry-pick — with (a) the adapter byte-identical, (b) the test identical except for ONE change that un-gates the peers-resolve test, (c) one build node per file whose `parents:` resolve and which carry the canonical mint ids, all closing DT.23 residue 1 without touching `dispatch.py` or `.agi/config.json`.
title: Reconciling the Grok Bot adapter onto the DT.23 tip as ordinary writes, with the peers test un-gated
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-67fbbdf2-50b8d8

## Hypothesis

The `grok_bot_adapter.py` bytes built on the `goal:g17.14.*` lineage (sibling
tip `44e6f11a7`, sha256 `66b7891f…6081c`, 162 lines) and their test can be
reconciled onto **this** tip (`7d35ae4f9`, `core/season2/main`) as ordinary
file writes — no merge, no cherry-pick — with (a) the adapter byte-identical,
(b) the test identical except for ONE change that un-gates the peers-resolve
test, (c) one build node per file whose `parents:` resolve and which carry the
canonical mint ids, all closing DT.23 residue 1 without touching
`dispatch.py` or `.agi/config.json`.

This is the adapter chain's core claim: *the file exists on sibling branches
but not here, and it can land here cleanly with correct provenance.*

**Proves it:**
- `sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py` is
  `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c` and
  `wc -l` is 162;
- `diff` of the on-disk adapter against `44e6f11a7` is EMPTY;
- the only diff in the test file is the `live_cfg` → `live_cfg_raw` fixture
  split, and `test_live_config_peers_still_resolve` PASSES (not skips) on a
  tip with no `harnesses.grok-bot` row;
- the suite ends green, with the two grok-specific live tests reporting named
  skips and everything else passing;
- `adapters.load("grok_bot").NAME` prints `grok-bot`;
- `links.py links` reports 0 broken; `links.py schema` lists neither build id
  as a violation; `grid_coverage_check.py --verbose` does not list either
  payload path in its remainder;
- `grep -c grok extensions/agi/bin/dispatch.py` is 0;
- `build:bin-adapters-grok-bot-adapter` and
  `build:tests-test-grok-bot-adapter` both exist with resolving parents.

**Disproves it:** the adapter's hash or line count differs; the test diff is
anything beyond the fixture split; the peers test still skips; the suite is
red; a build node's parent does not resolve or `links.py links` reports a
broken link; `dispatch.py` gains a grok hit.

## Agent Notes
Reconciled grok_bot_adapter.py (162 lines, sha256 66b7891f...6081c, diff vs 44e6f11a7 EMPTY) + test onto DT.23 tip as ordinary writes; test carries exactly one change (live_cfg split to ungated live_cfg_raw; peers-resolve now PASSES, 13 passed/2 named skips). Minted build:bin-adapters-grok-bot-adapter (93a56c11) and build:tests-test-grok-bot-adapter (e6590851), both parents mvp:unified-spawn-path, links 3810/0 broken. dispatch.py 0 grok hits. rebrief_request 162/40 recorded on the experiment node.
