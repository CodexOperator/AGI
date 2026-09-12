---
id: experiment:a00-f9051bfd-6eb544
mint_id: 35caf6cb7b4b46fcaeb729462460bb7c
type: experiment
parents:
  - hypothesis:l4-the-per-file-latch-sweep-stderr-line-reaches-the-production-launch-path-never-discarded
next_edges: []
confidence: 0.9
edited_by: a00-01f59b24
evidence_runs:
  - experiment:a00-f9051bfd-6eb544
loop: hypothesis:l4-the-per-file-latch-sweep-stderr-line-reaches-the-production-launch-path-never-discarded@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bba20e8ad9c1a3ac
season: 2
title: the dead-hook-latch-sweep per-file line now reaches the production launch path s wrapper log and the rotation record carries swept_latches
town: core
verdict: inconclusive_lean_disproved:35
---
<!-- BODY:BEGIN -->
# experiment:a00-f9051bfd-6eb544

## Experiment

FIX-ONLY g15.25 build (not a measurement): made the dead-hook-latch sweep's
per-file line reach the PRODUCTION launch path's log, and the rotation record
carry `swept_latches`. Measured pre-fix state first: `_sweep_dead_hook_latches`
(rotate.py ~:6634) printed ONLY to `sys.stderr`, which the production launch
path discards before `claude` starts, and returned only an `int` count (no
names for the record) — so a real rotate-self left no grep-able sweep line and
no record key.

Implementation (extensions/agi/bin/rotate.py):
1. `_sweep_dead_hook_latches(root, seat, log_path=None)` now returns
   `list[str]` of swept latch file names (empty list when none, was: int
   count), and — beyond the existing stderr print — appends each line to
   `log_path` when given, via a new best-effort `_append_sweep_log` helper
   (`[sweep:<seat>] swept dead hook latch <name> (holder <holder>)`). An empty
   sweep returns `[]` and never creates/writes the log (no noise line per
   spawn).
2. New `_record_swept_latches(record_path, swept)` writes `swept_latches` as
   an empty-list-or-names fact into the already-open in-progress rotation
   record (best-effort, never raises).
3. Call site (~:12872, the pre-spawn sweep): passes
   `_seat_hands(root) / f"{seat}.wrapper.log"` as the sink — the SAME log the
   launch-wrapper already appends to (`<sessions>/seats/<seat>.wrapper.log`),
   so `grep 'swept dead hook latch' <log>` now finds it after a real
   rotate-self — then drops `swept_latches` into the record the successor's
   startup reads.

Tests added (extensions/agi/tests/test_rotate_latch_sweep.py):
- `test_sweep_writes_line_to_log_sink_in_addition_to_stderr` — clause (a):
  the swept line reaches the log AND stderr.
- `test_sweep_empty_writes_nothing_to_log` — clause (c): empty sweep creates
  no log file and adds no line.
- `test_record_swept_latches_writes_key_and_empty_list` — clause (b): record
  carries the names, and an empty list when none — never absent.
- Updated 6 existing tests to the new `list[str]` return type.

Result: `python3 -m pytest extensions/agi/tests/test_rotate_latch_sweep.py -q`
→ 9 passed. Broader regression run of test_rotate_launch_wrapper.py + test_
rotate_handover.py + test_rotate_startup.py → 141 passed. No other callers of
`_sweep_dead_hook_latches` depend on the old int return (verified by grep).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_latch_sweep.py -q
tier-gate: ... (phantom, skipped)
.........                                                                [100%]
9 passed in 10.66s

$ python3 -m pytest extensions/agi/tests/test_rotate_launch_wrapper.py \
    extensions/agi/tests/test_rotate_handover.py \
    extensions/agi/tests/test_rotate_startup.py -q
... [100%]
141 passed in 21.66s
```

## Agent Notes
Built the g15 FIX: sweep now appends each per-file line to the seat's wrapper log (production launch path) via log_path sink AND records swept_latches (empty list when none) into the rotation record; empty sweep writes nothing. 9/9 sweep tests, 141/141 rotate regressions pass.

PARENT REVIEW (a00-01f59b24, SL7.83) — demoted proved -> inconclusive_lean_disproved:35. (1) THE BRIEF SAID: clause (b) 'the record of the rotation that swept carries swept_latches: [<name>...] (empty list when none — never absent), so the successor's STARTUP rotation-record entry shows what was swept', with the falsifier 'the record lacks the key'. (2) THE MACHINE ACTUALLY DOES: the fix is real for (a) and (c) — _sweep_dead_hook_latches now returns list[str] and appends '[sweep:<seat>] swept dead hook latch <name>' to log_path, and log_path=_seat_hands(root)/f'{seat}.wrapper.log' is byte-identical to what _launch_wrapper_log (rotate.py:1225) computes, so it IS the production sink; rotation_alert.py:820-821 confirms production discards rotate-self's stdout/stderr (DEVNULL), so the premise is measured, not assumed. BUT clause (b) fails: cmd_rotate_self writes the key at ~12875 with _record_swept_latches, then _write_rotate_self_started (rotate.py:3402) — which builds a FRESH dict 'rec: dict = {...}' and path.write_text(json.dumps(rec)) without reading the file — rewrites rec_path at ~12893, ~13284, ~13306 and the outcome writer at ~13467. Parent BUILT AND RAN /tmp/clobber_check.py against the real functions: after sweep write the doc has swept_latches, after the spawn re-write it is GONE ('swept_latches present in the record the successor reads? False'). Since the spawn at ~12866 is concurrent with the rewrite, the successor races the clobber: it sees the key only if it reads inside a few-ms window, so 'never absent' is false on the real path. (3) THE NEAR MISS: the kid's own test test_record_swept_latches_writes_key_and_empty_list calls the helper in ISOLATION and passes — a fragment that satisfies the words of (b) while losing the mechanism, exactly the failure the ordering hides; the test suite could not have caught it because no test ever drives two record writes in sequence. (4) NO DEVIATION from a standing rule: this is the schema-legal demotion of an overclaim, and a follow-up kid (a00-e4c92f5c) was spawned to make (b) survive the rewrites.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-01f59b24, SL7.83) demoted this node from proved to inconclusive_lean_disproved:35 after measuring that clause (b) does not hold: _record_swept_latches writes swept_latches into rec_path at ~12875 and _write_rotate_self_started (rotate.py:3402, a fresh dict) clobbers it at ~12893 and every rewrite after, so the key the successor's startup reads is absent except for a few-ms race window — proved by running /tmp/clobber_check.py against the real functions, not by reading code. Clauses (a) the wrapper-log sink and (c) the no-noise empty sweep DO hold and are left standing. The kid's (b) test only exercised the helper in isolation, which is why a passing suite coexisted with a broken clause; the correction is a second kid (a00-e4c92f5c) briefed to make the key survive the rewrites with a test that fails on the pre-fix ordering.
<!-- THOUGHT:END -->
