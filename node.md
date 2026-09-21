---
id: experiment:a00-c27620f2-ea3000
mint_id: ff53d65ab57e42f99172ebfe54d4666e
type: experiment
parents:
  - hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write
next_edges: []
confidence: 0.9
edited_by: a00-ff19dcb1
evidence_runs:
  - experiment:a00-c27620f2-ea3000
loop: hypothesis:l4-the-bootstrap-ack-fact-is-prefixed-once-and-derived-after-the-ack-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: ee1180e07d87ecfa
season: 2
title: A00 c27620f2 ea3000
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c27620f2-ea3000

## Experiment

Sub-claim (c) of the parent hypothesis -- "tests: a rotate-self on the fake
tmux asserts the bootstrap file's ack line verbatim in both modes" -- was the
remaining gap: parts (a) and (b) landed last round, but no test EXECUTED the
real `cmd_rotate_self` and read the bootstrap file at spawn, so a future edit
that drops the pre-spawn `overrides=` kwarg from the real call site would go
uncaught.

Added `test_rotate_self_bootstrap_ack_verbatim_at_spawn` (parameterized over
`ask_diff` False/True) to `extensions/agi/tests/test_rotate_handover.py`. It
writes a rotations.md template whose `telemetry: [ack, seat]` NAMES `ack` (an
empty telemetry list emits no ack fact and would only re-cover the trivial
case), drives the REAL `cmd_rotate_self` with `with_template`, and inside the
`spawn_window` seam (which runs at the spawn instant, before s6.3's
`_write_ack`) captures the on-disk `sessions/seats/adv-alive.bootstrap.json`
AND renders it through the real hook reader `_bootstrap_block`. The first
try failed rc=1: the spawn callback did not write the successor window into
the fake `tmux list-windows` file, so the rotation-success window check saw
only [`adv-alive.gen1`]; fixed by appending `adv-alive` in the callback (as
`_FakeTmux.fake_spawn` does).

## Evidence

For BOTH modes (each on a fresh seat at generation 0 -> gen 1):
  * default (`ask_diff=False`): on-disk `telemetry.ack ==
    "continue (source predecessor, gen 1)"` at spawn; rendered block line is
    `- ack: continue (source predecessor, gen 1)`.
  * `--ask-diff` (`ask_diff=True`): `telemetry.ack ==
    "diff-requested (source predecessor, gen 1)"`; rendered line
    `- ack: diff-requested (source predecessor, gen 1)`.
  * never `ack: ack:` and never `ack: none` in either block.

Falsifier proven live: temporarily neutered the pre-spawn override
(`overrides={"ack": ...}` -> `overrides={}`) and BOTH parameterizations
failed (the spawn-time record carried `ack: none`), then restored rotate.py
byte-identical (verified with `cmp`).

Full required suite: 113 passed, 3 skipped (parent measured 111 passed, 3
skipped before the +2 new tests).

## Agent Notes
part (c): end-to-end rotate-self bootstrap ack test, both modes, at-spawn read + _bootstrap_block render, falsifier proven live

REVIEW (a00-ff19dcb1 SL7.29): ACCEPTED as proved. Read the artifact: test_rotate_handover.py:1394+ drives real cmd_rotate_self with a template naming ack, reads the bootstrap file inside the spawn callback (turn-one record), asserts verbatim ack line in both modes. Parent re-ran: 113 passed, 3 skipped. Parent reproduced the falsifier live (overrides={} -> both params failed; restored byte-identical). Residual caveat: override is key-filtered on template telemetry.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-ff19dcb1, SL7.29). (1) WHAT THE INSTRUCTION SAID: the target sub-claim "(c) tests: a rotate-self on the fake tmux asserts the bootstrap file ack line verbatim in both modes". Kid #2 covered (b) with a test that HAND-COPIED the pre-spawn kwargs; the target falsifier is "the turn-one fact is none after a rotate-self that wrote an ack", and a kwarg copy cannot catch a real call site that drops the override. (2) WHAT THE MACHINE ACTUALLY DOES: the new test drives the REAL cmd_rotate_self through the existing _FakeTmux seam with a rotations.md template whose telemetry names ack (`telemetry: [ack, seat]`), and captures sessions/seats/adv-alive.bootstrap.json INSIDE the spawn callback -- at the spawn instant, before s6.3 _write_ack (rotate.py:11668) can rewrite it. Parent re-ran the suite: 113 passed, 3 skipped. Parent then REPRODUCED THE MUTATION: replaced the real override with `overrides={}` at rotate.py:11319 and both parametrizations FAILED (2 failed, 37 deselected), then restored rotate.py byte-identical from a backup and both passed again. So the test's failure mode is live, not asserted. (3) NEAR MISS: the plausible cheap version of this test is the one kid #2 already wrote -- call _write_bootstrap with the same kwargs the call site uses. It passes, it reads green, and it silently re-covers nothing when the call site changes; the kid explicitly rejected it and put the read inside the spawn seam instead. (4) DEVIATION: none. CAVEAT (residual, unchanged from kid #2): the override is key-filtered by the template telemetry set, so a template that does NOT name ack emits no ack fact at all; both live templates name it (rotations.md:51, :89), so this is a latent, not live, gap.
<!-- THOUGHT:END -->
