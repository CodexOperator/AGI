---
id: hyp:chain-engine-r7
mint_id: 2efa24ebc4b6441aa9ec578d5e3271af
type: hypothesis
parents:
  - idea:domain-chain-engine
confidence: 0.5
edited_by: l1.09-execution-parent
origin: build-site
status: deprecated
subgraph: false
tags:
  - chain-engine
  - R7
testable_claim: Configuration File
thought_session: L1.09
title: "chain-engine/R7: Configuration File"
---
**Description:** Tunable parameters live in a single chain-configuration file at a documented path inside the project context. The file declares the join, fork, fresh-start, idea-split, and weight parameters.

**Acceptance Criteria:**
- [ ] The configuration file declares the keys `chain_min_join_length`, `mid_chain_join_prob`, `fresh_start_prob`, `big_idea_vs_small_idea_split`, and `attractiveness_weights` with the four documented sub-keys (`length`, `depth`, `recency`, `mvp_count`)
- [ ] When the file is missing, documented defaults apply and a warning identifies the absent file
- [ ] When a key is missing or out of range, the engine raises a structured error naming the offending key
- [ ] Editing the file changes engine behavior on next run without code changes

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Deprecated 2026-09-03 in L1.09 per the build-site survey (`.agi/sessions/L1.09-mining/report.md` §C/§E); disposition CLOSE-BY-SMALL-EXPERIMENT, not run: no TOML file or loader exists, but `mid_chain.py::MidChainConfig` already holds the values as a dataclass; the small experiment is wiring that dataclass to `.agi/config.json` rather than inventing config machinery.
<!-- THOUGHT:END -->
