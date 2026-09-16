---
id: hypothesis:l4-the-launch-wrapper-order-tests-anchor-on-the-binary-token-not-a-substring-of-the-checkout-path
mint_id: fdaeaccb4f264181a8453555c7d65c75
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 58ee6d3e0bc2839e
season: 2
testable_claim: "Measured 2026-09-16 by master-sensei gen 8 (15:1xZ, gate 130c140b9 / MAIN 251614b74) and by sanctuary-master gen 3 (11:5xZ, unattributed at the time): test_rotate.py::test_spawn_window_agi_seat_export_and_byte_identical_absent and test_rotate_launch_wrapper.py::test_shell_cmd_seat_wraps_no_seat_byte_identical assert `seated.index('launch-wrapper') < seated.index('claude')` -- the bare token `claude` matches the CHECKOUT PATH when it contains that string (a throwaway worktree under /tmp/claude-1001/... or any clone under a claude-named dir) before it matches the binary, so both fail on such a tree and pass in MAIN by accident of location. CLAIM: both assertions anchor on the binary token as the shell command spells it (the argv element that is the claude binary / `-- claude` boundary the wrapper emits), never a substring of the whole command line, so the tests pass byte-identically on a checkout at any path. FALSIFIERS: either test still red on a throwaway worktree under a path containing `claude`; any change to the launch-wrapper bytes under test. TESTS: the two existing tests, run on a throwaway tree under /tmp/claude-<x>/ AND in MAIN -- green in both. FILE SCOPE: the two test files only, no production line. CEILING: <=4 lines, 1 kid -- or the Prime writes it in directly under this node (owner ruling 09-16 06:3xZ: a small fix cheaper than a parent round), whichever is cheaper on the day."
title: L4 the launch wrapper order tests anchor on the binary token not a substring of the checkout path
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-launch-wrapper-order-tests-anchor-on-the-binary-token-not-a-substring-of-the-checkout-path

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
DIRECTOR ADDENDUM (sanctuary-master gen 3, 15:4xZ): a SECOND stale test assertion of the same class, RED ON MAIN since the 477e87546 merge-up: test_rotate_verb_resolvers.py::test_unkeyed_post_refuses_keygen asserts `"keygen fresh" in why` (the old positional spelling argparse rejects) while SM.39 landed rotate.KEYGEN_LINE = `python3 extensions/agi/bin/send.py keygen --post {seat}` (send.py:4978 declares --seat/--post; the positional tail was a usage error). The production line is right; the assertion must match rotate.KEYGEN_LINE.format(seat="fresh") (one test line). Same kid, same ceiling (+1 line), or the Prime writes both in directly.
