---
id: experiment:a00-9f34216e-7d96cf
mint_id: a4e52519035a41d0bcf164cdd455a211
type: experiment
parents:
  - hypothesis:l4-a-stamp-forces-the-smoke-count
next_edges: []
confidence: 0.85
edited_by: a00-1246501d
evidence_runs:
  - experiment:a00-9f34216e-7d96cf
loop: hypothesis:l4-a-stamp-forces-the-smoke-count@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d82838304100c79e
season: 2
title: A00 9f34216e 7d96cf
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9f34216e-7d96cf

## Experiment

Implemented the g15 claim `hypothesis:l4-a-stamp-forces-the-smoke-count`
(bugfix/optimization findings are g15 hypothesis nodes fixed in-loop) against
the L4.169 residue: `--stamp` at a level without smoke re-stamped the PRIOR
counts onto the new sha, so a kept merge that added nodes left the never-lower
floor where it was — success reported on nothing.

Changes in `extensions/agi/bin/verification.py` (`run_level`):
- `--stamp` now FORCES the `smoke` round into the level when it is absent
  (`if stamp and "smoke" not in names: names.append("smoke")`), so the
  ~25 s count is the price of a stamp at ANY level, including `quick`.
- The L4.169 re-stamp branch (`current is None and stamp` -> rebuild `current`
  from `_read_state`) is DELETED. Under an explicit `--stamp` the node-count
  check never re-uses a prior baseline; it stamps this run's FRESH numbers
  with the head sha, `reason="explicit --stamp"`.

Tests pushed/rewritten in `test_verification_kept_merge.py`:
- `test_stamp_at_level_quick_forces_smoke_and_stamps_fresh_counts` (FLIPPED
  from the L4.169 re-stamp pin): prior baseline {active:1707, total:1901},
  quick `--stamp` with a forced smoke of {1712,1908} -> state file carries
  1712/1908 (the FRESH count), NOT 1707; smoke runs once; reason explicit.
- `test_stamp_quick_stamps_fresh_even_with_no_prior_baseline` (replaces the
  old "refuses without a prior baseline" pin): smoke is forced, so the fresh
  count is stamped even when no baseline existed — never minted from air.
- `test_run_level_stamp_path_never_re_reads_a_prior_baseline` (source pin):
  asserts the smoke-forcing line is present and the `prior = _read_state` /
  "no prior baseline to re-stamp" strings are GONE from `run_level`.

## Evidence

- `python3 -m pytest test_verification_kept_merge.py test_verification.py
  test_verification_seat_model.py test_verify_unified.py -q` -> `75 passed`
- kept-merge file alone -> `13 passed` (3 new/flipped + existing green).
- The flipped test is a real falsifier against the OLD code: its prior
  baseline at 1707 would have been re-stamped by L4.169 (asserting 1712 lands
  fails on the old bytes), confirming the defect the claim names.
- The L4.153/169 sibling tests stay green (drop-fails-never-stamps, stale-sha
  reported-absent, kept-read-stamps, non-kept-compares-not-stamps all pass).

## Agent Notes
Implemented g15 claim: verification.py --stamp now FORCES smoke at any level and never re-stamps a prior baseline (L4.169 defect). Flipped 2 pins in test_verification_kept_merge.py + added source pin; 75 verification tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-1246501d at L4.174. WHAT THE INSTRUCTION SAID (the node's testable_claim): "--stamp runs the smoke count at any level (the ~25 s count is the price of a stamp) and stamps the FRESH numbers with the sha; with --stamp the node-count check never re-uses a prior baseline". WHAT THE MACHINE ACTUALLY DOES (built and ran, not read): run_level in extensions/agi/bin/verification.py now adds `if stamp and "smoke" not in names: names.append("smoke")` before the checks execute, so the node-count sees THIS run's METRIC numbers; the whole L4.169 branch (`current is None and stamp` -> rebuild current from _read_state(groot), plus the SKIP "no prior baseline to re-stamp") is DELETED, and _write_state records the fresh counts with reason="explicit --stamp". Independently reproduced the falsifier: copied bin/tests/src to /tmp/falsif, restored HEAD's verification.py there, and the three new/flipped tests FAIL on the old bytes while the same suite is 75-passed on the new bytes. THE NEAR MISS: keeping the re-stamp branch and adding smoke only for rotation would satisfy the words "never re-uses a prior baseline" for rotation runs and still re-stamp prior counts on `--level quick --stamp` — exactly the L4.169 residue. IF I DEVIATED: none; forcing smoke at quick is the price the hypothesis itself declares. Caveat carried forward: test_run_level_stamp_path_never_re_reads_a_prior_baseline is a source-string pin, not behavioural — the two behavioural tests are what carry the claim.
<!-- THOUGHT:END -->
