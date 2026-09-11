---
id: hypothesis:l4-spawn-budget-status-waits-for-the-parent
mint_id: 40a4dd14f91d41e68ac0a24d9048fca9
type: hypothesis
parents:
  - goal:g15
  - hypothesis:harvest-table-subcommand
next_edges: []
edited_by: sanctuary-director
scaffold_hash: c0560e8f26f7eb21
season: 2
testable_claim: "OWNER 2026-09-11 14:0xZ via master-sensei (wake audit of sanctuary-director 135144Z, one dm 14:08Z): \"never hand-poll spawn_budget for a round (call 47: 55 iterations, 69 s) -- L4.113's dm is the wait\"; Sensei loose proposal (c), sized and minted by sanctuary-director 14:4xZ as a g15 build order. MEASURED: `spawn_budget.py status --iter L4.NNN` (`_round_status`, spawn_budget.py:679-740) prints the round's live rows and ONE verdict line (`round LNNN: parent alive, K live kid(s)` / `parent alive, reviewing` / the exit) and returns at once; a director waiting for a parent to exit therefore either loops `status` by hand (the audited 55-iteration shell loop) or watches the inbox file's mtime for the kid/parent dm -- neither is an engine surface, and the dm can be missed (a parent that dies silent sends none). CLAIM: `spawn_budget.py status --iter L4.NNN --wait [--timeout S]` (default timeout 1800) polls the SAME lease view at a <=5 s interval until no PARENT-tier lease for that round remains (the parent exited, whatever the kids did) -- or, when `--iter` matches no live lease at call time but the round's session dir exists, returns immediately as already-finished -- then prints the normal `status --iter` view and exits 0; on timeout it prints the last-seen view and `ERR: L4.NNN parent still live after Ss` to stderr and exits 2; an id with neither a lease nor a session dir exits 3 with `ERR: unknown round L4.NNN`. It never sleeps past an already-finished round (first read decides), never signals or reaps anything (the reaper's), and `--wait` without `--iter` is an argparse error. TESTS (test_spawn_budget.py, the L4.168/L4.232 fixture shape: real sleeping pids + real lease files under a tmp budget dir, `time.sleep` monkeypatched to raise where zero sleep is asserted): (a) a parent lease already gone at call -> exit 0 with no sleep; (b) a parent lease whose pid a background thread removes 0.3 s in -> `--wait --timeout 10` returns 0 after the removal with the final view printed; (c) a parent lease that never goes -> `--timeout 1` exits 2 with the ERR line; (d) unknown id -> exit 3; (e) `--wait` without `--iter` -> argparse error exit 2. FALSIFIER: a `--wait` that returns 0 while a parent-tier lease for the round is still present, or that sleeps on an already-finished round. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/spawn_budget.py (`_round_status` + argparse; additive) + extensions/agi/tests/test_spawn_budget.py. No other spawn_budget.py round is live (L4.232 landed in merge-up 37)."
title: spawn_budget.py status --iter L4.NNN --wait blocks until the round's parent lease is gone; the dm is no longer the only wait
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-spawn-budget-status-waits-for-the-parent

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
