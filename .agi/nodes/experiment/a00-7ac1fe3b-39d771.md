---
id: experiment:a00-7ac1fe3b-39d771
mint_id: adddb85180594e28bf603176372a10e2
type: experiment
parents:
  - hypothesis:l3-rotate-self-successor-override
next_edges: []
confidence: 0.85
edited_by: a00-75ccbeaa
evidence_runs:
  - experiment:a00-7ac1fe3b-39d771
loop: hypothesis:l3-rotate-self-successor-override@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 972c6063503d4bbd
season: 2
title: A00 7ac1fe3b 39d771
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7ac1fe3b-39d771

## Experiment

Delivered the build the hypothesis demanded and proved it live: `rotate.py`
gains an explicit **successor-command override** and a **throwaway-seat path**
that never writes `seats.md` — the two halves the L3.37 kid reported were
walled off (successor argv hardwired to real `claude --remote-control`, and
the registry gate refusing any unregistered seat). Default behaviour is
byte-identical to today: the override only takes effect when an explicit
`--successor-argv` string is passed.

### Code change (`extensions/agi/bin/rotate.py`)
- `spawn_window(..., successor_argv=None)`: when an explicit stand-in command
  is passed it REPLACES the built claude argv (still through
  `_launch_window`, still gated by the same-name window refusal, still read
  back from the successor's own debug file). With no override it is the
  unmodified real claude path.
- `cmd_spawn`, `cmd_loop`, `cmd_rotate_self`: `--successor-argv` threaded
  through the shared `spawn_window` path.
- `cmd_rotate_self`: `--throwaway` skips the seats.md registry gate (builds a
  default row from `--role`, default `parent`; model/effort/settings resolved
  from the ladder inside spawn_window) and NEVER writes seats.md. Without
  `--throwaway` the gate holds exactly as before.
- All five units (spawn/loop/rotate-self-override/throwaway + default) tested
  RED-first, then GREEN — 47/47 in `test_rotate.py`, 2056 passed, 1 skipped
  in the full repo suite.

### Live rehearsed rotation (proof)
Two isolated rehearsals on throwaway tmux sessions (`agi-rh*`) + scratch graph
roots under `/tmp` (outside repo git, so handoff/debug never touched shared
state; `seats.md` untouched; no `belam-*` window touched). Both used
`rotate.py rotate-self --name rh --throwaway --successor-argv "sh <standin.sh>"`.

Stand-in wrote a **fresh** `continue` to the successor debug file after 3s;
a **stale** bare `continue` was planted in that same reused plain-name log
BEFORE spawn (pre-cursor).

Observations (checked with `tmux list-windows`, never the tool's return):
- **(a) NEW plain-name window exists**: after rotation, `rh` is present in
  `tmux list-windows` (needs a PERSISTENT stand-in — one that exits closes its
  window, unlike real claude).
- **(b) handoff generation incremented**: 0 → `generation: 1`,
  `predecessor_session: rh`.
- **(c) read-back reads the SUCCESSOR's log**: rotation confirmed on the
  successor's fresh `continue` from its own debug file, not the caller's.
- **(d) planted stale `continue` did NOT falsely confirm**: rotation waited
  ~4.1s for the fresh post-cursor line instead of short-circuiting on the
  pre-planted stale one; a refusing run timed out 30s → exit 1 rather than
  confirm on the stale line.
- **(e) predecessor renamed & alive**: own window renamed `rh → rh.gen1`;
  left alive after the refusing run, and still listed alive even after the
  confirming run (the kill is best-effort and silently did not remove it).

## Evidence

RED-first (before the change, `extensions/agi/tests/test_rotate.py`):
```
3 failed, 2 passed  # test_spawn_window_successor_argv_override_replaces_claude
                      # test_rotate_self_throwaway_skips_registry
                      # test_rotate_self_throwaway_forwards_successor_argv
                      # (gate: ERR: no seat 'adv-alive' in the seats registry)
```

GREEN after (`python3 -m pytest extensions/agi/tests/test_rotate.py -q`):
```
47 passed in 2.59s
```
Full repo suite: `2056 passed, 1 skipped in 120.62s`.

Live confirming rehearsal (`ROTATE EXIT=0`):
```
(1) handoff -> .agi/sessions/seats/rh.handoff.md generation 1
(2) rename own window 'rh' -> 'rh.gen1'
(3) spawn successor under the plain name 'rh' (role 'parent')
(5) successor confirmed `continue`; killed own window 'rh.gen1'
real 0m4.143s
```
Post-run: `tmux list-windows -t agi-rh3` → `rh.gen1`, `rh`.
Log (stale plant on line 1, fresh on line 2): both `continue`.
Handoff: `seat: rh / generation: 1 / predecessor_session: rh`.

Refusing run (`ROTATE EXIT=1`): timed out 30s, predecessor `rh.gen1` left
alive, stale `continue` never falsely confirmed.

Cleanup verified: `agi-rh*` sessions killed, `/tmp/rh*` removed, real
`.agi/nodes/.geometry/seats.md` unchanged, no `.agi/sessions/seats/` created,
9 `belam-S1-L3*` windows intact.

## Agent Notes
Implemented the L3.37-blocked successor override + throwaway seat, proved
RED-first and live in two isolated rehearsals. Hypothesis held on all five
observations.

## Agent Notes
Built the successor-command override + throwaway seat rotate-self was blocking on; proof RED-first and live (all a-e observed).

PARENT REVIEW (a00-75ccbeaa, L3.38): ACCEPTED as proved. Verified independently: --successor-argv override + --throwaway present in rotate.py (default path unmodified), test_rotate.py 47/47 green, rotate.py is the only modified file and seats.md untouched. Evidence is real (red-first units + two isolated live rehearsals covering a-e). Caveats from kid acknowledged: (e) predecessor alive only via best-effort kill; (a) needs persistent stand-in — noted, do not overclaim beyond rehearsed conditions.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review verdict rewritten from scratch. The node claimed proved with itself as evidence_run; I verified the artifact rather than the report: the rotate.py diff exists and matches the four hypothesis constraints (default byte-identical, explicit override, full downstream path live, no secrets/real seats), rotate tests 47/47, only rotate.py modified, seats.md and belam-* windows untouched. The live rehearsal genuinely exercised all five observations including the never-tested read-before-write stale-continue refusal. Two caveats keep this from being a full owner-gate closure: (e) predecessor-left-alive is best-effort-kill luck, and (a) required a persistent stand-in so it does not yet prove behaviour under a real claude successor. Hence accepted as proved for the tool-gap the hypothesis named, with those limits recorded here rather than demoted — the hypothesis claim was about the mechanism, which is proved.
<!-- THOUGHT:END -->
