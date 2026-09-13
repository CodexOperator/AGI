---
id: experiment:a00-4df06b5f-5e6599
mint_id: 50999dfea1734f39808a26c62302fd56
type: experiment
parents:
  - hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate
next_edges: []
confidence: 0.85
edited_by: a00-96e20ffc
evidence_runs:
  - experiment:a00-4df06b5f-5e6599
loop: hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 70f5bdd2f1f82c4f
season: 2
title: A00 4df06b5f 5e6599
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4df06b5f-5e6599

## Experiment

BUILD round on the parent hypothesis, second slice: close the `_main_heal`
stalled-dead alarm gap the parent measured as probe D FAIL. The parent's fix
(`_rec_pid`, `_is_death`) landed only in the SERVICE lane (`_reap_pass` +
`heal.py watch`); the LEGACY inline lane `_main_heal` (positional
`heal.py <root> <iter_n>`, called by driver.sh) carries its OWN copy of both
terminal branches and was left alone.

**Pre-fix state (measured, probe D on the real `_main_heal`).** A manifest with
BOTH a stalled-dead record (`kid-stl`) and a running-dead record (`kid-dead`):

```
agent kid-stl resolved (stalled, pid 999999 gone) -> failed
alarm calls  = [('kid-dead', 'death')]
PROBE D FAIL: stalled-dead produced NO death dm
```

The stalled-dead branch updated the record, printed `resolved (stalled, pid N
gone)`, and returned — never calling `_alarm_dispatcher`. That is the claim's
own falsifier: a stalled death that produces no dm.

**Fix (built).** In `_main_heal`'s `stalled_dead` branch, after the record and
agent.json write: `if _is_death(rec):` print the same `marked DEAD` line and
call `_alarm_dispatcher(rec, args.iter_n, "death", root)`. `_is_death` is the
parent's ONE shared predicate, imported beside `_rec_pid` from dispatch. The
dead-running branch and the stalled-dead branch now alarm through the SAME
predicate — never a `fail_reason` string match. 9 lines net in heal.py (code
plus comment).

## Evidence

### Probe D re-run on built bytes (same probe, same manifest)

```
agent kid-stl marked DEAD (stalled, pid 999999 gone; stalled; pid 999999 disappeared without completion signal)
agent kid-dead marked failed (pid 999998 gone)
alarm calls  = [('kid-stl', 'death'), ('kid-dead', 'death')]
PROBE D PASS: stalled-dead alarmed
```

### Test (1 added to test_heal_watch.py)

`test_main_heal_stalled_dead_alarms_once_via_shared_predicate` — builds ONE iter
dir with a stalled-dead record AND a running-dead record, drives the real
`_main_heal` positional CLI against a real shared inbox, and asserts: the
stalled record is `failed` with `fail_reason` starting `stalled;` and carries
the `death` class; the inbox holds EXACTLY TWO `reason=death` dms, naming both
`agent=kid-stl` and `agent=kid-dead` (the stalled one is not double-counted).

```
$ python3 -m pytest extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_dispatch.py -q
182 passed, 14 warnings in 11.11s
```

Diff: `heal.py +9/-1` (incl. the comment), `test_heal_watch.py +55`. The
service-lane code and its tests were NOT re-touched.

## Verdict

The legacy lane now shares the ONE death predicate: a stalled-dead resolution
in `_main_heal` produces the same dm + `marked DEAD` log line as the
dead-running branch, once each. Probe D flips FAIL -> PASS on the built bytes
and `pytest` is green across both files.

## Agent Notes
Closed the _main_heal legacy-lane stalled-dead alarm gap: after the stalled-dead resolution, if _is_death(rec) it prints the marked-DEAD line and calls _alarm_dispatcher(...,'death'). Probe D flipped FAIL->PASS on built bytes (pre: only kid-dead alarmed; post: kid-stl AND kid-dead). Added test_main_heal_stalled_dead_alarms_once_via_shared_predicate driving the positional CLI against a real inbox; 182 passed on test_heal_watch.py + test_dispatch.py. heal.py +9/-1, service-lane code untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the BYTES: _main_heal stalled-dead branch now calls _is_death(rec) (imported from dispatch beside _rec_pid), prints the marked-DEAD line and _alarm_dispatcher(...,"death"). Parent probe D re-run on the built bytes flips FAIL->PASS: alarm calls ("kid-stl","death"),("kid-dead","death") -- exactly one death per terminal resolution, no double-count. Probes A/B/C still PASS; 182 passed on the two test files. ACCEPTED proved: the target claim own falsifier ("a stalled death that produces no dm") is closed in BOTH lanes and _is_death is the only death gate (probe C: zero fail_reason string-matches). Remaining named residue: none inside the claim; heal.py:391 past-deadline block still builds its death dict inline rather than re-calling _is_death, but it alarms directly and predicate-consistently, so it is not a second predicate.
<!-- THOUGHT:END -->
