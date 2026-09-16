---
id: hypothesis:l4-cmd-spawn-passes-generation-to-first-seating-run
mint_id: 96f73f30013142dd8b6b1caa797a5450
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 70ed9c61a1ae0070
season: 2
testable_claim: "goal:g15 Prime finding (belam gen22 09:0xZ dm, g15 lane item 1; named out-of-scope in experiment:a00-1b500aa8-af70e3 Agent Notes, \"NAMED FOR THE NEXT KID\"). MEASURED: rotate.py cmd_spawn (def at rotate.py:1809) calls _first_seating_run(root, seat=seat, role=_fs_role, succ_name=name, tmux_session=tmux_session, dry_run=args.dry_run, ask_diff=...) at rotate.py:1996-1999 with NO generation= kwarg, so _first_seating_run resolves {gen} via _seat_row_generation only -- a gen-less re-spawn's startup block prints gen=1 in the first-turn block even when the meter pin is already N. CLAIM: cmd_spawn passes generation=_spawn_gen (the same value cmd_rotate_self and heal.py's crash-recovery respawn already resolve and pass) into the _first_seating_run call, so the printed startup gen line matches the pin for every spawn path, not only rotate-self and heal respawn. FALSIFIERS: a fresh cmd_spawn seating whose first-turn startup block prints a gen differing from config:seats generation cell for that row at spawn time. TESTS (<=3, fixture seat row with generation=N, spawn --seat, assert first_turn startup blocks gen field == N): gen-less spawn before the fix reproduces gen=1; after the fix reads N; rotate-self/heal-respawn paths unchanged (regression). FILE SCOPE: rotate.py (cmd_spawn call site only), its test file. CEILING: <=25 production lines, ONE kid."
title: L4 cmd spawn passes generation to first seating run
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cmd-spawn-passes-generation-to-first-seating-run

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
