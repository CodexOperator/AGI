---
id: hypothesis:l4-reap-helpers-have-other-tty-and-non-child-fixtures
mint_id: 0f157d4072e94a669ad6b35b4a58bae1
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-rotate-self-keeps-the-numeral-window-reaps-fifo-and-records-before-it-terms
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 6120777a59752f4d
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-13: `_descendant_chain`, `_read_ps_parent_table` and the pane-pid branch are exercised only through F1's same-tty CHILD sleeps via the `belam_pids` seam — the live failure modes (a chain on another tty, pids that are not rotate.py's children so `waitpid` raises, L4.122 criterion 1/2) are not what the fixtures reproduce. CLAIM: tests spawn stand-in trees on ANOTHER pty (`os.openpty` / `script -q` / `setsid` so the pids are not children of pytest and sit on a different tty) and assert (a) `_read_ps_parent_table` sees them, (b) `_descendant_chain(pane_pid)` returns the full chain deepest-last, (c) `_reap_chain` TERMs them without `ChildProcessError` and records gone_after, (d) the pane-pid branch derives from a fake `@id` → pane pid seam; all skip-cleanly (named) on a box without a pty. FALSIFIER: the helpers pass on same-tty children and fail on the other-tty tree. TESTS ONLY — rotate.py is byte-identical unless a test exposes a defect (state it with the failing run). CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_rotate_selfreap.py + test_rotate_handover.py (+ a tests/conftest helper). May run PARALLEL with the rotate.py rounds ONLY if it does not touch rotate.py; if a defect needs a rotate.py edit, STOP, record it, and the point cuts a fix-only. EXCLUDED: rotate.py edits, everything else."
title: The reap helpers are proven against OTHER-tty processes and non-child pids, not same-tty child sleeps
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-reap-helpers-have-other-tty-and-non-child-fixtures

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 28 review by name (wf_2a45a87d-b16), goal:g15 newest note at 3cd6e6bd9; line numbers on 9b4186086. g15-13: `_descendant_chain`, `_read_ps_parent_table` and the pane-pid branch are exercised only through F1's same-tty CHILD sleeps via the `belam_pids` seam — the live failure modes (a chain on another tty, pids that are not rotate.py's children so `waitpid` raises, L4.122 criterion 1/2) are not what the fixtures reproduce. CLAIM: tests spawn stand-in trees on ANOTHER pty (`os.openpty` / `script -q` / `setsid` so the pids are not children of pytest and sit on a different tty) and assert (a) `_read_ps_parent_table` sees them, (b) `_descendant_chain(pane_pid)` returns the full chain deepest-last, (c) `_reap_chain` TERMs them without `ChildProcessError` and records gone_after, (d) the pane-pid branch derives from a fake `@id` → pane pid seam; all skip-cleanly (named) on a box without a pty. FALSIFIER: the helpers pass on same-tty children and fail on the other-tty tree. TESTS ONLY — rotate.py is byte-identical unless a test exposes a defect (state it with the failing run). CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/test_rotate_selfreap.py + test_rotate_handover.py (+ a tests/conftest helper). May run PARALLEL with the rotate.py rounds ONLY if it does not touch rotate.py; if a defect needs a rotate.py edit, STOP, record it, and the point cuts a fix-only. EXCLUDED: rotate.py edits, everything else.
