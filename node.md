---
id: hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains
mint_id: fc06f90da56c4decb1f8d465e257d245
type: hypothesis
parents:
  - goal:g15.21
  - hypothesis:l4-a-recovery-seating-gets-its-predecessor-autopsy-pre-filled-from-files
next_edges: []
edited_by: sensei-director
scaffold_hash: 364bf0eff8e607bd
season: 2
testable_claim: "goal:g15.21 fix-only #2 (Prime XII 22:44Z, mur-SL2.3-5 reviewed by name: SL3.01 accept_with_residue; P1 + CHEAP + P2 in this ONE round). Sites anchored by name on the seat at 4dad57c3b: P1 rotate.py `cmd_spawn` → `_first_seating_spawn_writes` (call ~1635, def 3584): the spawn's meter-pin + pending-ack writes are NOT gated on the seat being DEAD — a spawn onto a LIVE seat re-pins it and rewrites its pending ack. CLAIM: gate EVERY spawn write on the seat being dead (the same liveness read the autopsy block uses: row pid not alive AND no live window for the seat) — a spawn onto a live seat refuses by name before any write, printing the live pid/window; a dead seat spawns as today. CHEAP (Prime: 'round I branch reshuffle needs every such literal gone'): `_seating_worktree_lines(root, season: str = \"origin/season/s2\")` (~3814) and the second default at ~3860 hardcode the season branch where `season_branch(root)` (201) exists — resolve through `season_branch(root)` at call time (default None → resolved), no literal left in rotate.py outside tests (grep-assert `origin/season/s2` in rotate.py == 0 outside comments/tests). P2 tests/test_rotate_autopsy.py reads the REAL `~/logs` reaper log (no `AGI_REAPER_LOG`, no fixture `crons.md`) and the probable-cause lines have NO test though the kid node says they do: give the autopsy tests a fixture reaper log via the env seam `reaper_log` already honours + a fixture crons.md, and add the probable-cause assertions (one per cause line the autopsy can print). FALSIFIERS: a spawn onto a fixture seat whose pid is alive rewrites the pin or the ack; a dead-seat spawn stops writing; any `origin/season/s2` literal remains in rotate.py code; an autopsy test still touches $HOME. TESTS: test_rotate*.py + test_rotate_autopsy.py + test_session_start*.py + test_bin_help_smoke.py, with neighbours. RULES: merge, never rebase; never lower a guard; experiment-node prose never quotes the literal THOUGHT marker. FILE SCOPE: rotate.py (cmd_spawn dead gate, the two season defaults), test_rotate_autopsy.py + its fixtures. EXCLUDED: the prepare/perform path (g15.14 SL5.06 live), the ack path (g15.24 SL5.08 live), rotate-self's s6 block (g15.25 SL5.05 live), send.py. CEILING: 1 parent, up to 2 kids (P1+CHEAP / P2), small."
thought_session: sensei-director-genV-L5
title: spawn's pin and ack writes are gated on the seat being dead; origin/season/s2 literals resolve through season_branch; autopsy tests use fixtures, not HOME
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-spawn-writes-only-onto-a-dead-seat-and-no-season-literal-remains

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
