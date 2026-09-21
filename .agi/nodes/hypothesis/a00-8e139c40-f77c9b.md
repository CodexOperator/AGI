---
id: hypothesis:a00-8e139c40-f77c9b
mint_id: 49ae71949eaa4d0da7ef93e6cc7d4fbc
type: hypothesis
parents:
  - goal:g17.14.2
next_edges: []
edited_by: a00-8e139c40
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 158606546566e673
season: 2
title: config-row-only grok-bot harness resolves without dispatch.py
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:a00-8e139c40-f77c9b

## Hypothesis

A single config row is all the seam needs on the config side: adding
`harnesses."grok-bot"` = `{adapter: grok_bot, bin: <peer path>, models:
{kid, parent}}` to `.agi/config.json`, with NO `provider` key, makes
`adapters.resolve(cfg, "grok-bot")` return the row with
`adapter == "grok_bot"`, keeps the dash-to-underscore default working when
the `adapter` key is absent, and leaves `pi` and `copilot-cli` resolution
unchanged — all without touching `dispatch.py`.

**Would prove it:** the three acceptance probes pass on the live config and
`grep -Ein 'grok' extensions/agi/bin/dispatch.py` prints nothing.

**Would disprove it:** `resolve` raises for grok-bot, returns the wrong
adapter name, or any pre-existing harness row stops resolving after the
edit.

Measured by `experiment:a00-8e139c40-e048c6`; ruled on by
`verdict:a00-8e139c40-859afa`.
