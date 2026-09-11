---
id: experiment:a00-f0612463-a3d3e1
mint_id: fbf5e69671ee4777b39c87f2fcf2be62
type: experiment
parents:
  - hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one
next_edges: []
confidence: 0.72
edited_by: a00-11c41cc9
evidence_runs:
  - experiment:a00-f0612463-a3d3e1
loop: hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 045260f46db6c299
season: 2
title: A00 f0612463 a3d3e1
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-f0612463-a3d3e1

## Experiment

SL1.07 fix round under `hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-fires-at-turn-one` — three owed items, all landed, 3 new tests + 1 repaired test, suite green.

### Item 1 — core fix: stop refusing tmux's own format syntax as a startup placeholder

`_resolve_startup_placeholders` (rotate.py) `re.sub`s `\{([A-Za-z_][A-Za-z0-9_]*)\}` and RAISED on any key not in `STARTUP_PLACEHOLDERS`. The template's `after_join` `join` entry carries tmux's OWN literal `#{window_id}` / `#{window_name}`, so the regex matched `{window_id}` inside `#{window_id}` and refused the WHOLE join command — meaning the service could never perform the join step on any real rotation (the previous kid's own caveat (9), confirmed real).

Fix (`_sub` in `_resolve_startup_placeholders`): a `{name}` immediately preceded by `#` is LITERAL tmux syntax — return it byte-for-byte and do NOT raise. A bare `{window_id}` NOT preceded by `#` still refuses (kept, owed item ii). `refuse_empty` unchanged. Narrow by construction.

Proved on the built bytes:
```
(9) after_join dry-run: 4 command(s) resolved after a 20s delay; NOTHING run, no dm sent
    [join] dry-run: tmux list-windows -t agi-rc -F '#{window_id} #{window_name}' | grep throwaway-fix
```
The `join` entry is now RESOLVED (not REFUSED), `#{window_id} #{window_name}` passed through literally, and NOTHING ran (dry-run). Before the fix this line was `[join] REFUSED: unknown startup placeholder {window_id}`.

Test: `test_tmux_hash_brace_format_is_literal_but_bare_brace_is_not` (test_rotate_startup.py) — asserts `#{window_id} #{window_name}` passes through byte-for-byte, `{tmux_session}`/`{succ_name}` still substitute, and bare `echo {window_id}` still raises naming `window_id`.

### Item 2 — bootstrap-before-spawn falsifier (owed iv)

`test_bootstrap_writes_before_spawn_in_rotate_self` (test_rotate.py) reads the LIVE `cmd_rotate_self` source and asserts the first `_write_bootstrap(` call site precedes the `spawn_window(` call site. Demonstrated FAILING when deliberately inverted — moved the pre-spawn write to after the spawn call:
```
E       AssertionError: _write_bootstrap() must run BEFORE spawn_window() in cmd_rotate_self; a turnaround-one bootstrap is only valid pre-spawn
E       assert 14048 < 13378
```
…then restored the original order; passes. This is the falsifier the SL1.03 harvest asked for (turn-one proof is now a code-ORDER assertion, not a code-position guess).

### Item 3 — AGI_SEAT export for cmd_loop / cmd_spawn (owed v)

Added `--seat` to both the `spawn` and `loop` subparsers; `cmd_spawn` and `cmd_loop` now forward `seat=getattr(args, "seat", None)` into `spawn_window` → `_shell_cmd`, which exports `AGI_SEAT=<name>` only when a seat is given. Absent → forwarded as None → launch line byte-identical to today.

Tests: `test_spawn_window_agi_seat_export_and_byte_identical_absent` (seat=None line has no `AGI_SEAT=`, seated line carries `export AGI_SEAT='sanctuary-director' && `, and stripping that export makes the two lines equal) and `test_cmd_spawn_and_loop_forward_seat` (monkeypatches spawn_window, asserts both commands forward args.seat through, None when absent).

### Repaired regression (consequence of owed i) — test_rotate_selfreap.py

`test_rotate_self_s12_skip_names_missing_connection` was ALREADY red in the tree (fails with my placeholder guard reverted too): the rotate-self after_join fallback (owed i, landed SL1.05) now fires `send_dm`, and send.py resolves the recipient via `tmux list-windows` — a real subprocess a hermetic fixture never stubbed. Repaired by allowing that read in the test (list nothing → no recipient → nudge no-ops); every other subprocess stays refused.

## Evidence

- Dry-run join RESOLVED, `#{window_id} #{window_name}` literal (above).
- New tests: 3 pass. Repaired: selfreap suite 19 pass.
- Batched suites: `test_after_join_service.py test_rotate.py test_rotate_startup.py test_rotate_selfreap.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py` → 212 passed; `test_session_complete.py test_rotate_complete.py test_rotate_handover.py test_rotate_next.py test_rotate_tail.py test_rotate_templates.py` → 78 passed; `test_heal_watch.py` → 15 passed. 305 total. (Informational line about a phantom dead-pid record appears from the tier gate; harmless.)

## Verdict reasoning

Per the assignment's own bar, `proved` requires FIXING the refusal AND showing the dry-run join RESOLVED — both done. The residual gap: the JOIN executes and AGI_SEAT rides the argv, but no LIVE tmux/turn-one hook firing was observed end-to-end (fixture-level order, incl. `model_confirm` and the hook-keyed AGI_SEAT export, is proven by tests; a live claude first turn is not). Hence an honest `inconclusive_lean_proved` rather than a bare `proved`.

## Agent Notes
Fixed the false-positive refusal: tmux '\#{window_id}'/'#{window_name}' is literal (byte passthrough), bare '{window_id}' still refuses; join now RESOLVES in rotate-self dry-run. Added bootstrap-before-spawn falsifier (fails when inverted, restored). Wired AGI_SEAT export for cmd_loop/cmd_spawn --seat (absent stays byte-identical). Repaired a pre-existing red selfreap test (after_join send_dm now reaches a real tmux read a hermetic fixture never stubbed). 305 tests green incl 3 new + 1 repaired.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SL1.07 (a00-11c41cc9): ACCEPTED at inconclusive_lean_proved:75, no demotion. I verified the mechanism, not the report. (1) The resolver fix is real and narrow: _resolve_startup_placeholders L4770 now returns m.group(0) when the char before the match is "#", so tmux-s literal #{window_id}/#{window_name} passes through; my own dry-run now shows "[join] dry-run: tmux list-windows -t agi-rc -F \x27#{window_id} #{window_name}\x27 | grep dryfixA" RESOLVED, where it was REFUSED before. A bare {window_id} still raises. This is the load-bearing fix of the round: the service can now perform the join. (2) The order falsifier is a real code-order assertion that the kid demonstrated failing when inverted (14048 < 13378), not a comment. (3) --seat wired through cmd_spawn L1265 / cmd_loop L1464 into spawn_window. I re-ran the six touched/neighbour suites myself: 223 passed. The selfreap repair is legitimate and worth flagging: the after_join fallback (owed i) fires send_dm, whose recipient resolution reads tmux list-windows, so test_rotate_self_s12_skip_names_missing_connection was red on the tree after the owed-(i) landing; the kid stubs ONLY that read (empty -> no recipient -> nudge no-ops) and leaves every other subprocess refused. 75 not 100 because no live tmux/ps/claude first turn was exercised, which is the PRIME-s install/verify step by rule (L4.94). NOT cleaned: owed (iii) briefs-stripped is deliberately NOT cut as a kid — the prime-director successor brief already reduces the successor first action to the single ACK (extensions/agi/briefs/prime-director-successor.md first-action section) and the remaining first-do-X lines live in .agi/sessions/quorum/*.md, which the repo declares seat-local generational content that must NOT be merged prose-wise; a kid editing them is a collision hazard with live seats, so it belongs to the seat owners, not this round.
<!-- THOUGHT:END -->
