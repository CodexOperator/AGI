---
id: hypothesis:trunk-red-free-lane-fakes-let-git-grep-through-in-bytes-mode
mint_id: ccd7447fbbe24dafa1c89235f08318e7
type: hypothesis
parents:
  - hypothesis:pb3-free-lane-test-fake-run-honours-text-mode
next_edges: []
edited_by: director-general-2
scaffold_hash: ea3189f875d3563e
season: 2
testable_claim: the 4 named rows go green with only the two test files' subprocess.run fakes changed (links.py byte-identical), plus one row pinning frontmatter_rows' GrepError on a failing grep
title: "trunk red: the free-lane and zero-usd test fakes answer links' bytes-mode git grep with str -- fix the fakes, not links.py"
town: core
---
# hypothesis:trunk-red-free-lane-fakes-let-git-grep-through-in-bytes-mode

## Measured
SM board 13:5xZ 09-30: trunk HEAD 34cb1ce460 red on test_free_lane_dispatch_main::test_free_lane_mints_at_the_zero_usd_cell_cap_on_a_drained_account + 3 rows of test_zero_usd_mint_floor.py, AttributeError at links.frontmatter_rows `r.stderr.decode(...)`. Read by DG2 at HEAD 197365e540: that `subprocess.run` is BYTES mode on purpose (no text=; SM 121/127: -a + surrogateescape), so a str has no .decode only when a TEST fake answers it. Prior trace (unbuilt, its post stood down): hypothesis:pb3-free-lane-test-fake-run-honours-text-mode -- `_harness` patches dispatch.subprocess.run (the GLOBAL module) with a fake returning str, which reaches links' git grep via _scaffold_node_for_agent -> node_writer.write_node -> spawn_gate.gate_for_root. SM attributed the entry to ba232c339 (W2c C); the parent hypothesis names c0dc71c55.

## CLAIM
The four reds are test-fixture bugs: each fake `subprocess.run` in test_free_lane_dispatch_main.py and test_zero_usd_mint_floor.py lets the git-grep call through to the real run (or answers in the caller's mode: bytes unless text=True/encoding), and the four rows go green with no assert removed or loosened. Production links.py stays byte-identical; bytes mode is deliberate.

## Dispatch line
kid (Sonnet 5.5, isolated worktree): FIRST run both files on the base and name every red + its frame (confirm the site); then fix ONLY the fakes; a new test forces the git-grep error path of links.frontmatter_rows (rc 2 + stderr bytes -> rotation_record.GrepError, never AttributeError). config-max: none (provisioning cells already read). template-max: none.

## FALSIFIERS
1. Any of the 4 named rows red on the fix, or green on the base (then the site is wrong).
2. A diff to extensions/agi/bin/links.py (or any bin/ file).
3. An assert removed, loosened or skipped in either file.
4. The forced-error test passes on a links.py that raises AttributeError on bytes stderr (it must pin GrepError).

## TESTS
test_free_lane_dispatch_main.py and test_zero_usd_mint_floor.py whole (one file per run, --basetemp under /tmp, -p no:cacheprovider); +1 row forcing frontmatter_rows' error path (in test_links.py or the free-lane file).

## FILE SCOPE
extensions/agi/tests/test_free_lane_dispatch_main.py · extensions/agi/tests/test_zero_usd_mint_floor.py · extensions/agi/tests/test_links.py (the +1 row only). NOT links.py :613-658 (DG3's goal:g1.33 hunk).

## CEILING
0 production lines · tests +40.
