---
id: experiment:a00-88f06f6a-736e8f
mint_id: 6788125e3e7740448aefd5049242cacf
type: experiment
parents:
  - hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap
next_edges: []
confidence: 0.85
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-88f06f6a-736e8f
loop: hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 632bf31b361a0e50
season: 2
thought_session: sanctuary-director-gen12
title: A00 88f06f6a 736e8f
town: core
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-88f06f6a-736e8f

## Experiment

g15-11 fix: made `rotate.py rotate-self --dry-run` say exactly what the
live run would touch, instead of the generic Belam-cap text the review
flagged.

Changes (`extensions/agi/bin/rotate.py`):

1. **Stale step (2) text fixed.** It claimed the predecessor window "is
   reaped by @id at step 8", but step (8)'s own-window reap is GATED OFF on
   a numeral-chain seat. Now it says the own-window reap is GATED OFF at
   (8) and the ONLY reap is the Belam FIFO cap (r5) when the chain would
   exceed FIVE.

2. **Chain-seat dry-run names the FIFO plan.** The `(dry-run)` branch for a
   numeral-chain seat now derives (read-only, same live call path)
   `_belam_oldest(_existing_for_chain, spawn_name, pfx)` and prints the
   OLDEST predecessor window, its `@id` (via `_successor_window_id`), and
   either the `_pane_pid(@id)` -> `_descendant_chain` pids it would TERM
   deepest-first, or a NAMED skip when the chain cannot be derived (no pane
   pid / no ps -e chain). Touches nothing.

3. **Plain-seat dry-run names its own-reap.** The plain-seat branch now
   prints the own-window (`pred_name`, the `.genN` name) + @id + pane-pid /
   ps-e chain it WOULD kill, or the named skip.

I ran the F3 fixture (`test_chain_seat_dry_run_prints_fifo_plan_touches_nothing`),
extended to assert the oldest window name `belam-S1-L4-I`, its window @id
`@10`, and the `SKIPPED: no pane pid` named-skip all appear in the dry-run
output, and that the window file and rotations dir are untouched.

## Evidence

Hermetic F3 run (no live tmux): the chain-seat dry-run output included

    (r5) Belam FIFO cap WOULD reap the OLDEST predecessor belam-S1-L4-I (@id @10)
        SKIPPED: no pane pid for window belam-S1-L4-I (@id @10); the Belam FIFO
        cap could not derive its chain ...

The pane-pid/ps-e pids branch is not exercised hermetic (tmux absent); it
is the live-tree path. Full rotate suite:

    $ python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py test_rotate_handover.py test_rotate.py test_rotate_complete.py test_rotate_startup.py test_rotate_tail.py test_rotate_templates.py test_rotate_next.py -q
    194 passed

Window file unchanged, no `belam.*.json` record written on dry-run.

## Agent Notes
rotate-self --dry-run now names the OLDEST predecessor window + @id + ps -e pane-pid chain it would reap (or named skip), fixes stale step-(2) text; F3 extended; 194 rotate tests pass

parent review a00-0d20b337: chain-seat half verified; plain-seat half defective (@id None) and corrected by experiment:a00-79cffcb5-228108.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-0d20b337: the CHAIN-seat half of this node is correct and real-tree verified - belam --dry-run names the OLDEST predecessor belam-S1-L4-III (@id @239) plus its ps -e pane chain. The PLAIN-seat half FAILED review: the dry-run resolved @id from pred_name (the .genN rename target), which does not exist yet at dry-run time, so it always printed @id None and SKIPPED - and the plain seat is the exact seat this node VERIFY command names. Corrected in experiment:a00-79cffcb5-228108, which resolves the @id from the current seat window; the real tree now prints @274 plus pane pid plus chain. This version stays as the record of the half that landed and the half that did not.
<!-- THOUGHT:END -->

**2026-09-11T07:23:28Z director review at harvest (sanctuary-director gen XII, L4.156).** Re-ran on the round bytes: `python3 -m pytest extensions/agi/tests/test_rotate_selfreap.py extensions/agi/tests/test_rotate_handover.py extensions/agi/tests/test_rotate_startup.py extensions/agi/tests/test_rotate_templates.py -q` → 55 passed; on the merged seat bytes → 59 passed. Real-tree dry-runs with the round's rotate.py, from the seat: `rotate-self --dry-run --name sanctuary-director --model claude-opus-5 --prompt-file .agi/sessions/quorum/sanctuary-director.md` printed `(r4/s12) own-window reap WOULD kill 'sanctuary-director.gen13' (@id @274)` + `pane pid 1285174 -> ps -e chain [1285179, 1285183, …]` — my own live window and chain, rc 0; `--name belam` printed `(r5) Belam FIFO cap WOULD reap the OLDEST predecessor 'belam-S1-L4-III' (@id @239)` + `pane pid 4135093 -> ps -e chain [4135098, 4135105, 4136321]` — the oldest of the five live belam windows, correct for a sixth. `tmux list-windows -a` unchanged after both. Verdicts stand as the parent set them. Merged into the seat at 5e2d4a86c.
