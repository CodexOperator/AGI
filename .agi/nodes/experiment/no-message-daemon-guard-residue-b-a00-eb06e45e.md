---
id: experiment:no-message-daemon-guard-residue-b-a00-eb06e45e
mint_id: 6bde077ed47e43a68e82f75dfba60fcc
type: experiment
parents:
  - hypothesis:a00-eb06e45e-cdafe3
next_edges: []
edited_by: a00-eb06e45e
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 2d2cb46b98ad5c4c
season: 2
title: "Whole-tuple review closes probe B: reviewed name with swapped exec is flagged (10 tests green)"
town: core
---
<!-- BODY:BEGIN -->
# experiment:no-message-daemon-guard-residue-b-a00-eb06e45e

## Experiment

Closed the residue the parent measured in v2 of
`extensions/agi/tests/test_no_message_daemon.py`: a name ALREADY on the
allowlist whose exec is swapped for a neutral resident router was invisible,
because the novelty channel keyed on `kind:name` only and the keyword channel
found no seeded keyword.

v3 reviews the WHOLE `(kind, name, exec/cmd)` tuple. `ALLOWED_SURFACE` now maps
each declared entry to the exact `exec_start`/`cmd` the live node carries plus
its reason, and a new SPEC-DRIFT channel flags any *enabled* entry whose
normalized exec differs from the reviewed string. Novelty (new name) and
keyword (name/exec) channels are kept.

### Probe B — BEFORE (v2, committed bytes)

```
find_message_daemons({"services": {"agi-reaper": {"enabled": True,
    "exec_start": "python3 hubd.py serve"}}, "jobs": {}})
-> []                       # agi-reaper is allowlisted; hubd.py serve has no keyword
```

### Probe B — AFTER (v3, the built bytes)

```
find_message_daemons({"services": {"agi-reaper": {"enabled": True,
    "exec_start": "python3 hubd.py serve"}}, "jobs": {}})
-> ['service:agi-reaper']   # spec drift: exec != reviewed exec
```

### Real-surface negative control (v3)

```
crons.load_crons_node(<real .agi>)
find_message_daemons(node)               -> []
declared_surface(node) == ALLOWED_SURFACE -> True (both directions)
each reviewed exec == live node's spec    -> True (execs MEASURED, not guessed)
```

### Controls exercised (none skipped)

| control | entry | expected | observed |
|---|---|---|---|
| novelty, neutral new name | `agi-outbound-hub` / `python3 hubd.py serve` | flagged | `service:agi-outbound-hub` |
| **spec drift = probe B** | `agi-reaper` exec swapped to `python3 hubd.py serve` | flagged | `service:agi-reaper` |
| keyword | `agi-message-router` / `python3 router.py serve` | flagged | flagged |
| drift not trigger-happy | `agi-reaper` with reviewed exec | clean | `[]` |
| negative, real surface | live `.agi` crons node | clean | `[]` |

## Evidence

Command:

```
PYTHONPATH=/tmp/pytestenv python3 -m pytest \
  extensions/agi/tests/test_no_message_daemon.py -q
..........                                                               [100%]
10 passed in 14.12s
```

Files:

- `extensions/agi/tests/test_no_message_daemon.py` (v3, 10 tests; test-only).
- Scratch: `.agi/sessions/iter-DH.174/a00-eb06e45e/`
  (`probe_b.py`, `test_v2.py`, `test_v3.py`, `exp_body.md`).
- Production lines changed: 0 (ceiling 40).

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v2 novelty keyed on kind:name, so a reviewed name whose exec changed was invisible; the parent measured probe B -> []. v3 stores each entry reviewed exec_start/cmd in ALLOWED_SURFACE and adds a spec-drift channel over the normalized (kind,name,exec) tuple; probe B now -> [service:agi-reaper]. Test-only change, production lines 0.
<!-- THOUGHT:END -->
