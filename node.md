---
id: goal:g14.11
mint_id: 373a25fed620451e8584301b4bee3813
type: goal
parents:
  - goal:g14
next_edges: []
confidence: 0.8
edited_by: thought-master
goal_id: G14.11
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 43470de7ea43f8ec
season: 2
seeds:
  - hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery
  - hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box
  - hypothesis:lm-bonsai2-27b-kid-tier
status: active
tags:
  - local-maxxing
  - switch
  - battery
  - mvp
title: "G14.11: THE SWITCH — one battery (HumanEval + IFEval + the typed-round row), one reference bar (deepseek-v4.1-flash), one rule: within 10 pct on every row → the contributing chains mint ONE mvp → build node → the town runs its own parents and kids on it (owner 21:5xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.11

## Agent Notes
**Owner source (2026-09-20 21:5xZ, verbatim on goal:g14):** "if any of these ideas pan out let the chain mint an mvp that ties all the different chains together that contributed and make a build node and start using it. So start using our own you to run your own kids and parents if performance starts approaching within %10 of deepseek v4.1 flash bench performance." Trajectory (21:4xZ): "overall trajectory is maximize evaluation performance on the local model."

**Commits to.** One battery, one reference bar, one switch. The **battery** is agentic coding + instruction following measured the same way for every candidate and for the reference: HumanEval 164 (execution pass@1), IFEval 541 (strict prompt-level accuracy), and — when it exists — the town's own typed-round success (a minimal engine round on the candidate, done-or-not, as in round 0). The **reference** is deepseek-v4.1-flash via OpenRouter on the same protocol, re-taken when the model id changes. The **switch**: when a local candidate is within 10 % (relative) of the reference on every battery row, the contributing chains (G14.6–G14.9) mint ONE mvp that cites each contributing hypothesis, a build node follows, and the town's parents and kids run on it.

**Invariants.** The gap table (candidate × eval, absolute and relative, paired discordant counts vs the reference, tok/s, VRAM, USD/1M tokens, `abliterated?`) is the only place a candidate's standing is read from; every row resolves into `datasets/`; a proof of "within 10 %" never switches anything by itself — it triggers the mvp mint; the mvp names every contributing chain by id; the first real rounds on the local build are compared to the same rounds on the reference before the switch is called complete.

**Falsifiers.** (a) The switch rule is falsified as a criterion if a candidate within 10 % on the battery fails ≥ 30 % of real typed rounds the reference completes — then the battery is missing the agentic row and is extended before any switch. (b) The goal is falsified for a season if no candidate reaches 90 % of the reference on any battery row after G14.6, G14.7 and G14.9 each have a landed chunk — recorded, not hidden.

**Done when.** The town's parents and kids run on its own build for one full week of rounds with the gap table showing ≤ 10 % on every row and the round-completion rate within 10 % of the reference's.

**First chunk (minted):** `hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery` (SWR.01: the missing reference row + the first gap table). Sub-sub-goals are the director's to mint (G14.11.1 the battery + reference, G14.11.2 the mvp/build/switch), same format, before any chunk runs.
