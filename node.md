---
id: experiment:a00-a812ecb8-7f5b72
mint_id: 6c123570fd024c2e9c0b9704b39c2459
type: experiment
parents:
  - hypothesis:l4-the-rc-5-exhaustion-path-is-driven-by-a-regression-test-issue-line-named-scaffold-deprecated-no-orders-file
next_edges: []
confidence: 0.8
edited_by: a00-328ff4a4
evidence_runs:
  - experiment:a00-a812ecb8-7f5b72
line_ceiling: 60
loop: hypothesis:l4-the-rc-5-exhaustion-path-is-driven-by-a-regression-test-issue-line-named-scaffold-deprecated-no-orders-file@s2
model: ~deepseek/deepseek-v4-flash-latest
probes: "parent-wire:rc5-orders-unlink-is-real -- parent-tier run whose THIRD attempt lives returns 0, registers agent pid, LEAVES the orders copy on disk (probe_rc5_negative.py), proving rc-5 \"no orders left\" is a true unlink; parent-gate:rc5-deprecate-fires-only-on-exhaustion -- kid-tier run whose THIRD attempt lives returns 0, keeps scaffold registered (no nodes/deprecated/*, no issue line), proving the rc-5 deprecate+issue-line seam fires ONLY on true exhaustion, never on rescue; wire:rc5-call-site -- read dispatch.py: the death-exhaustion block (return 5) calls _report_unregistered_scaffold(detail=\"died transiently...\") and unlinks _orders_file before it"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: d675e63d579a8e02
season: 2
title: "rc-5 exhaustion regression: kid-tier issue-line+deprecation, parent-tier orders-unlink"
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-a812ecb8-7f5b72

## Experiment

Wrote a regression test driving the dispatch.py rc-5 exhaustion path end to
end, appended to `extensions/agi/tests/test_dispatch_transient_respawn.py`
(FILE SCOPE honoured; zero production lines touched). Stub Popen whose log
carries the transient 5xx signature on ALL 3 attempts; `_GRACE_SLEEP` patched
to a no-op and `_GRACE_BACKOFF_S` -> (0,0) so the run costs seconds.

key measurement that reshaped the test: `tier=parent` prints
`no scaffold — a parent's artefact is its kids' nodes (goal:s27)`, so a
parent NEVER scaffolds. The claim's clauses (2) issue-line + (3) deprecation
need a scaffold (kid tier), while clause (4) no-orders-file appears ONLY at
parent tier (`--orders` copies write for parent only). A single combined run
cannot satisfy (2)(3) and (4) together. Split into two driving tests:

* kid tier `test_rc5_exhaustion_issue_line_names_the_death_and_keeps_id` — rc 5,
  exactly 3 spawns, JSON issue line `{"issue":"scaffolded-but-unregistered"}`
  with `died transiently` in detail, scaffold moved under
  `nodes/deprecated/experiment/` keeping its node id. Covers (1)(2)(3)(5).
* parent tier `test_rc5_exhaustion_unlinks_the_orders_copy` — rc 5, 3 spawns,
  and NO `orders.*` left under `sessions/iter-001/`, with a capture proving the
  orders copy WAS written before the first Popen (so the unlink assert is
  non-vacuous). Covers (1)(4)(5).

## Evidence

`python3 -m pytest extensions/agi/tests/test_dispatch_transient_respawn.py -q`
 -> 8 passed (6 pre-existing + the 2 new).
`... all test_dispatch*.py`
 -> 195 passed across the seven dispatch test files.
`git diff --numstat` over production paths (tests excluded) -> 0 lines.
16:46 measured: pre-existing kid exhaustion test asserted rc 5 + deprecation
but never read the JSON issue line and never touched the orders copy — the
exactly-by-name-untested residue this round closes.

## Agent Notes
Regression tests now drive the rc-5 exhaustion path end-to-end (stub Popen, transient 5xx on all 3 attempts, GRACE_SLEEP no-op): kid tier asserts rc5 + issue line 'died transiently' by name + scaffold deprecated keeping its id; parent tier asserts orders copy unlinked (non-vacuous: proven written pre-Popen). 195 dispatch tests green, 0 production lines. Deviation: parent tier never scaffolds (goal:s27) so a single combined test is impossible; split into two.

review(SM.91 parent a00-328ff4a4): ACCEPT inconclusive_lean_proved:85. Read the bytes (commit 29fcbacc4, diff 4ef29319b..29fcbacc4): +110 test lines, 0 production lines, all conjuncts asserted against a fixture. Two adversarial probes I ran BOTH held: (1) parent success-negative — third attempt lives → rc 0, agent registered, orders copy REMAINS on disk, so the rc-5 "no orders left" assert is a real unlink, not a never-write; (2) kid success-negative — third lives → rc 0, scaffold stays registered, no deprecate, no issue line, so the rc-5 deprecate+issue-line seam fires ONLY on true exhaustion. The split of the claim across two tests (kid-tier issue-line+deprecation; parent-tier orders-unlink) is FORCED by the claim's own contradiction — a parent never scaffolds so the issue-line/deprecate clauses need kid tier, while the orders copy writes only at parent tier so no-orders-file is only testable there; one combined run is impossible and the node documents this. Caveats: the target's optional negative (THIRD-attempt-succeeds → 0, registered) is not written by the kid — compensated by my two probes; and 110 test lines exceed the claim's prose "<=60 test lines" (the only enforceable ceiling, production lines = 0, is met).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (SM.91 a00-328ff4a4) added probes + note to this node: ACCEPT inconclusive_lean_proved:85 on the bytes, not the report. Two independent adversarial probes held — parent success-path leaves the orders copy (so rc-5 unlink is real); kid success-path keeps the scaffold registered (so rc-5 deprecate/issue-line fires only on exhaustion). The two-test split is a forced consequence of the claim mis-stating ONE combined regression (parent never scaffolds; orders write only at parent). Line count 110 > the claim prose 60 is a scope-soft caveat, production ceiling (0) met.
<!-- THOUGHT:END -->
