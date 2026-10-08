---
id: goal:g1.31.4.5
mint_id: 4c02a4cffd02487ca77b2d2040239777
type: goal
parents:
  - goal:g1.31.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 5db808248b27ef81
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - config
title: "G1.31.4.5: box literals + engine root -- no /home/<user> cell in config.json, paths.get resolves on this box, engine_for refuses, no bogus engine_commit drift"
town: core
---
# goal:g1.31.4.5

## Why this exists
goal:g1.31.4: PASS B3 (trunk @578650193, re-located at HEAD ff09c6101) upheld 4 residues where a box-specific literal or a silent fallback stands in for a root the engine can derive, council LANES #47 #34 #10 #2 (DG6, config.json cells + driver + verification):
- `harness-bin-paths-resolve-per-box` — `.agi/sessions/workflows/runs/mur-pb3retry5/verify_harness-bin-paths-resolve-per-box.json`, 1 upheld (item 4).
- `lm-every-experiment-path-is-a-config-variable` — `.agi/sessions/workflows/runs/mur-pb3chunk7of20/verify_lm-every-experiment-path-is-a-config-variable.json`, 1 upheld (stale box.root).
- `l4-verification-counts-and-engine-root` — `.agi/sessions/workflows/runs/mur-pb3chunk16of20/verify_l4-verification-counts-and-engine-root.json`, 1 upheld (engine_for fallback).
- `a00-4d063889-c4e95d` — `.agi/sessions/workflows/runs/mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json`, 1 upheld (item 2).

```
.agi/config.json :158 locations.pi_home   /home/<user>/.pi/agent   <- not this box's user
                 :159 locations.claude_home /home/<user>/.claude
                 :172 box.root            /home/<user>/work/agi    (does not exist here)
                 :173 box.logs_dir        /home/<user>/logs
                 :27  engine_commit       179f9560…  (git cat-file: not an object)
paths.py:87-98  get() joins onto box.root  -> paths.py sessions_dir = non-existent dir
commands.py:61-82 engine_for: no ancestor engine -> return ENGINE_ROOT (:82), silent
driver.sh:138-180 HEAD != engine_commit on every run -> DRIFT WARNING (:178)
```

## Target end-state
- `.agi/config.json` :158-159 (`locations.pi_home`, `locations.claude_home`) and :172-173 (`box.root`, `box.logs_dir`) hold no `/home/<user>` literal: each is derived per box (placeholder/`~`/resolver) or right for this box, and a committed test scans the LIVE config for home literals (today `test_retired_box_prefix.py:43,60` covers box.root only via EXEMPT; `test_no_home_literal.py` walks code only).
- `.agi/context/local-maxxing/paths.py:87-98` `get()` returns a path under a root that exists on this box, or refuses by name (`box.root … does not exist`), never a silent non-existent path; `paths.py:8` docstring matches.
- `extensions/agi/bin/commands.py:61-82` `engine_for` resolves the engine for both layouts (ancestor, and the `<project>/agi/` clone child per CLAUDE.md Layout) and REFUSES a graph root it cannot resolve instead of returning the script's `ENGINE_ROOT` (:82); `verification.py:1796` never prints an unflagged mixed engine/graph pair.
- `.agi/config.json:27` `engine_commit` no longer pins a non-object: in the one-repo layout the pin is retired (or the check skips when `$PLUGIN_ROOT` is the project repo), so `driver.sh:138-180` prints no DRIFT WARNING on a clean smoke run.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- A home path belongs in a `box.*` / `locations.*` cell, never in code (`test_no_home_literal.py:1-9`); the fix changes the cell's value or derivation, never moves the literal into code.
- No cell is deleted without re-pointing every reader in the same commit.

## Falsifier
1. From /data/work/agi, each exits 0: `test -d "$(python3 .agi/context/local-maxxing/paths.py sessions_dir)"` · `test -d "$(python3 .agi/context/local-maxxing/paths.py pi_traj_dir)"` · `! python3 -c "import sys,tempfile,pathlib;sys.path.insert(0,'extensions/agi/bin');import commands;d=pathlib.Path(tempfile.mkdtemp())/'.agi';d.mkdir();commands.engine_for(d)" 2>/dev/null` (a graph root with no resolvable engine must raise) · `! (bash extensions/agi/driver.sh --smoke --max-iters 1 2>&1 | grep -q 'DRIFT WARNING')`.
2. Negative: `git grep -n '"/home/' -- .agi/config.json` returns zero hits.

## Out of scope
goal:g1.31.4.4 (workflows config-max) · goal:g1.31.4.6 (missing tests + lost warnings, incl. the behavioural drift test) · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.
