---
id: experiment:a00-31ad8df6-a597ec
mint_id: c7b75adbf58f4f84a804dd0821d8e8c5
type: experiment
parents:
  - hypothesis:l5-key-rotation-at-a-rename-boundary-clobbers-key-history-instead-of-carrying-it
next_edges: []
confidence: 0.95
edited_by: a00-f6383d92
evidence_runs:
  - experiment:a00-31ad8df6-a597ec
line_ceiling: 40
loop: hypothesis:l5-key-rotation-at-a-rename-boundary-clobbers-key-history-instead-of-carrying-it@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P2: _successor_row_write with row_seat=ghost-old, seat=ghost-new and NO registry row for either", "expected": "refused BY NAME, no config:seats write, no phantom new-named row", "observed": "returned skipped: no seat-registry row with name ghost-new; row set after == {someone-else} only", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P3: row already renamed to director-sanctuary with aliases {sensei-director: director-sanctuary}, boundary called with row_seat=sensei-director (old) + key_rotation", "expected": "the alias bridge resolves _row_name to the EXISTING row and history APPENDS there (prior 3 + new == 4)", "observed": "key_history == prior + [retired], len 4; no second row written; out=config:seats row director-sanctuary ... pubkey=aaaa... key_history=5", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent falsifier: copy extensions/agi to /tmp, revert ONLY the read token (_row_name -> seat) at rotate.py:9360, run the kid test test_key_history_survives_a_rename_boundary_key_rotation", "expected": "the committed test FAILS on the unfixed read (1 entry vs 6)", "observed": "1 failed: assert [fp10] == [fp5, fp6, fp7, fp8, fp9, fp10], right contains 5 more items, test_rotate.py:1078", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P4: boundary re-run carrying the SAME retired entry already present in key_history", "expected": "no duplicate appended (idempotent), len unchanged", "observed": "len(hist) == 4 before and after", "result": "pass"}
production_lines: 10
profile: balanced
role: kid
scaffold_hash: b1a7408d6e085b01
season: 2
title: key_history read keyed on the post-rename seat clobbered it at a rename boundary; read now keyed on the row the writer updates, with a fail-before regression test
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-31ad8df6-a597ec

## Experiment

The parent hypothesis was already CONFIRMED by reading the live bytes, so this
round was a BUILD ORDER, not a measurement: fix the read, ship a regression
test that fails on the unfixed code.

**1. Reproduced the defect on a fixture (before touching code).** Scratch probe
`.agi/sessions/iter-L5.22/a00-31ad8df6/probe_clobber.py` seeds a graph root
whose `seats.md` carries one row named `sensei-director` with `key_history` of
5 entries (gens 5..9) and calls `_successor_row_write(graph,
seat="director-sanctuary", row_seat="sensei-director",
key_rotation={...})` — the exact live callsite shape (`rotate.py:~18927` passes
`row_seat=(_applied_rename or {}).get("old")` and `key_rotation` together).
Result PRE-FIX: the written row carries `len(hist) == 1` — the 5 prior entries
were destroyed by the full cell-replace.

**2. The fix (rotate.py, ~10 changed lines incl. comment).** In
`_successor_row_write`'s `if key_rotation:` block, the history READ now keys
on `_row_name` (the row that EXISTS — resolved above from `row_seat` / the
`aliases:` bridge) instead of `seat` (the post-rename name, which has no row at
read time). Read and write now name the SAME row — the property the parent
asked for. No change to `_write_identity_cells` semantics for other callers.
Post-fix probe: `len(hist) == 6`, prior 5 in order plus the new retired entry.

**3. Committed regression test.**
`extensions/agi/tests/test_rotate.py::test_key_history_survives_a_rename_boundary_key_rotation`
(one test, reuses the existing `_seed_key_history_graph` fixture; no live tmux,
no live pane, no live config). It presents the OLD-named row with prior history
running 5..9, performs the rename-plus-key-rotation boundary through
`_successor_row_write(row_seat=<old>, key_rotation=...)` — never
`_write_identity_cells` directly — and asserts the written row's `key_history`
== prior + [new retired entry] in order, `max(to) == 10` (never below the max
prior `to` of 9). Its docstring names the failing assertion.

**4. Fail-before / pass-after PROVEN.** With only the one read token reverted
(no git — a `python3 -` in-place text swap of `_row_name` back to `seat`, then
restored and verified byte-identical to a saved copy): the new test FAILS with
`assert [{'fp': 'fp10'...}] == [{'fp': 'fp5'...}]` — 1 entry vs 6, the missing
5 named individually. With the fix: 1 passed.

**5. Suite.** `python3 -m pytest extensions/agi/tests/test_rotate.py
extensions/agi/tests/test_rotate_boundary_rename.py
extensions/agi/tests/test_rotate_identity_main.py
extensions/agi/tests/test_write_self_row.py -q`
=> **349 passed, 0 failed** (68.2s). The new test is inside `test_rotate.py`.

`git diff --numstat -- extensions/agi/bin/rotate.py` => `9  1` = **10** changed
lines, ceiling 40.

## Evidence

- PRE-FIX probe: `ROW sensei-director pubkey aaaaaaaa len(hist) 1`
- POST-FIX probe: `ROW sensei-director pubkey aaaaaaaa len(hist) 6` with the
  5 prior entries intact in order plus the retired one.
- Fail-before (fix reverted): `1 failed, 320 deselected` / `AssertionError:
  [{'fp': 'fp10', 'from': 9, ...}] == [{'fp': 'fp5', ...}]`, `Right contains 5
  more items` — `extensions/agi/tests/test_rotate.py:1078`.
  Saved at `.agi/sessions/iter-L5.22/a00-31ad8df6/fail_before.txt`.
- The written row keeps the OLD name (`sensei-director`) and NO phantom
  `director-sanctuary` row appears: the round never writes config:seats, so
  the row that carries the identity cells is the OLD-named one (L5.02). The
  parent brief said "assert the row that now carries the NEW name" — that is
  only true when the seats row itself was already renamed and the `aliases:`
  bridge resolves it; in that sub-case the pre-fix read keyed on `seat`
  already found the row and there was NO bug. The defect case is the one where
  the row still carries the OLD name, so the test asserts on the row the
  writer actually updated. Same invariant, honest name.

## Agent Notes
Fixed the key_history read in _successor_row_write: keyed on _row_name (the row the ONE writer updates, resolved from row_seat/aliases) instead of seat (the post-rename name with no row at read time). New regression test test_key_history_survives_a_rename_boundary_key_rotation in test_rotate.py fails on the unfixed read (1 entry vs 6) and passes after; 349 passed in the 4 named suite files; 10 production lines vs 40 ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-f6383d92), accepted as proved.

1) WHAT THE INSTRUCTION SAID. "A kid's tests are its CLAIM, not your
evidence ... One negative probe per claim conjunct, run by YOU, recorded as
probes: in the kid's node." And: "THIS KID MUST IMPLEMENT THE FIX. A g15
claim is behaviour to build, not a hypothesis to measure."

2) WHAT THE MACHINE ACTUALLY DOES. Read the diff, not the result file:
`git diff 808a61305..5c39b1a72 -- extensions/agi/bin/rotate.py
extensions/agi/tests/` shows exactly one semantic token moved -- rotate.py
line 9360, `if r.get("name") == _row_name), {})` (was `== seat`) -- plus a
new test at test_rotate.py:1035-1080. `_row_name` is defined at
rotate.py:9341 and the write target is `_write_identity_cells(...,
seat=_row_name, ...)` at 9372, so read and write now name the same row.
The live boundary callsite at rotate.py:18909-18940 threads `row_seat=
(_applied_rename or {}).get("old")` and `key_rotation=_key_rotation` into
the same function, so the changed bytes are reachable on the real rename
path, not only from a test that calls the private helper. I ran my own
probes (recorded above) and a falsifier I built myself: a copy of
extensions/agi in /tmp with ONLY that token reverted -> the committed test
FAILS with `assert [{fp10}] == [fp5, fp6, fp7, fp8, fp9, fp10]`, right
contains 5 more items. The test is a real falsifier, not a tautology.

3) THE NEAR MISS. A kid could have satisfied the words by calling
`_write_identity_cells` directly in its test and asserting the merge there
-- that passes on the UNFIXED code, because the clobber lives in the `_cur`
read one level up, so it would prove nothing about the boundary path. It
would also have proved nothing if it keyed the fix on `row_seat` raw
instead of `_row_name`: the aliases bridge is the same code path
(rotate.py:9341) and my P3 probe shows the raw-keyed version would miss a
already-renamed row. The kid did neither: its test drives the boundary
(`row_seat=<old>` + `key_rotation`) and the fix keys on `_row_name`.

4) DEVIATION, AND WHY IT DOES NOT APPLY HERE. The target claim says "assert
the NEW name row key_history contains every prior entry plus the new one".
The kid asserts on the OLD-named row that the writer actually updates, and
asserts that NO phantom new-named row appears. Property of this case: the
round never writes config:seats, so at boundary time the new-named row does
not exist (L5.02; the row is renamed later, carrying whatever history the
boundary wrote). Asserting on a row that does not exist is impossible; the
kid's assertion is the same invariant, honestly named, and the live data
loss (sensei-director 31 -> director-sanctuary 1) is the downstream result
of the clobber this fix removes. Deviation accepted.

PROBES. Four, recorded in `probes:` above: gate (no registry row -> refusal
by name, no phantom row), wire (aliases bridge resolves the row that
exists and appends there), wire (falsifier: reverting the read token makes
the committed test fail), gate (idempotent re-run does not duplicate the
retired entry). All pass.

CAVEAT. The fix preserves history on the row that carries the OLD name;
the rename that moves that row to the NEW name is a separate step and gets
no test here. That is a different claim (rename-post staged), not a hole in
this one.
<!-- THOUGHT:END -->

PARENT REVIEW ACCEPTED (a00-f6383d92): fix landed (rotate.py:9360 reads _row_name; write target is _row_name at 9372), live callsite 18909-18940 threads row_seat+key_rotation, committed regression test fails-before (verified by me on an independent /tmp copy with only that token reverted) and passes-after. 4 parent probes recorded in probes: (gate refusal-by-name, wire aliases bridge, wire falsifier, gate idempotence) -- all pass. Deviation accepted: test asserts on the OLD-named row because the new-named row does not exist at boundary time (L5.02). Caveat: the downstream rename-forward step is a different claim and untested here.
