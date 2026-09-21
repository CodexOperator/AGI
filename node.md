---
id: hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap
mint_id: 56bc8c7d4efd4c4e99a541d5f1752e15
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-rotate-self-keeps-the-numeral-window-reaps-fifo-and-records-before-it-terms
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 629f0cce8dd8d7bd
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-11: rotate.py:4456 `--dry-run` prints generic text for the Belam cap; the owner's rule is that a dry-run says exactly what the live run would touch. CLAIM: on a numeral-chain seat whose chain would exceed five, `--dry-run` prints the OLDEST predecessor's window name, its @id, the pane pid and the derived pid chain it would TERM (deepest-first order), and `touches nothing` — derived live through the same `_pane_pid(@id)` → ps -e climb the real path uses (read-only); on a plain seat it prints the own-window/@id/chain it would reap; when the chain cannot be derived it prints the NAMED skip. Also fix the stale text the review noted: step (2) still says 'reaped by @id at step 8' while (8) gates it off on a numeral seat. TESTS: F3 (`test_chain_seat_dry_run_prints_fifo_plan_touches_nothing`) extended to assert the window name, @id and pids appear; a plain-seat dry-run asserts its own chain line; both assert no record and no window change. FALSIFIER: a dry-run whose text omits the @id or the pids of what the live run would reap. VERIFY ON THE REAL TREE: `rotate.py rotate-self --dry-run --name sanctuary-director --model claude-opus-5 --prompt-file .agi/sessions/quorum/sanctuary-director.md` from the seat worktree — paste the (2)/(8) lines. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (dry-run text + the read-only derivation call) + test_rotate_selfreap.py/test_rotate_handover.py. SERIAL on rotate.py behind hypothesis:l4-the-belam-cap-record-is-planned-first (p4 = g15-10). EXCLUDED: everything else."
title: rotate-self --dry-run names the oldest window, its @id and the pids it WOULD reap
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-11: rotate.py:4456 `--dry-run` prints generic text for the Belam cap; the owner's rule is that a dry-run says exactly what the live run would touch. CLAIM: on a numeral-chain seat whose chain would exceed five, `--dry-run` prints the OLDEST predecessor's window name, its @id, the pane pid and the derived pid chain it would TERM (deepest-first order), and `touches nothing` — derived live through the same `_pane_pid(@id)` → ps -e climb the real path uses (read-only); on a plain seat it prints the own-window/@id/chain it would reap; when the chain cannot be derived it prints the NAMED skip. Also fix the stale text the review noted: step (2) still says 'reaped by @id at step 8' while (8) gates it off on a numeral seat. TESTS: F3 (`test_chain_seat_dry_run_prints_fifo_plan_touches_nothing`) extended to assert the window name, @id and pids appear; a plain-seat dry-run asserts its own chain line; both assert no record and no window change. FALSIFIER: a dry-run whose text omits the @id or the pids of what the live run would reap. VERIFY ON THE REAL TREE: `rotate.py rotate-self --dry-run --name sanctuary-director --model claude-opus-5 --prompt-file .agi/sessions/quorum/sanctuary-director.md` from the seat worktree — paste the (2)/(8) lines. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (dry-run text + the read-only derivation call) + test_rotate_selfreap.py/test_rotate_handover.py. SERIAL on rotate.py behind hypothesis:l4-the-belam-cap-record-is-planned-first (p4 = g15-10). EXCLUDED: everything else.
