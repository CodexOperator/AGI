---
id: experiment:a00-9c1eec0f-6b2908
mint_id: 5578178037e34588a3a267a0035b167a
type: experiment
parents:
  - hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp
next_edges: []
confidence: 0.7
edited_by: sensei-director
evidence_runs:
  - experiment:a00-9c1eec0f-6b2908
line_ceiling: 50
loop: hypothesis:l4-pi-review-stages-return-structured-reports-persisted-whole-with-timeouts-named-and-a-private-basetemp@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 57
profile: balanced
role: kid
scaffold_hash: d6d5098fd7af353b
season: 2
title: A new spawns pre-flight consults only the credential it will run on — another iters key does not gate it, the owning iters drained key refuses by iter name, and the cap==floor skip closes to <=
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-9c1eec0f-6b2908

## Experiment — item (6) provisioning pre-flight: ownership gate + `<=` skip

**Claim (6) built:** a dispatch pre-flight consults ONLY the credential the
spawn will run on; an outstanding key of a DIFFERENT iteration does not gate
this spawn; a drained key refuses only the round that owns it, naming the
owning iter; the cap==floor skip uses `<=`; the runtime-key (provisioning
ABSENT) path is unchanged.

### What I did

Edited `extensions/agi/bin/provisioning.py` (`check_key_floor`) only:

1. Added a `iter_n: int | str | None = None` parameter (dispatch's spawn
   iteration, the owning iteration). The runtime leg (ABSENT) is untouched;
   the LISTING scan now skips any machine-minted key whose `iter` token does
   not equal `iter{iter_n}` — another iteration's key is a PROXY for the
   fresh mint this spawn will run on and must not gate it. `iter_n=None`
   (a non-dispatch caller) consults every machine-minted key byte-for-byte
   as today → fail-open fallback.
2. Closed the sub-floor skip to `<=`: a key whose CAP is **at or below** the
   floor (cap==floor touches it — the TM.20 key is under the floor from its
   first cent of spend, remaining $0.9999 < floor $1.00) is SKIPPED with one
   stderr line, never refused.
3. The same-iteration drained key still refuses, and the refusal now names
   the owning iter explicitly.
4. Restored `provisioning.min_key_remaining_usd` to `1.0` in `.agi/config.json`
   (the Prime's interim `0.25`; test 5 asserts the live value).

### What happened

`python3 -m pytest extensions/agi/tests/test_provisioning.py -q` →
**89 passed, 5 skipped** (the 5 are the real-API `@live` tests, refused by
`hypothesis:l4-mint-refuses-under-pytest-unless-mocked` by design).
`git diff --numstat`: provisioning.py +57/-11, tests +100, config +1/-1.

### Six new tests (all pass)

1. `test_l4p6_another_iters_drained_key_does_not_refuse_this_spawn` — TM.20
   key (cap 1.0, remaining 0.9999) with `iter_n="SM.70"` does NOT refuse.
2. `test_l4p6_owning_it_iter_drained_key_refuses_and_names_the_iter` — same
   iteration key refuses, message contains the owning iter.
3. `test_l4p6_cap_equal_to_floor_is_skipped_not_refused` — the `<=` boundary.
4. `test_l4p6_non_dispatch_no_iter_n_keeps_todays_scan` — `iter_n=None` keeps
   today's all-key scan.
5. `test_l4p6_runtime_leg_unchanged_when_provisioning_absent` — ABSENT +
   drained runtime key still refuses, iter_n or not.
6. `test_l4p6_config_min_key_floor_is_restored_to_1_0` — reads the LIVE config.

## Evidence

`89 passed, 5 skipped in 0.34s` — full `test_provisioning.py` suite green
including the six new `l4p6` tests and every pre-existing sub-floor / gate /
runtime-leg test. `check_key_floor(..., iter_n=...)` comes with an explicit
`iter_n=None` default, so every older caller resolves unchanged.

**Follow-up (NOT in this round's lockout):** the ONE wiring line that makes the
gate live in production is `provisioning.check_key_floor(cfg, root,
iter_n=args.iter_n)` at the dispatch pre-flight (`dispatch.py`, the
`check_key_floor` call beside `check_runtime_key_usable`). `dispatch.py` is
outside the locked file scope for this round, so the check-side capability is
built and proven here and the dispatch-side threading is the next round's one
line.

## Agent Notes
Item (6): check_key_floor gains iter_n ownership gate (only same-iteration keys gate a spawn, other iters fail open), sub-floor skip closes to <= (cap==floor TM.20 key skipped never refused), owning-iter refusal names the iter, runtime ABSENT leg unchanged; floor restored to 1.0 in config. 89 passed/5 skipped. dispatch.py wiring line deferred (file locked).

Preserved as partial evidence by the director at SM.70 harvest. This kids mechanism half landed on its OWN branch only and was never independently merged -- experiment:a00-daad1e21-74be76 composed it with the sibling dispatch-wiring half (experiment:a00-2a887327-f4f77e) on one tree, re-verified with a real (non-stubbed) integration test, and IS what actually landed in provisioning.py. Kept here so the mechanism half is not lost from the graph; the working code lives in the composition node, not this one.
