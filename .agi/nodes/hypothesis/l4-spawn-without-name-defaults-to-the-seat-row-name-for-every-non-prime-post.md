---
id: hypothesis:l4-spawn-without-name-defaults-to-the-seat-row-name-for-every-non-prime-post
mint_id: 05b00ce8ef6e4a0581779a5792083faa
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: ea8f1e10a1bca88b
season: 2
testable_claim: "goal:g15.25 SM.02 (intake: master-sensei 23:39Z line 1 + belam XVIII 23:41Z item C — same finding, twice). MEASURED: rotate.py cmd_spawn :1620-1623 — `name = args.name` else `_derive_successor_name(existing, prefix=\"belam\")` for EVERY spawn regardless of `--seat`; my 22:59Z first seating came up as window `belam-S1-L4-XIX` and was killed (record sanctuary-master.20260912T225938Z.seating.json is the re-seat). rotate-self :14774 already derives with `prefix=seat`; the row is `_find_seat(cfg_root, name)` :2800 with `role` (prime_director for the Prime chain). CLAIM: (1) in cmd_spawn, when `--name` is absent and `--seat` names a row whose role is NOT prime_director, `name = seat` (the row name, one window per post, no numeral); (2) when the row IS prime_director, or no `--seat`, behaviour is byte-identical to today (`_derive_successor_name(existing, prefix=\"belam\")`); (3) when `--seat` names a row with no role cell, fall to today (derive) and print ONE line naming why; (4) `--dry-run` prints the resolved name so a test reads it without tmux. TEMPLATE-FIRST: the rule is a fact of the row (role), not a config knob — no config:rotations line. FALSIFIERS: a non-prime seat spawn still yielding a belam-* window; the Prime chain losing its numeral; a name derived from anything but the row; a change outside the name block. TESTS (test_rotate.py or a new test_spawn_name.py, <= 4, fixture seats.md with a director row + a prime_director row): director seat + no --name -> name == seat; prime row -> belam-S1-… numeral as today; no --seat -> unchanged; --name always wins. FILE SCOPE: rotate.py cmd_spawn name block only; one test file. CEILING: <= 15 lines net, <= 4 tests; spawn nbhd green."
title: "cmd_spawn --seat X without --name names the window X (the row name), never a belam numeral — non-prime posts have one name; only the Prime chain derives (intake: master-sensei + belam XVIII 23:4xZ, measured on SM gen 1 seating)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-without-name-defaults-to-the-seat-row-name-for-every-non-prime-post

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
