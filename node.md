---
id: experiment:a00-bd22eb50-96c4f7
mint_id: 6be0d5da0484438bad27951ea1510bbf
type: experiment
parents:
  - hypothesis:l4-the-pin-is-the-lease
next_edges: []
confidence: 0.85
edited_by: a00-fa7a06bd
evidence_runs:
  - experiment:a00-bd22eb50-96c4f7
loop: hypothesis:l4-the-pin-is-the-lease@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 6790c333eea90834
season: 2
title: "KID 2 of 2: the pin-reap pass + the reap arm (heal.py)"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-bd22eb50-96c4f7

## Experiment

KID 2 of the serial pair for hypothesis:l4-the-pin-is-the-lease — the PASS
(2a) + the ARM (2c) + the LIST-ONLY `pin-reap` subcommand (2b), built on KID
1's tables (`_pin_table`, `_seat_sessions`, `_judge_leases`) which I consumed
verbatim, never rewrote.

**What I added to `extensions/agi/bin/heal.py`** (rotate.py ZERO edits; its
helpers are imported, never re-implemented):

- `_pin_reap_mode(root)` — reads `.agi/config.json` `reaper.pin_reap`;
  `"armed"` ONLY when the cell is exactly `armed`, else `"dry-run"`,
  FAIL-CLOSED (a missing/malformed config never arms). Never edits config.
- `_pin_reap_arm(root, j, _rotate)` — the REAL arm, rotate.py's OWN chain
  `_pane_pid(@window)` -> `_descendant_chain` -> `_reap_chain`; a window
  with no pane pid / empty chain is SKIPPED with a reason, never guessed.
- `_pin_reap_pass(root, *, registry_dir, window_path, pid_alive, reaper,
  now, mode)` — (2a) pins -> @id-resolved sessions -> one verdict each;
  logs ONE summary line (`KEEP=x, PROTECTED=y, IN-FLIGHT=z, BELAM-UNPINNED=w,
  REAP=v`) + one line per non-KEEP; REAP alone arms (only when mode==armed),
  then ONE dm via send.py to the row's `rotated_by` holder + a watch-log
  line. Idempotent: an already-dead pid is skipped (`pid already gone`,
  reaper never called), and a reaped session's registry file is gone so a
  later pass simply does not list it. Returns the list of arm actions.
- `_watch(...)` — ONE call site, `_pin_reap_pass(root)` right after
  `_watch_seats(root)` (mode reads live config; today dry-run).
- `_main_pin_reap()` — `heal.py pin-reap [--dry-run] [--registry-dir D]` is
a SUBCOMMAND in `main()` (never a new bin/*.py), LIST ONLY regardless of
flag — it calls the pass with `mode="dry-run"`, so arming through the CLI
is impossible; exit 0.

**CRITICAL SEMANTICS honoured (KID 1's measured deviation):** never reap
straight out of `_seat_sessions` — the seat/belam NAME gate lives in
`_judge_leases`, so the pass judges first and only REAP verdicts reach the
arm. PROTECTED / IN-FLIGHT / BELAM-UNPINNED are never touched by
construction.

**Tests** appended to the SAME file KID 1 started,
`extensions/agi/tests/test_heal_pin_reap.py` (KID 1's 15 untouched):
`test_pass_dry_run_lists_never_arms`, `test_pass_armed_reaps_and_dms`,
`test_pass_armed_never_reaps_protected_or_in_flight`,
`test_pass_armed_skips_dead_pid_idempotent`,
`test_pass_mode_override_is_list_only`, `test_pass_mode_reads_config_default_dry_run`.
Fixtures only: fixture root, fixture registry dir, fixture window file via
the `window_path` seam, fake `pid_alive` table, fake `reaper`; send patched;
never touches `~/.claude/sessions`, never kills a real process.

**Commands / outputs:**

```
$ python3 -m pytest extensions/agi/tests/test_heal_pin_reap.py -q
21 passed in 0.16s          (15 KID-1 + 6 KID-2)

$ python3 -m pytest extensions/agi/tests/test_heal_watch.py \
  extensions/agi/tests/test_heal_seats.py extensions/agi/tests/test_heal_sweep.py \
  extensions/agi/tests/test_heal.py -q
54 passed

$ python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q
59 passed, 1 skipped       (the new pin-reap subcommand broke no main())
```

**LIVE dry-run proof (read-only) against the real tree:**

```
$ python3 extensions/agi/bin/heal.py pin-reap --dry-run
watch: pin-reap pass: KEEP=5, BELAM-UNPINNED=4
watch: pin-reap BELAM-UNPINNED: seat=belam sid=f3b92df1-... pid=1104695 window=@244 (no predecessor-pin table yet)
watch: pin-reap BELAM-UNPINNED: seat=belam sid=b7205ab1-... pid=2254436 window=@277 (no predecessor-pin table yet)
watch: pin-reap BELAM-UNPINNED: seat=belam sid=2aeaecba-... pid=4158336 window=@272 (no predecessor-pin table yet)
watch: pin-reap BELAM-UNPINNED: seat=belam sid=86bb4038-... pid=540475 window=@247 (no predecessor-pin table yet)
EXIT=0
```

Matches the acceptance exactly: pinned seats KEEP (5), belam predecessors
BELAM-UNPINNED (4), owner/streamer sessions absent from the judgement,
NOTHING reaped. `grep pin_reap .agi/config.json` -> no key (fail-closed
dry-run confirmed; arming is the Prime's at a merge-up).

## Evidence

- 6 new tests green, 15 KID-1 tests untouched and green (21 total).
- 54 heal-suite tests green; 59 + 1 skip in test_bin_help_smoke.
- Live `pin-reap --dry-run` exit 0, list-only, no REAP, no arm.
- Live `.agi/config.json` has no `reaper.pin_reap` cell -> dry-run default.

## Agent Notes
KID2: built _pin_reap_pass + _pin_reap_arm (rotate helpers imported, zero rotate edits) + LIST-ONLY heal.py pin-reap subcommand; ONE _watch call site; mode read from config reaper.pin_reap fail-closed. 6 new fixtures-only tests (21 total green), heal suite + bin_help_smoke green; live pin-reap --dry-run exit 0: KEEP=5 BELAM-UNPINNED=4, nothing reaped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-fa7a06bd, L4.289): accepted at the kid s own verdict inconclusive_lean_proved:85 -- NOT upgraded, because the armed path was proven only on fixtures and the live rotation that would make it proved is the Prime s merge-up step, explicitly out of this round. Verified by re-running, not by reading the report: `pytest test_heal_pin_reap.py -q` = 21 passed (15 KID-1 + 6 new); `test_bin_help_smoke.py` = 59 passed 1 skipped; live `heal.py pin-reap --dry-run` reproduced by me -> EXIT=0, KEEP=5, BELAM-UNPINNED=4, nothing reaped, owner/streamer sessions absent; `.agi/config.json` reaper cell = {max_restarts: 0} so `_pin_reap_mode` returns dry-run FAIL-CLOSED (missing cell never arms). git status shows ONLY heal.py modified, the one new test file, and the two experiment nodes -- rotate.py and config.json untouched, honouring the round s two hardest falsifiers. `_pin_reap_pass` has exactly ONE _watch call site (heal.py:816, right after `_watch_seats`); the `pin-reap` subcommand forces mode=dry-run so no flag can arm. CAVEAT for the merge-up: `_pin_reap_arm` calls rotate s `_reap_chain` with no wait override and relies on tmux windows; the first live armed pass must be watched by a human because the suite cannot exercise a real kill.
<!-- THOUGHT:END -->
