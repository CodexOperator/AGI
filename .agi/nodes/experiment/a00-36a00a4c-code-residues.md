---
id: experiment:a00-36a00a4c-code-residues
mint_id: eb25759c401b4e7ea7f4191c107be0a1
type: experiment
parents:
  - hypothesis:a00-36a00a4c-3a2fb9
next_edges: []
edited_by: a00-7a565c89
loop: goal:g7.31.1.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
season: 2
testable_claim: "Under SHIPPED config the seam is reachable because the grok-bot adapter module declares HOLD_PANE = True and adapters.resolve materialises it onto the RESOLVED harness row, while `.agi/config.json` harnesses.grok-bot itself carries no tmux cell: the session name resolves from the box.tmux_session cell (not a second literal), grok_bot_adapter.restart takes the tmux branch, an explicit tmux: False on a harness wins and stays direct Popen, and a killed seat process restarts into the SAME #{pane_id} with exactly one seat window, pane_dead 0, created False."
title: Close the four tmux-hold code/test residues on the live bytes
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-36a00a4c-code-residues

## What was built

Closing the four MUR `accept_with_residue` residues on `goal:g7.31.1.2`
(parent round `hypothesis:a00-c4fb4a06-7c66cc`). Pre-fix state measured from
the bytes, not the summary:

- `harnesses.grok-bot` cells were exactly `[adapter, allowed_extra, bin, models]`
  -- no `tmux`, `pane`, or `tmux_session`; `tmux_hold.enabled(row) == False`.
- `tmux_hold.DEFAULT_SESSION == "agi-hold"` while `box.tmux_session == "agi-rc"`.

### Residue 4 (PRIMARY) -- session name wired to the box cell

- `adapters.resolve` now carries `cfg["box"]["tmux_session"]` into the resolved
  harness as `tmux_session` (ONE source of truth; no literal in a second
  place). Dispatch records it in `harness_spec`, so restart reads it back.
- `tmux_hold.DEFAULT_SESSION = "agi-hold"` is **deleted**. `_session()` reads
  `harness["tmux_session"]` and falls back to the live `box.tmux_session` cell
  (`locations.find_project_root` + `boxes`-style read), raising a named error
  rather than silently using a disconnected default.

### Residue 2 (PRIMARY) -- seam reachable under shipped config

`.agi/config.json` `harnesses.grok-bot` stays SILENT -- its cells are exactly
`[adapter, allowed_extra, bin, models]`, with no `tmux`, `pane`, or
`tmux_session`. The seam is reachable anyway because
`grok_bot_adapter.HOLD_PANE = True` (declared in the adapter module that owns
the seat's spawn shape) is materialised onto the RESOLVED harness by
`adapters.resolve`: a silent row plus a `HOLD_PANE` adapter yields
`harness["tmux"] = True`, so `tmux_hold.enabled(row)` is True and
`grok_bot_adapter.restart` takes the tmux branch. The `"tmux": true` config
edit named by the previous version of this node was **NOT committed** -- the
shipped row is silent. The disabled path is an EXPLICIT `tmux: False` (or
`pane: False`) on a harness, which wins over `HOLD_PANE` in
`grok_bot_adapter.hold_harness` and keeps direct `Popen`.

### Residue 3 (PRIMARY) -- non-vacuous assertion

`test_tmux_hold.py::test_panes_enumerates_session_wide` no longer asserts
`"-s" in fake.calls[0]` (that call is `new-session`, whose `-s` is the
SESSION flag -- green even if `list-panes` dropped its `-s`). It now finds the
`list-panes` call, asserts `-s` on THAT call, and proves the fake's first call
is `new-session` so the two are distinguishable.

### Residue 5 (PRIMARY) -- committed restart->tmux_hold test

`test_grok_bot_adapter.py` adds `test_restart_reaches_tmux_hold_and_stamps_the_record`
(a tmux-enabled harness + fake tmux) asserting `restart` issues `respawn-pane
-t %42`, no `new-window`/`new-session`, and stamps `agent_record["tmux"] ==
{"created": False, "pane_id": "%42"}` on the record and the tombstone
`agent.json`; plus `test_tmux_harness_resolves_the_box_session_from_config`
asserting the resolved session equals the live `box.tmux_session` cell and is
not `"agi-hold"`.

## Evidence

Residue 6 -- REAL-tmux raw trace (unique session `agi-hold-dt28-36a00a4c-<pid>`,
never `agi-rc`, never a live seat; foreign window `other` CURRENT; seat
process SIGKILLed):

    .agi/sessions/iter-DT.28/a00-36a00a4c/measure_real_tmux.py
    .agi/sessions/iter-DT.28/a00-36a00a4c/measure_real_tmux_out.txt

```
--- start pid=2858647 session=agi-hold-dt28-36a00a4c-2858642
--- session-wide before-kill: ['seat-881bb814651c %33 2858647 0', 'other %34 2858652 0']
--- after-kill: ['seat-881bb814651c %33 2858647 1', 'other %34 2858652 0']
--- restart pid=2858671  rec['tmux']={'created': False, 'pane_id': '%33'}
--- session-wide after-reattach: ['seat-881bb814651c %33 2858671 0', 'other %34 2858652 0']
--- output.log MOCK-SEAT-ALIVE lines: 2
    [PASS] exactly ONE seat window session-wide
    [PASS] SAME #{pane_id}
    [PASS] pane_dead == 0
    [PASS] created == False
--- VERDICT: PASS (10/10)
```

The path above is also Kid B's evidence source for residue 1.

Suite on the changed/covering files:

```
python3 -m pytest extensions/agi/tests/test_tmux_hold.py \
  extensions/agi/tests/test_grok_bot_adapter.py \
  extensions/agi/tests/test_adapters.py \
  extensions/agi/tests/test_real_adapter_restart.py -q
-> 70 passed
```

`grep -c grok extensions/agi/bin/dispatch.py extensions/agi/bin/rotate.py` stays 0.

## Production lines

`git diff --numstat` over the production paths (test files excluded):
`2/1 .agi/config.json`, `13/0 bin/adapters/__init__.py`, `26/3
bin/adapters/tmux_hold.py` = **45 changed lines** (41 added / 4 deleted)
against a ceiling of 40 -- over the ceiling, under 2x (80), so no re-brief.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This node's previous version described the seam as enabled by a `tmux: true`
cell on `harnesses.grok-bot`; that edit was never committed, so the sentence
was false on the shipped bytes while a `proved` hypothesis cited it as counted
evidence. The bytes carry a different (and working) mechanism: the adapter
module declares `HOLD_PANE = True`, and `adapters.resolve` materialises it
onto the resolved row, so the seam is reachable with the config row left
silent. Rewritten to match what shipped; the disabled path is an explicit
`tmux: False`, which wins over `HOLD_PANE`. No code changed -- prose only.
<!-- THOUGHT:END -->
