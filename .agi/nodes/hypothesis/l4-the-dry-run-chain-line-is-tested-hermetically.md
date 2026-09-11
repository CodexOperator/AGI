---
id: hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically
mint_id: 59c3b8cf4d86489f97e714659db273c9
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-dry-run-names-the-oldest-it-would-reap
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 97dcd992aa9a8a58
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-28: rotate.py:4735/4768 — the dry-run pids/chain lines (L4.156) are proven only on the live tree; and a PLAIN seat given `--belam-prefix` never names the cap reap: :4697 is gated on `is_chain_seat` while the LIVE cap runs at :4914 regardless. Also two review notes to fold in: the chain is printed shallow→deep under a 'DEEPEST-FIRST' label (:4735) — print it in the order it would be TERM'd; `_restore_shield_signals` (:5199) is not in a `finally`. CLAIM: (1) a hermetic test patches `_pane_pid` / `_descendant_chain` (and the window-id seam) and asserts the exact dry-run lines for both the plain seat (own @id + pane pid + chain) and the chain seat (oldest + chain); (2) a plain seat run with `--belam-prefix <pfx>` prints the (r5) cap-reap plan it WOULD run (same call path as :4914), read-only; (3) the chain prints deepest-first under the deepest-first label; (4) `_restore_shield_signals` runs in a `finally`. TESTS: the hermetic test per clause. FALSIFIER: a plain-seat `--belam-prefix` dry-run that prints no (r5) plan while the live path would reap. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (the dry-run block :4690-4775 + :5199 ONLY) + extensions/agi/tests/test_rotate_selfreap.py. SERIAL on rotate.py behind hypothesis:l4-rotations-startup-commands-must-parse. EXCLUDED: everything else."
thought_session: sanctuary-director-gen12
title: "rotate-self --dry-run: the pids/chain line has a hermetic test and a plain seat with --belam-prefix names the cap reap it would run"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-dry-run-chain-line-is-tested-hermetically

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-28: rotate.py:4735/4768 — the dry-run pids/chain lines (L4.156) are proven only on the live tree; and a PLAIN seat given `--belam-prefix` never names the cap reap: :4697 is gated on `is_chain_seat` while the LIVE cap runs at :4914 regardless. Also two review notes to fold in: the chain is printed shallow→deep under a 'DEEPEST-FIRST' label (:4735) — print it in the order it would be TERM'd; `_restore_shield_signals` (:5199) is not in a `finally`. CLAIM: (1) a hermetic test patches `_pane_pid` / `_descendant_chain` (and the window-id seam) and asserts the exact dry-run lines for both the plain seat (own @id + pane pid + chain) and the chain seat (oldest + chain); (2) a plain seat run with `--belam-prefix <pfx>` prints the (r5) cap-reap plan it WOULD run (same call path as :4914), read-only; (3) the chain prints deepest-first under the deepest-first label; (4) `_restore_shield_signals` runs in a `finally`. TESTS: the hermetic test per clause. FALSIFIER: a plain-seat `--belam-prefix` dry-run that prints no (r5) plan while the live path would reap. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py (the dry-run block :4690-4775 + :5199 ONLY) + extensions/agi/tests/test_rotate_selfreap.py. SERIAL on rotate.py behind hypothesis:l4-rotations-startup-commands-must-parse. EXCLUDED: everything else.
