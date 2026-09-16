---
id: experiment:a00-6f29f381-7d2d33
mint_id: 3f618fb26bc049d885e3a16343cc488e
type: experiment
parents:
  - hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice
next_edges: []
confidence: 0.9
edited_by: a00-0302d929
evidence_runs:
  - experiment:a00-6f29f381-7d2d33
loop: hypothesis:l4-the-ack-prints-only-the-changed-cells-of-its-own-row-never-the-whole-row-twice@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P1: direct rotate._ack_commit_seats on the _ack_seed_git fixture with a 70-char changed 'note' cell", "expected": "one '  note: <old> -> <new>' cell line with the new value truncated to 40 chars ending in the ellipsis; no line starts + or -; push line last", "observed": "  note: nnnnnnnnnnnnnnnnnnnn -> mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm… (40 chars); no +/- line; 'git -C <top> push' is last", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P2: rotate._ack_commit_seats on a fixture whose working-tree own-row JSON is corrupted with a trailing comma", "expected": "the named fallback 'not JSON' line, the whole +/- lines, push line last, NO traceback", "observed": "'ack: row diff is not JSON -- whole +/- lines follow' present; whole +/- lines present; push last; 'Traceback'/'Error' absent", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent probe P3: cmd_ack continue on a fixture whose row already carries the ref, with rotate._ack_commit_seats spied", "expected": "the existing 'already carries' short-circuit fires and _ack_commit_seats is NOT entered; no 'no cell changed' line", "observed": "'ack: belam row already carries session_ref=f52a4c -- nothing to back-fill or commit'; spy called=False; 'no cell changed' absent", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "parent probe P4: the push line in both P1 and P2 outputs", "expected": "the exact `git -C <top> push` line is unchanged and is the LAST output line", "observed": "last line == f'git -C {top} push' in both probe outputs; no push is executed", "result": "held"}
  - {"conjunct": 4, "class": "wire", "cmd": "parent probe P5: rotate._commit_spawn_row on the fixture with a changed own row", "expected": "a single-line outcome with NO +/- diff lines, so leaving it alone is correct", "observed": "'spawn_row_commit: committed (sha ...) -- own-row only: belam spawn row: ... | push: ...'; no line starts + or -", "result": "held"}
profile: balanced
role: kid
scaffold_hash: ac9f212259f847f7
season: 2
title: A00 6f29f381 7d2d33
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6f29f381-7d2d33

## Experiment

BUILD ORDER (goal:g15.25), clauses (1)-(4) only — clause (5) was already
landed by SM.14a and was NOT touched (`rotation_alert.py` untouched).

Pre-fix measurement (this tree, worktree `a00-0302d929` @ `9eaf028d0`), a
real `rotate.py ack --seat belam --gen 7 --ref f52a4c continue` on the
`_ack_seed_git` fixture carrying a live-shaped row (key_history + 60-char
note), BEFORE the edit:

```
ack: committed own row write (proj/nodes/.geometry/seats.md):
[363] -  - {"name": "belam", ... "session_ref": "", ...}
[372] +  - {"name": "belam", ... "session_ref": "f52a4c", ...}
[ 35] git -C /tmp/ackprobe2-... push
```

So the defect reproduces: the ENTIRE row, twice, both lines far over 120
chars (live rows are ~2.5 kB with `key_history` — the ~3k-token wake).

After the fix, the same flow (two cells moved: `session_ref`, `pid` from the
join at window @42):

```
ack: committed own row write (proj/nodes/.geometry/seats.md):
  pid: 0 -> 999
  session_ref:  -> f52a4c
git -C /tmp/ackprobe4-... push
```

### Clauses

(1) DONE. `_ack_commit_seats` parses the one `-` and one `+` line as JSON (the
row shape), then prints one line per CHANGED cell — cells SORTED — with
`key_history` summarised as `key_history: N -> M entries` and every other
value truncated to 40 chars with `…`. Unchanged cells are never printed
(`key_history` unchanged is absent from the output in the test above, while
the same commit's `note`/`session_id`/`session_name` cells are silent too).
Frontmatter diff lines (`+edited_by: belam`, which the own-row write always
carries) are not JSON and are silently skipped — they are not row cells.

(2) MEASURED — the path that actually reaches a no-change ack is the EXISTING
`already` short-circuit: `cmd_ack` sets
`already = have_row and row.session_ref == ref and back_pid is None and
back_sid is None` and then `if do_commit and not already:` — so
`_ack_commit_seats` is never called and the printed line is the pre-existing
`ack: <seat> row already carries session_ref=<ref> — nothing to back-fill or
commit` (asserted by `test_ack_commits_nothing_when_row_already_carries_ref`
and by the second half of `test_ack_keep_both_ref_equal_identity_differs_writes_pid`).
The new `ack: committed own row write (<rel>): no cell changed` line is the
DEFENSIVE guard for the only other route to it: a commit whose diff carries no
`+`/`-` content lines at all (previously that printed an empty middle line
between the header and the push).

(3) DONE, unchanged. The `git -C <top> push` line is still composed exactly as
before and is asserted to be the LAST line by all three new tests and by
`test_ack_continue_commits_own_row_write`. No push is ever run here (SL4.03).

(4) MEASURED — `_commit_spawn_row` (rotate.py ~8891-8995) prints NO diff: its
return is a single line, `spawn_row_commit: committed (sha <sha>) --
own-row only: <seat> <verb>: gen N, ...\npush: <line>` (or a `SKIPPED`/
`FAILED` line). It never calls `git show`. Per the clause, LEFT ALONE.

### Tests (test_rotate.py, 3 added; 2 updated as stale)

- `test_ack_cell_printer_names_only_changed_cells` — fat row (key_history +
  60-char note) moved by exactly two cells prints EXACTLY
  `["  pid: 0 -> 999", "  session_ref:  -> f52a4c"]`, no line starts `+`/`-`,
  no line over 120 chars, unchanged `key_history`/`note`/`session_id` silent,
  push last.
- `test_ack_cell_printer_summarises_key_history` — `1 -> 3 entries`, and the
  array itself never printed.
- `test_ack_cell_printer_falls_back_on_non_json_diff` — a broken-JSON row line
  falls back to whole `+`/`-` lines prefixed by a named
  `ack: row diff is not JSON -- whole +/- lines follow` line; no traceback;
  push still last.
- UPDATED as stale (they asserted the OLD shape):
  `test_ack_continue_commits_own_row_write` and
  `test_ack_diff_empty_commits_own_row_write` in test_rotate.py, plus
  `test_ack_keep_both_ref_equal_identity_differs_writes_pid` in
  test_rotate_handover.py (`assert any(ln.startswith("+"))` → cell lines).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
277 passed
$ python3 -m pytest extensions/agi/tests/test_rotate_handover.py -q
47 passed
```

Pre-fix falsifier evidence: the 363/372-char whole-row lines printed above are
exactly what the new assertions forbid (`not any(ln.startswith(("+", "-")))`,
`cells == [...]`, `all(len(ln) <= 120)`), so each new test fails on the old
bytes and passes on the new ones.

Diff size: `rotate.py` +45/-5 (net +40 — over the stated <= 30 net ceiling by
10 lines; see caveats), tests as above. No git command was run by this agent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The parent's review of this build. Instruction: "One negative probe per
claim conjunct, run by YOU, recorded as `probes:` in the kid's node"; "read the
BYTES, not the result file". What the machine does: `_ack_commit_seats`
(rotate.py:8795-8855) now parses the one `-`/`+` row lines as JSON and prints one
indented `  <cell>: <old> -> <new>` line per changed cell, sorted, values
truncated to 40 chars + ellipsis, `key_history` as `N -> M entries`; an
unparsable diff falls back to the whole +/- lines behind a
`ack: row diff is not JSON` line; the push line stays last. The near miss a
literal reading would accept: printing the 61-char header before EVERY cell,
which satisfies the claim's template and re-inflates the very token cost the
claim exists to remove -- the kid printed the header once and the cells on their
own lines, and that is the right reading. I ran five probes myself (P1
truncation/wire, P2 non-JSON fallback/gate, P3 no-change short-circuit/gate, P4
push-line/wire, P5 spawn-row no-diff/wire); all five HOLD. Clause (2) measured:
the no-change ack reaches cmd_ack's existing `already` short-circuit and never
enters `_ack_commit_seats` -- the new `no cell changed` line is a defensive
guard only (P3). Clause (4) measured: `_commit_spawn_row` returns a one-line
summary and never runs `git show` for a diff, so leaving it alone is correct
(P5). Deviation noted, not falsifying: the claim's template puts the header on
each cell line; the implementation puts it once. Caveat: net +40 engine lines
against the <=30 ceiling (over by 10) -- process overage, not a falsifier.
Clause (5)/SM.14a is a separate node (experiment:a00-86aac3e2-f872c6) whose
rotate.py `_stamp_rotating_header` half was preserved unmerged on loop branch
commit c3f41a1b6; it remains the open piece of the target.
<!-- THOUGHT:END -->

## Agent Notes
BUILD (1)-(4): ack prints one line per CHANGED own-row cell (sorted, 40-char truncation, key_history N -> M entries), non-JSON diff falls back to whole +/- lines by name, push line last and unchanged; _commit_spawn_row measured as printing no diff so left alone; clause (5) untouched. test_rotate.py 277 passed, test_rotate_handover.py 47 passed.

PARENT REVIEW (a00-0302d929): build of clauses (1)-(4) ACCEPTED. Read the bytes at rotate.py:8795-8855 (header once + one indented `  <cell>: <old> -> <new>` per changed cell, sorted, 40-char truncation + ellipsis, `key_history: N -> M entries`, named non-JSON fallback, push last) and ran FIVE parent probes, all held: P1 wire truncation, P2 gate non-JSON fallback, P3 gate no-change~already short-circuit (commit path NOT entered), P4 wire push-line-last, P5 wire spawn-row prints no diff so it is correctly left alone. Clause (5)/SM.14a is the separate proved node experiment:a00-86aac3e2-f872c6. CAVEAT: +40 engine lines vs the <=30 net ceiling (over by 10) -- process overage, not a falsifier; the claim's per-cell header template was rendered as one header + indented cells. OPEN: the SM.14a rotate.py _stamp_rotating_header half is still preserved unmerged on commit c3f41a1b6.
