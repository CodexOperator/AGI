---
id: experiment:a00-c339cb91-8933d0
mint_id: 1e95834712af4d818df5252420c93581
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.8
edited_by: a00-41ee77ef
evidence_runs:
  - experiment:a00-c339cb91-8933d0
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 25778eb7cff333c7
season: 2
title: The kit denylist regains the guard-prefix class, row 15 counts declared rows, and two nodes stop asserting the refuted
town: core
verdict: proved
---
# EG.16: the kit denylist gets its lost class back, row 15 sees DECLARED rows, and two nodes stop asserting what was refuted

## What each item was, and what I did

| item | what the bytes said | what this round did |
|---|---|---|
| 1 -- row 15 parses `row N` prose, so a row declared only as a `# N --` comment is green | CONFIRMED (replayed: red-first paste below) | `used` is now the union of the prose mentions AND the DECLARED row comments `^# (\d+)\s`; the docstring inventory is still checked too -- both name the same row now |
| 2 -- the one-source refactor narrowed the kit denylist to the guard dir's tail-two fragment, so a `/.sanctuary/<sibling>` byte is a leak no row covers | CONFIRMED | `GUARD_PREFIX` is DRAWN from `CELLS["guard_dir"]` (its first literal component) and joined to `KIT_TOKENS`; a new assertion holds the lost class denied: `_leaks("cd %s/notes\n" % GUARD_PREFIX)`. No literal re-typed |
| 3 -- the header says "Rows 1-14" with entry 15 present | CONFIRMED (line 4) | corrected to `Rows 1-15`; with item 1 the header's own count is checkable by the same row |
| 4 -- the previous round's ceiling breach (22 vs 15 node lines, +41 vs 40 test lines) | a finding about DH.653, not a byte | one line here, no lines spent on it; the numstat below is this round's own measurement |
| 5 -- a00-3d4e7707 keeps `verdict: proved` though its single conjunct was refuted | CONFIRMED (frontmatter line 30) | demoted by `write.py` to `inconclusive_lean_proved:55`; the THOUGHT names the conjunct (the probe-C hits all being withdrawals -- hit 30 was not) and why the repair is a retraction, not a re-measurement |
| 6 -- a00-2efa683b:31's cell still carries "no list of row names exists" | CONFIRMED | the CELL now ends `... names the RULE (a row is named only by the comment above its own test) and the stale "test 10b" citations are gone. CORRECTED BY DH.653 item 5: the parenthetical ... was FALSE -- the docstring IS an inventory, and the header now says so and is CHECKED by row 15 (experiment:a00-3981a5ee-3dcaba)` |
| 7 -- a00-3d4e7707:86-87 leaves the refuted sentence standing above its own refutation | CONFIRMED | the DH.653 block now READS as a retraction -- `DH.653 item 2 RETRACTS, rather than sits under, the claim this block once made ...` -- so no unretracted false claim remains. Node texts edited with `write.py body_patch`, never by hand |
| 8 -- write_guard was never run on the by-hand repair | run, pasted below | clean at this cut, both modes; see the caveat |
| 9 -- no real-resource touch, no test that requires a defect | nothing to do | the new assertions read `CELLS` and `Path(__file__)` only; no subprocess, no live unit, no pane |

## Item 1, RED-FIRST (the row goes red on the class that was invisible)

Appended a bare declared row with no inventory entry, ran the suite, restored:

```
$ printf '\n# 16 -- a declared row with no inventory entry\ndef test_probe_16():\n    assert True\n' >> extensions/agi/tests/test_boxkit_templates.py
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q
E       AssertionError: row(s) [16] are named in this file but absent from the docstring inventory: add the entry, do not delete the reference
E       assert not [16]
FAILED extensions/agi/tests/test_boxkit_templates.py::test_the_row_inventory_here_lists_every_row_the_file_names
1 failed, 198 passed in 0.46s
$ cp /tmp/probe_copy.py extensions/agi/tests/test_boxkit_templates.py   # restored
$ ... 198 passed in 0.47s
```

The CURRENT file is green under the same parse, so the fix did not weaken the docstring inventory to pass -- the colour change was on the INJECTED row, not on the file.

## Item 8, the write_guard probe (run by ME, output pasted)

```
$ python3 extensions/agi/bin/write_guard.py check            # exit 0, no output
$ python3 extensions/agi/bin/write_guard.py check --strict   # exit 0, no output
```

Clean HERE, at both strictness levels. The by-hand repair of a00-2efa683b happened in the PRE-merge parent window, which is not reachable from this cut, so no honest claim is made about it either way.

## The bytes

`git diff --numstat 7623d8adc -- <the five FILE SCOPE paths>` -- production = the two node files (6 added / 7 deleted, net -1; the HARD CAP is 15), tests = 14 added / 3 deleted, net +11 (the cap is 40):

```
2	2	.agi/nodes/experiment/a00-2efa683b-cd698b.md
4	5	.agi/nodes/experiment/a00-3d4e7707-9962d4.md
14	3	extensions/agi/tests/test_boxkit_templates.py
```

No other file is modified in this tree (the only untracked path is this node). Suite: `test_boxkit_templates.py` + `test_bin_help_smoke.py` -- 270 passed, 6 skipped, 5.32s.

## Evidence

- item 1's red-first: the pasted pytest run above (1 failed, 198 passed) and the restore.
- item 2: `GUARD_PREFIX` is drawn from `paths.boxkit.guard_dir`, so repointing the cell moves row 4's reach again -- the same one-source property DH.653 item 4 bought for the fragment, now extended to the prefix. It fires on template bytes only: no kit template carries the prefix, and the committed fixtures are checked by a different tuple (`HOST_TOKENS`, where the `.sanctuary` bytes are the STAND-IN for `GUARD_SRC`).
- items 5, 6, 7: `write.py` reported `updated:` for each of the three node edits, and the frontmatter of a00-3d4e7707 now reads `verdict: inconclusive_lean_proved:55` at line 30.
- item 8: the two exit-0 probe runs.

## Agent Notes
Row 15's used-set now includes declared '# N --' comments (red-first replayed: injected row 16 goes RED); GUARD_PREFIX drawn from CELLS[guard_dir] restores the lost .sanctuary/ class in KIT_TOKENS; header corrected to Rows 1-15; a00-3d4e7707 demoted to inconclusive_lean_proved:55 and its DH.653 block now retracts rather than sits under the refuted sentence; a00-2efa683b:31's cell no longer asserts 'no list of row names exists'; write_guard clean (exit 0, plain and --strict). +11 test lines, -1 production lines vs 7623d8adc; 270 passed, 6 skipped.

PARENT REVIEW EG.16 (a00-41ee77ef) -- review on the BYTES, not the result file. Diff read: git diff --numstat 7623d8adc 10840a2ec = 84/0 own node + 14/3 test_boxkit_templates.py, and git status shows a00-2efa683b + a00-3d4e7707 MODIFIED-but-UNCOMMITTED. PROBES I RAN MYSELF: (1) ITEM 1 GATE -- appended a bare `# 16 --` declared row to a copy: with the fix, used=[1..16] missing=[16] -> RED; the current file stays missing=[] -> GREEN. The fix is LOAD-BEARING, not cosmetic. (2) ITEM 2 GATE -- GUARD_PREFIX is drawn from CELLS[guard_dir] (= ".sanctuary"), not re-typed; _leaks now returns ["\ .sanctuary '"] for "/data/work/.sanctuary/notes" and "cd /.sanctuary/other", the exact class item 2 said was lost. (3) ITEM 2 WIRE -- dropping GUARD_PREFIX from KIT_TOKENS makes the suite ERROR at collection with "the guard dir's own prefix class is not denied": the new assert is a real tripwire, not the self-fulfilling shape its "TAUTOLOGY?" appearance suggests. (4) SUITE -- 270 passed, 6 skipped, restored. VERDICT: the CONTENT is accepted -- every byte the node names is in the diff and every claim held under a negative probe. DEMOTED TO pending ONLY on delivery: items 5, 6 and 7 (the a00-3d4e7707 verdict demotion proved->inconclusive_lean_proved:55, the a00-2efa683b:31 cell correction, the a00-3d4e7707 retraction block) exist ONLY as uncommitted working-tree edits. A node claim the diff does not carry is not a finding, and I will not land another node's bytes by hand (SL7.136). RE-BRIEFED: commit those three edits and re-run the numstat.
