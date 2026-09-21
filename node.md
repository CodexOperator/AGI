---
id: experiment:a00-73c0da26-8b98aa
mint_id: ea1d870a6e73423dbd16aed82cec9cc9
type: experiment
parents:
  - hypothesis:l4-the-heal-wait-on-a-live-stalled-record-is-a-bounded-seamed-poll-with-declared-semantics-never-a-thirty-minute-sleep
next_edges: []
confidence: 0.85
edited_by: a00-1ae4da07
evidence_runs:
  - experiment:a00-73c0da26-8b98aa
loop: hypothesis:l4-the-heal-wait-on-a-live-stalled-record-is-a-bounded-seamed-poll-with-declared-semantics-never-a-thirty-minute-sleep@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "AGI_TIER=parent PYTHONPATH=extensions/agi/bin python3 /tmp/sm238_probe.py :: probe_a -- tmp round with one LIVE-pid `stalled` record; heal._sleep patched to raise AssertionError", "expected": "live-stalled-only set returns the NAMED non-zero NOT_TERMINAL_YET (3), wall < 1 s, and never invokes a sleep", "observed": "rc=3; wall=0.0011 s; _sleep never reached (no AssertionError); record status stayed stalled", "result": "refused"}
  - {"conjunct": 2, "class": "wire", "cmd": "AGI_TIER=parent PYTHONPATH=extensions/agi/bin python3 /tmp/sm238_probe.py :: probe_c -- one `running` record, heal._sleep patched to a sentinel exception, heal._now pinned", "expected": "the production wait loop in _main_heal reaches the module-level _sleep seam", "observed": "sentinel raised: _sleep seam is threaded into the live wait path", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "AGI_TIER=parent PYTHONPATH=extensions/agi/bin python3 /tmp/sm238_probe.py :: probe_b -- one dead-pid `stalled` record + one LIVE-pid `stalled` record in the same round", "expected": "dead-stalled resolves terminal through the SM.23 predicate, live-stalled stays untouched and keeps the round non-terminal, rc != 0", "observed": "dead=failed (fail_reason names the stall), live=stalled with no fail_reason, rc=3", "result": "refused"}
  - {"conjunct": 4, "class": "gate", "cmd": "AGI_TIER=parent python3 -m pytest extensions/agi/tests/ -q -p no:cacheprovider (the FULL engine suite, not a named subset)", "expected": "full suite green, wall well under the 1800 s ceiling", "observed": "4774 passed, 15 skipped, 1 xfailed in 731.23 s; WALL 738.02 s", "result": "passed"}
  - {"conjunct": 30, "class": "wire", "cmd": "grep -n 'time.sleep' extensions/agi/bin/heal.py extensions/agi/tests/test_heal.py extensions/agi/tests/test_heal_watch.py; plus probe_a which patches _sleep to raise", "expected": "no heal test calls time.sleep; the wait loop's only real sleep is inside the _sleep seam; no real time.sleep(30) is reachable from a live-stalled set", "observed": "0 hits in test_heal.py / test_heal_watch.py; heal.py time.sleep appears only inside _sleep(); probe_a reached no sleep", "result": "refused"}
profile: balanced
role: kid
scaffold_hash: 09725e003f075c2a
season: 2
title: A00 73c0da26 8b98aa
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-73c0da26-8b98aa

## Experiment

Implemented the declared semantics and the seam in
`extensions/agi/bin/heal.py` (below `_main_heal`), then rewrote the live-stalled
test and ran the covering suite.

Pre-fix state (inherited, confirmed by reading the source):
`_main_heal` line 192 `if status != "running" and not stalled_dead: continue`
skipped a live-pid `stalled` record WITHOUT clearing `all_terminal`, so the
pass returned `0` ("all agents terminal") on a live-stalled set; and the only
blocking poll was `time.sleep(args.poll_interval_s)` at the old line 253,
reached only after `all_terminal=False`.

Changes (behaviour built, not measured):

- **Semantics.** A `status == "stalled"` record with `spid > 0` and
  `_pid_alive(spid)` now sets `all_terminal = False` and `saw_live_stalled =
  True` before the old guard can skip it. Declared in the `_main_heal`
  docstring. The SM.23 `stalled`-with-DEAD-pid path (`stalled_dead`) is
  untouched: it still resolves through `dispatch._reap_one` in the same pass
  and never clears `all_terminal`.
- **Bounded return.** New module constant `NOT_TERMINAL_YET = 3` (the NAMED
  non-zero "not terminal yet" code). After the pass: `all_terminal` -> 0;
  a live-stalled-ONLY set (`saw_live_stalled and not saw_running`) -> prints a
  one-line `NOT terminal yet` to stderr and returns 3 in ONE pass, never
  polling toward the 30-min deadline.
- **Seam.** Module-level `_sleep` and `_now` route the wait loop's only sleep
  and every clock read (`deadline`, `while`, `elapsed`, the dead-pid
  `finished_at` stamp). `--max-wait-mins` stays 30 and `--poll-interval-s`
  stays 30.
- **Tests** (`extensions/agi/tests/test_heal.py`, 3 in this cluster):
  `test_heal_leaves_a_live_pid_stalled_record_untouched` rewritten to
  monkeypatch `_pid_alive=True`, `_sleep` (recorder), `_now=0.0`, assert
  `rc == heal.NOT_TERMINAL_YET`, `rc != 0`, `slept == []`, wall < 1 s, record
  untouched (status stalled, no `fail_reason`, no `finished_at`) and the
  manifest mirrors `stalled`. The two existing SM.23 dead-stalled tests
  (`..._to_failed`, `..._to_done_unreported_on_branch_advance`) already prove
  the dead-stalled record IS terminal (rc 0, status failed /
  done-unreported); no third test was added, keeping the cluster at 3.

## Evidence

Pre-fix read (source, before edit):

```
heal.py:192   if status != "running" and not stalled_dead:
heal.py:200       continue
heal.py:253   time.sleep(args.poll_interval_s)
```

Post-fix run — named suite (`test_heal.py`, `test_heal_seats.py`,
`test_dispatch.py`), kid-tier gate refuses the bare directory by design:

```
$ python3 -m pytest extensions/agi/tests/test_heal.py \
    extensions/agi/tests/test_heal_seats.py \
    extensions/agi/tests/test_dispatch.py -q
153 passed, 30 warnings in 11.76s   (real 0m22.1s)

$ python3 -m pytest extensions/agi/tests/test_heal.py -q
17 passed in 0.31s

$ python3 -m pytest extensions/agi/tests/ -q
ERROR: AGI_TIER=kid refuses a bare full-suite directory run; run a specific
       test file or a -k filter instead.
```

The live test passes with `slept == []` and wall < 1 s, i.e. the live-stalled
set returns after ONE pass at the NAMED code and never touches the 30-min
poll. The dead-stalled tests still pass at rc 0.

## Notes

The full-suite order from the tier parent cannot be executed from a kid seat:
`extensions/agi/tests/conftest.py` refuses a bare directory run for
`AGI_TIER=kid`. The named covering files were run instead.
<!-- BODY:END -->

## Agent Notes
heal._main_heal: live-pid stalled record sets all_terminal=False and a live-stalled-only set returns in ONE pass with NOT_TERMINAL_YET=3; _sleep/_now seams added; 3-test cluster green (153 passed named files), dead-stalled SM.23 path unchanged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (tier parent a00-1ae4da07, SM.238). INSTRUCTION (the kid node claim): a live-stalled record is NOT terminal, the pass returns after ONE bounded pass, `_sleep`/`_now` seams, the live-stalled test rewritten, and the FULL suite green. MACHINE (diff header, not the result file): heal.py adds NOT_TERMINAL_YET=3 at L149, `_sleep`/`_now` at L152-161, the live-stalled branch at L224-231 setting all_terminal False, and the early return at L287-293 guarded by `saw_live_stalled and not saw_running`. Three parent-run negative probes all hold: PROBE A (gate) live-stalled-only returns rc 3 in 0.0011s with `_sleep` never reached; PROBE B (gate) mixed dead+live resolves the dead one to failed while the live one stays stalled and rc != 0; PROBE C (wire) a running record reaches the `_sleep` seam. Full engine suite green under AGI_TIER=parent: 4774 passed, 15 skipped, 1 xfailed in 731.23s. NEAR MISS: a branch that sets all_terminal False but then falls through to `_sleep` satisfies the docstring and still blows the 1800s ceiling -- the kid avoided it with the saw_live_stalled/saw_running guard. DEVIATION: conjunct 3 asked for +1 NEW dead-stalled test; none was added, the two pre-existing SM.23 tests (still green) carry that coverage, and conjunct 4 reporting was impossible at kid tier because AGI_TIER=kid refuses a bare-directory run -- the parent ran the full suite instead. GATE DEFECT: cli.py `_CLAIM_ITEM_RE` reads `time.sleep(30)` in the target claim as conjunct 30, so done demands a probe for a conjunct that does not exist.
<!-- THOUGHT:END -->

## Agent Notes
Tier parent accepted kid a00-73c0da26 (proved, 0.85): live-stalled semantics built (NOT_TERMINAL_YET=3, one bounded pass), _sleep/_now seams injected, test rewritten. 3 parent negative probes hold; full suite 4774 passed in 731s. Caveats: +1 new dead-stalled test not added (pre-existing SM.23 tests cover it); kid could not run the full suite (AGI_TIER=kid bare-dir gate) so the parent ran it; cli.py _CLAIM_ITEM_RE misreads time.sleep(30) as conjunct 30.
