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
testable_claim: "AMENDED BUILD ORDER (sanctuary-director 163547Z session, re-measured on the seat bytes at d17180366, 16:5xZ; the original g15-28 finding is in Agent Notes with its d0465c36a line numbers). Today: the r5 Belam-cap dry-run plan lives INSIDE `if is_chain_seat:` (rotate.py:5389-5432) while the LIVE cap at :5794-5806 runs for ANY seat whose handover carries `belam_cap.oldest_to_reap` — and :5606 derives that for `role == 'prime_director' OR --belam-prefix` — so a PLAIN seat given `--belam-prefix` reaps live but its dry-run prints no (r5) plan; the plain-seat r4/s12 own-chain dry-run (:5440-5475) prints `pane pid N -> ps -e chain [...]` but test_rotate_selfreap.py::test_dry_run_enumerates_s2_s12 (:235-262) asserts headings only, never those lines. CLAIM: (1) a HERMETIC test in test_rotate_selfreap.py (the file's existing `_ps_table` + `_pane_pid` monkeypatch + windows.txt seam) asserts the EXACT dry-run lines for a plain seat (own @id + pane pid + chain, deepest-first order) and for a chain seat (oldest + @id + chain); (2) a plain seat run with `--belam-prefix <pfx>` prints the (r5) cap-reap plan it WOULD run, through the same `_belam_oldest` call path as :5606/:5794, read-only, and the hermetic test asserts it; (3) both chain lines print in the order they would be TERM'd (deepest-first) under the DEEPEST-FIRST label. FALSIFIER: a plain-seat `--belam-prefix` dry-run that prints no (r5) plan while the live path would reap; or a test that passes with `_descendant_chain` patched to return the chain reversed. DEFERRED, NOT IN THIS ROUND: the original clause (4) `_restore_shield_signals` in a `finally` (:5891) — a try/finally around the tail of cmd_rotate_self re-indents the first_turn/bootstrap/spawn/handoff regions the sensei-director's live rounds SL1.02/SL1.04 are editing, and rotate-self is a CLI that returns to main() and exits right after, so the missing finally has no live consequence; it lands as its own minimal round after those merge. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/rotate.py — ONLY the dry-run r4/r5 block of cmd_rotate_self (today :5385-5475) — plus extensions/agi/tests/test_rotate_selfreap.py. EXCLUDED: every other region of rotate.py (first_turn/bootstrap/spawn/handoff/prepare/status are the sensei-director's or landed), every other file. PARALLEL with SL1.02/SL1.04 on disjoint regions of the same file; the parent merges kid branches before done."
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
163547Z session: claim rewritten as the assignment after re-measuring on d17180366 — every cited line moved (d0465c36a :4697/:4735/:4768/:4914 -> :5389/:5440/:5475/:5794) and the defect is unchanged; clause (4) deferred to keep the round's rotate.py region disjoint from the sensei-director's live SL1.02/SL1.04 (a try/finally re-indents their regions); the stale SERIAL-behind-startup-commands-must-parse constraint dropped (landed).
<!-- THOUGHT:END -->
