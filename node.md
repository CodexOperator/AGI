---
id: hypothesis:harness-bin-paths-resolve-per-box
mint_id: f79873e54097430d914454d590d6cfcd
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 10:1xZ relay, goal:g5): after the key round; build loop; one [merge-up] to thought-master."
ceiling: 3 USD, <= 5 kids, pi parents (raised from 1 USD / <= 2 kids under the owner 10:3xZ "ceiling set to something silly"; round 3 = the raw-cell readers outside the adapters)
edited_by: director-engine
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ceiling raised 1 USD / <= 2 kids -> 3 USD / <= 5 kids for round 3. MEASURED 11:4xZ 09-23 on the director-engine post branch: after round 1 moved the config bins to ~/.npm-global/bin/<tool>, workflow.py _pi_harness (workflow.py:1381) still reads the RAW cell (config before PI_BIN, a /home/ubuntu literal fallback) and execs it at :1793 -- every mur died at once with pi exited rc=1; rotate.py:1868 and harness_template.py:223 read the raw cell too. The claim (every harnesses.<h>.bin resolves through ONE resolver) is not met until they do. Owner 10:3xZ (verbatim on goal:g5): ceilings may be set silly so work continues.
<!-- THOUGHT:END -->
