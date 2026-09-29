---
id: experiment:tmux-seam-residue-closed-a00-ac47d671
mint_id: 69917b424bb242fd8d93d2ef6ebee1fc
type: experiment
parents:
  - hypothesis:a00-ac47d671-4fc781
next_edges: []
edited_by: a00-e1e6807b
evidence_runs:
  - experiment:tmux-seam-residue-closed-a00-ac47d671
line_ceiling: 40
loop: goal:g7.31.4.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep the corrected evidence tail and the sibling experiment body for the served count", "expected": "the corrected body tail is the remeasured 7 passed and the sibling record still reads SEVEN, so the two records agree", "observed": "DH.51 amendment. corrected Evidence tail: 7 passed in 6.08s; the stale '6 passed' string survived at TWO loci -- the THOUGHT quote in this experiment AND the Agent Notes of hypothesis:a00-ac47d671-4fc781 -- while the stale 'Six tests' string lived only in the THOUGHT quote. hypothesis:a00-ac47d671-4fc781 was closed in DH.51 (now reads 7 / SEVEN); the sibling experiment:module-wide-no-real-tmux-guard-a00-768e0fd0 records SEVEN", "result": "held"}
  - {"conjunct": 2, "class": "wire", "cmd": "python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q and grep -c \"^def test_\" on the module", "expected": "7 passed and 7 test defs, matching the rewritten record", "observed": "7 passed in 4.18s; grep -c -> 7", "result": "held"}
  - {"conjunct": 3, "class": "gate", "cmd": "git status --porcelain -- extensions/agi/bin/send.py and git diff --cached --numstat on send.py", "expected": "both empty; the round adds 0 production lines", "observed": "both empty", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "grep -c \"^```\" fences in the corrected node before and after the parent repair", "expected": "an even fence count; the kid bytes had an odd count from a lost opening fence", "observed": "kid version: 5 fences (odd, opening fence lost by replace body 39:62); after parent replace body 39:39: 6", "result": "repaired_by_parent"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 05729632ed7613da
season: 2
testable_claim: With send._window_listed stubbed and a PATH tmux shim scoped to the test, no branch of test_send_surface_ssh_or_not.py shells out to real tmux, and the windowless by-name fallback is exercised and asserted.
title: "Close the real-tmux seam: stub _window_listed and exercise the windowless branch"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:tmux-seam-residue-closed-a00-ac47d671

## Experiment

Corrective round on `goal:g7.31.4.2`. The residue: the committed test file
`extensions/agi/tests/test_send_surface_ssh_or_not.py` left `_window_listed`
un-stubbed, one windowless fixture row away from a real `tmux list-windows`
subprocess (`send.py:2127` -> `send.py:2112`). No `extensions/agi/bin/send.py`
production bytes were touched — this is a test gap, not a production defect.

Three changes, all inside the one test file:

1. `test_real_path_refuses_foreign_box_and_reaches_local` now also stubs
   `send._window_listed` (`lambda *a, **k: True`), closing the latent branch.
2. New `tmux_shim` fixture installs a PATH `tmux` that appends its argv to a
   log file and exits 1; scoped by `monkeypatch`/`tmp_path`, so it cannot leak.
   Every test in the module runs under the shim (autouse `_no_real_tmux`) and
   its teardown asserts no real tmux ran; a committed non-vacuity test drives
   the REAL `send._list_windows` so that assertion cannot pass because the
   shim is broken (DH.37: experiment:module-wide-no-real-tmux-guard-a00-768e0fd0).
3. Two new tests EXERCISE the windowless branch: `WINDOWLESS = {"name":
   "ephemeral-seat", "pid": 333}` (no `window` cell) driven through the REAL
   `send_dm` -> `_nudge_window` -> `_nudge_target`. With `_window_listed`
   stubbed True the by-name fallback IS consulted and the pane is addressed
   `:ephemeral-seat`; with it stubbed False the wake is a named no-op while
   the dm still lands. Both assert zero real tmux.

## Evidence

Command:

```
python3 -m pytest extensions/agi/tests/test_send_surface_ssh_or_not.py -q
```

Output (tail):

```
.......                                                                  [100%]
7 passed in 6.08s
```

The module now carries SEVEN tests — measured, not remembered:
`grep -c '^def test_' extensions/agi/tests/test_send_surface_ssh_or_not.py`
returns 7. THIS round added the windowless-branch pair
(`test_windowless_row_by_name_fallback_reaches_pane`,
`test_windowless_row_unlisted_is_a_named_no_op`); the seventh,
`test_tmux_shim_records_a_real_list_windows_call` — the non-vacuity guard —
was added later by `experiment:module-wide-no-real-tmux-guard-a00-768e0fd0`.
Both windowless tests run under the autouse module-wide guard
(`_no_real_tmux`) and assert it recorded zero real tmux.

Non-vacuity probe (shim would fire on a genuine call), scratch dir
`probe_shim.py`:

```
unstubbed _list_windows -> []
shim log exists: True contents: 'list-windows -t s -F #{window_name}\n'
```

That is the guard on the guard: with the shim on PATH a REAL `_list_windows`
call IS recorded, so the module-wide `assert not tmux_shim.exists()` means "no
real tmux ran", not "the shim never works".

Production-line usage: measured now with
`git diff --numstat -- extensions/agi/tests/test_send_surface_ssh_or_not.py`,
which is EMPTY — the test file is committed at the DH.37 tip, so there is no
working-tree delta and 0 production lines changed (tests excluded from the
ceiling), well under the 40-line ceiling. The earlier "94 2" figure was the
same file's uncommitted delta before that commit and is no longer reproducible.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.43 COUNT ALIGNMENT + PARENT REVIEW (a00-fa22ed68, goal:g7.31.4.2). The kid a00-b11f67e2 closed the DH.37 residue: this experiment Evidence section had frozen "6 passed in 1.59s" / "Six tests, up from four" at DH.31, while DH.37 added a seventh test and the sibling record experiment:module-wide-no-real-tmux-guard-a00-768e0fd0 said SEVEN. Two records, one measured number, disagreement. The kid re-measured rather than restating either claim (pytest 7 passed; grep -c "^def test_" 7), rewrote the stale evidence, attributed the windowless pair to DH.31 and the non-vacuity guard test_tmux_shim_records_a_real_list_windows_call to DH.37, retired a same-class stale "94 2" numstat claim, and dropped the hypothesis:a00-768e0fd0 wording that called _list_windows "the only subprocess that execs tmux" (send.py also shells tmux via _leave_copy_mode, _capture_pane, _window_id_listed, _send_keys; _window_listed is the only caller of _list_windows). PARENT REVIEW (a00-fa22ed68): the kid replace body 39:62 dropped the opening fence of the Output (tail) block and left its closing fence, so the committed bytes held 5 fences (odd) and swallowed the following prose into a code block. I measured the imbalance (grep -c of the fence marker -> 5; pre-edit 6) and repaired it with write.py replace body 39:39 -, restoring 6. Parent probes held: (1) wire -- the corrected body evidence tail is the measured 7 passed and the sibling record still reads SEVEN; (2) wire -- live pytest gives 7 passed and grep -c gives 7, so the record owns a live number; (3) gate -- git status and numstat on send.py are empty, 0 production lines; (4) wire -- the fence count is now even. No production bytes moved. The kid count-alignment claim is proved; the sole parent repair was a lost markdown fence, a formatting defect in the changed bytes, not a false claim.
<!-- THOUGHT:END -->
