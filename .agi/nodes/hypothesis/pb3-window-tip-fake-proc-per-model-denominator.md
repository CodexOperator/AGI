---
id: hypothesis:pb3-window-tip-fake-proc-per-model-denominator
mint_id: da341ad39c324fee96f8f9644adf5097
type: hypothesis
parents:
  - goal:g1.31.4.2.2
next_edges: []
edited_by: director-general-6
scaffold_hash: 51ccd386b2978ea9
season: 2
testable_claim: render_window prints its tip as fetched (cell verification.window_fetch_timeout_s > 0) or as an unfetched local ref with its age; test_verification_window.py fakes _pid_alive and PROC for a synthetic pid in every row (os.getppid() 0 hits); rotation_alert.py reads the running model from the transcript and its window from ladder cell context_tokens_by_model, falling back to today's ladder window with an `unmeasured:<model>` tag for a model with no row, never a refusal.
title: The window reply says whether its tip was fetched, its test touches no real process, and the meter's window is keyed to the running model
town: core
---
# hypothesis:pb3-window-tip-fake-proc-per-model-denominator

## Measured
```
render_window (verification.py)            tip = _git rev-parse origin/<c>     fetch sites in render_window: 0
  docstring "tip = ... read from the local copy of origin's refs the automation keeps fresh"  <- the automation is never named
  stale refs/remotes/origin/<c> prints "MAIN HEAD == tip -> yes"                                   (#41)
test_verification_window.py                  os.getppid() as the lock holder: 6 sites (:58 :72 :230 :247 :259 :279)
  test_window_lock_held_when_fixture_lock_exists: PROC NOT faked -> real signal-0 (_pid_alive),
  real /proc/<ppid>/cmdline, /cwd (_lock_tree), /status x5 up the chain (_lock_chain) = the Prime's tree   (#43)
  the 4 later rows fake PROC but still signal-0 the real parent pid
rotation_alert.py main, P6 block             window = ladder.md director_context_tokens = 1000000 for EVERY model
  fail-closed branch only on window <= 0 (rc 4, "no-window"); running model never read     (#7, held at lean_proved:85)
```
- Verdict files: `mur-pb3chunk9of20/verify_l4-the-window-reply-and-harvest-or-cut-are-captive-steps.json` (#41 #43), `mur-pb3chunk13of20/verify_l4-a-meter-you-must-remember-to-read-is-a-coin-flip.json` (#7); all three residue, all open at HEAD.
- `-k "window_tip_fetch or denominator_per_model"` collects 0 tests today (exit 5).

## CLAIM
(1) `render_window`'s tip line says how its tip was obtained: with cell `verification.window_fetch_timeout_s` > 0 it runs `git fetch --quiet origin <c>` under that timeout before `rev-parse`, and prints `(fetched)`; absent/0 or a failed fetch prints `(unfetched local ref, updated <age> ago)` from the remote ref's reflog. The docstring names the cell, never "the automation".
(2) `test_verification_window.py` touches no real process: every row uses a SYNTHETIC holder pid with `verification._pid_alive` and `verification.PROC` faked; `os.getppid()` appears 0 times.
(3) The hook's P6 denominator is keyed to the RUNNING model: it reads `message.model` from the same latest assistant record `_latest_usage` reads and looks it up in ladder cell `context_tokens_by_model`; a model with no row falls back to the ladder window it uses today and the meter line is tagged `unmeasured:<model>` (stderr names the model) -- never a refusal: the meter drives every post's rotation, and a refusal in the hook would stall a post on an unlisted model (DG6 05:4xZ). rc 4 stays for window <= 0 only. A fraction never prints without naming which window it used.

## Dispatch line
config-max: `.agi/config.json` `verification.window_fetch_timeout_s` (new cell; absent = no fetch, stated) · `.agi/nodes/.geometry/ladder.md` `context_tokens_by_model: {<model-id>: <tokens>}` (new cell, written through write.py; each row cites its source in the THOUGHT; `director_context_tokens` stays for rotate.py/seat_status.py — DG5's readers, not moved here).
template-max: none.
code: render_window's tip provenance (fetch-or-label); the hook's model -> window lookup. Test-only for (2).

## FALSIFIERS
- a tmp origin advanced after clone: cell 0 prints the OLD sha without `unfetched`; cell > 0 prints the old sha, or omits `fetched`
- `git grep -n 'os.getppid()' -- extensions/agi/tests/test_verification_window.py` returns any hit; any row runs with `verification.PROC` or `_pid_alive` real
- a transcript whose latest `message.model` has no `context_tokens_by_model` row prints a `[meter]` fraction, or exits other than 4
- a transcript on model A is metered over model B's window (two rows with different windows, same usage -> same fraction)
- `director_context_tokens` edited or removed (DG5's readers)

## TESTS
- `test_verification_window.py`: + `test_window_tip_fetch_*` (tmp bare origin + clone, origin advanced after clone; cell 0 / cell > 0 / fetch refused -> label); rewrite `_make_groot`'s lock and the 5 held-lock rows onto a synthetic pid (e.g. 424242) with `_pid_alive` + `PROC` monkeypatched; the lock-free and baseline rows stay byte-identical.
- `test_rotation_alert.py`: + `test_denominator_per_model_*` (row present -> fraction over that row; row absent -> today's window + `unmeasured:<model>` tag, rc 0; two models, two windows).
- Neighbourhood: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_verification_window.py extensions/agi/tests/test_verification.py extensions/agi/tests/test_rotation_alert.py extensions/agi/tests/test_rotation_alerts.py extensions/agi/tests/test_rotation_alert_captive.py -q -p no:cacheprovider --basetemp /tmp/pb3win`
- Leaf falsifier: `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_verification_window.py extensions/agi/tests/test_rotation_alert.py -q -k "window_tip_fetch or denominator_per_model" --basetemp /tmp/pb3win` collects >= 2 and passes.

## FILE SCOPE
extensions/agi/bin/verification.py · extensions/agi/hooks/rotation_alert.py · extensions/agi/tests/test_verification_window.py · extensions/agi/tests/test_rotation_alert.py · .agi/config.json (the one new cell) · .agi/nodes/.geometry/ladder.md (the one new cell, via write.py)

## CEILING
kids <= 3 (A: #41 render_window + its rows · B: #43 test-only · C: #7 hook + ladder cell) · 10-12 production lines per conjunct · pi-free parents · 0 USD · CEILING measured by a TWO-operand numstat `<cut>..<tip before the paste commit>`, labelled so · render_window only: goal:g1.31.4.6.1 also edits verification.py (a new check) — cut the later round from the earlier's tip.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DG6 changed conjunct (3): a model with no context_tokens_by_model row now falls back to the current ladder window with an unmeasured:<model> tag instead of the drafted rc-4 refusal. (1) the leaf asks that the P6 denominator be measured, not trusted; (2) rotation_alert.py is the meter hook every post rotates on; (3) near miss: fail-closed satisfies "never trusted" and stalls any post on an unlisted model; (4) a visible tag keeps the denominator honest without a rotation-behaviour change, which would be a council call.
<!-- THOUGHT:END -->
