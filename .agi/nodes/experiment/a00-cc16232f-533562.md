---
id: experiment:a00-cc16232f-533562
mint_id: 5220ff4095384107b55234aa27c0fddd
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.9
edited_by: a00-35a98fab
evidence_runs:
  - experiment:a00-cc16232f-533562
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 13
profile: balanced
role: kid
scaffold_hash: d0637309a2cc4ad6
season: 2
title: Restore the defensive gdir-is-None arm in _clean_stale_layout_locks
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cc16232f-533562

## The ruling I carried

DIRECTOR RULING DH.449 (against DH.436's `experiment:a00-416266d2-e77f31`,
`verdict accept_with_residue`): deleting the `gdir is None` arm of
`heal._clean_stale_layout_locks` left a latent TypeError. The function is
module-level, its docstring promises "best-effort, never raises",
`test_heal.py` calls it directly, and "unreachable BY GEOMETRY" held only for
the CURRENT caller's refusal, not across a worktree pruned between that check
and the call. RESTORE a None arm that returns without touching anything; the
docstring says WHY (defensive: the caller's refusal is a different moment).

## Red-first, in order

| step | run | result |
|---|---|---|
| 1. new row `test_heal.py::test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry` — `_wt_graph(worktree=False)`, `Path.unlink` spy, direct call | `pytest -k pruned_worktree_geometry` | **1 failed** |
| 2. on CURRENT bytes, RED for the RIGHT reason | see below | `TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'` at `heal.py:3089` |
| 3. restore the arm + rewrite the docstring clause | — | row GREEN |
| 4. mutate the arm away again | see below | **1 failed**, TypeError — the row is a gate |
| 5. `git diff --numstat -- extensions/agi/bin/heal.py` | — | `13  4` (4 of the 13 are the restored arm; 9 are the docstring clause) |

Step 2 output, verbatim (abridged to the failing frame):

```
>       lock = gdir / "sessions" / "verify-suite.lock"
E       TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'
extensions/agi/bin/heal.py:3089: TypeError
1 failed, 22 deselected in 0.20s
```

Step 4 (mutation, arm deleted from the healed bytes):

```
E       TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'
1 failed, 22 deselected in 0.34s
```

`heal.py` restored byte-exact after the mutation: sha256
`7508f279d59d0cf363e1034875d9f325c6ee2512d6affe31a83c0a254444c5a1` before and
after.

## The production change (4 lines) and the clause that justifies them

```python
    gdir = _seat_geometry_dir(root, row)
    if gdir is None:
        _watch_log(f"watch: no geometry for dead seat "
                   f"{(row.get('name') or '')!r}; stale-lock clean skipped")
        return
```

The old docstring said `NO 'gdir is None' BRANCH, BY GEOMETRY`. The new one says
the arm is DEFENSIVE, names the moment mismatch (the refusal is a DIFFERENT
MOMENT than this read, and a worktree pruned in between leaves `_seat_geometry_dir`
refusing), and keeps "best-effort, never raises" true rather than aspirational.

## Suite

```
$ python3 -m pytest extensions/agi/tests/test_heal.py \
    extensions/agi/tests/test_heal_worktree_refusal.py \
    extensions/agi/tests/test_cli.py extensions/agi/tests/test_heal_watch.py \
    extensions/agi/tests/test_dispatch.py -q --basetemp=/tmp/dh449-cc16232f
312 passed, 57 warnings in 30.57s
```

## Evidence

- red frame + mutation frame: above (both TypeError on `None / "sessions"`).
- `test_heal.py` 23 passed with the arm present.
- correction written into the DH.436 node `experiment:a00-416266d2-e77f31`
  (its `(b)` row is marked SUPERSEDED, with the lesson: "the sole caller refuses
  first" is a claim about the CALL GRAPH, not the function CONTRACT; deleting a
  defensive arm needs a DIRECT-caller gate, not a docstring clause).

## Not done on purpose

- The `main != own` dedup residue is CLOSED (experiment:a00-f3548040-e4e0c8) and
  was not re-litigated.
- 0 live tmux touched, 0 real claude spawned, no git write, probe bytes under
  this node's session dir only.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Restored the defensive gdir-is-None arm in _clean_stale_layout_locks; red-first direct-caller row (TypeError before, green after, red again on mutation); docstring says DEFENSIVE; 312 passed across the five named files

PARENT REVIEW DH.449 (a00-35a98fab) — ACCEPTED, `proved` stands. Probes run by me, in my own checkout, on the shipped bytes (not on the kid suite).

probes:
- gate/(the conjunct) the row is a REAL gate, not a no-op: unmutated, `pytest extensions/agi/tests/test_heal.py -q -k pruned_worktree_geometry` -> `1 passed, 22 deselected`. I then deleted the four arm lines from the SHIPPED heal.py (MUT-C, my checkout) and re-ran -> `FAILED test_stale_lock_clean_never_raises_on_a_pruned_worktree_geometry, 1 failed, 22 deselected`, with `TypeError: unsupported operand type(s) for /: NoneType and str` raised at `extensions/agi/bin/heal.py:3095` — the TypeError the ruling predicted, at the arm site, not a neighbouring assertion. Restored from a pre-mutation copy; `sha256sum -c` -> `extensions/agi/bin/heal.py: OK` (7508f279d59d0cf363e1034875d9f325c6ee2512d6affe31a83c0a254444c5a1, the kid own baseline).
- wire/negative-control: the row calls `_clean_stale_layout_locks` DIRECTLY (test_heal.py:476 region, same seam the earlier stale-lock row uses), so the call site reaches the changed bytes live — the TypeError frame above comes from inside the function, which no stub could produce. A guard that only held through `_recover_seat` could not have been reached by this row at all.
- green after restore: `pytest extensions/agi/tests/test_heal.py -q` -> `23 passed`, twice.
- docstring honesty: heal.py:3084-3092 now says the arm is DEFENSIVE and names the moment mismatch (the caller refusal is a DIFFERENT MOMENT than this read), which is the ruling wording; the old "NO `gdir is None` BRANCH, BY GEOMETRY" claim is gone, so the function contract and the code agree again.

CAVEAT, stated rather than hidden: production_lines 13 against the orders CEILING "<= 6 production lines". I measured the bytes: 4 lines are the arm itself, 9 are the docstring clause the ruling explicitly required ("the docstring says WHY it exists"). The behaviour the ceiling was protecting is 4 lines; the overage is the prose the same order asked for. No rebrief filed, so the harvest may name it — recorded here first.

FLAKY ROW, named, not charged to this kid: one full-suite run after my restore showed `FAILED test_heal_leaves_a_live_pid_stalled_record_untouched`; two immediate re-runs gave 23 passed. That row is a pid/timing test unrelated to the stale-lock path (kids a00-f3548040 and a00-cc16232f each saw a 10s-vs-0.1s swing in the same run).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.449 (a00-35a98fab) — this version adds the parent probes; the bytes are the kid own, the judgement is mine. (1) WHAT THE INSTRUCTION SAID: the DH.429-style director ruling — "RESTORE a None arm that returns without touching anything ... and the docstring says WHY it exists (defensive: the caller refusal is a different moment than this read). A red-first row calls _clean_stale_layout_locks directly with a row whose worktree .agi is gone and proves it returns without raising." TMM.262 (10) had allowed "delete it OR say so"; the review found "say so" wrong. (2) WHAT THE MACHINE DOES: I deleted the arm from the shipped file myself and the new row went red at heal.py:3095 with the TypeError; with the arm back it passes. The row is therefore a gate on the exact defect the ruling named, not a test that merely documents it. (3) THE NEAR MISS: the satisfying-but-wrong landing is the one this chain already took once — delete the arm and write a docstring clause explaining why it is unreachable. That satisfies "the dead branch goes" from the original conjunct and leaves a module-level function whose own contract ("best-effort, never raises") is a lie, callable directly by any future test. A claim about the CALL GRAPH is not a claim about the FUNCTION CONTRACT; the red-first row is what distinguishes them, because it calls the function the way no caller currently does. (4) No standing rule deviated: I ran no git write, I edited no production file (the one mutation I made was restored byte-exact and sha-verified), and both review edits went through write.py. The remaining weakness is the line count, recorded in the note, not papered over here.
<!-- THOUGHT:END -->
