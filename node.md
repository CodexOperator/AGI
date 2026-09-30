---
id: goal:g1.31.1.1
mint_id: 2ec429c2b0c64ba3b7c58686a707d183
type: goal
parents:
  - goal:g1.31.1
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.1.1
goal_kind: subgoal
origin: goals-doc
scaffold_hash: f2684f8ae1738a70
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - pass-b3
  - residue
  - engine-delta-1
  - config
  - formation
title: "G1.31.1.1: one cell per run-mode fact -- enhanced_survival cites goal:g7.16.2, config:formations `active` is the only mode switch, council-loop town agrees"
town: core
---
# goal:g1.31.1.1

## Why this exists
goal:g1.31.1: PASS B3 round `engine-delta-1` (demote; `.agi/sessions/workflows/runs/mur-pb3chunk1of20/verify_engine-delta-1.json`) upheld 3 items that each give one run-mode fact two answers. Measured at HEAD ff09c6101, all 3 still open:
```
fact                    home A                                         home B                                        reader
quote for enh.survival  config.json:22  goal:g7.16:29/:28 (wrong)      goal:g7.16.2.md:32,:34 (the verbatim)         brief.py:673 SOURCE line -> every brief (_prepend_head :681)
mode in force           config.json:26  active_operating_mode          .geometry/formations.md:8  active: doc:council-loop   brief.py:663 vs verification.py:1283 check_formation
                        config.json:2   operating_mode: full  (3rd!)   config.json:9,:16,:23  in_force flags         brief.py:110 _configured_profile
council-loop town       council-loop.md:12  town: core                 council-loop.md:18  "town local-maxxing"  spawn_gate nearest_vision (own town wins)
```

## Target end-state
- `.agi/config.json` `operating_modes.enhanced_survival.source` (now :22) cites goal:g7.16.2 (:32 "Let's gently dial up the concurrency…", :34 "…this is just enhanced survival mode…"), as doc:l4-formation-2-texas-two-step.md:31,:33 already do; no `goal:g7.16:2[89]` cite remains in config.json.
- ONE cell says which run mode is in force: config:formations `active` (.agi/nodes/.geometry/formations.md:8, the switch goal:g7.16's target names). `.agi/config.json` carries no `active_operating_mode` (now :26) and no per-mode `in_force` (now :9, :16, :23); brief.py `_operating_mode_block` (brief.py:641, reads config.json at :663) resolves the in-force mode from config:formations, so one brief never prints two modes (the `ACTIVE:` block vs `operating_mode: full` read at brief.py:110).
- doc:council-loop's frontmatter `town` (.agi/nodes/.geometry/formations/council-loop.md:12, `core`) equals the town its "Seated …" line states (:18, `town local-maxxing`).

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Exactly one formation is active at any moment (goal:g7.16); `verification.py` `formation` check stays PASS.
- An absent mode declaration still renders NOTHING in a brief (brief.py:641 docstring contract).

## Falsifier
1. `grep -q 'goal:g7.16.2' .agi/config.json && ! git grep -qnE '"(active_operating_mode|in_force)"' -- .agi/config.json extensions/agi/bin && git grep -qn 'config:formations' -- extensions/agi/bin/brief.py && python3 -c "import re,sys;t=open('.agi/nodes/.geometry/formations/council-loop.md').read();f=re.search(r'^town: (\S+)$',t,re.M).group(1);s=re.search(r'^Seated .*$',t,re.M).group(0);sys.exit(0 if f'town {f} ' in s else 1)" && env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_brief_render.py -q`
2. Negative: `git grep -nE 'goal:g7\.16:(28|29)' -- .agi/config.json` returns zero hits.

## Out of scope
goal:g1.31.1.2 · goal:g1.31.2 · the other goal:g1.31.* leaves · goal:g1.30 · goal:g1.29. The survival/ultimate_survival profile semantics themselves (hypothesis:l4b18-survival-modes).

## Agent Notes
Assigned to **director-general-6**.
