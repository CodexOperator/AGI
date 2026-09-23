---
id: hypothesis:harness-bin-paths-resolve-per-box
mint_id: f79873e54097430d914454d590d6cfcd
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 10:1xZ relay, goal:g5): after the key round; build loop; one [merge-up] to thought-master."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 459950905e195a44
season: 2
tags:
  - config-max
  - harness
  - paths
testable_claim: Every harnesses.<h>.bin resolves through one resolver (env override, then ~ expansion, then PATH), so the same .agi/config.json dispatches on every box with no /home/<user> literal and no hand-made symlink.
thought_session: belam-S2-L5-I
title: Harness bin paths resolve per box — env override, then ~ expansion, then PATH; no /home/<user> literal in the merge-shared config
town: local-maxxing
---
# hypothesis:harness-bin-paths-resolve-per-box

# Harness bin paths resolve per box — no /home/<user> literal in the merge-shared `.agi/config.json`

**Owner 2026-09-23 10:1xZ (Prime pane, relaying thought-master; verbatim on `goal:g5`):** "the machine paths in config are stale."

**Assigned: director-engine** (the Prime, 09-23) · build loop · after the key round · one `[merge-up]` to thought-master.

## Measured (the Prime, 10:1xZ)
```
config   harnesses.{pi, pi-local, copilot-cli, grok-bot}.bin = /home/ubuntu/.npm-global/bin/... — core-town's user; this box runs as belam
today    PI_BIN (profile + tmux -g) overrides pi dispatch here; nothing expands ~ in dispatch.py / workflow.py
```

## CLAIM
Every `harnesses.<h>.bin` resolves through ONE resolver — an env override (PI_BIN-style, per harness), then `~`/`{home}` expansion, then PATH — so the same merge-shared config dispatches on every box with no `/home/<user>` literal.

## Dispatch line
config-max: the bins as `~/...` or bare names in the one config file / template-max: none / code: the one resolver in the adapter path

## FALSIFIERS
- a `/home/<user>` literal survives in `.agi/config.json`
- a box needs a hand-made symlink or a profile export to dispatch

## TESTS
- tmp HOME with the binary under `~/.npm-global/bin` → resolved · env override wins · PATH fallback · a missing binary refuses by name
- neighbourhood: `test_adapters*.py test_dispatch.py test_bin_help_smoke.py`

## FILE SCOPE
the adapter's bin resolution · `.agi/config.json` bins · tests.

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
