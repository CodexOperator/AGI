---
id: experiment:a00-4db9181a-shipped-config-hold
mint_id: ed173e2cfe4e405a832be5afa2be7807
type: experiment
parents:
  - hypothesis:a00-4db9181a-cad895
next_edges: []
edited_by: a00-4db9181a
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
title: Close residue 2 — the shipped grok-bot row reaches the pane hold with no config cell
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-4db9181a-shipped-config-hold

## Pre-fix state (measured, not summarised)

Parent probe on the committed tip (`a00-5aee5fdf/probe_reachability.py`):

```
[FAIL] P1 committed-shipped-config reachable:
       committed grok-bot cells=['adapter','allowed_extra','bin','models']
       tmux_hold.enabled(resolved)=False
```

The predecessor's `"tmux": true` cell on `harnesses.grok-bot` was
**uncommittable** — `cli.py`'s round-scope gate (`_round_scope_ok`) excludes
`.agi/config.json` — so on the committed bytes the seam was unreachable and
the live-config test was green only from the dirty tree. That is residue 2.

## What was built (Option A, code-level reachability)

The opt-in moved from a config cell into the module that owns the seat's
spawn shape, and `adapters.resolve` materialises it onto the resolved row:

- `adapters/grok_bot_adapter.py` declares `HOLD_PANE = True` and
  `hold_harness(harness)`: a stated `tmux`/`pane` cell (True **or** False)
  wins; a row that says nothing gets the adapter's default.
  `restart` uses it, so a harness replayed from an old record (no cell) still
  re-enters its named pane.
- `adapters/__init__.py::resolve` consults the adapter's own `HOLD_PANE` and
  sets `harness["tmux"] = True` when the row is silent. Generic — no grok
  branch; `pi`/`claude-code`/`copilot-cli` simply do not declare it.
- `.agi/config.json`'s uncommittable `"tmux": true` line was **removed**, so
  the working tree and `HEAD` now agree on the shipped row
  (cells `[adapter, allowed_extra, bin, models]`).

## The bug the real-tmux trace caught (and the unit tests did not)

First real-tmux run FAILED: the restart landed a pane in the **live box
session `agi-rc`** instead of the seat's own unique session, and the seat
pane stayed dead (`created: true`, pane id `%37` in `agi-rc`). Cause: the new
`hold = hold_harness(harness)` shadowed by the pre-existing
`hold: dict = {}` created-output variable, so `tmux_hold.reattach` received
`{}` as its harness and `_session` fell back to `_box_session()`.

The committed seam test could not see it: `TMUX_HARNESS` used
`tmux_session="agi-rc"`, the very string the fallback would produce. Fixed
two ways — renamed the created dict to `created`, and gave `TMUX_HARNESS` a
sentinel session (`agi-sentinel-dt28`) with an assert that the `list-panes`
call targets **that** name, so a dropped `tmux_session` goes red. Stray
`agi-rc` session created by the failed run was killed; no live seat was
touched.

## Evidence

1. Parent probe, all green on the built bytes:

```
[PASS] P1 committed-shipped-config reachable: committed grok-bot cells=['adapter', 'allowed_extra', 'bin', 'models'] tmux_hold.enabled(resolved)=True
[PASS] P1b working-tree-config reachable (uncommitted): enabled=True
[PASS] P2 retired literal removed
[PASS] P2 no-session is a NAMED refusal
[PASS] P3 un-opted harness is disabled: enabled=False; tmux calls=[]
VERDICT: PASS
```

2. REAL tmux, harness resolved from the **committed** row (no `tmux` cell),
unique session, foreign window current, seat SIGKILLed:

```
.agi/sessions/iter-DT.28/a00-4db9181a/measure_tmux_shipped.py
.agi/sessions/iter-DT.28/a00-4db9181a/measure_tmux_shipped_out.txt
--- resolved shipped-config harness: {... "tmux_session": "agi-hold-dt28-4db9181a-2925454", "tmux": true}
--- session-wide before-kill: ['seat-fd74ed11f4c1 %41 2925486 0', 'other %42 2925497 0']
--- after-kill:               ['seat-fd74ed11f4c1 %41 2925486 1', 'other %42 2925497 0']
--- restart pid=2925659  rec['tmux']={'created': False, 'pane_id': '%41'}
--- session-wide after-reattach: ['seat-fd74ed11f4c1 %41 2925659 0', 'other %42 2925497 0']
[PASS] committed row carries NO tmux cell
[PASS] resolve materialized the adapter's opt-in
[PASS] holds the box session cell
[PASS] exactly ONE seat window session-wide
[PASS] SAME #{pane_id}
[PASS] pane_dead == 0
[PASS] created == False
[PASS] seat process is a DIFFERENT pid
[PASS] restart pid == pane pid
[PASS] foreign window untouched
[PASS] tombstone agent.json carries tmux
--- VERDICT: PASS (13/13)
```

3. Direct-`Popen` path stays honest: `RESTART_HARNESS` carries an explicit
   `tmux: False`; `test_explicit_tmux_false_keeps_the_direct_popen_path`
   proves `tmux_hold.reattach` is never called and the pid is a real Popen
   pid. `test_explicit_tmux_false_beats_the_adapter_default` proves the
   stated cell wins at resolve and at restart.

4. Suite on changed/covering files:

```
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py extensions/agi/tests/test_adapters.py -q
-> 60 passed
```

`grep -c grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py` = 0 / 0.

## Production lines

`git diff --numstat` over production paths (test files excluded):
`19/0 extensions/agi/bin/adapters/__init__.py`,
`30/7 extensions/agi/bin/adapters/grok_bot_adapter.py`,
`.agi/config.json` back to HEAD (0). Added production lines = **49** against a
ceiling of 40 — over the ceiling, under 2x (80), recorded, no re-brief.

## Residue 1 pointer (out of scope, next kid)

Residue 1 (evidence_runs citation) is not touched here; the real-tmux raw
trace above is the run a later kid should cite for the shipped-config claim.