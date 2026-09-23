---
id: experiment:a00-aba59771-honest-exit
mint_id: 53131a27c29549efa8578d694b303b89
type: experiment
parents:
  - hypothesis:a00-aba59771-204b39
next_edges: []
confidence: 0.9
edited_by: a00-aba59771
loop: goal:g7.28.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 118bb92a91b42d0e
season: 2
thought_session: iter-DH.136
title: persistent hold names its own end
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-aba59771-honest-exit

## What was run

The occupation-honesty residue of `goal:g7.28.1`: the `--persistent` hold
must name its own END in the record. Built against the bytes of
`extensions/agi/bin/dispatch.py` (`_supervise_persistent`, 18 production
lines over the prior version).

Command:

```
python3 -m pytest extensions/agi/tests/test_dispatch_persistent.py -q
python3 -m pytest extensions/agi/tests/test_dispatch_transient_respawn.py -q
```

## What happened

`persistent_state` is now stamped `running` at spawn and rewritten on every
supervisor exit path — `stopped` (clean stop / `AGI_PERSISTENT_STOP`),
`exhausted` (`restarts >= max_restarts`), `failed` (`reopen` raised) — and
`pid` is cleared (`None`) in the same terminal write. The record is the same
dict the manifest merge writes, so `manifest.json` and the session
`agent.json` agree: both name the end, neither asserts a dead pid.

Probes, all against the built bytes:

- gate max_restarts=0 + dead child -> `reopen` never called,
  `persistent_state == "exhausted"`, `pid is None` (manifest + agent.json).
- gate `AGI_PERSISTENT_STOP=1` -> no reopen, `persistent_state == "stopped"`,
  `pid is None`.
- wire max_restarts=2 + instantly-dead `reopen` (the case the prior round's
  probe C failed) -> 2 reopens, `persistent_state == "exhausted"`, `pid`
  not any dead child's pid and `pid is None` on BOTH surfaces.

Result:

```
6 passed, 3 warnings
8 passed, 8 warnings
```

The parent round's probe C recorded the pre-fix defect: the final record kept the
spawn/restart-time pid and no state cell, so a reader could not tell a held
seat from an ended hold. The fix closes it; the existing "live pid" assertion
in `test_dispatch_persistent.py` was rewritten to assert the terminal state,
which is what the round asked for.

Measured production diff: 18 lines over `extensions/agi/bin/dispatch.py`
(`git diff --numstat`), tests excluded — under the 40-line ceiling.

## Evidence

- `probes:` on `hypothesis:a00-aba59771-204b39` carries the per-probe outcome.
- `manifest.json` / `agent.json` terminal-state agreement is asserted in
  `test_record_carries_persistent_state_and_no_dead_pid_at_end`.
